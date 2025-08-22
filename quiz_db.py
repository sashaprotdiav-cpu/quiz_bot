"""База данных для квиза (True/False).

Модуль предоставляет простые функции для работы с вопросами:

- init_db: создание таблиц в SQLite-базе
- add_question: добавление одного вопроса
- get_all_questions: выборка всех вопросов
- seed_base_questions: автоматическое базовое наполнение (3 вопроса)
- prompt_fill_db: интерактивное наполнение через консоль

"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_DB_PATH = str(Path(__file__).with_name("quiz.db"))


def _connect(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Создаёт подключение к базе данных.

    :param db_path: Путь к файлу базы данных. Если не указан, используется DEFAULT_DB_PATH.
    :return: Открытое подключение sqlite3.Connection
    """
    return sqlite3.connect(db_path or DEFAULT_DB_PATH)


def init_db(db_path: Optional[str] = None) -> None:
    """Инициализирует базу данных и создаёт таблицу вопросов, если её нет.

    Таблица `questions` хранит:
      - id INTEGER PRIMARY KEY
      - text TEXT NOT NULL
      - is_true INTEGER NOT NULL (0 или 1)

    :param db_path: Путь к файлу базы данных.
    :return: None
    """
    with _connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                is_true INTEGER NOT NULL CHECK (is_true IN (0, 1))
            )
            """
        )
        conn.commit()


def add_question(text: str, is_true: bool, db_path: Optional[str] = None) -> int:
    """Добавляет один вопрос в базу данных.

    :param text: Текст утверждения/вопроса (на который отвечают «правильно/неправильно»)
    :param is_true: Верный ли ответ для этого утверждения
    :param db_path: Путь к файлу базы данных
    :return: ID добавленной записи
    """
    with _connect(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO questions (text, is_true) VALUES (?, ?)",
            (text, 1 if is_true else 0),
        )
        conn.commit()
        return int(cursor.lastrowid)


def get_all_questions(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Возвращает список всех вопросов из базы данных.

    :param db_path: Путь к файлу базы данных
    :return: Список словарей вида {"id": int, "text": str, "is_true": bool}
    """
    with _connect(db_path) as conn:
        cursor = conn.execute("SELECT id, text, is_true FROM questions ORDER BY id ASC")
        rows = cursor.fetchall()
    return [
        {"id": int(row[0]), "text": str(row[1]), "is_true": bool(row[2])}
        for row in rows
    ]


def seed_base_questions(db_path: Optional[str] = None) -> None:
    """Добавляет три базовых вопроса, если таблица пустая.

    Вопросы примерные и предназначены для начального наполнения.

    :param db_path: Путь к файлу базы данных
    :return: None
    """
    with _connect(db_path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        if count > 0:
            return
    add_question("Париж — столица Франции.", True, db_path)
    add_question("2 + 2 = 5.", False, db_path)
    add_question("Земля вращается вокруг Солнца.", True, db_path)


def prompt_fill_db(db_path: Optional[str] = None) -> None:
    """Интерактивно наполняет базу: спрашивает текст и верность утверждения.

    Введите пустую строку для завершения. Для ответа на вопрос:
    - Введите "y"/"да"/"true" для «правильно»
    - Введите "n"/"нет"/"false" для «неправильно»

    :param db_path: Путь к файлу базы данных
    :return: None
    """
    init_db(db_path)
    while True:
        text = input("Введите текст утверждения (пусто — завершить): ").strip()
        if not text:
            break
        raw = input("Это утверждение верно? (y/n): ").strip().lower()
        is_true = raw in {"y", "yes", "да", "true", "истина", "1", "+"}
        add_question(text, is_true, db_path)
        print("Добавлено!\n")

if __name__ == '__main__':
    pass
    # Изучи модуль
    # Вызови тут функци на создание бд и добвления 3 базовых вопросов
