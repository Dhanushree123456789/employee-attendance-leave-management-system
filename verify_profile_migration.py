import sqlite3
import os

def verify_profile_migration():
    """Verify that the employee profile columns were added correctly"""
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'attendance.db')

    if not os.path.exists(db_path):
        print("❌ Database doesn't exist")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check users table schema
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()

    print("Users table schema:")
    column_names = [col[1] for col in columns]
    print(f"Columns: {', '.join(column_names)}")

    # Check for new columns
    required_columns = ['phone', 'qualification', 'experience', 'job_role']
    missing_columns = []

    for col in required_columns:
        if col not in column_names:
            missing_columns.append(col)

    if missing_columns:
        print(f"❌ Missing columns: {', '.join(missing_columns)}")
    else:
        print("✅ All required profile columns are present")

    # Check sample data
    cursor.execute("SELECT user_id, full_name, phone, qualification, experience, job_role FROM users WHERE role_id = 2 LIMIT 3")
    employees = cursor.fetchall()

    print(f"\nSample employee data ({len(employees)} employees):")
    for emp in employees:
        print(f"ID: {emp[0]}, Name: {emp[1]}, Phone: {emp[2] or 'Not set'}, Qualification: {emp[3] or 'Not set'}, Experience: {emp[4] or 'Not set'}, Job Role: {emp[5] or 'Not set'}")

    conn.close()

if __name__ == '__main__':
    verify_profile_migration()
