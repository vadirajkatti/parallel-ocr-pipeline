from __future__ import annotations

from queue import Queue
from threading import Thread
from typing import Callable

from PIL import Image

from .models import OCRResult, Tile


class OCRWorkerPool:
    """
    Explicit producer/consumer worker pool.

    This keeps the queue/threading concept from the original Res5, but avoids
    creating a new set of threads for every OCR region.
    """

    def __init__(
        self,
        thread_count: int,
        image: Image.Image,
        tiles: list[Tile],
        ocr_function: Callable[[Image.Image], str],
    ) -> None:
        self.thread_count = thread_count
        self.image = image
        self.tiles = tiles
        self.ocr_function = ocr_function

        self._jobs: Queue[Tile | None] = Queue()
        self._results: Queue[OCRResult] = Queue()
        self._errors: Queue[tuple[Tile, Exception]] = Queue()

    def run(self) -> tuple[list[OCRResult], list[tuple[Tile, Exception]]]:
        for tile in self.tiles:
            self._jobs.put(tile)

        workers = [
            Thread(target=self._worker, name=f"ocr-worker-{i + 1}")
            for i in range(self.thread_count)
        ]

        for worker in workers:
            worker.start()

        for _ in workers:
            self._jobs.put(None)

        for worker in workers:
            worker.join()

        results = []
        while not self._results.empty():
            results.append(self._results.get())

        errors = []
        while not self._errors.empty():
            errors.append(self._errors.get())

        results.sort(key=lambda result: (result.tile.row, result.tile.column))
        errors.sort(key=lambda item: item[0].index)

        return results, errors

    def _worker(self) -> None:
        while True:
            tile = self._jobs.get()
            try:
                if tile is None:
                    return

                cropped = self.image.crop(
                    (tile.left, tile.top, tile.right, tile.bottom)
                )
                text = self.ocr_function(cropped)
                self._results.put(OCRResult(tile=tile, text=text))
            except Exception as exc:
                if tile is not None:
                    self._errors.put((tile, exc))
            finally:
                self._jobs.task_done()
