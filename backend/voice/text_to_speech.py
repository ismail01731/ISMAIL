class TextToSpeech:
    """
    Text-to-Speech module for ISMAIL AI.
    Browser-side speech synthesis will handle actual audio playback.
    This backend module keeps TTS logic isolated for future expansion.
    """
    def __init__(self):
        self.name = "ISMAIL AI Text-to-Speech"
    def normalize_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        return " ".join(text.strip().split())
    def prepare(self, text: str) -> str:
        return self.normalize_text(text)
text_to_speech = TextToSpeech()
