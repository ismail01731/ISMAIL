from backend.web_research import WebResearch
import urllib.parse
r = WebResearch()
u = (
    "https://www.google.com/search?q="
    + urllib.parse.quote_plus("What is Python programming language?")
    + "&num=10&hl=en"
)
html_text = r._http_get(
    u,
    headers={
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    },
)
print("TYPE =", type(html_text).__name__)
print("LENGTH =", len(html_text or ""))
print("HAS_H3 =", "<h3" in (html_text or "").lower())
print("HAS_GOOGLE =", "google" in (html_text or "").lower())
print("HAS_CAPTCHA =", "captcha" in (html_text or "").lower())
print()
print((html_text or "")[:5000])
