"""
Database Initialization Script
Creates all necessary tables with proper relationships and constraints
"""

import os
import sqlite3
import hashlib
from datetime import datetime

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """Initialize the database with all required tables"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'attendance.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Roles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role_id INTEGER NOT NULL,
            date_joined DATE DEFAULT CURRENT_DATE,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (role_id) REFERENCES roles(role_id)
        )
    ''')
    
    # Create Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            attendance_date DATE NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
            marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            remarks TEXT,
            UNIQUE(user_id, attendance_date),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Create Leave Requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leave_requests (
            leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            leave_type TEXT NOT NULL CHECK(leave_type IN ('Sick', 'Casual', 'Annual')),
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            reason TEXT NOT NULL,
            status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Rejected')),
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reviewed_by INTEGER,
            reviewed_at TIMESTAMP,
            admin_remarks TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (reviewed_by) REFERENCES users(user_id)
        )
    ''')

    # Create Holidays table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holidays (
            holiday_id INTEGER PRIMARY KEY AUTOINCREMENT,
            holiday_date DATE NOT NULL UNIQUE,
            holiday_name TEXT NOT NULL,
            description TEXT,
            created_by INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(user_id)
        )
    ''')

    # Create Break Times table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS break_times (
            break_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            attendance_date DATE NOT NULL,
            break_in_time TIMESTAMP,
            break_out_time TIMESTAMP,
            break_duration INTEGER, -- Duration in minutes
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, attendance_date, break_in_time)
        )
    ''')
    
    # Insert default roles
    cursor.execute("INSERT OR IGNORE INTO roles (role_name, description) VALUES ('Admin', 'Administrator with full access')")
    cursor.execute("INSERT OR IGNORE INTO roles (role_name, description) VALUES ('Employee', 'Regular employee with limited access')")
    
    # Insert default admin user (username: admin, password: admin123)
    admin_password = hash_password('admin123')
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, full_name, email, role_id) 
        VALUES ('admin', ?, 'System Administrator', 'admin@company.com', 1)
    """, (admin_password,))
    
    # Insert sample employees for testing
    emp1_password = hash_password('emp123')
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, full_name, email, role_id) 
        VALUES ('john.doe', ?, 'John Doe', 'john.doe@company.com', 2)
    """, (emp1_password,))
    
    emp2_password = hash_password('emp123')
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, full_name, email, role_id) 
        VALUES ('jane.smith', ?, 'Jane Smith', 'jane.smith@company.com', 2)
    """, (emp2_password,))
    
    emp3_password = hash_password('emp123')
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, full_name, email, role_id) 
        VALUES ('mike.johnson', ?, 'Mike Johnson', 'mike.johnson@company.com', 2)
    """, (emp3_password,))
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully!")
    print("\nDefault Credentials:")
    print("Admin - Username: admin, Password: admin123")
    print("Employee - Username: john.doe, Password: emp123")
    print("Employee - Username: jane.smith, Password: emp123")
    print("Employee - Username: mike.johnson, Password: emp123")

if __name__ == '__main__':
    init_database()
