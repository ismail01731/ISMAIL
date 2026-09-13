class VoiceAI:
    """
    Core Voice AI module for ISMAIL AI.
    Keeps voice processing isolated from the main AI system.
    """
    def __init__(self):
        self.name = "ISMAIL AI Voice AI"
    def normalize_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        return " ".join(text.strip().split())
    def prepare_for_ai(self, text: str) -> str:
        return self.normalize_text(text)
voice_ai = VoiceAI()
