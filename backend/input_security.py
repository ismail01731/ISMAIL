import re
from dataclasses import dataclass
@dataclass(frozen=True)
class SecurityResult:
    allowed: bool
    risk_level: str
    reason: str
class InputSecurity:
    """Conservative pre-AI input security scanner for ISMAIL AI."""
    MAX_INPUT_LENGTH = 12000
    HIGH_RISK_PATTERNS = (
        re.compile(r"\bignore\s+(all\s+)?previous\s+instructions\b", re.I),
        re.compile(r"\bignore\s+(all\s+)?system\s+instructions\b", re.I),
        re.compile(r"\bdisregard\s+(all\s+)?previous\s+instructions\b", re.I),
        re.compile(r"\breveal\s+(your\s+)?system\s+prompt\b", re.I),
        re.compile(r"\bshow\s+(me\s+)?your\s+system\s+prompt\b", re.I),
        re.compile(r"\bprint\s+(your\s+)?system\s+prompt\b", re.I),
        re.compile(r"\bdeveloper\s+instructions?\b", re.I),
        re.compile(r"\bextract\s+(the\s+)?(api|secret|private)\s+key\b", re.I),
        re.compile(r"\bshow\s+(me\s+)?(your\s+|the\s+)?(api|secret|private)\s+key\b", re.I),
        re.compile(r"\b(?:jailbreak|bypass)\s+(?:your\s+)?(?:safety|security|rules?)\b", re.I),
    )
    SUSPICIOUS_PATTERNS = (
        re.compile(r"\b(?:rm\s+-rf|format\s+[a-z]:|del\s+/[fq])\b", re.I),
        re.compile(r"\b(?:powershell|cmd\.exe)\s+.*(?:-enc|-encodedcommand)\b", re.I),
        re.compile(r"\b(?:base64|hex)\s+decode\b", re.I),
    )
    def scan(self, message: str) -> SecurityResult:
        if not isinstance(message, str):
            return SecurityResult(
                False,
                "high",
                "Invalid input type.",
            )
        text = message.strip()
        if not text:
            return SecurityResult(
                False,
                "low",
                "Message cannot be empty.",
            )
        if len(text) > self.MAX_INPUT_LENGTH:
            return SecurityResult(
                False,
                "high",
                "Input is too large.",
            )
        for pattern in self.HIGH_RISK_PATTERNS:
            if pattern.search(text):
                return SecurityResult(
                    False,
                    "high",
                    "Input contains a potentially malicious instruction.",
                )
        for pattern in self.SUSPICIOUS_PATTERNS:
            if pattern.search(text):
                return SecurityResult(
                    False,
                    "medium",
                    "Input contains a suspicious command pattern.",
                )
        return SecurityResult(
            True,
            "low",
            "Input passed security screening.",
        )

