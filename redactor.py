import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class RedactionResult:
    """
    Stores the result of a text redaction operation.
    """
    redacted_text: str
    redaction_count: int
    redaction_details: Dict[str, int] = field(default_factory=dict)

# A comprehensive list of compiled regex patterns for PII detection.
# Each tuple contains: (pattern_name, compiled_regex, replacement_label)
# Specific contextual patterns are ordered before more generic ones.
PATTERNS: List[Tuple[str, re.Pattern, str]] = [
    (
        'DOB',
        re.compile(r'(?i)(\b(?:DOB|Date\s*of\s*Birth|D\.O\.B)[\s:=]+)([a-zA-Z0-9/\-.,\s]{6,20})\b'),
        r'\g<1>[DOB REDACTED]'
    ),
    (
        'NAME',
        re.compile(r'(?i:Patient\s*Name|Name|Referred\s*by)\s*[:=]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b'),
        r'[NAME REDACTED]'
    ),
    (
        'NAME',
        re.compile(r'\b(?:Dr\.|Mr\.|Mrs\.|Ms\.)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b'),
        r'[NAME REDACTED]'
    ),
    (
        'ADDRESS',
        re.compile(r'(?i)(\b(?:Address|Residence|Addr)[\s:=]+)(.*?)(?=\n|$)'),
        r'\g<1>[ADDRESS REDACTED]'
    ),
    (
        'PINCODE',
        re.compile(r'(?i)(\b(?:PIN|Pincode)[\s:=]*)(\d{6})\b'),
        r'\g<1>[PINCODE REDACTED]'
    ),
    (
        'PINCODE',
        re.compile(r'(?m)\b\d{6}\b(?=\s*$)'),
        r'[PINCODE REDACTED]'
    ),
    (
        'MRN',
        re.compile(r'(?i)\b(?:MR-\d{4}-\d{5}|MRN-\d{6}|MRN:\s*\d{6}|Medical\s*Record\s*No[\s:=]*\w+)\b'),
        r'[MRN REDACTED]'
    ),
    (
        'INSURANCE_ID',
        re.compile(r'(?i)(\b(?:Insurance\s*ID|Policy\s*No|Insurance\s*No)[\s:=]+)([a-zA-Z0-9\-]+)\b'),
        r'\g<1>[INSURANCE_ID REDACTED]'
    ),
    (
        'PHONE',
        re.compile(r'\b(?:\+?91[\-\s]?)?[6-9]\d{9}\b|\b(?:\+?1[\-\s]?)?\(?\d{3}\)?[\-\s]?\d{3}[\-\s]?\d{4}\b'),
        r'[PHONE REDACTED]'
    ),
    (
        'EMAIL',
        re.compile(r'(?i)\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}\b'),
        r'[EMAIL REDACTED]'
    ),
    (
        'AADHAAR',
        re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'),
        r'[AADHAAR REDACTED]'
    ),
    (
        'SSN',
        re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        r'[SSN REDACTED]'
    ),
    (
        'DATE',
        re.compile(r'(?i)\b(?:\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}|\d{4}[/\-]\d{1,2}[/\-]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b'),
        r'[DATE REDACTED]'
    )
]

def redact_text(text: str) -> RedactionResult:
    """
    Applies PII redaction patterns to the provided text.
    Patterns are applied in the priority order defined in PATTERNS list.
    
    Args:
        text (str): The original text that may contain PII.
        
    Returns:
        RedactionResult: An object containing the redacted text, total count of redactions,
                         and a dictionary detailing redaction counts by category.
    """
    redacted = text
    total_count = 0
    details: Dict[str, int] = {}
    
    for category_name, regex, replacement in PATTERNS:
        # regex.subn returns a tuple: (new_string, number_of_subs_made)
        redacted, count = regex.subn(replacement, redacted)
        if count > 0:
            total_count += count
            details[category_name] = details.get(category_name, 0) + count
            
    return RedactionResult(
        redacted_text=redacted,
        redaction_count=total_count,
        redaction_details=details
    )

def get_supported_patterns() -> list[str]:
    """
    Returns a list of human-readable names of all supported redaction patterns.
    
    Returns:
        list[str]: A list of unique pattern category names.
    """
    # Use a dictionary to maintain insertion order while removing duplicates
    categories = {}
    for name, _, _ in PATTERNS:
        categories[name] = True
    return list(categories.keys())
