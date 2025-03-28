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

