# এই ফাইল দিয়ে মেডিক্যাল সিস্টেম অন/অফ করা যায়।
# False করলে পুরনো সিস্টেম আগের মতোই চলবে।

MEDICAL_ENABLED = True

# মেডিক্যাল মনে হলেও যদি নিশ্চিত না হন, পুরনো সিস্টেমে পাঠাবে
STRICT_INTENT = False

DEFAULT_COUNTRY = "Bangladesh"
DEFAULT_LANGUAGE = "bn"  # bn = সহজ বাংলা

# শিশু / গর্ভাবস্থা / মেন্টাল হেলথ — v1 এ সাবধানে
ALLOW_CHILD = True
ALLOW_PREGNANCY = True
ALLOW_MENTAL_HEALTH = True

DISCLAIMER = (
    "এটি চিকিৎসকের বিকল্প নয়। নিশ্চিত রোগ নির্ণয় বা প্রেসক্রিপশন নয়। "
    "অবস্থা খারাপ হলে দ্রুত ডাক্তার/হাসপাতালে যান।"
)