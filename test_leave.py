import sqlite3
import os

DATABASE = os.path.join('attendance-system', 'database', 'attendance.db')

conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check leave_requests with reviewer name
cursor.execute('''
    SELECT lr.*, u.full_name as reviewer_name
    FROM leave_requests lr
    LEFT JOIN users u ON lr.reviewed_by = u.user_id
''')
rows = cursor.fetchall()

print("Leave requests with reviewer names:")
for row in rows:
    print(f"ID: {row['leave_id']}, Status: {row['status']}, Reviewed By: {row['reviewer_name'] or '-'}")

conn.close()
