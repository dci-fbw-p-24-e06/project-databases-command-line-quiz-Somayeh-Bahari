import psycopg2
import random


def connect_db():
    """Connect to PostgreSQL database"""
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


def show_menu():
    """Display main menu"""
    print("\nMain Menu:")
    print("1. Start Quiz")
    print("2. Add New Question")
    print("3. Exit")
    return input("Please enter your choice: ")


def take_quiz(conn):
    """Start a new quiz"""
    cur = conn.cursor()

    # Get available topics
    cur.execute("SELECT topic_name FROM quiz_topics")
    topics = [row[0] for row in cur.fetchall()]

    if not topics:
        print("No topics available. Please add questions first.")
        return

    print("\nAvailable Topics:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic}")

    try:
        choice = int(input("Select a topic: ")) - 1
        selected_topic = topics[choice]
    except (ValueError, IndexError):
        print("Invalid selection")
        return

    
