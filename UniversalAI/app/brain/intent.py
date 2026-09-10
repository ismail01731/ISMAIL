def detect_intent(message: str):

    message = message.lower()

    if "মেসি" in message:
        return "sports"

    elif "ক্রিকেট" in message:
        return "sports"

    elif "খবর" in message:
        return "news"

    elif "আবহাওয়া" in message:
        return "weather"

    else:
        return "general"