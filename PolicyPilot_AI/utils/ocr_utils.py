import os
import io
import streamlit as st

def extract_text_from_pdf(file):
    """Extract text from PDF using PyPDF2"""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {page_num + 1} ---\n{page_text}"
        return text.strip() if text.strip() else "No text could be extracted from this PDF."
    except Exception as e:
        return f"PDF extraction error: {str(e)}"

def extract_text_from_image(file):
    """Extract text from image using pytesseract"""
    try:
        import pytesseract
        from PIL import Image
        image = Image.open(file)
        text = pytesseract.image_to_string(image, lang='eng')
        return text.strip() if text.strip() else "No text detected in image."
    except ImportError:
        return "pytesseract not installed or Tesseract OCR engine missing. Please install Tesseract."
    except Exception as e:
        return f"OCR extraction error: {str(e)}"

def analyze_document(text):
    """Analyze extracted text for insurance document details"""
    keywords = {
        "Patient Name": ["patient", "name", "insured"],
        "Hospital Name": ["hospital", "clinic", "medical center", "healthcare"],
        "Date of Admission": ["admission", "admitted", "date of admission"],
        "Discharge Date": ["discharge", "discharged", "date of discharge"],
        "Diagnosis": ["diagnosis", "diagnosed", "condition", "disease"],
        "Treatment": ["treatment", "procedure", "surgery", "operation"],
        "Total Amount": ["total", "amount", "charges", "bill", "cost"],
        "Doctor Name": ["doctor", "physician", "dr.", "consultant"],
        "Policy Number": ["policy", "policy no", "policy number"],
        "Claim Amount": ["claim", "claim amount", "reimbursement"],
    }

    text_lower = text.lower()
    found_fields = {}
    missing_fields = []

    for field, kw_list in keywords.items():
        found = any(kw in text_lower for kw in kw_list)
        if found:
            found_fields[field] = "✅ Detected"
        else:
            missing_fields.append(field)

    suspicious_keywords = [
        "cash payment", "no receipt", "informal", "unregistered",
        "personal account", "avoid tax", "unofficial"
    ]
    suspicious_found = [kw for kw in suspicious_keywords if kw in text_lower]

    return {
        "found_fields": found_fields,
        "missing_fields": missing_fields,
        "suspicious_keywords": suspicious_found,
        "word_count": len(text.split()),
        "completeness_score": round((len(found_fields) / len(keywords)) * 100, 1)
    }

def validate_file(uploaded_file):
    """Validate uploaded file type and size"""
    if uploaded_file is None:
        return False, "No file uploaded"

    ALLOWED_TYPES = ["application/pdf", "image/jpeg", "image/png", "image/jpg", "image/tiff"]
    MAX_SIZE_MB = 10

    file_size_mb = uploaded_file.size / (1024 * 1024)

    if file_size_mb > MAX_SIZE_MB:
        return False, f"File size {file_size_mb:.1f}MB exceeds limit of {MAX_SIZE_MB}MB"

    if uploaded_file.type not in ALLOWED_TYPES:
        return False, f"File type '{uploaded_file.type}' not allowed. Use PDF, JPG, or PNG."

    return True, "File is valid"

def save_uploaded_file(uploaded_file, claim_id):
    """Save uploaded file to uploads directory"""
    os.makedirs("uploads", exist_ok=True)
    ext = os.path.splitext(uploaded_file.name)[1]
    save_path = f"uploads/{claim_id}{ext}"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path
