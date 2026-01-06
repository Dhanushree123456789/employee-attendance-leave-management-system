import sqlite3
import os

def check_tables():
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'attendance.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    print("Tables in database:")
    for table in tables:
        print(f"  - {table}")

    if 'break_times' in tables:
        print("\n✓ break_times table exists!")
    else:
        print("\n✗ break_times table is missing!")

    conn.close()

if __name__ == '__main__':
    check_tables()
