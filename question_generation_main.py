from file_extraction import FileExtractor
from incorrect_answer_generation import IncorrectAnswerGenerator
import re
from nltk.tokenize import sent_tokenize

# from PyPDF2 import PdfReader

# def pdf2text(filepath: str, file_ext: str)->str:
#     content = ""
#     if file_ext == 'pdf':
#         with open(filepath, 'rb') as pdf_file:
#             pdf_reader = PdfReader(pdf_file)
#             for page in range(len(pdf_reader.pages)):
#                 content += pdf_reader.pages[page].extract_text()
#             print("PDF file extracted successfully!")

#     elif file_ext == 'txt':
#         with open(filepath, 'r') as txt_file:
#             content = txt_file.read()
#             print("Text file extracted successfully!")
#     print(content)
#     return content

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
        for i in range(1, self.num_questions + 1):
            if i not in self.questions_dict:
                #print('ques_dict:', self.questions_dict)
                continue
            if 'answer' in self.questions_dict[i]:
                self.questions_dict[i]['choices'] = self.incorrect_answer_generator.get_all_options_dict(
                    self.questions_dict[i]['answer'], 
                    self.num_options
                )
          
        return self.questions_dict
        

# if __name__ == '__main__':

#     # Example test case
#     file_path = "pdfs\MAPTEST.pdf"
#     file_extension = 'pdf'

#     # Call the pdf2text function
#     text_content = pdf2text(file_path, file_extension)
#     qgen = QuestionGenerator(3, 3)
#     text_content = qgen.clean_text(text_content)
