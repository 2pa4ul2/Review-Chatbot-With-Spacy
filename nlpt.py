# this section is assigned to extract text from pdf files
# Originally intended to extract text from only pdf files
# But I might add other file types later
# Such as .docx, .txt and just a text sent from the telegram bot
import spacy
from PyPDF2 import PdfReader

pdf = PdfReader("pdfs/modelling.pdf")
class Extract:
    def __init__(self, pdf_path):
        self.nlp = spacy.load("en_core_web_sm")
        self.pdf_path = pdf_path

    def extract_text(self):
        text = ""
        with open(self.pdf_path, "rb") as file:
            pdf = PdfReader(file)
            text = self._extract_text_from_pdf(pdf)
        for page in pdf.pages:
            text += page.extract_text()
        return text

if __name__ == "__main__":
    extractor = Extract("pdfs/modelling.pdf")
    print(extractor.extract_text())