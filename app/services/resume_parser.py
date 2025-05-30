import re
import spacy
from docx import Document
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    text = ''
    with open(file_path, "rb") as f:
        pdf = PdfReader(f)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_resume_text(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.search(r'(\+\d{1,2}\s?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}', text)
    doc = nlp(text)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break
    # Add more logic for skills if desired
    skills = []
    if "python" in text.lower():
        skills.append("Python")
    return {
        "name": name,
        "email": email.group() if email else None,
        "phone": phone.group() if phone else None,
        "skills": skills
    }
