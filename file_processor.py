"""
File processing module for MedShield.
Handles reading and parsing of different file formats (.txt, .csv, .pdf).
"""

import csv
import io
import os
from typing import Tuple

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


# Constants
ALLOWED_EXTENSIONS = ['.txt', '.csv', '.pdf']
MAX_FILE_SIZE_MB = 10


def validate_file(uploaded_file) -> Tuple[bool, str]:
    """
    Validates the uploaded file's type and size.
    
    Args:
        uploaded_file: The file object uploaded via Streamlit.
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if uploaded_file is None:
        return False, "No file uploaded."

    # Check extension
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file type '{ext}'. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}."

    # Check file size
    # Assuming uploaded_file has a size attribute (Streamlit UploadedFile)
    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File size exceeds {MAX_FILE_SIZE_MB}MB limit. (Actual size: {size_mb:.2f}MB)"

    return True, ""


def read_txt(file_bytes: bytes) -> str:
    """
    Decodes and returns text content from a text file.
    
    Args:
        file_bytes (bytes): The raw bytes of the file.
        
    Returns:
        str: The decoded text content.
    """
    try:
        return file_bytes.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return file_bytes.decode('latin-1')
        except Exception as e:
            raise ValueError(f"Could not decode text file: {str(e)}")


def read_csv(file_bytes: bytes) -> str:
    """
    Parses a CSV file and returns its content as formatted text.
    
    Args:
        file_bytes (bytes): The raw bytes of the CSV file.
        
    Returns:
        str: The formatted text content.
    """
    try:
        # Decode bytes to string
        text_content = read_txt(file_bytes)
        
        # Parse CSV
        csv_reader = csv.reader(io.StringIO(text_content))
        formatted_rows = []
        for row in csv_reader:
            formatted_rows.append(" | ".join(row))
            
        return "\n".join(formatted_rows)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {str(e)}")


def read_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from all pages of a PDF file.
    
    Args:
        file_bytes (bytes): The raw bytes of the PDF file.
        
    Returns:
        str: The extracted text content with page markers.
    """
    if fitz is None:
        raise ImportError("PyMuPDF (fitz) is not installed. Cannot read PDF files.")
        
    try:
        # Open PDF from memory
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        
        text_content = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            
            text_content.append(f"--- Page {page_num + 1} ---")
            text_content.append(page_text)
            
        pdf_document.close()
        
        return "\n".join(text_content)
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {str(e)}")


def process_file(uploaded_file) -> Tuple[bool, str, str]:
    """
    Main entry point for processing an uploaded file.
    Routes to the appropriate reader based on extension.
    
    Args:
        uploaded_file: The file object uploaded via Streamlit.
        
    Returns:
        tuple[bool, str, str]: (success, content_or_error, file_type)
    """
    is_valid, error_msg = validate_file(uploaded_file)
    if not is_valid:
        return False, error_msg, ""
        
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()
    
    try:
        file_bytes = uploaded_file.getvalue()
        
        if ext == '.txt':
            content = read_txt(file_bytes)
        elif ext == '.csv':
            content = read_csv(file_bytes)
        elif ext == '.pdf':
            content = read_pdf(file_bytes)
        else:
            return False, f"Unsupported extension: {ext}", ""
            
        return True, content, ext
    except Exception as e:
        return False, f"Error processing file: {str(e)}", ext


def create_download_content(redacted_text: str, original_filename: str) -> Tuple[bytes, str]:
    """
    Creates downloadable content for the redacted text.
    
    Args:
        redacted_text (str): The text after redaction.
        original_filename (str): The original filename.
        
    Returns:
        tuple[bytes, str]: (file_bytes, suggested_filename)
    """
    # Create bytes
    file_bytes = redacted_text.encode('utf-8')
    
    # Create suggested filename
    name, ext = os.path.splitext(original_filename)
    suggested_filename = f"REDACTED_{name}.txt"
    
    return file_bytes, suggested_filename
