#!/usr/bin/env python3
"""
Test script for time-based attendance functionality
"""
import sqlite3
import os
from datetime import datetime, date

def get_db_connection():
    """Get database connection"""
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'attendance.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def test_mark_absent_for_day():
    """Test the mark_absent_for_day functionality"""
    print("Testing mark_absent_for_day functionality...")

    today = date.today().isoformat()
    now = datetime.now().isoformat()

    conn = get_db_connection()

    # Get all active employees
    all_employees = conn.execute('SELECT user_id, full_name FROM users WHERE role_id = 2 AND is_active = 1').fetchall()
    print(f"Total active employees: {len(all_employees)}")

    # Get employees who have already marked attendance today
    marked_employees = conn.execute('SELECT user_id FROM attendance WHERE attendance_date = ?', (today,)).fetchall()
    marked_user_ids = {emp['user_id'] for emp in marked_employees}
    print(f"Employees who marked attendance today: {len(marked_user_ids)}")

    # Mark absent for employees who haven't marked
    absent_count = 0
    for employee in all_employees:
        if employee['user_id'] not in marked_user_ids:
            print(f"Would mark {employee['full_name']} as absent")
            absent_count += 1

    print(f"Would mark {absent_count} employees as absent for today")
    conn.close()

    return absent_count

def test_time_check():
    """Test the time checking logic"""
    print("\nTesting time check logic...")

    now = datetime.now()
    print(f"Current time: {now}")
    print(f"Current hour: {now.hour}")

    if now.hour >= 19:  # 19:00 is 7 PM
        print("After 7 PM - would mark as Absent")
    else:
        print("Before 7 PM - normal attendance marking allowed")

if __name__ == "__main__":
    test_time_check()
    test_mark_absent_for_day()
    print("\nTest completed successfully!")
