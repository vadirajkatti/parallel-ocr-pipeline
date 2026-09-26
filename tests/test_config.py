import os

from app.config import OCRConfig


def test_config_reads_thread_count(monkeypatch):
    monkeypatch.setenv("OCR_THREADS", "7")
    config = OCRConfig.from_env()
    assert config.threads == 7
