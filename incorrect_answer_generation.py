import spacy
import random

class IncorrectAnswerGenerator:
    ''' This class contains the methods
    for generating the incorrect answers
    given an answer
    '''

    def __init__(self, file):
        # model required to fetch similar words
        self.model = spacy.load("en_core_web_sm")
        self.all_words = [token.text for token in self.model(file)]

    def get_all_options_dict(self, answer, num_options):
        ''' This method returns a dict
        of 'num_options' options out of
        which one is correct and is the answer
        '''
        options_dict = dict()
        try:
            similar_words = self.get_similar_words(answer, topn=15)

            for i in range(1, num_options + 1):
                options_dict[i] = similar_words[i - 1][0]

        except:
            self.all_sim = []
            for word in self.all_words:
                if word != answer:
                    try:
                        self.all_sim.append(
                            (self.get_similarity(answer, word), word))
                    except:
                        self.all_sim.append(
                            (0.0, word))
                else:
                    self.all_sim.append((-1.0, word))

            self.all_sim.sort(reverse=True)

            for i in range(1, num_options+1):
                options_dict[i] = self.all_sim[i-1][1]

        replacement_idx = random.randint(1, num_options)

        options_dict[replacement_idx] = answer

        return options_dict

    def get_similar_words(self, word, topn=10):
        target_token = self.model.vocab[word]
        similar_words = []

        for token in self.model.vocab:
            if token.text != target_token.text:
                similarity = target_token.similarity(token)
                similar_words.append((token.text, similarity))

        similar_words.sort(key=lambda x: x[1], reverse=True)
        return similar_words[:topn]

    def get_similarity(self, word1, word2):
        token1 = self.model(word1)
        token2 = self.model(word2)
        return token1.similarity(token2)
