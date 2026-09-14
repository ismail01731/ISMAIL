from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class DomainMatch:
    domain: str
    confidence: str
    matches: tuple[str, ...] = ()
class DomainDetector:
    DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
        "medical": (
            "medical",
            "medicine",
            "health",
            "doctor",
            "symptom",
            "disease",
            "hospital",
            "fever",
            "pain",
            "headache",
            "cough",
            "cold",
            "vomiting",
            "diarrhea",
            "রোগ",
            "চিকিৎসা",
            "ডাক্তার",
            "লক্ষণ",
            "জ্বর",
            "ব্যথা",
            "মাথাব্যথা",
            "কাশি",
            "সর্দি",
            "বমি",
            "ডায়রিয়া",
            "স্বাস্থ্য",
        ),
        "electronics": (
            "electronics",
            "electrical",
            "circuit",
            "voltage",
            "current",
            "resistor",
            "capacitor",
            "transistor",
            "diode",
            "arduino",
            "esp32",
            "ohm",
            "watt",
            "ampere",
            "frequency",
            "inductor",
            "relay",
            "sensor",
            "ইলেকট্রনিক্স",
            "সার্কিট",
            "ভোল্টেজ",
            "কারেন্ট",
            "ওহম",
            "ওয়াট",
            "অ্যাম্পিয়ার",
            "ফ্রিকোয়েন্সি",
            "ইন্ডাক্টর",
            "রিলে",
            "সেন্সর",
        ),
        "education": (
            "education",
            "study",
            "exam",
            "school",
            "college",
            "university",
            "lesson",
            "homework",
            "শিক্ষা",
            "পড়াশোনা",
            "পরীক্ষা",
            "স্কুল",
            "কলেজ",
            "বিশ্ববিদ্যালয়",
        ),
        "mathematics": (
            "math",
            "mathematics",
            "algebra",
            "geometry",
            "calculus",
            "equation",
            "গণিত",
            "বীজগণিত",
            "জ্যামিতি",
            "ক্যালকুলাস",
            "সমীকরণ",
        ),
        "science": (
            "science",
            "physics",
            "chemistry",
            "biology",
            "astronomy",
            "বিজ্ঞান",
            "পদার্থবিজ্ঞান",
            "রসায়ন",
            "জীববিজ্ঞান",
            "জ্যোতির্বিজ্ঞান",
        ),
    }
    def detect(self, message: str) -> list[DomainMatch]:
        if not isinstance(message, str):
            return []
        normalized = message.strip().lower()
        if not normalized:
            return []
        results: list[DomainMatch] = []
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            matches = tuple(
                keyword
                for keyword in keywords
                if keyword in normalized
            )
            if not matches:
                continue
            confidence = "high" if len(matches) >= 2 else "medium"
            results.append(
                DomainMatch(
                    domain=domain,
                    confidence=confidence,
                    matches=matches,
                )
            )
        return results
