import sqlite3
import os

def migrate_database():
    """Add break_times table to existing database"""
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'attendance.db')

    if not os.path.exists(db_path):
        print("Database doesn't exist. Run init_db.py first.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if break_times table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='break_times'")
    if cursor.fetchone():
        print("✓ break_times table already exists")
        conn.close()
        return

    # Create break_times table
    cursor.execute('''
        CREATE TABLE break_times (
            break_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            attendance_date DATE NOT NULL,
            break_in_time TIMESTAMP,
            break_out_time TIMESTAMP,
            break_duration INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, attendance_date, break_in_time)
        )
    ''')

    conn.commit()
    conn.close()
    print("✓ break_times table created successfully!")

if __name__ == '__main__':
    migrate_database()
