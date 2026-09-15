from database.connection import Database
from database.models import HistoricalRecord
from database.repositories.historical import HistoricalRepository
def test_database():
    db = Database(
        "data/test_ismail.db"
    )
    repository = HistoricalRepository(
        db
    )
    record = HistoricalRecord(
        topic="test",
        value="123",
        source="test",
        source_type="test",
        timestamp="2026-09-15T00:00:00+00:00",
        reliability=0.90,
    )
    record_id = repository.insert(
        record
    )
    assert record_id > 0
    data = repository.list_by_topic(
        "test"
    )
    assert len(data) >= 1
