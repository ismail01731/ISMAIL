from intelligence.adapter import ExistingAIAdapter
def test_not_connected():
    adapter = ExistingAIAdapter()
    result = adapter.generate(
        "test prompt",
        {"x": 1},
    )
    assert result["status"] == "not_connected"
def test_one_argument_ai():
    def fake_ai(prompt):
        return "AI RESPONSE: " + prompt[:10]
    adapter = ExistingAIAdapter(
        fake_ai,
        name="fake_one_arg",
    )
    result = adapter.generate(
        "hello future",
        {},
    )
    assert result["status"] == "success"
    assert "AI RESPONSE" in result["response"]
def test_two_argument_ai():
    def fake_ai(prompt, context):
        return {
            "prompt": prompt,
            "context_received": bool(
                context
            ),
        }
    adapter = ExistingAIAdapter(
        fake_ai,
        name="fake_two_arg",
    )
    result = adapter.generate(
        "hello",
        {"forecast": 123},
    )
    assert result["status"] == "success"
    assert result["response"]["context_received"]
def test_keyword_ai():
    def fake_ai(
        prompt=None,
        context=None,
    ):
        return {
            "ok": True,
            "prompt": prompt,
            "context": context,
        }
    adapter = ExistingAIAdapter(
        fake_ai,
        name="fake_keyword",
    )
    result = adapter.generate(
        "hello",
        {"x": 1},
    )
    assert result["status"] == "success"
    assert result["response"]["ok"] is True
def test_status():
    adapter = ExistingAIAdapter()
    status = adapter.status()
    assert status["connected"] is False
    assert status["owns_model"] is False
    assert status["creates_new_ai"] is False
