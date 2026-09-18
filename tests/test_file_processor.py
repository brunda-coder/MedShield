"""
Tests for the file_processor module.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from file_processor import (
    read_txt,
    read_csv,
    create_download_content,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
)


def test_read_txt():
    """Test basic text reading from bytes."""
    content = b"Hello, this is a test document."
    result = read_txt(content)
    assert result == "Hello, this is a test document."


def test_read_txt_encoding():
    """Test UTF-8 encoded text with special characters."""
    content = "Héllo Wörld — special chars".encode("utf-8")
    result = read_txt(content)
    assert "Héllo" in result
    assert "Wörld" in result


def test_read_csv():
    """Test CSV parsing returns pipe-separated formatted text."""
    content = b"col1,col2\nval1,val2"
    result = read_csv(content)
    # read_csv formats with " | " separator
    assert "col1 | col2" in result
    assert "val1 | val2" in result


def test_create_download_content():
    """Test that create_download_content returns (bytes, filename) tuple."""
    text = "Redacted text content"
    original_filename = "data.txt"
    file_bytes, suggested_name = create_download_content(text, original_filename)
    # Should return bytes
    assert isinstance(file_bytes, bytes)
    assert file_bytes == b"Redacted text content"
    # Suggested filename should start with REDACTED_
    assert "REDACTED_" in suggested_name
    assert suggested_name.endswith(".txt")


def test_allowed_extensions():
    """ALLOWED_EXTENSIONS should be a list containing txt, csv, pdf."""
    assert isinstance(ALLOWED_EXTENSIONS, list)
    assert ".txt" in ALLOWED_EXTENSIONS
    assert ".csv" in ALLOWED_EXTENSIONS
    assert ".pdf" in ALLOWED_EXTENSIONS


def test_max_file_size():
    """MAX_FILE_SIZE_MB should be a reasonable positive number."""
    assert isinstance(MAX_FILE_SIZE_MB, (int, float))
    assert MAX_FILE_SIZE_MB > 0
