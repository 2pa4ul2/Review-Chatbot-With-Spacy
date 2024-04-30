import spacy
# from polyglot.text import Text


nlp = spacy.load("en_core_web_sm")
nlp.get_pipe("ner")

doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

doc.ents

print([(X.text, X.label_) for X in doc.ents])#printing all entities and their labels
print(doc.ents[0], doc.ents[0].label_)#printing the first entity and its label

print(len(doc))#number of tokens in the doc

# text = """For example, en_core_web_sm is a small English pipeline trained on written web text (blogs, news, comments), that includes vocabulary, syntax and entities."""

# ptext = Text(text)