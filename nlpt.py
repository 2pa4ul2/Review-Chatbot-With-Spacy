import spacy

from PyPDF2 import PdfReader


pdf = PdfReader("pdfs/modelling.pdf")

text = ""
for pages in pdf.pages:
    text += pages.extract_text()


nlp = spacy.load("en_core_web_sm")
doc = nlp(text)


print(text)