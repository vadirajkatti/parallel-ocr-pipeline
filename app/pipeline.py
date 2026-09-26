from __future__ import annotations

from pathlib import Path

from .config import OCRConfig
from .image_loader import ImageLoader
from .models import OCRResult
from .ocr_engine import TesseractEngine
from .preprocessor import ImagePreprocessor
from .tiler import ImageTiler
from .worker_pool import OCRWorkerPool


class OCRPipeline:
    """Coordinates image loading, tiling, preprocessing and parallel OCR."""

    def __init__(self, config: OCRConfig) -> None:
        self.config = config
        self.loader = ImageLoader()
        self.preprocessor = ImagePreprocessor(config)
        self.ocr = TesseractEngine(config)
        self.tiler = ImageTiler(
            rows=config.tile_rows,
            columns=config.tile_columns,
            overlap=config.tile_overlap,
        )

    def process(self, path: Path) -> tuple[str, list[tuple[int, Exception]]]:
        image = self.loader.load(path)
        image = self.loader.resize_for_ocr(image, self.config.max_dimension)

        tiles = self.tiler.create_tiles(image, self.config.threads)

        def ocr_tile(tile_image):
            prepared = self.preprocessor.prepare(tile_image)
            return self.ocr.extract_text(prepared)

        pool = OCRWorkerPool(
            thread_count=self.config.threads,
            image=image,
            tiles=tiles,
            ocr_function=ocr_tile,
        )

        results, errors = pool.run()

        return self._merge_results(results), [
            (tile.index, error) for tile, error in errors
        ]

    @staticmethod
    def _merge_results(results: list[OCRResult]) -> str:
        chunks = []
        for result in results:
            if result.text:
                chunks.append(result.text)

        return "\n\n".join(chunks).strip()
