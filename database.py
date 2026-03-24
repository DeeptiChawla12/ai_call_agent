import sqlite3

def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        ai TEXT,
        time TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_log(user, ai, time):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO logs (user, ai, time) VALUES (?, ?, ?)", (user, ai, time))
    conn.commit()
    conn.close()

def save_appointment(name, date, time):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO appointments (name, date, time) VALUES (?, ?, ?)", (name, date, time))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT user, ai, time FROM logs ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

def get_appointments():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT name, date, time FROM appointments ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data