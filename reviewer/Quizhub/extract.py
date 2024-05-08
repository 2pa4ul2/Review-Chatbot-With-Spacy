from PyPDF2 import PdfReader 
import os

def extract(uploaded_file):
    pdf = PdfReader(uploaded_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text