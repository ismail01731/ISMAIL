from __future__ import annotations

from backend.medical.medical_ai import MedicalAI, MedicalAssessment


class MedicalResponse:
    """
    Safety-focused medical response layer for ISMAIL AI.

    Emergency cases are handled directly.
    Routine medical cases return a safe instruction for LLM processing.
    """

    def __init__(self) -> None:
        self.medical_ai = MedicalAI()

    def assess(self, message: str) -> MedicalAssessment:
        return self.medical_ai.assess(message)

    def get_response(self, message: str) -> str | None:
        assessment = self.assess(message)

        if not assessment.is_medical:
            return None

        if assessment.urgency == "emergency":
            return assessment.response

        return (
            "আপনার প্রশ্নটি একটি সাধারণ মেডিকেল প্রশ্ন হিসেবে শনাক্ত হয়েছে। "
            "জ্বর, ব্যথা বা অন্যান্য উপসর্গের কারণ বিভিন্ন হতে পারে এবং "
            "শুধু একটি উপসর্গ দেখে নিশ্চিত রোগ নির্ণয় করা যায় না। "
            "উপসর্গটি গুরুতর, দীর্ঘস্থায়ী বা ক্রমশ খারাপ হলে একজন যোগ্য "
            "চিকিৎসকের পরামর্শ নেওয়া উচিত। "
            "জরুরি লক্ষণ যেমন শ্বাসকষ্ট, তীব্র বুকব্যথা, অজ্ঞান হওয়া বা "
            "অতিরিক্ত রক্তপাত হলে দ্রুত জরুরি চিকিৎসা সেবা নিন।"
        )

    def build_llm_prompt(self, message: str) -> str:
        assessment = self.assess(message)

        if not assessment.is_medical:
            raise ValueError("Message is not a medical request.")

        if assessment.urgency == "emergency":
            raise ValueError(
                "Emergency medical requests must use the safety response."
            )

        return f"""
You are the medical information layer of ISMAIL AI.

User's medical question:
{message}

STRICT MEDICAL SAFETY RULES:

1. Provide general medical information only.
2. Never diagnose the user.
3. Never invent medical history, test results, symptoms, or measurements.
4. Never invent numerical medical facts.
5. Do not give medication dosage or prescription instructions.
6. If a fact is uncertain, clearly say that it is uncertain.
7. Do not make claims that are not supported by the user's question.
8. Explain common possibilities carefully without presenting them as a diagnosis.
9. Mention important warning signs when relevant.
10. If the symptoms may be serious or worsening, recommend contacting a qualified healthcare professional.
11. If the user describes an emergency, recommend urgent medical care.
12. Keep the answer concise, clear, and practical.
13. Respond in the same language as the user's question.
14. Do not say that you are a doctor.
15. Do not replace professional medical evaluation.

Important:
Only answer what can be safely explained from the user's question.
Do not fabricate facts.

User question:
{message}
""".strip()