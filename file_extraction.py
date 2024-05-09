import nltk
import spacy
from  nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

class FileExtractor:
    def __init__(self, num_questions):
        self.num_questions = num_questions
        self.ner_tagger = spacy.load('en_core_web_sm')
        self.stop_words = set(stopwords.words('english'))
        self.tfidf = TfidfVectorizer()
        self.questions_dict = dict()

    def get_questions_dict(self, file):
        '''

        This functions extracts text from a file and returns a dictionary of questions.
        Need: file
        Return: dictionary of questions
        Format of dictionary: question_number{question: [answer1, answer2, answer3, ...]}

        '''
        self.possible_keywords = self.get_possible_entities(file)
        self.set_tdidf_scores(file)
        self.rank_keywords()
        self.form_questions()
        return self.questions_dict
    
    def get_cleaned_sentences(self, file):
        '''
        This function extracts text from a file and returns a list of cleaned sentences.
        Need: file
        Return: list of cleaned sentences
        '''
        sentences = sent_tokenize(file)
        return [self.clean_sentences(sentence) for sentence in sentences] 
    
    def clean_sentences(self, sentence):
        '''
        This function takes a sentence and returns a cleaned sentence.
        Need: sentence
        Return: cleaned sentence
        '''
        words = word_tokenize(sentence)
        return " ".join([w for w in words if w not in self.stop_words])
    
    def get_possible_entities(self, file):
        '''
        This function extracts text from a file and returns a list of possible entities.
        Need: file
        Return: list of possible entities
        '''
        entities = self.ner_tagger(file)
        entity_list = []

        for ent in entities.ents:
            entity_list.append(ent.text)
        return list(set(entity_list))
    
    def set_tdidf_scores(self, file):
        """
        Set the TF-IDF scores for each word in the given file.

        Need: The file to extract TF-IDF scores from.
        Returns: None
        """
        self.uncleaned_sentences = sent_tokenize(file)
        self.cleaned_sentences = self.get_cleaned_sentences(file)

        self.word_score = dict()

        self.sentence_for_max_word_score = dict()

        self.vectorizer = TfidfVectorizer()
        tf_idf_vector = self.vectorizer.fit_transform(self.cleaned_sentences)
        feature_names = self.vectorizer.get_feature_names_out()
        tf_idf_matrix = tf_idf_vector.todense().tolist()

        num_sentences = len(self.uncleaned_sentences)
        num_features = len(feature_names)

        for i in range(num_features):
            word = feature_names[i]
            self.sentence_for_max_word_score[word] = ""
            tot = 0.0
            cur_max = 0.0

            for j in range(num_sentences):
                tot += tf_idf_matrix[j][i]

                if tf_idf_matrix[j][i] > cur_max:
                    cur_max = tf_idf_matrix[j][i]
                    self.sentence_for_max_word_score[word] = self.uncleaned_sentences[j]
            # Compute average score for each word
            self.word_score[word] = tot/num_sentences
    
    def get_keyword_score(self, keyword):
        '''
        This function returns the score for a keyword
        Need: keywords
        Return: score
        '''
        score = 0.0
        for word in word_tokenize(keyword):
            if word in self.word_score:
                score+=self.word_score[word]
        return score
    
    def get_corresponding_sentence_for_keyword(self, keyword):
        '''
        Finds and returns the sentences containing the keyword
        '''
        words = word_tokenize(keyword)
        for word in words:
            if word not in self.sentence_for_max_word_score:
                continue
            sentence = self.sentence_for_max_word_score[word]

            all_present = True
            for w in words:
                if w not in sentence:
                    all_present = False
            
            if all_present:
                return sentence
        return ""
    
    def rank_keywords(self):
        '''
        This functions ranks keywords according to their score
        '''
        self.possible_triples = []

        for possible_keyword in self.possible_keywords:
            self.possible_triples.append([
                self.get_keyword_score(possible_keyword),
                possible_keyword,
                self.get_corresponding_sentence_for_keyword(possible_keyword)
            ])

        self.possible_triples.sort(reverse=True)
    
    def form_questions(self):
        '''
        Forms the question and populates the question dictionary
        '''
        used_sentences = list()
        idx = 0
        ctr = 1

        num_possibles = len(self.possible_triples)
        while ctr <= self.num_questions and idx < num_possibles:
            possible_triple = self.possible_triples[idx]

            if possible_triple[2] not in used_sentences:
                used_sentences.append(possible_triple[2])

                self.questions_dict[ctr] = {
                    "question": possible_triple[2].replace(
                        possible_triple[1],
                        '_' * len(possible_triple[1])),
                    "answer": possible_triple[1]
                }

                ctr += 1
            idx += 1