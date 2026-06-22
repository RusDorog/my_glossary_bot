import sqlite3
import datetime

DB_NAME = "tarot_bot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            text TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_message(user_id, msg_type, text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO messages (user_id, type, text, created_at)
        VALUES (?, ?, ?, ?)
    ''', (user_id, msg_type, text, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()