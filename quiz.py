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

    # Sanitize topic name for table query
    selected_topic = f"quiz_{selected_topic.lower().replace(' ', '_')}"

    try:
        cur.execute(f"""
            SELECT question, correct_answer, wrong_answer1, wrong_answer2
            FROM {selected_topic}
            ORDER BY RANDOM() LIMIT 5
        """)
        questions = cur.fetchall()
    except Exception as e:
        print("Error loading questions:", e)
        return

    score = 0
    for i, (question, correct, *wrong) in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question}")

        # Display options
        options = [correct] + list(wrong)
        random.shuffle(options)

        for j, option in enumerate(options, 1):
            print(f"{j}. {option}")

        # Get user answer
        try:
            answer = int(input("Your answer: ")) - 1
            if options[answer] == correct:
                print(" Correct!")
                score += 1
            else:
                print(f"Wrong! Correct answer: {correct}")
        except (ValueError, IndexError):
            print("Invalid input, skipping question")

    print(f"\nYour final score: {score} out of {len(questions)}")


def add_question(conn):
    """Add a new question"""
    topic = input("Question topic (e.g., Movies, History, Geography): ").strip()

    # Create topic if not exists
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO quiz_topics (topic_name)
        VALUES (%s) 
        ON CONFLICT (topic_name) DO NOTHING
    """, (topic,))

    # Sanitize topic name for table query
    table_name = f"quiz_{topic.lower().replace(' ', '_')}"

    # Create the topic table if it doesn't exist
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            question TEXT,
            correct_answer TEXT,
            wrong_answer1 TEXT,
            wrong_answer2 TEXT
        )
    """)

    # Get question details
    question = input("Enter question: ")
    correct = input("Correct answer: ")
    wrong1 = input("Wrong answer 1: ")
    wrong2 = input("Wrong answer 2: ")

    # Save question
    cur.execute(f"""
        INSERT INTO {table_name} 
        (question, correct_answer, wrong_answer1, wrong_answer2)
        VALUES (%s, %s, %s, %s)
    """, (question, correct, wrong1, wrong2))

    conn.commit()
    print("Question added successfully!")


def main():
    conn = connect_db()
    if not conn:
        return

    cur = conn.cursor()

    # Create quiz_topics table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_topics (
            id SERIAL PRIMARY KEY,
            topic_name TEXT UNIQUE NOT NULL
        )
    """)

    # Insert default topics into quiz_topics table if they don't exist
    cur.execute("""
        INSERT INTO quiz_topics (topic_name) 
        VALUES ('science'), ('history'), ('geography'), ('sports'), ('movies')
        ON CONFLICT (topic_name) DO NOTHING
    """)

    conn.commit()

    while True:
        choice = show_menu()

        if choice == "1":
            take_quiz(conn)
        elif choice == "2":
            add_question(conn)
        elif choice == "3":
            break
        else:
            print("Please enter a valid option (1-3).")

    conn.close()
    print("Goodbye!")


if __name__ == "__main__":
    main()
