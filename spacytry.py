#no model  

import spacy
from spacypdfreader.spacypdfreader import pdf_reader

nlp = spacy.load("en_core_web_sm")
doc = pdf_reader("pdfs\MAPTEST.pdf", nlp)

# Normalization (convert to lowercase) and stopword removal
normalized_text = [token.text.lower() for token in doc if not token.is_stop]

# Lemmatization
lemmatized_text = [token.lemma_ for token in doc if not token.is_stop]

# Named Entity Recognition
for ent in doc.ents:
    print(ent.text, ent.label_)

print("Normalized and stopword removed text: ", normalized_text)
print("Lemmatized text: ", lemmatized_text)