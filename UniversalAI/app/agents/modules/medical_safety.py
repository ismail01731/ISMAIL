import re


class MedicalSafety:

    # =========================================================
    # EMERGENCY INPUT DETECTION
    # =========================================================

    EMERGENCY_KEYWORDS = [
        # English
        "chest pain",
        "severe chest pain",
        "difficulty breathing",
        "breathing difficulty",
        "can't breathe",
        "cannot breathe",
        "severe bleeding",
        "unconscious",
        "seizure",
        "stroke",
        "heart attack",

        # বাংলা
        "বুকে ব্যথা",
        "বুকে প্রচণ্ড ব্যথা",
        "বুকে তীব্র ব্যথা",
        "বুকের ব্যথা",
        "শ্বাসকষ্ট",
        "শ্বাস নিতে কষ্ট",
        "শ্বাস নিতে পারছি না",
        "শ্বাস নিতে পারছেন না",
        "অতিরিক্ত রক্তপাত",
        "অনেক রক্তপাত",
        "অজ্ঞান",
        "খিঁচুনি",
        "স্ট্রোক",
        "হার্ট অ্যাটাক",
    ]


    # =========================================================
    # UNSAFE MEDICATION PHRASES
    # =========================================================

    UNSAFE_PHRASES = [
        # English
        "stop taking your medication",
        "stop your medication",
        "stop taking the medicine",
        "stop the medicine",
        "stop taking this medicine",

        "double your dose",
        "increase your dose",
        "decrease your dose",
        "change your dose",

        "start antibiotics",
        "take antibiotics without",
        "use antibiotics without",

        "take extra medicine",
        "take an extra dose",

        # বাংলা
        "ওষুধ বন্ধ করুন",
        "ওষুধ বন্ধ করবেন",
        "ওষুধ বন্ধ করো",
        "এই ওষুধ বন্ধ করুন",

        "ডোজ বাড়ান",
        "ডোজ বাড়ান",
        "ডোজ কমান",
        "ডোজ পরিবর্তন করুন",
        "ডোজ পরিবর্তন করবেন",

        "নিজে থেকে অ্যান্টিবায়োটিক",
        "নিজে থেকে অ্যান্টিবায়োটিক",
        "অ্যান্টিবায়োটিক শুরু করুন",
        "অ্যান্টিবায়োটিক শুরু করুন",

        "অতিরিক্ত ওষুধ নিন",
        "অতিরিক্ত ডোজ নিন",
    ]


    # =========================================================
    # DOSAGE DETECTION
    # =========================================================

    DOSAGE_PATTERNS = [

        # English
        r"\b\d+(?:\.\d+)?\s*mg\s*/\s*kg\b",
        r"\b\d+(?:\.\d+)?\s*mg\s+per\s+kg\b",
        r"\b\d+(?:\.\d+)?\s*mg\b",
        r"\b\d+(?:\.\d+)?\s*(?:g|gram|grams)\b",

        r"\b\d+\s*(?:tablet|tablets)\b",
        r"\b\d+\s*(?:capsule|capsules)\b",

        r"\bevery\s+\d+(?:\s*[-–]\s*\d+)?\s*(?:hours?|hrs?)\b",

        r"\b(?:maximum|max)\s+\d+(?:\.\d+)?\s*(?:mg|g|gram|grams)\b",

        # বাংলা units
        r"[০-৯]+(?:[.,][০-৯]+)?\s*মি\.?\s*গ্রা\.?",
        r"[০-৯]+(?:[.,][০-৯]+)?\s*মিগ্রা",
        r"[০-৯]+(?:[.,][০-৯]+)?\s*মিলিগ্রাম",
        r"[০-৯]+(?:[.,][০-৯]+)?\s*গ্রাম",

        r"[০-৯]+\s*(?:ট্যাবলেট|ট্যাবলেটটি)",
        r"[০-৯]+\s*(?:ক্যাপসুল|ক্যাপসুলটি)",

        r"প্রতি\s+[০-৯]+(?:\s*[-–]\s*[০-৯]+)?\s*(?:ঘণ্টা|ঘন্টা)",
        r"প্রতি\s+[0-9]+(?:\s*[-–]\s*[0-9]+)?\s*(?:ঘণ্টা|ঘন্টা)",

        r"দিনে\s+[০-৯]+\s*বার",
        r"দিনে\s+[0-9]+\s*বার",

        r"[০-৯]+\s*মি\.?\s*গ্রা\.?\s*/\s*কেজি",
        r"[০-৯]+\s*মিগ্রা\s*/\s*কেজি",
        r"[০-৯]+\s*মিলিগ্রাম\s*/\s*কেজি",

        r"[০-৯]+\s*[-–]\s*[০-৯]+\s*(?:mg|মিগ্রা|মিলিগ্রাম|মি\.?\s*গ্রা\.?)",
        r"\d+\s*[-–]\s*\d+\s*(?:mg|মিগ্রা|মিলিগ্রাম|মি\.?\s*গ্রা\.?)",
    ]


    # =========================================================
    # PRESCRIPTION COMMANDS
    # =========================================================

    PRESCRIPTION_PATTERNS = [
        r"\btake\s+\d+",
        r"\buse\s+\d+",
        r"\bgive\s+\d+",

        r"প্রতিবার\s+[০-৯]+",
        r"প্রতিবার\s+\d+",

        r"দিনে\s+[০-৯]+\s*বার",
        r"দিনে\s+\d+\s*বার",

        r"প্রতি\s+[০-৯]+\s*(?:ঘণ্টা|ঘন্টা)",
        r"প্রতি\s+\d+\s*(?:ঘণ্টা|ঘন্টা)",

        r"খান\s+[০-৯]+",
        r"খান\s+\d+",

        r"নিন\s+[০-৯]+",
        r"নিন\s+\d+",
    ]


    # =========================================================
    # UNSAFE SELF-TREATMENT
    # =========================================================

    SELF_TREATMENT_PATTERNS = [

        # English
        r"\byou should take\b",
        r"\byou should use\b",
        r"\byou need to take\b",
        r"\byou need to use\b",
        r"\btake this medicine\b",
        r"\bstart taking\b",
        r"\bstart using\b",

        # বাংলা
        r"ওষুধটি .*নিন",
        r"ওষুধটি .*খান",
        r"ওষুধটি ব্যবহার করুন",

        r"এই ওষুধ .*নিন",
        r"এই ওষুধ .*খান",
        r"এই ওষুধ .*ব্যবহার করুন",

        r"নিজে থেকে .*নিন",
        r"নিজে থেকে .*খান",
        r"নিজে থেকে .*ব্যবহার করুন",
    ]


    # =========================================================
    # UNSUPPORTED DIAGNOSIS CERTAINTY
    # =========================================================

    CERTAINTY_PATTERNS = [

        # English
        "you definitely have",
        "this definitely means",
        "this proves that you have",
        "you certainly have",
        "the diagnosis is",

        # বাংলা
        "আপনার নিশ্চিতভাবে",
        "আপনার অবশ্যই",
        "এটি নিশ্চিতভাবে",
        "এটাই আপনার রোগ",
        "আপনার রোগটি নিশ্চিত",
    ]


    # =========================================================
    # UNSAFE GENERIC MEDICATION ADVICE
    # =========================================================

    GENERIC_MEDICATION_ADVICE = [

        # English
        "take it at the same time every day",
        "take it with food",
        "take it after food",
        "take it before food",
        "take it on an empty stomach",

        # বাংলা
        "প্রতিদিন একই সময়ে নিন",
        "প্রতিদিন একই সময়ে নিন",
        "খাবারের সঙ্গে নিন",
        "খাবারের সাথে নিন",
        "খাবারের পরে নিন",
        "খাবার পরে নিন",
        "খাবারের আগে নিন",
        "খাবার আগে নিন",
        "খালি পেটে নিন",
    ]


    # =========================================================
    # EMERGENCY CHECK
    # =========================================================

    def check(self, message: str):

        if not message:
            return {
                "is_emergency": False,
                "matches": [],
                "message": None
            }

        text = message.lower()

        matches = [
            keyword
            for keyword in self.EMERGENCY_KEYWORDS
            if keyword.lower() in text
        ]

        if matches:

            return {
                "is_emergency": True,
                "matches": matches,
                "message": (
                    "This may be a medical emergency. "
                    "Please seek immediate emergency medical care."
                )
            }

        return {
            "is_emergency": False,
            "matches": [],
            "message": None
        }


    # =========================================================
    # CONTROLLED FEVER RESPONSE
    # =========================================================

    def controlled_fever_response(self, user_message: str):

        return (
            "জ্বর হলে সাধারণভাবে পর্যাপ্ত বিশ্রাম নিন এবং "
            "পানি ও অন্যান্য উপযুক্ত তরল পান করে শরীরকে "
            "হাইড্রেটেড রাখুন।\n\n"

            "হালকা ও আরামদায়ক পোশাক পরুন এবং অতিরিক্ত "
            "গরমে বা অতিরিক্ত ঠান্ডায় থাকার চেষ্টা করবেন না।\n\n"

            "জ্বরের সঙ্গে শ্বাসকষ্ট, বুকে ব্যথা, খিঁচুনি, "
            "অজ্ঞান হওয়া, খুব বেশি দুর্বলতা, বিভ্রান্তি বা "
            "অন্য কোনো গুরুতর উপসর্গ থাকলে দ্রুত চিকিৎসা "
            "সহায়তা নিন।\n\n"

            "শিশু, বয়স্ক ব্যক্তি, গর্ভবতী ব্যক্তি বা "
            "দীর্ঘমেয়াদি অসুস্থতা/কম রোগপ্রতিরোধ ক্ষমতা "
            "থাকা ব্যক্তির ক্ষেত্রে চিকিৎসকের পরামর্শ নেওয়া "
            "বিশেষভাবে গুরুত্বপূর্ণ।\n\n"

            "জ্বরের কারণ বিভিন্ন হতে পারে। তাই শুধু জ্বরের "
            "উপসর্গ দেখে নির্দিষ্ট রোগের নিশ্চিত diagnosis "
            "দেওয়া সম্ভব নয়। প্রয়োজন হলে চিকিৎসকের সরাসরি "
            "পরামর্শ নিন।"
        )


    # =========================================================
    # MEDICAL RESPONSE QUALITY FILTER
    # =========================================================

    def quality_filter(self, user_message: str, response: str):

        if not response:
            return response

        user_text = (user_message or "").lower()
        answer = response.strip()


        # -----------------------------------------------------
        # Fever
        # -----------------------------------------------------

        fever_question = (
            "জ্বর" in user_text
            or "fever" in user_text
        )

        if fever_question:
            return self.controlled_fever_response(user_message)


        # -----------------------------------------------------
        # Detect whether medicine name was actually supplied
        # -----------------------------------------------------

        medicine_words = [
            "ওষুধ",
            "ঔষধ",
            "medicine",
            "drug",
            "tablet",
            "ট্যাবলেট",
            "capsule",
            "ক্যাপসুল",
        ]

        medicine_question = any(
            word in user_text
            for word in medicine_words
        )


        # -----------------------------------------------------
        # Unknown medicine detection
        # -----------------------------------------------------

        unknown_medicine = (
            medicine_question
            and not re.search(
                r"(?:নাম|name|নামটি|নামটা)\s*[:\-]?\s*\S+",
                user_text
            )
        )


        # -----------------------------------------------------
        # Unknown medicine + side effects
        # -----------------------------------------------------

        side_effect_question = (
            "পার্শ্বপ্রতিক্রিয়া" in user_text
            or "পার্শ্বপ্রতিক্রিয়া" in user_text
            or "side effect" in user_text
            or "side effects" in user_text
        )

        if side_effect_question and unknown_medicine:

            return (
                "কোন ওষুধটি ব্যবহার করছেন তার নাম না জানলে "
                "ওষুধটির নির্দিষ্ট পার্শ্বপ্রতিক্রিয়া সম্পর্কে "
                "নির্ভরযোগ্য তথ্য দেওয়া সম্ভব নয়।\n\n"

                "ওষুধের নাম জানালে সেটি সম্পর্কে সাধারণ "
                "তথ্য ব্যাখ্যা করা যেতে পারে।\n\n"

                "যদি ওষুধ ব্যবহারের পর শ্বাসকষ্ট, মুখ বা গলা "
                "ফুলে যাওয়া, অজ্ঞান হওয়া, তীব্র র‍্যাশ বা "
                "অন্য কোনো গুরুতর উপসর্গ দেখা দেয়, দ্রুত "
                "জরুরি চিকিৎসা নিন।"
            )


        # -----------------------------------------------------
        # Remove invented emergency numbers
        # -----------------------------------------------------

        answer = re.sub(
            r"(?:৯৯৯|999)\s*(?:নম্বরে|নম্বর|number|কল করুন|call)",
            "স্থানীয় জরুরি সেবায় যোগাযোগ করুন",
            answer,
            flags=re.IGNORECASE
        )


        # -----------------------------------------------------
        # Remove obviously fabricated terminology
        # -----------------------------------------------------

        bad_terms = [
            "সাঁতার-সদৃশ অ্যানাফাইল্যাক্সিস",
            "গোঁফে হালকা শুষ্কতা",
            "স্নায়ুজনিত ফাঁস",
            "স্নায়ুজনিত ফাঁস",
            "গা দুয়াই দাহ",
            "গা দুয়াই দাহ",
        ]

        for term in bad_terms:
            answer = answer.replace(term, "")


        # -----------------------------------------------------
        # Final cleanup
        # -----------------------------------------------------

        answer = re.sub(
            r"\n{3,}",
            "\n\n",
            answer
        ).strip()

        return answer


    # =========================================================
    # FINAL RESPONSE VALIDATION
    # =========================================================

    def validate_response(self, response: str):

        if not response:
            return response

        text = response.lower()


        # -----------------------------------------------------
        # Unsafe phrases
        # -----------------------------------------------------

        found_phrases = [
            phrase
            for phrase in self.UNSAFE_PHRASES
            if phrase.lower() in text
        ]


        # -----------------------------------------------------
        # Dosage
        # -----------------------------------------------------

        found_dosage = [
            pattern
            for pattern in self.DOSAGE_PATTERNS
            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )
        ]


        # -----------------------------------------------------
        # Prescription commands
        # -----------------------------------------------------

        found_prescription = [
            pattern
            for pattern in self.PRESCRIPTION_PATTERNS
            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )
        ]


        # -----------------------------------------------------
        # Self-treatment
        # -----------------------------------------------------

        found_self_treatment = [
            pattern
            for pattern in self.SELF_TREATMENT_PATTERNS
            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )
        ]


        # -----------------------------------------------------
        # Diagnosis certainty
        # -----------------------------------------------------

        found_certainty = [
            phrase
            for phrase in self.CERTAINTY_PATTERNS
            if phrase.lower() in text
        ]


        # -----------------------------------------------------
        # Generic medication instructions
        # -----------------------------------------------------

        found_generic_medication = [
            phrase
            for phrase in self.GENERIC_MEDICATION_ADVICE
            if phrase.lower() in text
        ]


        # -----------------------------------------------------
        # BLOCK
        # -----------------------------------------------------

        if (
            found_phrases
            or found_dosage
            or found_prescription
            or found_self_treatment
            or found_certainty
            or found_generic_medication
        ):

            return (
                "আমি সাধারণ চিকিৎসা-তথ্য দিতে পারি, তবে ব্যক্তিগত "
                "অবস্থা না জেনে নির্দিষ্ট চিকিৎসা বা ওষুধ ব্যবহারের "
                "নির্দেশনা দেওয়া নিরাপদ নয়।\n\n"

                "ওষুধের নিরাপদ ব্যবহার ও পার্শ্বপ্রতিক্রিয়া "
                "ওষুধের নাম, বয়স, শারীরিক অবস্থা এবং অন্যান্য "
                "ওষুধের ওপর নির্ভর করতে পারে।\n\n"

                "নিজে থেকে কোনো প্রেসক্রিপশন ওষুধ শুরু, বন্ধ বা "
                "ডোজ পরিবর্তন করবেন না। অ্যান্টিবায়োটিকও নিজে থেকে "
                "শুরু করবেন না।\n\n"

                "শুধু উপসর্গ দেখে নিশ্চিত রোগ নির্ণয় করা যায় না। "
                "উদ্বেগজনক বা গুরুতর উপসর্গ থাকলে যোগ্য "
                "স্বাস্থ্যসেবা পেশাদারের মূল্যায়ন নিন।\n\n"

                "যদি শ্বাসকষ্ট, বুকে তীব্র ব্যথা, অজ্ঞান হওয়া, "
                "খিঁচুনি, অতিরিক্ত রক্তপাত বা অন্য কোনো গুরুতর "
                "লক্ষণ থাকে, দ্রুত জরুরি চিকিৎসা নিন।"
            )


        return response