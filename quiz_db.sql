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
VALUES 
('What is the capital of France?', 'Paris', 'London', 'Berlin'),
('What color is the sky?', 'Blue', 'Red', 'Yellow'),
('What is the boiling point of water?', '100°C', '0°C', '50°C'),
('Which planet is known as the Red Planet?', 'Mars', 'Earth', 'Venus'),
('What is the chemical symbol for water?', 'H2O', 'O2', 'CO2');

-- History Questions
CREATE TABLE IF NOT EXISTS quiz_history (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    wrong_answer1 TEXT NOT NULL,
    wrong_answer2 TEXT NOT NULL
);

INSERT INTO quiz_history (question, correct_answer, wrong_answer1, wrong_answer2)
VALUES
('Who was the first president of the United States?', 'George Washington', 'Thomas Jefferson', 'Abraham Lincoln'),
('In which year did World War II end?', '1945', '1939', '1950'),
('Who was the first man to step on the moon?', 'Neil Armstrong', 'Buzz Aldrin', 'Yuri Gagarin'),
('Which empire was known for its Colosseum?', 'Roman Empire', 'Ottoman Empire', 'Mongol Empire'),
('Who was the Queen of France during the French Revolution?', 'Marie Antoinette', 'Catherine de Medici', 'Elizabeth I');

-- Geography Questions
CREATE TABLE IF NOT EXISTS quiz_geography (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    wrong_answer1 TEXT NOT NULL,
    wrong_answer2 TEXT NOT NULL
);

INSERT INTO quiz_geography (question, correct_answer, wrong_answer1, wrong_answer2)
VALUES
('What is the largest country by area?', 'Russia', 'Canada', 'China'),
('Which continent is the Sahara Desert located on?', 'Africa', 'Asia', 'Australia'),
('What is the longest river in the world?', 'Nile', 'Amazon', 'Yangtze'),
('Which mountain is the highest on Earth?', 'Mount Everest', 'K2', 'Kangchenjunga'),
('What is the capital of Japan?', 'Tokyo', 'Seoul', 'Beijing');

-- Sports Questions
CREATE TABLE IF NOT EXISTS quiz_sports (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    wrong_answer1 TEXT NOT NULL,
    wrong_answer2 TEXT NOT NULL
);

INSERT INTO quiz_sports (question, correct_answer, wrong_answer1, wrong_answer2)
VALUES
('Who won the FIFA World Cup in 2018?', 'France', 'Brazil', 'Germany'),
('Which country is known for inventing cricket?', 'England', 'Australia', 'India'),
('How many players are there in a standard football team?', '11', '9', '12'),
('In which year did Michael Jordan retire for the first time?', '1993', '1998', '2000'),
('Who holds the record for the most Olympic gold medals?', 'Michael Phelps', 'Usain Bolt', 'Carl Lewis');

-- Movies Questions
CREATE TABLE IF NOT EXISTS quiz_movies (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    wrong_answer1 TEXT NOT NULL,
    wrong_answer2 TEXT NOT NULL
);

INSERT INTO quiz_movies (question, correct_answer, wrong_answer1, wrong_answer2)
VALUES
('Who directed the movie "Jaws"?', 'Steven Spielberg', 'George Lucas', 'Martin Scorsese'),
('In what year was the first "Star Wars" movie released?', '1977', '1980', '1975'),
('Which actor played Jack Dawson in Titanic?', 'Leonardo DiCaprio', 'Johnny Depp', 'Brad Pitt'),
('What is the name of the fictional African country in "Black Panther"?', 'Wakanda', 'Zamunda', 'Genovia'),
('Who played the character of Harry Potter in the film series?', 'Daniel Radcliffe', 'Rupert Grint', 'Emma Watson');