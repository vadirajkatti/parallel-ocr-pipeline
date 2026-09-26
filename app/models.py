from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Tile:
    index: int
    row: int
    column: int
    left: int
    top: int
    right: int
    bottom: int


@dataclass(frozen=True)
class OCRResult:
    tile: Tile
    text: str
