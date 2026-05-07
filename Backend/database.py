import sqlite3

def connect_db():
    return sqlite3.connect("food.db")


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # ✅ USERS TABLE (MISSING BEFORE — THIS CAUSED ERROR)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # ✅ FOOD TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        quantity TEXT,
        location TEXT,
        expiry TEXT,
        lat REAL,
        lng REAL
    )
    """)

    # ✅ REQUEST TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_id INTEGER,
        ngo_name TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


# ✅ CALL FUNCTION
create_tables()