from __future__ import annotations

from PIL import Image, ImageOps, ImageFilter

from .config import OCRConfig


class ImagePreprocessor:
    def __init__(self, config: OCRConfig) -> None:
        self.config = config

    def prepare(self, image: Image.Image) -> Image.Image:
        result = image

        if self.config.grayscale:
            result = ImageOps.grayscale(result)

        # A small median filter is useful for noisy scanned documents while
        # being less destructive than aggressive blur.
        result = result.filter(ImageFilter.MedianFilter(size=3))

        if self.config.threshold:
            result = result.point(
                lambda pixel: 255 if pixel >= self.config.threshold_value else 0
            )

        return result
