from urllib.parse import quote_plus
def detect_browser_action(message: str) -> dict:
    """
    Detect simple browser actions from a user command.
    """
    text = message.strip().lower()
    if text in {"youtube open koro", "youtube open karo", "youtube kholo", "open youtube"}:
        return {
            "action": "open_url",
            "url": "https://www.youtube.com",
        }
    if text in {"google open koro", "google open karo", "google kholo", "open google"}:
        return {
            "action": "open_url",
            "url": "https://www.google.com",
        }
    if text in {"facebook open koro", "facebook open karo", "facebook kholo", "open facebook"}:
        return {
            "action": "open_url",
            "url": "https://www.facebook.com",
        }
    youtube_prefixes = [
        "youtube e ",
        "youtube te ",
        "youtube ",
    ]
    for prefix in youtube_prefixes:
        if text.startswith(prefix) and ("search koro" in text or "search karo" in text):
            query = text[len(prefix):].replace("search koro", "").strip()
            if query:
                return {
                    "action": "open_url",
                    "url": (
                        "https://www.youtube.com/results?search_query="
                        + quote_plus(query)
                    ),
                }
    google_prefixes = [
        "google e ",
        "google te ",
        "google ",
    ]
    for prefix in google_prefixes:
        if text.startswith(prefix) and "search koro" in text:
            query = text[len(prefix):].replace("search koro", "").strip()
            if query:
                return {
                    "action": "open_url",
                    "url": (
                        "https://www.google.com/search?q="
                        + quote_plus(query)
                    ),
                }
    return {
        "action": "none",
        "url": None,
    }
