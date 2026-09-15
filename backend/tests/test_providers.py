from live_data.manager import LiveDataManager
def test_provider_registration():
    manager = LiveDataManager()
    providers = (
        manager.available_providers()
    )
    assert "manual" in providers
    assert "newsapi" in providers
    assert "alphavantage" in providers
