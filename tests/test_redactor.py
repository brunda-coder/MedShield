import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from redactor import redact_text, get_supported_patterns

def test_phone_redaction():
    text = "Call me at +91-98765-43210 or 9876543210 or 987-654-3210."
    result = redact_text(text)
    assert result.redaction_count > 0
    assert '[PHONE REDACTED]' in result.redacted_text

def test_email_redaction():
    text = "Email me at test@example.com."
    result = redact_text(text)
    assert result.redaction_count == 1
    assert '[EMAIL REDACTED]' in result.redacted_text

def test_aadhaar_redaction():
    text = "My Aadhaar is 1234 5678 9012 and 1234-5678-9012."
    result = redact_text(text)
    assert result.redaction_count > 0

def test_ssn_redaction():
    text = "My SSN is 123-45-6789."
    result = redact_text(text)
    assert result.redaction_count == 1

def test_dob_redaction():
    text = "DOB: 15/03/1990 and Date of Birth: March 15, 1990."
    result = redact_text(text)
    assert result.redaction_count > 0

def test_date_redaction():
    text = "The event is on 12-05-2023 or 2023/05/12."
    result = redact_text(text)
    assert result.redaction_count > 0

def test_mrn_redaction():
    text = "Patient MR-2024-00456 and MRN: 123456."
    result = redact_text(text)
    assert result.redaction_count > 0

def test_name_redaction():
    text = "Patient Name: John Doe and Dr. Smith and Mr. Kumar."
    result = redact_text(text)
    assert result.redaction_count > 0
    assert '[NAME REDACTED]' in result.redacted_text

def test_address_redaction():
    text = "Address: 42 MG Road, Bangalore."
    result = redact_text(text)
    assert result.redaction_count > 0

def test_insurance_redaction():
    text = "Insurance ID: INS-KA-12345."
    result = redact_text(text)
    assert result.redaction_count > 0

def test_medical_content_preserved():
    """Verify medical terms are NOT redacted as PII."""
    text = "Patient has Hemoglobin A1c of 6.5%. Diagnosed with Diabetes and taking Metformin."
    result = redact_text(text)
    assert "Hemoglobin" in result.redacted_text
    assert "Diabetes" in result.redacted_text
    assert "Metformin" in result.redacted_text

def test_redaction_count():
    text = "test@example.com 123-45-6789"
    result = redact_text(text)
    assert result.redaction_count == 2
    assert isinstance(result.redaction_details, dict)

def test_empty_text():
    text = ""
    result = redact_text(text)
    assert result.redacted_text == ""
    assert result.redaction_count == 0

def test_no_pii():
    text = "Just a normal sentence without any PII."
    result = redact_text(text)
    assert result.redacted_text == text
    assert result.redaction_count == 0

def test_get_supported_patterns():
    patterns = get_supported_patterns()
    assert isinstance(patterns, list)
    assert len(patterns) > 0
