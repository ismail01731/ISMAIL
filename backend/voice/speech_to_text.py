import io
import os
from typing import Optional

from groq import Groq


class SpeechToText:
    def __init__(self):
        self.name = "ISMAIL AI Speech-to-Text"
        self.model = os.getenv(
            "ISMAIL_STT_MODEL",
            "whisper-large-v3-turbo",
        )
        self.last_error = ""

    def normalize_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        return " ".join(text.strip().split())

    def process_text(self, text: str) -> str:
        return self.normalize_text(text)

    def transcribe_pcm16(
        self,
        pcm_bytes: bytes,
        sample_rate: int,
        channels: int = 1,
    ) -> Optional[str]:

        self.last_error = ""

        if not isinstance(pcm_bytes, (bytes, bytearray)):
            self.last_error = "INVALID_PCM_BYTES"
            return None

        if not pcm_bytes:
            self.last_error = "EMPTY_AUDIO"
            return None

        if sample_rate <= 0:
            self.last_error = "INVALID_SAMPLE_RATE"
            return None

        if channels != 1:
            self.last_error = "ONLY_MONO_SUPPORTED"
            return None

        if len(pcm_bytes) % 2 != 0:
            self.last_error = "INVALID_PCM16"
            return None

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            self.last_error = "GROQ_API_KEY_NOT_SET"
            return None

        try:
            client = Groq(api_key=api_key)

            data_size = len(pcm_bytes)
            byte_rate = sample_rate * channels * 2
            block_align = channels * 2

            wav_buffer = io.BytesIO()

            wav_buffer.write(b"RIFF")
            wav_buffer.write(
                (36 + data_size).to_bytes(4, "little")
            )
            wav_buffer.write(b"WAVE")

            wav_buffer.write(b"fmt ")
            wav_buffer.write((16).to_bytes(4, "little"))
            wav_buffer.write((1).to_bytes(2, "little"))
            wav_buffer.write(channels.to_bytes(2, "little"))
            wav_buffer.write(sample_rate.to_bytes(4, "little"))
            wav_buffer.write(byte_rate.to_bytes(4, "little"))
            wav_buffer.write(block_align.to_bytes(2, "little"))
            wav_buffer.write((16).to_bytes(2, "little"))

            wav_buffer.write(b"data")
            wav_buffer.write(
                data_size.to_bytes(4, "little")
            )
            wav_buffer.write(pcm_bytes)

            wav_buffer.seek(0)
            wav_buffer.name = "voice.wav"

            result = client.audio.transcriptions.create(
                file=("voice.wav", wav_buffer, "audio/wav"),
                model=self.model,
            )

            text = getattr(result, "text", "")

            return self.normalize_text(text)

        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            print("ISMAIL_STT_ERROR:", self.last_error)
            return None


speech_to_text = SpeechToText()