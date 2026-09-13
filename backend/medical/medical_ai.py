from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MedicalAssessment:
    is_medical: bool
    urgency: str
    response: str


class MedicalAI:
    """
    Safety-focused medical AI layer for ISMAIL AI.

    This module provides general medical information and triage guidance.
    It does not diagnose diseases or replace a qualified clinician.
    """

    MEDICAL_KEYWORDS = {
        "জ্বর",
        "কাশি",
        "সর্দি",
        "ব্যথা",
        "মাথাব্যথা",
        "পেটব্যথা",
        "বমি",
        "ডায়রিয়া",
        "ডায়রিয়া",
        "রক্তপাত",
        "শ্বাসকষ্ট",
        "বুকব্যথা",
        "অ্যালার্জি",
        "ওষুধ",
        "ঔষধ",
        "medicine",
        "symptom",
        "symptoms",
        "fever",
        "cough",
        "pain",
        "headache",
        "vomiting",
        "diarrhea",
        "bleeding",
        "breathing",
        "chest pain",
        "allergy",
    }

    EMERGENCY_KEYWORDS = {
        "শ্বাস নিতে পারছি না",
        "শ্বাস নিতে কষ্ট হচ্ছে",
        "শ্বাসকষ্ট",
        "বুকে তীব্র ব্যথা",
        "অজ্ঞান",
        "খিঁচুনি",
        "অতিরিক্ত রক্তপাত",
        "বিষ খেয়েছে",
        "বিষ খেয়েছে",
        "can't breathe",
        "cannot breathe",
        "severe chest pain",
        "chest pain",
        "unconscious",
        "seizure",
        "heavy bleeding",
        "poisoning",
    }

    def is_medical_request(self, message: str) -> bool:
        if not isinstance(message, str):
            return False

        text = message.strip().lower()

        if not text:
            return False

        return any(keyword in text for keyword in self.MEDICAL_KEYWORDS) or any(
            keyword in text for keyword in self.EMERGENCY_KEYWORDS
        )

    def detect_urgency(self, message: str) -> str:
        text = message.strip().lower()

        if any(keyword in text for keyword in self.EMERGENCY_KEYWORDS):
            return "emergency"

        if self.is_medical_request(text):
            return "routine"

        return "unknown"

    def assess(self, message: str) -> MedicalAssessment:
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Medical message cannot be empty.")

        if not self.is_medical_request(message):
            return MedicalAssessment(
                is_medical=False,
                urgency="unknown",
                response="এটি মেডিকেল প্রশ্ন হিসেবে শনাক্ত হয়নি।",
            )

        urgency = self.detect_urgency(message)

        if urgency == "emergency":
            return MedicalAssessment(
                is_medical=True,
                urgency="emergency",
                response=(
                    "এটি জরুরি চিকিৎসা পরিস্থিতি হতে পারে। "
                    "দ্রুত স্থানীয় জরুরি চিকিৎসা সেবা বা নিকটস্থ হাসপাতালের "
                    "জরুরি বিভাগে যোগাযোগ করুন।"
                ),
            )

        return MedicalAssessment(
            is_medical=True,
            urgency="routine",
            response=(
                "এটি একটি মেডিকেল প্রশ্ন। সাধারণ স্বাস্থ্যতথ্য দেওয়া যেতে পারে, "
                "তবে উপসর্গের ভিত্তিতে নিশ্চিত রোগ নির্ণয় করা উচিত নয়। "
                "প্রয়োজনে একজন যোগ্য চিকিৎসকের পরামর্শ নিন।"
            ),
        )