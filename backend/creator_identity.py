"""
ISMAIL AI - Creator Identity System

This module contains the official identity information of ISMAIL AI
and its creator.

IMPORTANT:
Only put information here that the creator wants ISMAIL AI to reveal.
"""

from __future__ import annotations

import re
from typing import Optional


# ============================================================
# OFFICIAL CREATOR PROFILE
# ============================================================

CREATOR_PROFILE = {
    "name": "ISMAIL",

    "role": [
        "ISMAIL AI-এর Creator",
        "ISMAIL AI-এর Developer"
    ],

    "project": "ISMAIL AI",

    "work": [
        "Artificial Intelligence",
        "Software Development",
        "AI System Development"
    ],

    "description": (
        "ISMAIL AI হলো একটি intelligent AI assistant project, "
        "যেটি তার creator নিজে develop করছেন।"
    ),

    "purpose": (
        "মানুষকে information, reasoning, automation এবং "
        "বিভিন্ন AI capability-এর মাধ্যমে সাহায্য করা।"
    ),

    # এখানে শুধু public information রাখবেন।
    "public_information": True,
}


# ============================================================
# ISMAIL AI IDENTITY
# ============================================================

AI_IDENTITY = {
    "name": "ISMAIL AI",

    "type": "Artificial Intelligence Assistant",

    "creator": CREATOR_PROFILE["name"],

    "creator_role": "Creator and Developer",

    "purpose": CREATOR_PROFILE["purpose"],
}


# ============================================================
# IDENTITY QUESTION DETECTION
# ============================================================

IDENTITY_PATTERNS = [
    # English
    r"\bwho created you\b",
    r"\bwho made you\b",
    r"\bwho built you\b",
    r"\bwho developed you\b",
    r"\bwho is your creator\b",
    r"\bwho is your developer\b",
    r"\bwho owns you\b",
    r"\bwho are you\b",
    r"\bwhat is your name\b",

    # Bangla
    r"তোমাকে কে বানিয়েছে",
    r"তোমাকে কে বানিয়েছে",
    r"তোমাকে কে তৈরি করেছে",
    r"কে তোমাকে বানিয়েছে",
    r"কে তোমাকে বানিয়েছে",
    r"কে তোমাকে তৈরি করেছে",
    r"তোমার creator কে",
    r"তোমার ক্রিয়েটর কে",
    r"তোমার ক্রিয়েটর কে",
    r"তোমার developer কে",
    r"তোমার ডেভেলপার কে",
    r"তোমার মালিক কে",
    r"তুমি কে",
    r"তোমার নাম কি",
    r"তোমার নাম কী",

    # Mixed Bangla/English
    r"ismail ai কে বানিয়েছে",
    r"ismail ai কে বানিয়েছে",
    r"ismail ai কে তৈরি করেছে",
    r"ismail ai creator কে",
    r"ismail ai developer কে",
]


def is_identity_question(message: str) -> bool:
    """
    Return True when the user is asking about ISMAIL AI's identity
    or creator.
    """

    if not message:
        return False

    text = message.strip().lower()

    return any(
        re.search(pattern, text, flags=re.IGNORECASE)
        for pattern in IDENTITY_PATTERNS
    )


# ============================================================
# IDENTITY ANSWER GENERATOR
# ============================================================

def get_identity_answer(message: str) -> Optional[str]:
    """
    Return a deterministic answer for creator/identity questions.

    This information does not depend on the LLM.
    """

    if not is_identity_question(message):
        return None

    text = message.strip().lower()

    creator_name = CREATOR_PROFILE["name"]

    # --------------------------------------------------------
    # Creator questions
    # --------------------------------------------------------

    creator_keywords = [
        "creator",
        "created",
        "made",
        "built",
        "developed",
        "বানিয়েছে",
        "বানিয়েছে",
        "তৈরি করেছে",
        "ক্রিয়েটর",
        "ক্রিয়েটর",
        "ডেভেলপার",
        "developer",
        "মালিক",
    ]

    if any(keyword in text for keyword in creator_keywords):

        return (
            f"আমি ISMAIL AI। আমাকে {creator_name} তৈরি করেছেন। "
            f"তিনি ISMAIL AI-এর Creator এবং Developer।"
        )

    # --------------------------------------------------------
    # Name questions
    # --------------------------------------------------------

    name_keywords = [
        "তোমার নাম",
        "তুমি কে",
        "your name",
        "who are you",
    ]

    if any(keyword in text for keyword in name_keywords):

        return (
            f"আমার নাম ISMAIL AI। "
            f"আমাকে {creator_name} তৈরি করেছেন।"
        )

    # --------------------------------------------------------
    # Default identity response
    # --------------------------------------------------------

    return (
        f"আমি ISMAIL AI, একটি Artificial Intelligence Assistant। "
        f"আমার Creator এবং Developer হলেন {creator_name}।"
    )


# ============================================================
# CREATOR PROFILE ACCESS
# ============================================================

def get_creator_profile() -> dict:
    """
    Return a copy of the public creator profile.
    """

    return dict(CREATOR_PROFILE)


def get_ai_identity() -> dict:
    """
    Return a copy of ISMAIL AI's official identity.
    """

    return dict(AI_IDENTITY)
