from __future__ import annotations

from dataclasses import dataclass
from math import ceil

from PIL import Image

from .models import Tile


class ImageTiler:
    """Divides an image into overlapping regions for parallel OCR."""

    def __init__(self, rows: int, columns: int, overlap: float) -> None:
        self.rows = rows
        self.columns = columns
        self.overlap = overlap

    def create_tiles(self, image: Image.Image, worker_count: int) -> list[Tile]:
        width, height = image.size

        # For an arbitrary image, automatically create roughly one tile per
        # worker when rows were not explicitly configured.
        rows = self.rows or max(1, worker_count)
        columns = max(1, self.columns)

        # Avoid creating absurdly tiny OCR regions.
        rows = min(rows, max(1, height // 400))
        columns = min(columns, max(1, width // 800))

        tile_height = ceil(height / rows)
        tile_width = ceil(width / columns)

        overlap_y = round(tile_height * self.overlap)
        overlap_x = round(tile_width * self.overlap)

        tiles: list[Tile] = []
        index = 0

        for row in range(rows):
            top = max(0, row * tile_height - (overlap_y if row else 0))
            bottom = min(
                height,
                (row + 1) * tile_height + (overlap_y if row < rows - 1 else 0),
            )

            for column in range(columns):
                left = max(0, column * tile_width - (overlap_x if column else 0))
                right = min(
                    width,
                    (column + 1) * tile_width + (overlap_x if column < columns - 1 else 0),
                )

                tiles.append(
                    Tile(
                        index=index,
                        row=row,
                        column=column,
                        left=left,
                        top=top,
                        right=right,
                        bottom=bottom,
                    )
                )
                index += 1

        return tiles
