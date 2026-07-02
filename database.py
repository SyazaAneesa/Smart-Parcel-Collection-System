import sqlite3
import os

DATABASE = "database.db"

UPLOAD_FOLDER = "static/profile_pics"
QR_FOLDER = "static/qr_codes"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

def create_connection():
    return sqlite3.connect(DATABASE)


def create_tables():
    conn = create_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            username TEXT PRIMARY KEY,
            student_id TEXT UNIQUE,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            password TEXT,
            profile_pic_path TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS parcels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_username TEXT,
            tracking_number TEXT,
            courier TEXT,
            arrival_date TEXT,
            quantity INTEGER,
            payment_status TEXT DEFAULT 'Unpaid',
            collection_status TEXT DEFAULT 'Not Collected',
            qr_code TEXT,
            FOREIGN KEY (student_username) REFERENCES students(username)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            staff_id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_username TEXT,
            question TEXT NOT NULL,
            answer TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            answered_at TEXT
        )
    """)

    c.execute("""
        INSERT OR IGNORE INTO staff (staff_id, username, password)
        VALUES (?, ?, ?)
    """, ("S001", "admin", "admin123"))

    conn.commit()
    conn.close()

    print("Database setup completed successfully.")


if __name__ == "__main__":
    create_tables()