 == '__main__':
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
                print(f"\t{choice_number}: