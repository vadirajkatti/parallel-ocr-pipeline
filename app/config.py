from __future__ import annotations

import os
from dataclasses import dataclass


def _int_env(name: str, default: int, minimum: int = 1) -> int:
    value = int(os.getenv(name, default))
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return value


def _float_env(name: str, default: float, minimum: float = 0.1) -> float:
    value = float(os.getenv(name, default))
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return value


@dataclass(frozen=True)
class OCRConfig:
    # Number of OCR worker threads. Override with OCR_THREADS.
    threads: int = 4

    # Tesseract language/configuration.
    language: str = "eng"
    psm: int = 6

    # Resize the longest image dimension before OCR.
    # 0 means "do not resize". This replaces the old fixed-resolution
    # assumptions that were tied to one particular scanned PDF.
    max_dimension: int = 0

    # Fraction of tile height used as overlap between adjacent tiles.
    tile_overlap: float = 0.08

    # Number of rows/columns used to divide a page into OCR tiles.
    tile_rows: int = 0
    tile_columns: int = 1

    # Basic preprocessing.
    grayscale: bool = True
    threshold: bool = False
    threshold_value: int = 180

    @classmethod
    def from_env(cls) -> "OCRConfig":
        return cls(
            threads=_int_env("OCR_THREADS", 4),
            language=os.getenv("OCR_LANGUAGE", "eng"),
            psm=_int_env("OCR_PSM", 6),
            max_dimension=_int_env("OCR_MAX_DIMENSION", 0),
            tile_overlap=_float_env("OCR_TILE_OVERLAP", 0.08, 0.0),
            tile_rows=_int_env("OCR_TILE_ROWS", 0),
            tile_columns=_int_env("OCR_TILE_COLUMNS", 1),
            grayscale=os.getenv("OCR_GRAYSCALE", "true").lower() in {"1", "true", "yes"},
            threshold=os.getenv("OCR_THRESHOLD", "false").lower() in {"1", "true", "yes"},
            threshold_value=_int_env("OCR_THRESHOLD_VALUE", 180, 0),
        )
