import io
import os
import wave
import tempfile
from typing import Optional

import numpy as np
from faster_whisper import WhisperModel


class SpeechToText:
    def __init__(self):
        self.name = "ISMAIL AI Speech-to-Text"
        self.model_name = "medium"
        self.last_error = ""

        try:
            self.model = WhisperModel(
                self.model_name,
                device="cpu",
                compute_type="int8",
            )
        except Exception as exc:
            self.model = None
            self.last_error = f"{type(exc).__name__}: {exc}"
            print("ISMAIL_STT_INIT_ERROR:", self.last_error)

    def normalize_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""

        return " ".join(text.strip().split())

    def process_text(self, text: str) -> str:
        return self.normalize_text(text)

    def clean_audio(
        self,
        pcm_bytes: bytes,
        sample_rate: int,
    ) -> bytes:

        audio = np.frombuffer(
            pcm_bytes,
            dtype=np.int16,
        ).astype(np.float32)

        if len(audio) == 0:
            return pcm_bytes

        # Remove DC offset
        audio = audio - np.mean(audio)

        # Find actual voice/audio level
        peak = float(np.max(np.abs(audio)))

        if peak <= 1:
            return pcm_bytes

        # Normalize microphone volume
        target_peak = 16000.0
        gain = target_peak / peak

        # Prevent excessive amplification
        gain = min(gain, 12.0)

        audio *= gain

        # Soft clipping protection
        audio = np.clip(
            audio,
            -32768,
            32767,
        )

        # Remove very quiet ending/beginning
        threshold = max(
            250.0,
            float(np.max(np.abs(audio))) * 0.015,
        )

        active = np.where(
            np.abs(audio) >= threshold
        )[0]

        if len(active) > 0:

            padding = int(sample_rate * 0.20)

            start = max(
                0,
                int(active[0]) - padding,
            )

            end = min(
                len(audio),
                int(active[-1]) + padding,
            )

            audio = audio[start:end]

        return audio.astype(np.int16).tobytes()

    def transcribe_pcm16(
        self,
        pcm_bytes: bytes,
        sample_rate: int,
        channels: int = 1,
    ) -> Optional[str]:

        self.last_error = ""

        if not isinstance(
            pcm_bytes,
            (bytes, bytearray),
        ):
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

        if self.model is None:
            self.last_error = "WHISPER_MODEL_NOT_READY"
            return None

        try:

            # Clean and normalize microphone audio
            pcm_bytes = self.clean_audio(
                pcm_bytes,
                sample_rate,
            )

            wav_buffer = io.BytesIO()

            with wave.open(
                wav_buffer,
                "wb",
            ) as wav_file:

                wav_file.setnchannels(channels)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(pcm_bytes)

            wav_buffer.seek(0)

            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False,
            ) as temp_file:

                temp_file.write(
                    wav_buffer.getvalue()
                )

                wav_path = temp_file.name

            try:

                segments, info = self.model.transcribe(
                    wav_path,
                    language="bn",
                    task="transcribe",
                    beam_size=5,
                    best_of=5,
                    temperature=0.0,
                    vad_filter=True,
                    vad_parameters={
                        "min_silence_duration_ms": 300,
                    },
                    condition_on_previous_text=False,
                )

                parts = []

                for segment in segments:

                    text = self.normalize_text(
                        segment.text
                    )

                    if text:
                        parts.append(text)

                final_text = self.normalize_text(
                    " ".join(parts)
                )

                if not final_text:
                    self.last_error = (
                        "EMPTY_TRANSCRIPTION"
                    )
                    return None

                return final_text

            finally:

                try:
                    os.remove(wav_path)
                except Exception:
                    pass

        except Exception as exc:

            self.last_error = (
                f"{type(exc).__name__}: {exc}"
            )

            print(
                "ISMAIL_STT_ERROR:",
                self.last_error,
            )

            return None


speech_to_text = SpeechToText()