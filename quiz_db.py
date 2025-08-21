"""Простой модуль/скрипт для хранения вопросов квиза в SQLite.

Таблицы:
- questions(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT UNIQUE NOT NULL)
- answers(id INTEGER PRIMARY KEY AUTOINCREMENT, question_id INTEGER NOT NULL, text TEXT NOT NULL, score INTEGER NOT NULL CHECK(score IN (0,1)))

Использование (как скрипт):
просто запустите файл, он попросит ввести вопрос и варианты, затем выведет все вопросы.
"""

import sqlite3


DB_NAME = "quiz.db"


def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            score INTEGER NOT NULL CHECK(score IN (0,1)),
            FOREIGN KEY(question_id) REFERENCES questions(id) ON DELETE CASCADE
        )
        """
    )

    connection.commit()
    connection.close()


def add_question(question_text, answers):
    """Добавляет вопрос и варианты.

    question_text: str
    answers: список кортежей (text, score), где score 0 или 1
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("INSERT INTO questions(text) VALUES (?)", (question_text,))
    qid = cursor.lastrowid

    for text, score in answers:
        cursor.execute(
            "INSERT INTO answers(question_id, text, score) VALUES (?, ?, ?)",
            (qid, text, int(score)),
        )

    connection.commit()
    connection.close()


def get_question_with_answers(question_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    q = cursor.execute("SELECT text FROM questions WHERE id=?", (question_id,)).fetchone()
    a = cursor.execute("SELECT text, score FROM answers WHERE question_id=?", (question_id,)).fetchall()

    connection.close()
    return q[0] if q else None, a


def show_all_questions():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    rows = cursor.execute("SELECT id, text FROM questions ORDER BY id").fetchall()
    print(rows)
    connection.close()
    return rows


def add_question_interactive():
    question = input("Введите текст вопроса: ").strip()
    num = int(input("Сколько вариантов (>=2): ").strip())
    answers = []
    for i in range(num):
        text = input(f"Вариант #{i+1}: ").strip()
        correct = input("Правильный? (y/n): ").strip().lower() in ("y", "yes", "д", "да")
        answers.append((text, 1 if correct else 0))
    add_question(question, answers)


if __name__ == "__main__":
    init_db()
    add_question_interactive()
    show_all_questions()



