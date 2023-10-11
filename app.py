from flask import Flask, render_template, request, redirect, url_for, send_file
import openai  # Import the OpenAI library
import csv

# Set your OpenAI API key
openai.api_key = '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'

app = Flask(__name__)

# Define a global list to store questions and correct answers
diagnostic_data = []

# Load diagnostic data from the CSV file
with open('diagnostic_test.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        diagnostic_data.append(row)

# Create a dictionary to track incorrect answers count for each question type
incorrect_answers_count = {row['Question Type']: 0 for row in diagnostic_data}

@app.route('/')
def home():
    return render_template('index.html', diagnostic_data=diagnostic_data)

@app.route('/check_answers', methods=['POST'])
def check_answers():
    global incorrect_answers_count  # To access the global incorrect_answers_count

    for i, row in enumerate(diagnostic_data, start=1):
        user_answer = request.form.get(f'answer_{i}')
        correct_answer = row['Correct Answer'].strip()

        # Check if user_answer is not None before attempting to strip it
        if user_answer is not None:
            user_answer = user_answer.strip()

            if user_answer != correct_answer:
                question_type = row['Question Type']
                incorrect_answers_count[question_type] += 1

    return render_template('results.html', incorrect_answers_count=incorrect_answers_count)

# Create a route for generating new questions
@app.route('/generate_new_questions', methods=['POST'])
def generate_new_questions():
    num_incorrect = request.form.get('num_incorrect')
    category = request.form.get('category')

    # Use user input to create the prompt for GPT-3
    prompt = f"Generate {num_incorrect} questions in the {category} category."

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100
    )

    new_questions = response.choices[0].text.split('\n')  # Extract generated questions

    # Store the generated questions in a CSV file
    with open('new_questions.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows([question.strip()] for question in new_questions)

    # Read the contents of the CSV file
    with open('new_questions.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        new_questions = [row[0] for row in csv_reader]

    return render_template('new_questions.html', new_questions=new_questions)

@app.route('/download_csv')
def download_csv():
    return send_file('new_questions.csv', as_attachment=True)

@app.route('/')
def input_form():
    return render_template('input_form.html')

if __name__ == '__main__':
    app.run(debug=True)