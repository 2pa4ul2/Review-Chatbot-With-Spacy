from flask import Flask, render_template, request
from question_generation_main import QuestionGenerator
from PyPDF2 import PdfReader

app = Flask(__name__)

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
            with open(filepath, 'r', encoding='utf-8') as txt_file:
                content = txt_file.read()
                print("Text file extracted successfully!")
        return content

    def txt2questions(self, doc: str, num_questions: int, o=4) -> dict:
        qGenerator = QuestionGenerator(num_questions, o)
        qGenerator.generate_questions_dict(doc)
        return qGenerator.questions_dict

    def extract_questions(self, num_questions) -> dict:
        text_content = self.pdf2text(self.file_path, self.file_extension)
        questions = self.txt2questions(text_content, num_questions)
        print("DONE EXTRACTING QUESTIONS")
        return questions

@app.route('/', methods=['GET', 'POST'])
def home():
    questions = {}
    if request.method == 'POST':
        num_questions = int(request.form.get('num_questions', 10))
        file_path = request.form.get('file_path', 'pdfs/modelling.pdf')
        pdf = PDFtoQuestions(file_path)
        questions = pdf.extract_questions(num_questions)
        
    return render_template('index.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
