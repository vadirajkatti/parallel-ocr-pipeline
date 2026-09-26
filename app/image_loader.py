from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}


class ImageLoader:
    """Loads and normalizes scanned images."""

    def load(self, path: Path) -> Image.Image:
        if not path.exists():
            raise FileNotFoundError(path)

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported image type: {path.suffix}. "
                f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )

        image = Image.open(path)
        image = ImageOps.exif_transpose(image)
        return image.convert("RGB")

    def resize_for_ocr(self, image: Image.Image, max_dimension: int) -> Image.Image:
        if not max_dimension:
            return image

        width, height = image.size
        longest = max(width, height)

        if longest <= max_dimension:
            return image

        scale = max_dimension / longest
        new_size = (max(1, round(width * scale)), max(1, round(height * scale)))
        return image.resize(new_size, Image.Resampling.LANCZOS)
