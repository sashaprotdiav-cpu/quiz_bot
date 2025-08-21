import sqlite3

def init_db():
    conn = sqlite3.connect("quiz.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        score INTEGER
    )""")
    conn.commit()
    conn.close()

def get_user_score(username):
    conn = sqlite3.connect("quiz.db")
    c = conn.cursor()
    c.execute("SELECT score FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def add_score(username, value):
    conn = sqlite3.connect("quiz.db")
    c = conn.cursor()
    score = get_user_score(username) + value
    c.execute("REPLACE INTO users (username, score) VALUES (?, ?)", (username, score))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
