import tkinter as tk
from tkinter import messagebox
import psycopg2
import random

# Connect to the database


def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="quiz_db",
            user="somayeh",
            password="2020",
            host="localhost"
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

# Start the quiz


def start_quiz(selected_topic):
    global current_question, current_options, correct_answer, score, correct_answers, incorrect_answers, question_count
    if selected_topic is None:
        messagebox.showerror("Error", "Please select a topic first.")
        return

    selected_topic_label.config(text=f"Selected Topic: {selected_topic}")

    # Show quiz frame and hide the main menu
    menu_frame.pack_forget()
    quiz_frame.pack()

    # Reset scores and question count
    score = 0
    correct_answers = 0
    incorrect_answers = 0
    question_count = 0  # Reset question count

    # Load the first question
    load_question(selected_topic)

# Load a new question


def load_question(selected_topic):
    global current_question, current_options, correct_answer, question_count
    if question_count >= 5:
        show_results()
        return

    cur = conn.cursor()

    # Sanitize topic name for table query
    selected_topic_sanitized = f"quiz_{selected_topic.lower().replace(' ', '_')}"

    try:
        cur.execute(f"""
            SELECT question, correct_answer, wrong_answer1, wrong_answer2
            FROM {selected_topic_sanitized}
            ORDER BY RANDOM() LIMIT 1
        """)
        question_data = cur.fetchone()
        if question_data:
            question, correct_answer, wrong1, wrong2 = question_data
            current_question = question
            current_options = [correct_answer, wrong1, wrong2]
            random.shuffle(current_options)

            question_label.config(text=question)

            # Update button options
            option1_button.config(text=current_options[0])
            option2_button.config(text=current_options[1])
            option3_button.config(text=current_options[2])

            # Enable the answer buttons
            option1_button.config(state=tk.NORMAL)
            option2_button.config(state=tk.NORMAL)
            option3_button.config(state=tk.NORMAL)

            feedback_label.config(text="")
    except Exception as e:
        print("Error loading question:", e)

# Check the answer


def check_answer(selected_option):
    global score, correct_answers, incorrect_answers, question_count
    if current_options[selected_option] == correct_answer:
        feedback_label.config(text="Correct!", fg="green")
        correct_answers += 1
        score += 1
    else:
        feedback_label.config(text=f"Wrong! Correct answer: {correct_answer}", fg="red")
        incorrect_answers += 1

    # Disable the answer buttons after an answer is selected
    option1_button.config(state=tk.DISABLED)
    option2_button.config(state=tk.DISABLED)
    option3_button.config(state=tk.DISABLED)

    # Increment question count and load next question after a delay
    question_count += 1
    window.after(1000, load_question, selected_topic)

# Show the final score


def show_results():
    quiz_frame.pack_forget()
    result_label.config(text=f"Quiz Complete!\nCorrect Answers: {correct_answers}\nIncorrect Answers: {incorrect_answers}")
    result_frame.pack()

# Setup the main window


window = tk.Tk()
window.title("Quiz Game")
window.geometry("500x400")

# Connect to the database
conn = connect_db()
if not conn:
    messagebox.showerror("Error", "Failed to connect to the database.")
    exit()

# Global variables
score = 0
correct_answers = 0
incorrect_answers = 0
selected_topic = None
current_question = None
current_options = None
correct_answer = None
question_count = 0

# Main menu frame
menu_frame = tk.Frame(window)

# Header for the quiz
header_label = tk.Label(menu_frame, text="Welcome to the Quiz Game", font=("Arial", 24))
header_label.pack(pady=20)

# Topic selection label
selected_topic_label = tk.Label(menu_frame, text="Select a Topic", font=("Arial", 14))
selected_topic_label.pack()

# Function to show topic selection


def show_topic_selection():
    menu_frame.pack_forget()
    topic_frame.pack()

# Start quiz button


start_button = tk.Button(menu_frame, text="Start Quiz", font=("Arial", 14), command=show_topic_selection)
start_button.pack(pady=20)

# Pack the main menu frame first
menu_frame.pack()

# Topic selection frame
topic_frame = tk.Frame(window)


def start_quiz_from_topic(topic):
    global selected_topic
    selected_topic = topic
    start_quiz(selected_topic)

# Get available topics from the database


cur = conn.cursor()
cur.execute("SELECT topic_name FROM quiz_topics")
topics = [row[0] for row in cur.fetchall()]

for topic in topics:
    topic_button = tk.Button(topic_frame, text=topic, font=("Arial", 14), command=lambda t=topic: start_quiz_from_topic(t))
    topic_button.pack(pady=10)

# Back to menu button in topic selection frame
back_button = tk.Button(topic_frame, text="Back to Menu", font=("Arial", 14), command=show_topic_selection)
back_button.pack(pady=20)

# Quiz frame
quiz_frame = tk.Frame(window)

# Label for questions
question_label = tk.Label(quiz_frame, text="", font=("Arial", 14), wraplength=400)
question_label.pack(pady=10)

# Option buttons
option1_button = tk.Button(quiz_frame, text="", font=("Arial", 12), command=lambda: check_answer(0))
option1_button.pack(pady=5)

option2_button = tk.Button(quiz_frame, text="", font=("Arial", 12), command=lambda: check_answer(1))
option2_button.pack(pady=5)

option3_button = tk.Button(quiz_frame, text="", font=("Arial", 12), command=lambda: check_answer(2))
option3_button.pack(pady=5)

# Feedback label
feedback_label = tk.Label(quiz_frame, text="", font=("Arial", 12))
feedback_label.pack(pady=10)

# Result frame
result_frame = tk.Frame(window)

# Result label
result_label = tk.Label(result_frame, text="", font=("Arial", 16))
result_label.pack(pady=20)

# Back to menu button in result frame
back_button_result = tk.Button(result_frame, text="Back to Menu", font=("Arial", 14), command=lambda: window.quit())
back_button_result.pack(pady=20)

# Start the Tkinter main loop
window.mainloop()
