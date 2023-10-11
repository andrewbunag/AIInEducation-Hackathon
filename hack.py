import openai
import csv
import pandas as pd
import sys

# Set your OpenAI API key (replace 'YOUR_API_KEY' with your actual API key)
openai.api_key = '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'

# Function to generate ACT-style questions and answer choices based on the input question type
def generate_questions_and_save_to_csv(num_questions, question_type):
    # Define the prompt for generating ACT-style questions
    prompt = f"Create 1 ACT-style {question_type} question and display 5 different possible answer choices each: A. B. C. D. E, each of them being under each other. Start with the letter Q: and then add the question following that. Display the correct answer after following the format of 'Correct Answer: '"
    
    # Generate the questions and answer choices
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,  # You can adjust the token limit as needed
        n=num_questions,  # Generate the specified number of questions
        stop=None,
    )

    # Initialize a list to store question-answer pairs
    question_answer_pairs = []

    # Iterate through the generated questions and answer choices
    for i, choice in enumerate(response.choices, start=1):
        output_text = choice.text.strip()
        output_text = output_text.strip('"')
        lines = output_text.split("\n")
        question = lines[0].strip('"')  # Remove leading/trailing quotation marks
        answer_choices = '\n'.join(lines[1:-1])  # The remaining lines are answer choices
        correct_answer = lines[-1].strip('"')  # Remove leading/trailing quotation marks

        # Manually add a comma to the correct answer
        correct_answer = f"{correct_answer}"

        # Add the question, question type, answer choices, and correct answer to the list
        question_answer_pairs.append([question, question_type, answer_choices, correct_answer])

    # Define the CSV file path
    csv_file_path = "generated_questions.csv"

    # Write the question-answer pairs to the CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header row
        csv_writer.writerow(["Question", "Question Type", "Answer Choices", "Correct Answer"])
        
        # Write each question-answer pair
        for pair in question_answer_pairs:
            csv_writer.writerow([pair[0] + '\n', pair[1], pair[2] + '\n\n', pair[3] + '\n'])

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    

# Input for the number of questions to generate
num_questions = int(input("Enter the number of questions to generate: "))

# Input for the question type
question_type = input("Enter the question type (e.g., history, science, math, etc.): ")

# Call the function to generate and save questions
generate_questions_and_save_to_csv(num_questions, question_type)

sys.exit()
