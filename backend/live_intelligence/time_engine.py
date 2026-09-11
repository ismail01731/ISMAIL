from datetime import datetime
from zoneinfo import ZoneInfo


class TimeEngine:
    """
    Provides reliable current date/time information
    without using AI memory or web search.
    """

    DEFAULT_TIMEZONE = "Asia/Dhaka"

    @classmethod
    def now(cls, timezone_name: str = DEFAULT_TIMEZONE) -> datetime:
        """
        Return current timezone-aware datetime.
        """
        try:
            timezone = ZoneInfo(timezone_name)
        except Exception:
            timezone = ZoneInfo(cls.DEFAULT_TIMEZONE)

        return datetime.now(timezone)

    @classmethod
    def get_time(cls, timezone_name: str = DEFAULT_TIMEZONE) -> dict:
        """
        Return current time information.
        """
        current = cls.now(timezone_name)

        return {
            "type": "time",
            "timezone": timezone_name,
            "iso": current.isoformat(),
            "time_24": current.strftime("%H:%M:%S"),
            "time_12": current.strftime("%I:%M:%S %p"),
            "hour": current.hour,
            "minute": current.minute,
            "second": current.second,
        }

    @classmethod
    def get_date(cls, timezone_name: str = DEFAULT_TIMEZONE) -> dict:
        """
        Return current date information.
        """
        current = cls.now(timezone_name)

        return {
            "type": "date",
            "timezone": timezone_name,
            "iso_date": current.strftime("%Y-%m-%d"),
            "date": current.strftime("%d-%m-%Y"),
            "day": current.strftime("%A"),
            "month": current.strftime("%B"),
            "year": current.year,
        }

    @classmethod
    def get_datetime(cls, timezone_name: str = DEFAULT_TIMEZONE) -> dict:
        """
        Return both date and time.
        """
        current = cls.now(timezone_name)

        return {
            "type": "datetime",
            "timezone": timezone_name,
            "iso": current.isoformat(),
            "date": current.strftime("%d-%m-%Y"),
            "day": current.strftime("%A"),
            "month": current.strftime("%B"),
            "year": current.year,
            "time_24": current.strftime("%H:%M:%S"),
            "time_12": current.strftime("%I:%M:%S %p"),
        }