import PyPDF2
from io import BytesIO

def load_text_file(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("utf-8", errors="ignore")

def load_pdf_file(file_bytes: bytes) -> str:
    try:
        pdf_file = BytesIO(file_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def load_file(file_bytes: bytes, filename: str) -> str:
    """Load file based on its extension"""
    if filename.lower().endswith('.pdf'):
        return load_pdf_file(file_bytes)
    else:
        return load_text_file(file_bytes)

