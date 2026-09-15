from medical_system.router import maybe_handle_medical

tests = [
    "আজকের আবহাওয়া কেমন?",
    "২ দিন ধরে জ্বর আর গলা ব্যথা",
    "বুকে ব্যথা আর শ্বাসকষ্ট হচ্ছে",
]

for t in tests:
    r = maybe_handle_medical(t)
    print("USER:", t)
    print("RESULT:", r)
    print("-" * 40)
