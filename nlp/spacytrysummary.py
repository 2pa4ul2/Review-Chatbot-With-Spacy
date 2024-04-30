#no model  


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest



text = input("Enter the text: ")
print("Length of original text:",len(text))

#summarization of the text
def text_summarization(text, percentage):

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text) 

    tokens=[token.text for token in doc]
    frequency = dict()

    #cleaning text
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in frequency.keys():
                    frequency[word.text] = 1
                else:
                    frequency[word.text] += 1

    #setting max frequency of word
    max_frequency = max(frequency.values())

    #normalization
    for word in frequency.keys():
        frequency[word] = frequency[word]/max_frequency

    #sentence is weighed based on how often it contains the token
    sent_tokens = [sent for sent in doc.sents]
    sentscore = dict()
    for sent in sent_tokens:
        for word in sent:
            if word.text.lower() in frequency.keys():
                if sent not in sentscore.keys():
                    sentscore[sent] = frequency[word.text.lower()]
                else:
                    sentscore[sent] += frequency[word.text.lower()]

    len_tokens = int(len(sent_tokens)*percentage)

    #Summary for the sentences with maximum score. 
    #Here, each sentence in the list is of spacy.span type
    summary = nlargest(n = len_tokens, iterable = sentscore, key = sentscore.get)

    #preparation for final summary
    final_summary = [word.text for word in summary] 
    
    #string convert
    summary = ' '.join(final_summary)

    return summary



final_summary = text_summarization(text, 0.2)
print("#"*50)
print("Summary of the text")
print("Length of summarized text:",len(final_summary))
print("#"*50)
print()
print(final_summary)