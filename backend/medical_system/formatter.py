from .config import DISCLAIMER


def format_emergency(messages: list, extra: str = "") -> str:
    lines = ["জরুরি কি? **Yes**"]
    for m in messages:
        lines.append(f"- {m}")
    if extra:
        lines.append("")
        lines.append(extra)
    lines.append("")
    lines.append("এখনই করণীয়:")
    lines.append("- কাছের মানুষকে বলুন, হাসপাতাল/ইমার্জেন্সিতে যান")
    lines.append("- বাংলাদেশে সরকারি হাসপাতাল ইমার্জেন্সি বিনামূল্যে/কম খরচে হতে পারে")
    lines.append("- হটলাইন: 16263 (Shasthyo Batayon) — তথ্যের জন্য")
    lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)


def missing_intake_question() -> str:
    return (
        "আপনার সমস্যাটা নিরাপদে বুঝতে এই তথ্যগুলো দিন:\n"
        "1) বয়স ও লিঙ্গ\n"
        "2) জেলা/শহর\n"
        "3) প্রধান উপসর্গ + কতদিন\n"
        "4) তীব্রতা 1-10\n"
        "5) জ্বর/শ্বাসকষ্ট/বুকব্যথা/অজ্ঞান/খিঁচুনি/রক্তপাত আছে কি?\n"
        "6) আগের রোগ, চলতি ওষুধ, অ্যালার্জি\n\n"
        f"{DISCLAIMER}"
    )