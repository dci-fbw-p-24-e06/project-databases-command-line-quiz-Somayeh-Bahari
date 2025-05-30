# Command Line Quiz

In this project, you will create a quiz application that will allow users to test their knowledge on various topics. Also to enrich the topics and questions that are provided. The application will use command line input and output to communicate with the user.

#### Prerequisites:
- Basic SQL
- Command line input and output. 
- Using variables, operators and control flow structures, conditionals while loops.
- Use postgresql from python and query the database. 

By the end of this project, you will have gained experience in these areas and created a fully functional command line quiz application.


### Implementetion Feautures

1. The application will prompt the user with an initial menu where they can select to be tested on an existing topic or enter a new topic/new question or exit. 

2. If the user selects to be tested on an existing topic, the application will randomly select a specific number of questions (hardcoded in the code) from the corresponding table in the PostgreSQL database. Each question will be displayed one by one, along with a number of possible answers (3 to 6). The user will select the answer they believe is correct, and the application will move on to the next question. After the last question is answered, the user's total score will be displayed.

3. The questions will be stored and retrieved from the PostgreSQL database. For each main topic, there will be a separate table with entries for the module, submodule, difficulty level (1, 2, or 3), question, right answer, and 2-5 wrong answers. The choices will be displayed shuffled and the questions will be chosen in random.

4. If the user selects to add additional questions, they will choose the main topic, and a new table will be created. They will then be prompted to enter each field in sequence, including the question, the correct answer, and 2-5 wrong answers. Once all fields are entered, the user will have the option to store the question. If the topic already exists, the user can simply add questions to the existing table.

 
#### Extra Features (Optional):

- **Database Indexing**: Index columns such as `difficulty_level` for faster query performance if necessary.
- **Extend Features**: Add user management to allow users to create accounts and track their quiz progress over time.
- **Deploy**: Host the PostgreSQL server on a cloud platform and make the quiz available via a terminal or web interface.
- **Add graphical user interface**: Transform your application into a graphical user interface using any of Python's GUI applications such as Tkinter, PyGT, Kivy etc.

---

