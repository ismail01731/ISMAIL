from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VisionAssessment:
    is_image: bool
    valid: bool
    image_type: str
    size_bytes: int
    response: str


class VisionAI:
    """
    Safety-focused vision layer for ISMAIL AI.

    This module validates image input and provides the foundation
    for future image understanding.
    """

    SUPPORTED_IMAGE_TYPES = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    }

    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB

    IMAGE_SIGNATURES = {
        b"\x89PNG\r\n\x1a\n": "image/png",
        b"\xff\xd8\xff": "image/jpeg",
        b"GIF87a": "image/gif",
        b"GIF89a": "image/gif",
    }

    def detect_image_type(self, image_bytes: bytes) -> str | None:
        if not isinstance(image_bytes, bytes):
            raise TypeError("image_bytes must be bytes.")

        if image_bytes.startswith(b"RIFF") and image_bytes[8:12] == b"WEBP":
            return "image/webp"

        for signature, image_type in self.IMAGE_SIGNATURES.items():
            if image_bytes.startswith(signature):
                return image_type

        return None

    def validate_image(
        self,
        image_bytes: bytes,
        content_type: str = "",
    ) -> VisionAssessment:

        if not isinstance(image_bytes, bytes):
            raise TypeError("image_bytes must be bytes.")

        image_size = len(image_bytes)

        if image_size == 0:
            return VisionAssessment(
                is_image=True,
                valid=False,
                image_type="",
                size_bytes=0,
                response="Image is empty.",
            )

        if image_size > self.MAX_IMAGE_SIZE:
            return VisionAssessment(
                is_image=True,
                valid=False,
                image_type="",
                size_bytes=image_size,
                response="Image size exceeds the 10 MB limit.",
            )

        detected_type = self.detect_image_type(image_bytes)

        if detected_type is None:
            return VisionAssessment(
                is_image=True,
                valid=False,
                image_type="",
                size_bytes=image_size,
                response="Image format could not be verified.",
            )

        declared_type = str(content_type or "").strip().lower()

        if declared_type and declared_type != detected_type:
            return VisionAssessment(
                is_image=True,
                valid=False,
                image_type=detected_type,
                size_bytes=image_size,
                response="Declared image type does not match the actual image data.",
            )

        if detected_type not in self.SUPPORTED_IMAGE_TYPES:
            return VisionAssessment(
                is_image=True,
                valid=False,
                image_type=detected_type,
                size_bytes=image_size,
                response="Unsupported image format.",
            )

        return VisionAssessment(
            is_image=True,
            valid=True,
            image_type=detected_type,
            size_bytes=image_size,
            response="Image input is valid.",
        )

    def assess(
        self,
        image_bytes: bytes,
        content_type: str = "",
    ) -> VisionAssessment:
        return self.validate_image(image_bytes, content_type)


    def build_analysis_prompt(
        self,
        question: str,
    ) -> str:
        """
        Build a safe prompt for future vision-model processing.
        """

        question = str(question or "").strip()

        if not question:
            question = "Describe this image."

        return f"""
You are the Vision AI layer of ISMAIL AI.

Analyze the provided image and answer the user's question.

User question:
{question}

STRICT RULES:

1. Describe only what can actually be observed in the image.
2. Do not invent objects, people, text, locations, or events.
3. If something is unclear, say that it is unclear.
4. Do not identify a person's identity from their face.
5. Do not infer sensitive personal information.
6. If text is visible, report only text that can be reasonably read.
7. Keep the answer concise and useful.
8. Respond in the same language as the user's question.
9. Do not claim certainty when the image does not provide enough evidence.

Return a clear answer to the user's question.
""".strip()

    def prepare_for_analysis(
        self,
        image_bytes: bytes,
        content_type: str = "",
        question: str = "",
    ) -> str:
        """
        Validate an image and prepare the safe analysis prompt.
        """

        assessment = self.assess(image_bytes, content_type)

        if not assessment.valid:
            raise ValueError(assessment.response)

        return self.build_analysis_prompt(question)