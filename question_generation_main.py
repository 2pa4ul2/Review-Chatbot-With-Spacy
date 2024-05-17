from file_extraction import FileExtractor
from incorrect_answer_generation import IncorrectAnswerGenerator
import re
from nltk.tokenize import sent_tokenize


class QuestionGenerator:
    def __init__(self, num_questions, num_options):
        self.num_questions = num_questions
        self.num_options = num_options
        self.file_extractor = FileExtractor(num_questions)

    def clean_text(self, text):
        ''' This function cleans the text
        by removing special characters
        '''
        text = text.replace('\n', ' ')
        sentences = sent_tokenize(text)
        cleaned_text = ""
        for sentence in sentences:
            good_sentence = re.sub(r'([^\s\w]|_)+', '', sentence)
            good_sentence = re.sub(' +', ' ', good_sentence)
            cleaned_text += good_sentence.strip()  # Remove trailing space

            if cleaned_text and cleaned_text[-1] != '.':
                cleaned_text += '. '

        #print("cleaned_text:", cleaned_text)
        return cleaned_text
    
    def clean_words(self, text):
        ''' This function cleans the sentences
        by removing stop words and returns list of words
        '''
        words = self.file_extractor.clean_sentences(text)
        #print("stop removed:", words)
        return words
    
    def generate_questions_dict(self, file):
        ''' This function generates the questions
        dictionary from the file
        '''
        file = self.clean_text(file)
        self.questions_dict = self.file_extractor.get_questions_dict(file)
        self.incorrect_answer_generator = IncorrectAnswerGenerator(self.clean_words(file))
        print("num_questions", self.num_questions)
        print("len of questions generated:", len(self.questions_dict))

        for i in range(len(self.questions_dict)):
            if i not in self.questions_dict:
                continue
            if 'answer' in self.questions_dict[i]:
                self.questions_dict[i]['choices'] = self.incorrect_answer_generator.get_all_options_dict(
                    self.questions_dict[i]['answer'], 
                    self.num_options
                )

        min_num_ques = min(self.num_questions, len(self.questions_dict))

        return {i: self.questions_dict[i] for i in range(1, min_num_ques + 1)}
        

# if __name__ == '__main__':

#     # Example test case
#     file_path = "pdfs\MAPTEST.pdf"
#     file_extension = 'pdf'

#     # Call the pdf2text function
#     text_content = pdf2text(file_path, file_extension)
#     qgen = QuestionGenerator(3, 3)
#     text_content = qgen.clean_text(text_content)
