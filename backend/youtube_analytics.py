"""
ISMAIL AI - YouTube Analytics Intelligence
Task 18.8: Real YouTube Analytics API integration.
"""
from __future__ import annotations
import json
import urllib.parse
import urllib.request
from datetime import date
from typing import Any, Optional
DEFAULT_CHANNEL_ID = "UCP75FPRq4DaMoe88G9R3heg"
ANALYTICS_API_URL = (
    "https://youtubeanalytics.googleapis.com/v2/reports"
)
PRIVATE_METRICS = (
    "views",
    "likes",
    "comments",
    "video_thumbnail_impressions",
    "ctr",
    "average_view_duration_seconds",
    "average_percentage_viewed",
    "subscribers_gained",
    "estimated_minutes_watched",
)
class YouTubeAnalytics:
    def __init__(
        self,
        channel_id: str = DEFAULT_CHANNEL_ID,
    ):
        self.channel_id = channel_id
        self.access_token: Optional[str] = None
    def configure_access_token(
        self,
        access_token: str,
    ) -> bool:
        token = (access_token or "").strip()
        if not token:
            return False
        self.access_token = token
        return True
    def is_authorized(self) -> bool:
        return bool(self.access_token)
    def available_metrics(self) -> list[str]:
        return list(PRIVATE_METRICS)
    def status(self) -> dict[str, Any]:
        return {
            "success": True,
            "channel_id": self.channel_id,
            "authorized": self.is_authorized(),
            "oauth_ready": True,
            "private_metrics": self.available_metrics(),
        }
    @staticmethod
    def _validate_date(value: str) -> bool:
        try:
            date.fromisoformat(value)
            return True
        except Exception:
            return False
    def get_channel_metrics(
        self,
        start_date: str,
        end_date: str,
    ) -> dict[str, Any]:
        if not self.is_authorized():
            return {
                "success": False,
                "authorized": False,
                "channel_id": self.channel_id,
                "start_date": start_date,
                "end_date": end_date,
                "metrics": {},
                "error": (
                    "YouTube Analytics OAuth authorization "
                    "is required."
                ),
            }
        if not self._validate_date(start_date):
            return {
                "success": False,
                "authorized": True,
                "error": "Invalid start_date. Use YYYY-MM-DD.",
            }
        if not self._validate_date(end_date):
            return {
                "success": False,
                "authorized": True,
                "error": "Invalid end_date. Use YYYY-MM-DD.",
            }
        if start_date > end_date:
            return {
                "success": False,
                "authorized": True,
                "error": (
                    "start_date must be before or equal "
                    "to end_date."
                ),
            }
        params = {
            "ids": "channel==MINE",
            "startDate": start_date,
            "endDate": end_date,
            "metrics": (
                "views,"
                "likes,"
                "comments,"
                "estimatedMinutesWatched,"
                "averageViewDuration,"
                "averageViewPercentage,"
                "subscribersGained,"
            ),
        }
        url = (
            ANALYTICS_API_URL
            + "?"
            + urllib.parse.urlencode(params)
        )
        request = urllib.request.Request(
            url,
            method="GET",
            headers={
                "Authorization": (
                    "Bearer "
                    + self.access_token
                ),
                "Accept": "application/json",
                "User-Agent": (
                    "ISMAIL-AI-YouTube-Analytics/1.0"
                ),
            },
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=60,
            ) as response:
                raw = response.read().decode(
                    "utf-8",
                    errors="replace",
                )
            data = json.loads(raw)
        except Exception as exc:
            status_code = getattr(
                exc,
                "code",
                None,
            )
            reason = getattr(
                exc,
                "reason",
                None,
            )
            google_reason = None
            try:
                error_body = exc.read().decode(
                    "utf-8",
                    errors="replace",
                )
                error_json = json.loads(
                    error_body
                )
                google_error = error_json.get(
                    "error",
                    {},
                )
                google_reason = (
                    google_error.get("message")
                    or google_error.get("status")
                )
            except Exception:
                pass
            error_text = (
                "YouTube Analytics API request failed: "
                f"{type(exc).__name__}"
            )
            if status_code is not None:
                error_text += (
                    f" (HTTP {status_code})"
                )
            if reason:
                error_text += (
                    f": {reason}"
                )
            if google_reason:
                error_text += (
                    f" | Google: {google_reason}"
                )
            return {
                "success": False,
                "authorized": True,
                "channel_id": self.channel_id,
                "start_date": start_date,
                "end_date": end_date,
                "metrics": {},
                "error": error_text,
            }
        column_headers = data.get(
            "columnHeaders",
            [],
        )
        rows = data.get(
            "rows",
            [],
        )
        headers = [
            str(item.get("name", ""))
            for item in column_headers
        ]
        normalized_rows = []
        for row in rows:
            item = {}
            for index, name in enumerate(headers):
                if index < len(row):
                    item[name] = row[index]
            normalized_rows.append(item)
        totals = {}
        if normalized_rows:
            first = normalized_rows[0]
            totals = {
                "views": first.get("views", 0),
                "likes": first.get("likes", 0),
                "comments": first.get("comments", 0),
                "estimated_minutes_watched": first.get(
                    "estimatedMinutesWatched",
                    0,
                ),
                "average_view_duration_seconds": first.get(
                    "averageViewDuration",
                    0,
                ),
                "average_percentage_viewed": first.get(
                    "averageViewPercentage",
                    0,
                ),
                "subscribers_gained": first.get(
                    "subscribersGained",
                    0,
                ),
                "video_thumbnail_impressions": first.get(
                    "video_thumbnail_impressions",
                    0,
                ),
                "ctr": first.get(
                    "video_thumbnail_impressions_ctr",
                    0,
                ),
            }
        return {
            "success": True,
            "authorized": True,
            "channel_id": self.channel_id,
            "start_date": start_date,
            "end_date": end_date,
            "metrics": totals,
            "rows": normalized_rows,
            "row_count": len(normalized_rows),
            "raw_column_headers": headers,
        }
youtube_analytics = YouTubeAnalytics()
def youtube_analytics_status() -> dict[str, Any]:
    return youtube_analytics.status()
def get_channel_metrics(
    start_date: str,
    end_date: str,
    channel_id: str = DEFAULT_CHANNEL_ID,
) -> dict[str, Any]:
    if channel_id != youtube_analytics.channel_id:
        analyzer = YouTubeAnalytics(
            channel_id
        )
        return analyzer.get_channel_metrics(
            start_date,
            end_date,
        )
    return youtube_analytics.get_channel_metrics(
        start_date,
        end_date,
    )
