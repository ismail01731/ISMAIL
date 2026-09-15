from evidence import EvidenceCollector, EvidenceScorer
def test_evidence():
    collector = EvidenceCollector()
    item = collector.add(
        content="Example evidence",
        source="Example source",
        source_type="official",
        reliability=0.95,
        relevance=0.90,
        freshness=1.00,
    )
    assert item.quality_score() > 0.80
def test_scorer():
    scorer = EvidenceScorer()
    score = scorer.calculate(
        source_type="government",
        relevance=0.90,
        timestamp="2026-09-15T00:00:00+00:00",
    )
    assert 0 <= score <= 1
