from __future__ import annotations

import pytesseract
from PIL import Image

from .config import OCRConfig


class TesseractEngine:
    """Small adapter around Tesseract so OCR is isolated from the pipeline."""

    def __init__(self, config: OCRConfig) -> None:
        self.config = config

    def extract_text(self, image: Image.Image) -> str:
        text = pytesseract.image_to_string(
            image,
            lang=self.config.language,
            config=f"--psm {self.config.psm}",
        )
        return self._clean(text)

    @staticmethod
    def _clean(text: str) -> str:
        lines = [line.rstrip() for line in text.splitlines()]
        return "\n".join(lines).strip()
