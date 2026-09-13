from __future__ import annotations

import base64
import json
from urllib import request


class VisionProviderError(RuntimeError):
    """Raised when the vision provider cannot process an image."""


class OllamaVisionProvider:
    """
    Ollama-based Vision AI provider for ISMAIL AI.

    The selected Ollama model must support image input.
    """

    def __init__(
        self,
        model: str,
        ollama_url: str = "http://127.0.0.1:11434",
    ) -> None:
        self.model = str(model).strip()
        self.ollama_url = str(ollama_url).rstrip("/")

        if not self.model:
            raise ValueError("Vision model cannot be empty.")

    def analyze(
        self,
        image_bytes: bytes,
        prompt: str,
    ) -> str:
        if not isinstance(image_bytes, bytes):
            raise TypeError("image_bytes must be bytes.")

        if not image_bytes:
            raise ValueError("Image cannot be empty.")

        prompt = str(prompt or "").strip()

        if not prompt:
            prompt = "Describe this image."

        encoded_image = base64.b64encode(image_bytes).decode("ascii")

        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [encoded_image],
            "stream": False,
        }

        body = json.dumps(payload).encode("utf-8")

        req = request.Request(
            f"{self.ollama_url}/api/generate",
            data=body,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=300) as response:
                raw = response.read().decode("utf-8")

        except Exception as exc:
            error_body = ""

            if hasattr(exc, "read"):
                try:
                    error_body = exc.read().decode("utf-8", errors="replace")
                except Exception:
                    error_body = ""

            if error_body:
                raise VisionProviderError(
                    f"Vision provider request failed: {exc}; "
                    f"Ollama response: {error_body}"
                ) from exc

            raise VisionProviderError(
                f"Vision provider request failed: {exc}"
            ) from exc

        try:
            result = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise VisionProviderError(
                "Vision provider returned invalid JSON."
            ) from exc

        answer = result.get("response")

        if not isinstance(answer, str) or not answer.strip():
            raise VisionProviderError(
                "Vision provider returned an empty response."
            )

        return answer.strip()