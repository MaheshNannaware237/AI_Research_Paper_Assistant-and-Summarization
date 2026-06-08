from pypdf import PdfReader
import re
import io


def extract_text_from_pdf(pdf_file) -> str:
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def get_pdf_metadata(pdf_file) -> dict:
    pdf_reader = PdfReader(pdf_file)
    meta = pdf_reader.metadata or {}
    return {
        "pages": len(pdf_reader.pages),
        "title": meta.get("/Title", "Unknown"),
        "author": meta.get("/Author", "Unknown"),
        "subject": meta.get("/Subject", ""),
    }
