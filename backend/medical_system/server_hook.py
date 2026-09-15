# Medical server hook (isolated add-on)
from .router import maybe_handle_medical


def medical_emergency_payload(message):
    # Returns API dict ONLY for emergency cases, otherwise None
    try:
        result = maybe_handle_medical(message)
    except Exception:
        return None

    if not result:
        return None

    if not result.get("handled"):
        return None

    return {
        "name": "ISMAIL AI",
        "question": message,
        "response": result.get("reply", ""),
        "action": None,
    }
