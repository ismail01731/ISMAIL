MEDICAL_KEYWORDS = [
    "অসুখ", "অসুস্থ", "রোগ", "জ্বর", "কাশি", "সর্দি", "ব্যথা", "বমি",
    "ডায়রিয়া", "মাথাব্যথা", "গলা ব্যথা", "শ্বাসকষ্ট", "বুকব্যথা", "চুলকানি",
    "ডাক্তার", "ওষুধ", "ঔষধ", "হাসপাতাল", "ইনফেকশন", "এলার্জি",
    "fever", "pain", "cough", "vomit", "diarrhea", "medicine", "doctor",
    "rash", "headache", "infection", "pregnant", "baby", "child",
]


def is_medical_query(text: str) -> bool:
    t = (text or "").lower()
    return any(k.lower() in t for k in MEDICAL_KEYWORDS)