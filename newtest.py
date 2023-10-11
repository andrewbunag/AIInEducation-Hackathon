import csv

def load_new_questions_from_csv():
    new_test_questions = []

    # Assuming you saved the newly generated questions in a file named "new_test_questions.csv"
    with open('generated_questions.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_test_questions.append(row)

    return new_test_questions