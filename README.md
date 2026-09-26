# Parallel OCR Pipeline

A modular Python OCR pipeline for processing scanned images using configurable image preprocessing, parallel OCR workers, image tiling, and result aggregation.

## Overview

This project is a modernized implementation of an OCR automation solution originally developed several years ago.

The original implementation was a large procedural Python application that used image processing, Tesseract OCR, Python threading, and queues to extract information from scanned documents. The core idea was to divide OCR work into independent regions and process those regions concurrently.

This version preserves that core engineering approach while restructuring the application into a modular, maintainable, and testable Python project.

### Original approach

The original OCR workflow followed the general pattern:

```text
Scanned Document
       │
       ▼
  Image Conversion
       │
       ▼
  Region Extraction
       │
       ├──────────────┐
       ▼              ▼
   OCR Region 1   OCR Region 2  ...
       │              │
       └───────┬──────┘
               ▼
        Combine Results
```

The original implementation used fixed image regions and multiple threads/queues to perform OCR operations concurrently.

### Modernized approach

The current implementation generalizes the concept so that it can process arbitrary scanned images:

```text
                    ┌─────────────────┐
                    │   Input Image   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Image Loader   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Preprocessor   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Image Tiler     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         ┌─────────┐    ┌─────────┐    ┌─────────┐
         │ Worker 1│    │ Worker 2│    │ Worker N│
         │   OCR   │    │   OCR   │    │   OCR   │
         └────┬────┘    └────┬────┘    └────┬────┘
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                    ┌─────────────────┐
                    │ Result Aggregator│
                    └────────┬────────┘
                             │
                             ▼
                       OCR Text Output
```

## Key Features

* **Parallel OCR processing** using a configurable worker pool
* **Producer/consumer architecture** using `queue.Queue`
* Automatic image tiling instead of hard-coded OCR regions
* Configurable number of OCR workers
* Configurable image resolution
* Optional grayscale conversion
* Optional thresholding
* Configurable Tesseract language and page segmentation mode
* EXIF-aware image loading
* Structured OCR results using Python dataclasses
* Error collection from individual OCR workers
* Unit tests for core components
* Command-line interface
* Separation of configuration, preprocessing, OCR, orchestration, and worker management

## Project Structure

```text
parallel-ocr-pipeline/
│
├── main.py
├── requirements.txt
├── .env.example
├── README.md
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── image_loader.py
│   ├── models.py
│   ├── ocr_engine.py
│   ├── pipeline.py
│   ├── preprocessor.py
│   ├── tiler.py
│   └── worker_pool.py
│
└── tests/
    ├── test_config.py
    └── test_tiler.py
```

### Component responsibilities

| Component         | Responsibility                                                 |
| ----------------- | -------------------------------------------------------------- |
| `config.py`       | Runtime configuration and environment variables                |
| `image_loader.py` | Image loading, validation, orientation correction and resizing |
| `preprocessor.py` | Grayscale conversion and optional thresholding                 |
| `tiler.py`        | Divides an image into OCR-friendly regions                     |
| `ocr_engine.py`   | Tesseract OCR wrapper                                          |
| `worker_pool.py`  | Manages concurrent OCR workers                                 |
| `pipeline.py`     | Coordinates the complete OCR workflow                          |
| `models.py`       | Typed data structures for tiles and OCR results                |
| `main.py`         | Command-line entry point                                       |
| `tests/`          | Unit tests for core functionality                              |

## Technologies

* Python
* Tesseract OCR
* pytesseract
* Pillow
* `threading`
* `queue.Queue`
* Python dataclasses
* pytest

## Requirements

* Python 3.10+
* Tesseract OCR
* Windows, Linux, or macOS

`pytesseract` is a Python wrapper around the Tesseract executable. Tesseract itself must therefore be installed separately.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/vadirajkatti/parallel-ocr-pipeline.git
cd parallel-ocr-pipeline
```

### 2. Create a virtual environment

#### Windows

```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Tesseract

Install Tesseract OCR for your operating system and make sure the `tesseract` executable is available on the system PATH.

Verify the installation:

```bash
tesseract --version
```

## Usage

Run the pipeline against a scanned image:

```bash
python main.py "path/to/image.jpg"
```

Example:

```bash
python main.py "C:\Documents\invoice.jpg"
```

The pipeline loads the image, preprocesses it, divides it into regions, processes those regions concurrently, and combines the OCR output.

## Configuration

The pipeline can be configured through environment variables.

| Variable              | Description                                                 | Default |
| --------------------- | ----------------------------------------------------------- | ------: |
| `OCR_THREADS`         | Number of OCR worker threads                                |     `4` |
| `OCR_LANGUAGE`        | Tesseract language                                          |   `eng` |
| `OCR_PSM`             | Tesseract page segmentation mode                            |     `6` |
| `OCR_MAX_DIMENSION`   | Maximum image dimension; `0` disables resizing              |     `0` |
| `OCR_TILE_OVERLAP`    | Overlap between adjacent tiles                              |  `0.08` |
| `OCR_TILE_ROWS`       | Number of image rows; automatic when configured accordingly |     `0` |
| `OCR_TILE_COLUMNS`    | Number of image columns                                     |     `1` |
| `OCR_GRAYSCALE`       | Convert image to grayscale                                  |  `true` |
| `OCR_THRESHOLD`       | Apply binary thresholding                                   | `false` |
| `OCR_THRESHOLD_VALUE` | Threshold value                                             |   `180` |

### Windows example

```cmd
set OCR_THREADS=8
set OCR_MAX_DIMENSION=3500
set OCR_PSM=6
set OCR_GRAYSCALE=true
set OCR_THRESHOLD=false

python main.py "C:\Documents\scan.jpg"
```

### Linux / macOS example

```bash
export OCR_THREADS=8
export OCR_MAX_DIMENSION=3500
export OCR_PSM=6

python main.py "/documents/scan.jpg"
```

## Why Use Multiple OCR Workers?

OCR is performed independently for each image region. This makes the workload suitable for a worker-pool design.

Instead of repeatedly creating and joining individual threads, the modern implementation creates a fixed pool of workers:

```text
                 Job Queue
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    Worker 1     Worker 2     Worker N
        │            │            │
       OCR          OCR          OCR
        │            │            │
        └────────────┼────────────┘
                     ▼
               Result Queue
```

The number of workers can be adjusted without changing the application code.

More workers do not automatically mean better performance. OCR performance depends on factors such as CPU resources, image size, Tesseract configuration, and the underlying workload.

## Design Decisions

### Modular architecture

The original implementation contained a large amount of OCR and document-processing logic in a single procedural application.

The modernized version separates responsibilities so individual components can be tested and changed independently.

### Worker pool

The original implementation used Python threads and queues for concurrent OCR operations.

The modern implementation retains that concept but uses a reusable worker pool rather than repeatedly creating threads for individual OCR operations.

### Image tiling

The original implementation relied heavily on fixed crop coordinates for known document layouts.

That approach works when document layouts are predictable but does not generalize well.

The modern implementation divides arbitrary input images into configurable regions so the same pipeline can be used with different scanned images.

### Configuration

Concurrency, image sizing, OCR settings, and preprocessing behavior are configurable at runtime rather than embedded directly in the source code.

## Testing

Run the unit tests with:

```bash
pytest
```

The tests currently cover core configuration and image-tiling behavior.

## Historical Context

This project is also an exercise in software modernization.

The original OCR automation was developed several years before today's widespread AI-assisted software development workflows. It used techniques such as:

* Python image processing
* Tesseract OCR
* OpenCV/PIL-based preprocessing
* fixed-region extraction
* Python threading
* queues
* document conversion
* data extraction and validation

The goal of this repository is not to reproduce the original code line-for-line.

Instead, it demonstrates how the underlying engineering problem can be revisited and implemented using a cleaner architecture while preserving the important concepts from the original solution.

## Evolution

```text
Original OCR Automation
        │
        ├── Large procedural application
        ├── Fixed document regions
        ├── Multiple OCR functions
        ├── Explicit thread creation
        └── Global queues/state
                    │
                    ▼
             Modernized Design
                    │
        ├── Modular architecture
        ├── Configurable tiling
        ├── Reusable worker pool
        ├── Structured results
        ├── Environment configuration
        └── Unit tests
```

## Limitations

This is intentionally a lightweight OCR pipeline rather than a complete document-understanding system.

It does not currently attempt to:

* identify arbitrary document layouts using machine learning
* understand document semantics
* extract named business fields
* classify documents
* perform table understanding
* remove duplicate OCR text produced by overlapping tiles
* provide a web interface

These are possible extensions for future versions.

## Possible Future Improvements

Potential improvements include:

* Automatic text-block detection before tiling
* Layout-aware OCR
* Better handling of multi-column documents
* Duplicate-text removal across overlapping tiles
* PDF input support
* Batch directory processing
* Structured JSON output
* OCR confidence scoring
* Async job orchestration
* Performance benchmarking
* Docker support
* CI/CD with automated tests

## License

This project is provided for educational and portfolio purposes.
