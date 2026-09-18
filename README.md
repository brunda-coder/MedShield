# <div align="center">🛡️ MedShield</div>

<div align="center">

### **Protect Sensitive Information in Medical Documents — Locally & Securely**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-21%2F21_Passing-4ECDC4?style=for-the-badge&logo=pytest&logoColor=white)](#-running-tests)

<br/>

> **MedShield** is a beginner-friendly, privacy-first healthcare document redaction tool that automatically detects and hides personally identifiable information (PII) from medical documents before they are shared. No cloud. No APIs. Everything stays on your machine.

<br/>

🔒 **100% Local Processing** · 🚀 **Instant Redaction** · 📄 **TXT · CSV · PDF Support** · 🎨 **Beautiful Dark UI**

</div>

---

<br/>

## 📋 Table of Contents

- [✨ Features](#-features)
- [🔍 What Does MedShield Detect?](#-what-does-medshield-detect)
- [🚀 Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [📖 File Descriptions](#-file-descriptions)
- [🔧 How It Works](#-how-it-works)
- [📊 Sample Output](#-sample-output)
- [🧪 Running Tests](#-running-tests)
- [🎨 UI Design](#-ui-design)
- [⚠️ Privacy & Disclaimer](#️-privacy--disclaimer)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

<br/>

---

<br/>

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔒 **100% Local Processing** | All files are processed entirely on your machine. No data ever leaves your computer — no cloud uploads, no external APIs, no tracking. |
| 📄 **Multi-Format Support** | Upload and process **TXT**, **CSV**, and **PDF** files. MedShield intelligently extracts text from each format. |
| 🛡️ **Smart PII Detection** | Automatically detects **12+ types** of sensitive information using carefully crafted regex patterns — from Aadhaar numbers to patient names. |
| 🔍 **Side-by-Side Comparison** | View the original document and the protected version side-by-side, so you can verify exactly what was redacted. |
| 📊 **Redaction Summary** | Get a detailed breakdown of how many items were redacted and which categories were detected, displayed in beautiful stat cards. |
| ⬇️ **One-Click Download** | Download the protected file instantly with a single click. The redacted file is named clearly (e.g., `REDACTED_report.txt`). |
| 📋 **Sample Documents** | Three realistic fictional medical documents are included so you can try MedShield immediately — no file prep needed. |
| 🎨 **Premium Dark UI** | A stunning glassmorphism interface with animated gradients, floating cards, pulse effects, and smooth hover transitions. |
| ♿ **Accessible Design** | Readable fonts (Inter), clear buttons, useful labels, and keyboard-friendly navigation throughout the interface. |
| 🧪 **Fully Tested** | 21 unit tests covering all redaction patterns, file processors, and edge cases — all passing. |

<br/>

---

<br/>

## 🔍 What Does MedShield Detect?

MedShield scans for **12 types** of personally identifiable information using carefully designed regex patterns. Each detected item is replaced with a clear label while preserving medically useful information.

| # | PII Type | Replacement Label | Example Input | Example Output |
|:-:|----------|-------------------|---------------|----------------|
| 1 | **Date of Birth** | `[DOB REDACTED]` | `DOB: 15/03/1981` | `DOB: [DOB REDACTED]` |
| 2 | **Patient Names** | `[NAME REDACTED]` | `Patient Name: Arjun Mehta` | `Patient Name: [NAME REDACTED]` |
| 3 | **Doctor / Title Names** | `[NAME REDACTED]` | `Dr. Priya Sharma` | `Dr. [NAME REDACTED]` |
| 4 | **Addresses** | `[ADDRESS REDACTED]` | `Address: 42, Rajaji Nagar, Bangalore` | `Address: [ADDRESS REDACTED]` |
| 5 | **PIN Codes** | `[PINCODE REDACTED]` | `PIN: 560010` | `PIN: [PINCODE REDACTED]` |
| 6 | **Medical Record IDs** | `[MRN REDACTED]` | `MRN: MR-2024-00789` | `MRN: [MRN REDACTED]` |
| 7 | **Insurance IDs** | `[INSURANCE_ID REDACTED]` | `Insurance ID: INS-KA-20240156` | `Insurance ID: [INSURANCE_ID REDACTED]` |
| 8 | **Phone Numbers** | `[PHONE REDACTED]` | `+91-98765-43210` | `[PHONE REDACTED]` |
| 9 | **Email Addresses** | `[EMAIL REDACTED]` | `arjun.mehta@email.com` | `[EMAIL REDACTED]` |
| 10 | **Aadhaar Numbers** | `[AADHAAR REDACTED]` | `2345 6789 0123` | `[AADHAAR REDACTED]` |
| 11 | **SSN-like IDs** | `[SSN REDACTED]` | `123-45-6789` | `[SSN REDACTED]` |
| 12 | **General Dates** | `[DATE REDACTED]` | `March 15, 2024` | `[DATE REDACTED]` |

> 💡 **Note:** Medical terminology, diagnoses, medication names, lab values, and treatment details are **preserved** — only personally identifiable information is redacted.

<br/>

---

<br/>

## 🚀 Quick Start

### Prerequisites

- **Python 3.9** or higher
- **pip** (Python package manager)
- **Git** (to clone the repository)

### Setup on Windows

```bash
# 1. Clone the repository
git clone https://github.com/brunda-coder/MedShield.git
cd MedShield

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch MedShield
streamlit run app.py
```

### Setup on Linux / macOS

```bash
# 1. Clone the repository
git clone https://github.com/brunda-coder/MedShield.git
cd MedShield

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch MedShield
streamlit run app.py
```

### 🎉 That's it!

MedShield will open in your browser at **http://localhost:8501**. You can try it immediately by clicking one of the sample document buttons.

<br/>

---

<br/>

## 📁 Project Structure

```
MedShield/
│
├── 🎨 app.py                          # Streamlit web interface (premium dark UI)
├── 🔒 redactor.py                     # PII detection & redaction engine (regex)
├── 📄 file_processor.py               # File reading: TXT, CSV, PDF
│
├── 📋 sample_documents/               # Fictional sample files for testing
│   ├── sample_medical_report.txt      #   → Hospital discharge summary
│   ├── sample_patient_records.csv     #   → 5-patient CSV dataset
│   └── sample_lab_report.txt          #   → CBC blood test report
│
├── 🧪 tests/                          # Unit tests (21 tests, all passing)
│   ├── __init__.py
│   ├── test_redactor.py               #   → 15 redactor tests
│   └── test_file_processor.py         #   → 6 file processor tests
│
├── ⚙️ .streamlit/
│   └── config.toml                    # Streamlit theme & server configuration
│
├── 📦 requirements.txt                # Python dependencies
├── 📖 README.md                       # This file
└── 🚫 .gitignore                      # Git ignore rules
```

<br/>

---

<br/>

## 📖 File Descriptions

### `app.py` — The Web Interface
The main entry point of the application. Built with **Streamlit**, it provides a stunning glassmorphism dark-mode UI with:
- Animated gradient title and pulsing shield icon
- File upload with drag-and-drop support
- One-click sample document loading
- Document preview with character/line count stats
- "Protect Document" button with scanning animation
- Side-by-side comparison (red-tinted original vs green-tinted protected)
- Redaction summary with per-category stat cards
- One-click download of the protected file
- Sidebar showing all detectable PII patterns
- Privacy notice and disclaimer

### `redactor.py` — The Redaction Engine
The core intelligence of MedShield. Contains:
- **`RedactionResult`** dataclass — stores the redacted text, total count, and per-category breakdown
- **`PATTERNS`** list — 12 compiled regex patterns ordered by priority (specific patterns like DOB run before general date patterns to avoid conflicts)
- **`redact_text(text)`** — main function that applies all patterns and returns a `RedactionResult`
- **`get_supported_patterns()`** — returns human-readable names of all supported pattern categories

### `file_processor.py` — The File Reader
Handles reading and parsing of uploaded files:
- **`validate_file()`** — checks file type (`.txt`, `.csv`, `.pdf`) and size (max 10 MB)
- **`read_txt()`** — decodes text with UTF-8 → Latin-1 fallback
- **`read_csv()`** — parses CSV and formats rows with pipe separators for readability
- **`read_pdf()`** — uses PyMuPDF (fitz) to extract text from all pages with page markers
- **`process_file()`** — main entry point that routes to the correct reader
- **`create_download_content()`** — prepares the redacted file for download

### `tests/` — Unit Tests
Comprehensive test suite with **21 tests** covering:
- Each PII pattern type (phone, email, Aadhaar, SSN, DOB, dates, MRN, names, addresses, insurance)
- Medical content preservation (ensuring diagnoses and medication names are NOT redacted)
- Edge cases (empty text, no PII, redaction count accuracy)
- File reading (TXT, CSV encoding, download content generation)

### `sample_documents/` — Demo Files
Three realistic but **entirely fictional** medical documents:
- **`sample_medical_report.txt`** — A hospital discharge summary from "Sunrise General Hospital" with patient demographics, clinical notes, medications, and follow-up appointments
- **`sample_patient_records.csv`** — A CSV dataset with 5 fictional patients including names, phone numbers, Aadhaar numbers, diagnoses, and treating doctors
- **`sample_lab_report.txt`** — A CBC blood test report from "Sunrise Diagnostics Lab" with lab values, reference ranges, and clinical interpretations

<br/>

---

<br/>

## 🔧 How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  📤 Upload File  │ ──→ │  📄 Extract Text  │ ──→ │  🔍 Scan for PII │
│  (TXT/CSV/PDF)  │     │  (file_processor) │     │    (redactor)    │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  ⬇️ Download     │ ←── │  📊 Show Summary  │ ←── │  🛡️ Replace PII  │
│  Protected File │     │  & Comparison    │     │  with Labels    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

**Step-by-step:**

1. **Upload** a medical document (or click a sample button for instant demo)
2. **Preview** the extracted text content with character and line counts
3. **Click "Protect Document"** — MedShield scans for sensitive information
4. **Review the summary** — see how many items were redacted and in which categories
5. **Compare side-by-side** — original (red-tinted) vs protected (green-tinted)
6. **Download** the protected file with one click

<br/>

---

<br/>

## 📊 Sample Output

### Before (Original Document)
```
Patient Name: Arjun Mehta
Age/Gender: 45 years / Male
DOB: 15/03/1981
Phone: +91-98765-43210
Email: arjun.mehta@email.com
Address: 42, Rajaji Nagar, 3rd Block, Bangalore, Karnataka - 560010
Aadhaar No: 2345 6789 0123
MRN: MR-2024-00789
Insurance ID: INS-KA-20240156
Attending Physician: Dr. Priya Sharma
Diagnosis: Type 2 Diabetes Mellitus with Hypertension
```

### After (Protected Document)
```
Patient Name: [NAME REDACTED]
Age/Gender: 45 years / Male
DOB: [DOB REDACTED]
Phone: [PHONE REDACTED]
Email: [EMAIL REDACTED]
Address: [ADDRESS REDACTED]
Aadhaar No: [AADHAAR REDACTED]
MRN: [MRN REDACTED]
Insurance ID: [INSURANCE_ID REDACTED]
Attending Physician: Dr. [NAME REDACTED]
Diagnosis: Type 2 Diabetes Mellitus with Hypertension
```

> ✅ Notice how the **diagnosis** and **medical information** are preserved while all **personally identifiable information** is redacted.

<br/>

---

<br/>

## 🧪 Running Tests

MedShield includes a comprehensive test suite with **21 tests** covering all functionality.

```bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Run all tests with verbose output
pytest tests/ -v
```

### Expected Output
```
tests/test_file_processor.py::test_read_txt                  PASSED  [  4%]
tests/test_file_processor.py::test_read_txt_encoding          PASSED  [  9%]
tests/test_file_processor.py::test_read_csv                   PASSED  [ 14%]
tests/test_file_processor.py::test_create_download_content    PASSED  [ 19%]
tests/test_file_processor.py::test_allowed_extensions         PASSED  [ 23%]
tests/test_file_processor.py::test_max_file_size              PASSED  [ 28%]
tests/test_redactor.py::test_phone_redaction                  PASSED  [ 33%]
tests/test_redactor.py::test_email_redaction                  PASSED  [ 38%]
tests/test_redactor.py::test_aadhaar_redaction                PASSED  [ 42%]
tests/test_redactor.py::test_ssn_redaction                    PASSED  [ 47%]
tests/test_redactor.py::test_dob_redaction                    PASSED  [ 52%]
tests/test_redactor.py::test_date_redaction                   PASSED  [ 57%]
tests/test_redactor.py::test_mrn_redaction                    PASSED  [ 61%]
tests/test_redactor.py::test_name_redaction                   PASSED  [ 66%]
tests/test_redactor.py::test_address_redaction                PASSED  [ 71%]
tests/test_redactor.py::test_insurance_redaction              PASSED  [ 76%]
tests/test_redactor.py::test_medical_content_preserved        PASSED  [ 80%]
tests/test_redactor.py::test_redaction_count                  PASSED  [ 85%]
tests/test_redactor.py::test_empty_text                       PASSED  [ 90%]
tests/test_redactor.py::test_no_pii                           PASSED  [ 95%]
tests/test_redactor.py::test_get_supported_patterns           PASSED  [100%]

========================= 21 passed in 4.54s ==========================
```

<br/>

---

<br/>

## 🎨 UI Design

MedShield features a **premium dark-mode glassmorphism UI** designed to be visually stunning and functionally intuitive.

### Design Highlights

- **🌌 Dark Gradient Background** — Deep blue-to-purple gradient (`#0a0a1a` → `#1a1033`)
- **✨ Animated Title** — Gradient text that shifts through purple, teal, and lavender
- **💫 Pulsing Shield Icon** — Gentle glow animation on the shield emoji
- **🪟 Glassmorphic Cards** — Semi-transparent backgrounds with blur backdrop and subtle borders
- **🎯 Gradient Buttons** — Purple-to-teal gradient with hover lift and glow effects
- **📊 Stat Cards** — Floating cards with per-category icons (📱 Phone, 📧 Email, 🪪 Aadhaar, etc.)
- **🔴🟢 Comparison Panels** — Red-tinted original vs green-tinted protected document views
- **📝 Inter Font** — Google's Inter typeface for crisp, modern typography
- **🖱️ Micro-Animations** — Hover lift effects, smooth transitions, and fade-in animations

### Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Core language |
| **Streamlit** | Web application framework |
| **PyMuPDF (fitz)** | PDF text extraction |
| **re (stdlib)** | Regex-based PII detection |
| **csv (stdlib)** | CSV file parsing |
| **pytest** | Unit testing framework |

<br/>

---

<br/>

## ⚠️ Privacy & Disclaimer

### 🔒 Privacy Notice

MedShield processes all files **locally on your machine**. No data is uploaded to external servers, cloud services, or third-party APIs. Your medical documents never leave your computer.

However:
- **Do not upload files** if you do not trust this application
- **Do not use MedShield** as the sole method of protecting sensitive information
- **Always verify** redactions manually before sharing protected documents

### ⚖️ Disclaimer

MedShield is a **document-redaction tool** designed to assist with privacy protection. It is **NOT**:

- ❌ A guarantee of legal compliance (HIPAA, GDPR, DISHA, etc.)
- ❌ A medical diagnosis or treatment tool
- ❌ A substitute for professional legal or medical advice
- ❌ A certified data anonymization solution

MedShield uses regex-based pattern matching, which may not catch all forms of sensitive information. **Always review redacted documents** before sharing them.

<br/>

---

<br/>

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Ideas for Contributions

- 🌐 Add more language support for PII patterns (Hindi, Tamil, etc.)
- 📝 Support for DOCX files
- 🧠 Optional NLP-based name detection
- 📱 Mobile-responsive UI improvements
- 🌍 Internationalization (i18n) support
- 📋 Batch file processing

<br/>

---

<br/>

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

<br/>

---

<div align="center">

**Built with ❤️ by [Brunda G](https://github.com/brunda-coder) for healthcare privacy**

<br/>

🛡️ *Protecting what matters most — your personal information.*

</div>