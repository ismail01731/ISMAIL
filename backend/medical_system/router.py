from .config import MEDICAL_ENABLED
from .intent import is_medical_query
from .handler import local_precheck


def maybe_handle_medical(user_text: str) -> dict | None:
    """
    Return:
      None  -> মেডিক্যাল নয়, পুরনো সিস্টেম চালান (কিছুই চেঞ্জ হবে না)
      dict  -> মেডিক্যাল রুট
    """
    if not MEDICAL_ENABLED:
        return None

    if not is_medical_query(user_text):
        return None

    check = local_precheck(user_text)

    if check["type"] == "emergency":
        return {
            "handled": True,
            "reply": check["reply"],
            "use_llm": False,
        }

    return {
        "handled": False,
        "use_llm": True,
        "messages": check["messages"],
        "reply": None,
    }