"""
AI Study Buddy Demo Project May 2026 Project Demo

Course: Git + Python + AI
Audience: Middle and High School Students

This project demonstrates:
1. Python variables
2. Functions
3. Dictionaries
4. Loops
5. Conditions
6. File handling
7. CSV data
8. Simple AI-style prediction
9. Responsible AI use
10. Git and GitHub workflow

This version uses only built-in Python libraries.
No external package installation is required.
"""

import csv
import os
import string


TRAINING_DATA_FILE = "data/training_data.csv"
CHAT_HISTORY_FILE = "chat_history.txt"


RESPONSES = {
    "python": (
        "Python is a beginner-friendly programming language. "
        "Students can use Python to build apps, games, automation, data projects, and AI projects."
    ),
    "git": (
        "Git is a version control tool. "
        "It helps developers save code history, track changes, and work safely on projects."
    ),
    "ai": (
        "AI means Artificial Intelligence. "
        "AI systems use data and patterns to make predictions, suggestions, or decisions."
    ),
    "greeting": (
        "Hello! I am your AI Study Buddy. "
        "Ask me about Python, Git, GitHub, or AI."
    ),
    "thanks": (
        "You are welcome! Keep practicing daily. "
        "Consistent practice is the best way to learn programming."
    ),
    "bye": (
        "Goodbye! Remember to practice at least 1 hour daily."
    )
}


RESPONSIBLE_AI_NOTE = (
    "Responsible AI Reminder: AI can make mistakes. "
    "Always verify important answers with a teacher, parent, or trusted source."
)


def clean_text(text):
    """
    Clean user text before comparing it with training examples.

    This function:
    1. Converts text to lowercase
    2. Removes punctuation
    3. Removes extra spaces

    Example:
    'What is Python?' becomes 'what is python'
    """

    text = text.lower()

    for symbol in string.punctuation:
        text = text.replace(symbol, "")

    text = text.strip()

    return text


def load_training_data(file_path):
    """
    Load training data from a CSV file.

    The CSV file must have two columns:
    1. question
    2. label

    Example:
    what is python,python
    what is git,git
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Training data file not found: {file_path}")

    training_examples = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            question = clean_text(row["question"])
            label = row["label"].strip().lower()

            training_examples.append({
                "question": question,
                "label": label
            })

    return training_examples


def get_words(sentence):
    """
    Split a sentence into individual words.

    Example:
    'what is python' becomes ['what', 'is', 'python']
    """

    return sentence.split()


def calculate_match_score(user_question, training_question):
    """
    Compare the user's question with one training question.

    The score is based on how many words match.

    Example:
    User question: 'what is python'
    Training question: 'what is python'

    Matching words:
    what, is, python

    Score = 3
    """

    user_words = set(get_words(user_question))
    training_words = set(get_words(training_question))

    matching_words = user_words.intersection(training_words)

    score = len(matching_words)

    return score


def predict_label(user_question, training_examples):
    """
    Predict the best label for the student's question.

    This is a simple AI-style classifier:
    1. Compare user question with every training question
    2. Calculate a match score
    3. Choose the label with the highest score

    This is not ChatGPT.
    This is a beginner-friendly example of how classification works.
    """

    cleaned_question = clean_text(user_question)

    best_label = "unknown"
    best_score = 0

    for example in training_examples:
        training_question = example["question"]
        label = example["label"]

        score = calculate_match_score(cleaned_question, training_question)

        if score > best_score:
            best_score = score
            best_label = label

    confidence = calculate_confidence(best_score, cleaned_question)

    return best_label, confidence


def calculate_confidence(best_score, cleaned_question):
    """
    Calculate a simple confidence percentage.

    This is not a real probability.
    It is a simple score to help students understand model confidence.
    """

    total_words = len(get_words(cleaned_question))

    if total_words == 0:
        return 0

    confidence = int((best_score / total_words) * 100)

    if confidence > 100:
        confidence = 100

    return confidence


def get_response(predicted_label):
    """
    Return a chatbot response based on the predicted label.

    Example:
    If predicted_label is 'python', return the Python explanation.
    """

    return RESPONSES.get(
        predicted_label,
        "I am not sure yet. Try asking about Python, Git, GitHub, or AI."
    )


def save_chat_history(user_question, predicted_label, confidence, bot_response):
    """
    Save the conversation to a text file.

    This demonstrates Python file handling.
    """

    with open(CHAT_HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(f"Student: {user_question}\n")
        file.write(f"Predicted Category: {predicted_label}\n")
        file.write(f"Confidence Score: {confidence}%\n")
        file.write(f"Bot: {bot_response}\n")
        file.write("-" * 50 + "\n")


def display_welcome_message():
    """
    Display welcome message when the chatbot starts.
    """

    print("=" * 60)
    print("              AI Study Buddy Chatbot")
    print("=" * 60)
    print("Ask me about Python, Git, GitHub, or AI.")
    print("Type 'exit' to stop the chatbot.")
    print("=" * 60)
    print()


def run_chatbot(training_examples):
    """
    Run the chatbot.

    The chatbot keeps asking questions until the student types 'exit'.
    """

    display_welcome_message()

    while True:
        user_question = input("Student: ").strip()

        if user_question == "":
            print("Bot: Please type a question.")
            print()
            continue

        if user_question.lower() == "exit":
            print("Bot: Goodbye! Keep practicing daily.")
            break

        predicted_label, confidence = predict_label(
            user_question,
            training_examples
        )

        bot_response = get_response(predicted_label)

        print(f"Predicted Category: {predicted_label}")
        print(f"Confidence Score: {confidence}%")
        print(f"Bot: {bot_response}")
        print(RESPONSIBLE_AI_NOTE)
        print()

        save_chat_history(
            user_question=user_question,
            predicted_label=predicted_label,
            confidence=confidence,
            bot_response=bot_response
        )


def main():
    """
    Main function controls the complete program flow.

    Steps:
    1. Load training data
    2. Start chatbot
    3. Accept student questions
    4. Predict category
    5. Display answer
    6. Save chat history
    """

    print("Loading training data...")

    training_examples = load_training_data(TRAINING_DATA_FILE)

    print(f"Loaded {len(training_examples)} training examples.")
    print("AI Study Buddy is ready!")
    print()

    run_chatbot(training_examples)


if __name__ == "__main__":
    main()