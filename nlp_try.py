import spacy as nlp
import PyPDF2 as pdf
import spacy
file = open('pdfs/modelling.pdf', 'rb')
pdf_reader = pdf.PdfReader(file)
num_pages = len(pdf_reader.pages)
print(num_pages)


pdf_extracted_text = ""
nlp = spacy.load('en_core_web_sm')  #load spacy model
#extract text   
def extract_text_from_pdf(pdf_file):
    pdf_extracted_text = ""
    pdf_reader = pdf.PdfReader(pdf_file)
    for page in pdf_reader.pages:
        pdf_extracted_text += page.extract_text()
        for line in pdf_extracted_text:
            doc = nlp(line)
            #for ent in doc.ents:
                #print(ent.text, ent.label_)
        
    return pdf_extracted_text

pdf_file = 'pdfs/modelling.pdf'
extracted_text = extract_text_from_pdf(pdf_file)
#print(extracted_text)

#Doc object -> Tokens
#doc = nlp(extracted_text)
#for token in doc:
   #print(token, token.idx)

#Sentence Detection
def detect_sentences(text):
    doc = nlp(text)
    sentences = list(doc.sents)
    return sentences

detected_sentences = detect_sentences(extracted_text)
for sentence in detected_sentences:
    print(f"{sentence[:5]}...")
    