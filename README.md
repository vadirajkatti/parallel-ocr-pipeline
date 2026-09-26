# Modern Parallel OCR Pipeline

This is a clean-room modernization of the core architecture in the original
Res5: convert/prepare a scanned document image, divide the work into OCR
regions, process regions concurrently, collect the results, and print the
extracted text.

The original script was tied to one specific PDF layout and hard-coded crop
coordinates. This version deliberately removes those assumptions.

## What changed

### Original concept retained

- Python OCR with Tesseract
- image preprocessing
- multiple OCR operations running concurrently
- queues feeding worker threads
- configurable processing parameters

### Modernized

- classes instead of a large procedural script
- one responsibility per module
- `queue.Queue` + reusable worker pool
- no global queues
- no hard-coded document coordinates
- no temporary crop files
- no document-specific field names
- environment-variable configuration
- arbitrary scanned image input
- deterministic tile ordering
- explicit error collection
- CLI entry point

## Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

You also need the **Tesseract OCR executable** installed separately.

On Windows, install Tesseract and either put it on `PATH`, or configure
`pytesseract.pytesseract.tesseract_cmd` in `app/ocr_engine.py`.

## Run

```bash
python main.py "C:\path\to\scan.jpg"
```

Show the active configuration:

```bash
python main.py "C:\path\to\scan.jpg" --show-config
```

## Environment configuration

Copy `.env.example` values into your shell environment.

### Windows CMD

```cmd
set OCR_THREADS=6
set OCR_MAX_DIMENSION=3500
set OCR_PSM=6
set OCR_GRAYSCALE=true
set OCR_THRESHOLD=false

python main.py "C:\scans\document.jpg"
```

### PowerShell

```powershell
$env:OCR_THREADS="6"
$env:OCR_MAX_DIMENSION="3500"
$env:OCR_PSM="6"

python main.py "C:\scans\document.jpg"
```

## Resolution

The original Res5 contained several coordinate sets that implicitly depended
on the source image resolution (for example 150/200/400 DPI assumptions).

For a generic image pipeline, coordinates should not be hard-coded.

`OCR_MAX_DIMENSION` therefore controls the maximum pixel dimension used by
the OCR pipeline:

- `0` — preserve the original resolution
- `2500` — resize large scans down to roughly 2500 pixels on their longest side
- `3500` — higher-resolution OCR, usually slower
- `5000` — useful for very small text, but memory/CPU usage increases

If the source is a PDF, render it to an image at a chosen DPI first. This
project intentionally operates on images, as requested.

## Threads

`OCR_THREADS` controls the number of worker threads.

Example:

```cmd
set OCR_THREADS=8
```

The pipeline creates one reusable worker pool rather than creating and
destroying multiple threads for every OCR region.

The OCR operation itself invokes Tesseract, which runs outside the Python
interpreter, so this workload is a reasonable use case for threads.

## Why automatic tiling?

Your original Res5 had calls resembling:

```text
image → crop fixed coordinates → OCR
```

That worked because you knew the exact PDF layout.

This version changes that to:

```text
image
  ↓
resize if configured
  ↓
automatic overlapping tiles
  ↓
worker queue
  ↓
N OCR workers
  ↓
ordered results
  ↓
printed text
```

The overlap reduces the chance of cutting a line exactly at a tile boundary.

For documents with complex multi-column layouts, a future version could add
layout detection or Tesseract bounding-box based reading-order reconstruction.

## Important limitation

This is still traditional OCR. It does not use an LLM or document-AI model.

Accuracy depends heavily on:

- scan quality
- skew
- handwriting
- font
- contrast
- language
- Tesseract configuration
- image resolution

The purpose here is to modernize the engineering architecture of your old
solution, not pretend that generic OCR can perfectly understand every
document.
