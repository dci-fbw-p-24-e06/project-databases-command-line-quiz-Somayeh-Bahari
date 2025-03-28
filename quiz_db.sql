CREATE DATABASE quiz_db;

CREATE TABLE quiz_topics (
    id SERIAL PRIMARY KEY,
    topic_name TEXT UNIQUE NOT NULL
);

CREATE TABLE quiz_science (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    wrong_answer1 TEXT NOT NULL,
    wrong_answer2 TEXT NOT NULL
);

INSERT INTO quiz_science (question, correct_answer, wrong_answer1, wrong_answer2)
VALUES ('What is the capital of France?', 'Paris', 'London', 'Berlin');
