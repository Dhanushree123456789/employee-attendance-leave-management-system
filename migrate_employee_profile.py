import sqlite3
import os

def migrate_employee_profile():
    """Add employee profile columns to existing users table"""
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'attendance.db')

    if not os.path.exists(db_path):
        print("Database doesn't exist. Run init_db.py first.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if phone column already exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    # Add new columns if they don't exist
    if 'phone' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
        print("✓ Added phone column")

    if 'qualification' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN qualification TEXT")
        print("✓ Added qualification column")

    if 'experience' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN experience TEXT")
        print("✓ Added experience column")

    if 'job_role' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN job_role TEXT")
        print("✓ Added job_role column")

    conn.commit()
    conn.close()
    print("✓ Employee profile migration completed successfully!")

if __name__ == '__main__':
    migrate_employee_profile()
