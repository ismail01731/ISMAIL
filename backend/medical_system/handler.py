from .config import DISCLAIMER
from .red_flags import find_red_flags
from .formatter import format_emergency, missing_intake_question
from .system_prompt import SYSTEM_PROMPT


INTAKE_KEYS = ["বয়স", "age", "জ্বর", "দিন", "ব্যথা", "লিঙ্গ"]


def build_messages(user_text: str, history=None):
    """
    আপনার বিদ্যমান LLM কলে এই messages ব্যবহার করুন।
    অন্য সিস্টেমের prompt মুছবেন না—শুধু মেডিক্যাল রুটে এটা ব্যবহার করুন।
    """
    history = history or []
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    msgs.extend(history)
    msgs.append({"role": "user", "content": user_text})
    return msgs


def local_precheck(user_text: str) -> dict:
    """
    LLM এর আগে দ্রুত সেফটি চেক।
    emergency হলে সাথে সাথে উত্তর দিতে পারেন, LLM ছাড়াই।
    """
    flags = find_red_flags(user_text)
    if flags:
        return {
            "type": "emergency",
            "reply": format_emergency([f["message"] for f in flags]),
        }

    # খুব ছোট মেসেজ হলে ইনটেক চাইবে
    if len((user_text or "").strip()) < 12 or not any(
        k in (user_text or "").lower() for k in INTAKE_KEYS
    ):
        # তবুও উপসর্গ থাকলে LLM চালাতে দিন
        pass

    return {
        "type": "continue",
        "reply": None,
        "messages": build_messages(user_text),
        "fallback_if_no_llm": missing_intake_question() + "\n\n" + DISCLAIMER,
    }