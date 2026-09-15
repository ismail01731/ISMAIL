"""
ISMAIL Database Intelligence
Task 5
"""
from .connection import Database
from .models import (
    HistoricalRecord,
    PredictionRecord,
)
__all__ = [
    "Database",
    "HistoricalRecord",
    "PredictionRecord",
]
