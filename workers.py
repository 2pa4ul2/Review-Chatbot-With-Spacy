from PyPDF2 import PdfReader
from question_generation_main import QuestionGenerator

class PDFtoQuestions: 
    def __init__(self, file_path):
        self.file_path = file_path

        filename_parts = file_path.split('.')
        self.file_extension = filename_parts[-1]

    def pdf2text(self, filepath: str, file_ext: str) -> str:
        content = ""
        if file_ext == 'pdf':
            with open(filepath, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                for page in range(len(pdf_reader.pages)):
                    content += pdf_reader.pages[page].extract_text()
                print("PDF file extracted successfully!")

        elif file_ext == 'txt':
            with open(filepath, 'r') as txt_file:
                content = txt_file.read()
                print("Text file extracted successfully!")
        #print(content)
        return content

    def txt2questions(self, doc: str, num_questions: int, o=4) -> dict:
        qGenerator = QuestionGenerator(num_questions, o)
        q = qGenerator.generate_questions_dict(doc)
        # for i in range(len(q)):
        #     temp = []
        #     if "choices" in q[i+1]:
        #         for j in range(len(q[i+1]["choices"])):
        #             temp.append(q[i+1]["choices"][j])
        #     q[i+1]["choices"] = temp
        print(q)
        return q

    def extract_questions(self, num_questions) -> dict:
        
        # Call the pdf2text function
        text_content = self.pdf2text(self.file_path, self.file_extension)
        # Call the txt2questions function
        questions = self.txt2questions(text_content, num_questions)
        
        print("DONE EXTRACTING QUESTIONS")
        return questions



if __name__ == '__main__':
    pdf = PDFtoQuestions("pdfs/modelling.pdf")
    questions = pdf.extract_questions(10)

    # Print the generated questions
    for index, question_data in questions.items():
        print("\nQUESTION #", index)
        print("Question:", question_data['question'])
        print("Answer:", question_data['answer'])

        if 'choices' in question_data:
            print("Choices:")
            for choice_number, choice_text in question_data['choices'].items():
                print(f"\t{choice_number}: {choice_text}")
