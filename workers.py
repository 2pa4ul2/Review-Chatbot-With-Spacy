from PyPDF2 import PdfReader
from question_generation_main import QuestionGenerator

def pdf2text(filepath: str, file_ext: str)->str:
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
    print(content)
    return content

def txt2questions(doc: str, n=5, o=4)->dict:
    qGenerator = QuestionGenerator(n, o)
    q = qGenerator.generate_questions_dict(doc)
    for i in range(len(q)):
        temp = []
        if "choices" in q[i+1]:
            for j in range(len(q[i+1]["choices"])):
                temp.append(q[i+1]["choices"][j])
        q[i+1]["choices"] = temp
    #print(q)
    return q


# Example test case
file_path = "pdfs\MAPTEST.pdf"
file_extension = 'pdf'

# Call the pdf2text function
text_content = pdf2text(file_path, file_extension)

# Call the txt2questions function
questions = txt2questions(text_content)


# Print the generated questions
for index, ques in questions.items():
    print("QUESTION NUMBER:", index)
    for i in ques:
        print(f"{i}: {i.value()}")
    # print("QUESTION:", ques['question'])
    # print("ANSWER:", ques['answer'])
    # print("CHOICES:", ques['choices'])
