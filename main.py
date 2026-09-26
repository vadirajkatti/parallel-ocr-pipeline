from __future__ import annotations

import argparse
import sys
from pathlib import Path

from app.config import OCRConfig
from app.pipeline import OCRPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract text from arbitrary scanned images using parallel OCR."
    )
    parser.add_argument("image", type=Path, help="Path to scanned image")
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Print effective OCR configuration before processing",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = OCRConfig.from_env()

    if args.show_config:
        print(config)
        print()

    try:
        pipeline = OCRPipeline(config)
        text, errors = pipeline.process(args.image)

        print("=" * 80)
        print(f"OCR RESULT: {args.image}")
        print("=" * 80)
        print(text or "[No text detected]")

        if errors:
            print("\n" + "=" * 80)
            print("TILE ERRORS")
            print("=" * 80)
            for tile_index, error in errors:
                print(f"Tile {tile_index}: {error}")

        return 0 if not errors else 2

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
