import sqlite3

DATABASE = "database/tasks.db"

def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # -----------------------------
    # Tasks Table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        description TEXT,
        deadline TEXT,
        duration INTEGER,
        category TEXT,
        difficulty TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # -----------------------------
    # Commitments Table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS commitments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        start_time TEXT,
        end_time TEXT,
        category TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Database Created Successfully!")