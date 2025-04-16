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
    global current_question, current_options, correct_answer, score
    global correct_answers, incorrect_answers, question_count

    if selected_topic is None:
        messagebox.showerror("Error", "Please select a topic first.")
        return

    selected_topic_label.config(text=f"Selected Topic: {selected_topic}")

    menu_frame.pack_forget()
    quiz_frame.pack()

    score = 0
    correct_answers = 0
    incorrect_answers = 0
    question_count = 0

    load_question(selected_topic)

# Load a new question


def load_question(selected_topic):
    global current_question, current_options, correct_answer, question_count, timer_id

    if question_count >= 5:
        show_results()
        return

    cur = conn.cursor()
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

            option1_button.config(text=current_options[0], state=tk.NORMAL)
            option2_button.config(text=current_options[1], state=tk.NORMAL)
            option3_button.config(text=current_options[2], state=tk.NORMAL)

            feedback_label.config(text="")
            timer_label.config(text="Time left: 5s")

            start_timer()
    except Exception as e:
        print("Error loading question:", e)

# Start the timer


def start_timer():
    global time_left, timer_id
    time_left = 5
    update_timer()

# Update the timer display each second


def update_timer():
    global time_left, timer_id
    if time_left > 0:
        timer_label.config(text=f"Time left: {time_left}s")
        time_left -= 1
        timer_id = window.after(1000, update_timer)
    else:
        time_up()

# What to do when time runs out


def time_up():
    global incorrect_answers, question_count, timer_id
    feedback_label.config(text=f"Time's up! Correct answer: {correct_answer}", fg="orange")
    incorrect_answers += 1
    question_count += 1

    # Disable answer buttons
    option1_button.config(state=tk.DISABLED)
    option2_button.config(state=tk.DISABLED)
    option3_button.config(state=tk.DISABLED)

    timer_id = None
    window.after(2000, load_question, selected_topic)

# Check the selected answer


def check_answer(selected_option):
    global score, correct_answers, incorrect_answers, question_count, timer_id

    # Cancel the timer
    if timer_id is not None:
        window.after_cancel(timer_id)
        timer_id = None

    if current_options[selected_option] == correct_answer:
        feedback_label.config(text="Correct!", fg="green")
        correct_answers += 1
        score += 1
    else:
        feedback_label.config(text=f"Wrong! Correct answer: {correct_answer}", fg="red")
        incorrect_answers += 1

    # Disable buttons after selection
    option1_button.config(state=tk.DISABLED)
    option2_button.config(state=tk.DISABLED)
    option3_button.config(state=tk.DISABLED)

    question_count += 1
    window.after(2000, load_question, selected_topic)

# Show final results


def show_results():
    quiz_frame.pack_forget()
    result_label.config(text=f"Quiz Complete!\nCorrect Answers: {correct_answers}\nIncorrect Answers: {incorrect_answers}")
    result_frame.pack()

# Create the main window


window = tk.Tk()
window.title("Quiz Game")
window.geometry("500x500")

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
timer_id = None
time_left = 15

# Main menu frame
menu_frame = tk.Frame(window)
header_label = tk.Label(menu_frame, text="Welcome to the Quiz Game", font=("Arial", 24))
header_label.pack(pady=20)

selected_topic_label = tk.Label(menu_frame, text="Select a Topic", font=("Arial", 14))
selected_topic_label.pack()


def show_topic_selection():
    menu_frame.pack_forget()
    topic_frame.pack()


start_button = tk.Button(menu_frame, text="Start Quiz", font=("Arial", 14), command=show_topic_selection)
start_button.pack(pady=20)
menu_frame.pack()

# Topic selection frame
topic_frame = tk.Frame(window)


def start_quiz_from_topic(topic):
    global selected_topic
    selected_topic = topic
    topic_frame.pack_forget()
    start_quiz(selected_topic)


cur = conn.cursor()
cur.execute("SELECT topic_name FROM quiz_topics")
topics = [row[0] for row in cur.fetchall()]

for topic in topics:
    topic_button = tk.Button(topic_frame, text=topic, font=("Arial", 14), command=lambda t=topic: start_quiz_from_topic(t))
    topic_button.pack(pady=10)

back_button = tk.Button(topic_frame, text="Back to Menu", font=("Arial", 14), command=show_topic_selection)
back_button.pack(pady=20)

# Quiz frame
quiz_frame = tk.Frame(window)

question_label = tk.Label(quiz_frame, text="", font=("Arial", 14), wraplength=400)
question_label.pack(pady=10)

option1_button = tk.Button(quiz_frame, text="", font=("Arial", 12), command=lambda: check_answer(0))
option1_button.pack(pady=5)

option2_button = tk.Button(quiz_frame, text="", font=("Arial", 12), command=lambda: check_answer(1))
option2_button.pack(pady=5)

option3_button = tk.Button(quiz_frame, text="", font=("Arial", 12), command=lambda: check_answer(2))
option3_button.pack(pady=5)

feedback_label = tk.Label(quiz_frame, text="", font=("Arial", 12))
feedback_label.pack(pady=10)

timer_label = tk.Label(quiz_frame, text="Time left: 15s", font=("Arial", 12), fg="blue")
timer_label.pack(pady=5)

# Result frame
result_frame = tk.Frame(window)
result_label = tk.Label(result_frame, text="", font=("Arial", 16))
result_label.pack(pady=20)

back_button_result = tk.Button(result_frame, text="Exit", font=("Arial", 14), command=window.quit)
back_button_result.pack(pady=20)

# Start the Tkinter event loop
window.mainloop()