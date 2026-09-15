RED_FLAGS = [
    {
        "id": "chest_pain",
        "keywords": ["বুকব্যথা", "বুকে ব্যথা", "বুকে চাপ", "chest pain", "heart attack"],
        "message": "বুকব্যথা/বুকে চাপ জরুরি হতে পারে। এখনই ইমার্জেন্সি/হাসপাতালে যান।",
    },
    {
        "id": "breathing",
        "keywords": ["শ্বাসকষ্ট", "শ্বাস নিতে কষ্ট", "হাঁসফাঁস", "breathless", "can't breathe"],
        "message": "শ্বাসকষ্ট জরুরি। দেরি করবেন না—এখনই চিকিৎসা নিন।",
    },
    {
        "id": "unconscious",
        "keywords": ["অজ্ঞান", "জ্ঞান নেই", "খিঁচুনি", "seizure", "unconscious"],
        "message": "অজ্ঞান/খিঁচুনি—এখনই ইমার্জেন্সি সার্ভিস নিন।",
    },
    {
        "id": "stroke",
        "keywords": ["মুখ বেঁকে", "কথা জড়িয়ে", "এক পাশ দুর্বল", "stroke", "ফেস ড্রপ"],
        "message": "স্ট্রোকের লক্ষণ হতে পারে। এখনই হাসপাতালে যান।",
    },
    {
        "id": "bleeding",
        "keywords": ["অনেক রক্ত", "রক্তবমি", "কালো পায়খানা", "heavy bleeding"],
        "message": "তীব্র রক্তপাত জরুরি। এখনই হাসপাতালে যান।",
    },
    {
        "id": "allergy",
        "keywords": ["গলা ফুলে", "মুখ ফুলে", "অ্যালার্জি শ্বাসকষ্ট", "anaphylaxis"],
        "message": "তীব্র অ্যালার্জি জীবনঝুঁকি হতে পারে। এখনই ইমার্জেন্সি নিন।",
    },
    {
        "id": "pregnancy_emergency",
        "keywords": ["গর্ভবতী রক্তপাত", "প্রেগন্যান্সি রক্ত", "গর্ভাবে তীব্র ব্যথা"],
        "message": "গর্ভাবস্থায় রক্তপাত/তীব্র ব্যথা জরুরি। এখনই হাসপাতালে যান।",
    },
    {
        "id": "suicide",
        "keywords": ["আত্মহত্যা", "নিজেকে মেরে", "বাঁচতে ইচ্ছে নাই", "suicide"],
        "message": "আপনি একা নন। এখনই কাউকে বলুন এবং জরুরি সাহায্য নিন।",
    },
]


def find_red_flags(text: str) -> list:
    t = (text or "").lower()
    hits = []
    for item in RED_FLAGS:
        for kw in item["keywords"]:
            if kw.lower() in t:
                hits.append(item)
                break
    return hits