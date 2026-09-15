from __future__ import annotations
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv('config/.env')

from typing import Any
import requests
from database.models import HistoricalRecord
from database.repositories.historical import HistoricalRepository
class HistoricalDataIngestor:
    """
    Real historical market-data ingestion.
    Source:
        Alpha Vantage TIME_SERIES_DAILY
    Flow:
        Alpha Vantage
            -> validate
            -> normalize
            -> HistoricalRepository
            -> SQLite
    """
    BASE_URL = "https://www.alphavantage.co/query"
    def __init__(
        self,
        repository: HistoricalRepository | None = None,
        api_key: str | None = None,
        timeout: int | None = None,
    ):
        self.repository = repository or HistoricalRepository()
        self.api_key = (
            api_key
            or os.getenv("ALPHA_VANTAGE_API_KEY")
            or os.getenv("ALPHAVANTAGE_API_KEY")
            or ""
        )
        self.timeout = int(
            timeout
            or os.getenv("REQUEST_TIMEOUT")
            or 20
        )
    @staticmethod
    def _clean_symbol(symbol: str) -> str:
        return str(symbol or "").strip().upper()
    def fetch_daily(
        self,
        symbol: str,
        outputsize: str = "compact",
    ) -> dict[str, Any]:
        symbol = self._clean_symbol(symbol)
        if not symbol:
            raise ValueError("Symbol is required")
        if not self.api_key:
            raise RuntimeError(
                "ALPHA_VANTAGE_API_KEY is not configured"
            )
        outputsize = (
            "full"
            if str(outputsize).lower() == "full"
            else "compact"
        )
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize,
            "apikey": self.api_key,
        }
        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        if "Error Message" in data:
            raise RuntimeError(
                str(data["Error Message"])
            )
        if "Note" in data:
            raise RuntimeError(
                f"Alpha Vantage rate limit: {data['Note']}"
            )
        time_series = data.get(
            "Time Series (Daily)",
            {},
        )
        if not isinstance(time_series, dict):
            raise RuntimeError(
                "Alpha Vantage returned no daily historical series"
            )
        return {
            "symbol": symbol,
            "outputsize": outputsize,
            "series": time_series,
            "raw": data,
        }
    @staticmethod
    def _normalize_record(
        symbol: str,
        date: str,
        values: dict[str, Any],
    ) -> HistoricalRecord | None:
        try:
            close_value = float(
                values.get("4. close")
            )
        except (TypeError, ValueError):
            return None
        if close_value != close_value:
            return None
        timestamp = f"{date}T00:00:00+00:00"
        return HistoricalRecord(
            topic=symbol,
            value=str(close_value),
            source="alphavantage",
            source_type="api",
            timestamp=timestamp,
            reliability=0.80,
            metadata={
                "provider": "alpha_vantage",
                "date": date,
                "open": values.get("1. open"),
                "high": values.get("2. high"),
                "low": values.get("3. low"),
                "close": values.get("4. close"),
                "volume": values.get("5. volume"),
            },
        )
    def ingest(
        self,
        symbol: str,
        outputsize: str = "compact",
        limit: int | None = None,
    ) -> dict[str, Any]:
        symbol = self._clean_symbol(symbol)
        result = self.fetch_daily(
            symbol=symbol,
            outputsize=outputsize,
        )
        series = result["series"]
        dates = sorted(
            series.keys(),
            reverse=True,
        )
        if limit is not None:
            limit = max(1, int(limit))
            dates = dates[:limit]
        inserted = 0
        skipped = 0
        invalid = 0
        existing = self.repository.list_by_topic(
            symbol,
            limit=5000,
        )
        existing_keys = {
            (
                str(row.get("timestamp", ""))[:10],
                str(row.get("source", "")),
            )
            for row in existing
        }
        for date in dates:
            record = self._normalize_record(
                symbol,
                date,
                series.get(date, {}),
            )
            if record is None:
                invalid += 1
                continue
            key = (
                record.timestamp[:10],
                record.source,
            )
            if key in existing_keys:
                skipped += 1
                continue
            self.repository.insert(record)
            existing_keys.add(key)
            inserted += 1
        return {
            "status": "success",
            "symbol": symbol,
            "provider": "alphavantage",
            "records_received": len(dates),
            "inserted": inserted,
            "skipped_existing": skipped,
            "invalid": invalid,
            "database_total": self.repository.count(symbol),
        }

