# Employee Attendance and Leave Management System

![System Banner](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents
- [Problem Statement](#problem-statement)
- [System Features](#system-features)
- [Technology Stack](#technology-stack)
- [Database Design](#database-design)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Screenshots](#screenshots)
- [Project Structure](#project-structure)
- [Security Features](#security-features)
- [Future Enhancements](#future-enhancements)

## 🎯 Problem Statement

Many organizations still rely on manual registers, spreadsheets, or disconnected tools to track employee attendance and manage leave requests. This often results in data inconsistency, approval delays, and lack of visibility for HR teams.

This project addresses these challenges by providing a centralized, role-based system that automates attendance marking, leave approvals, and reporting, improving accuracy, efficiency, and transparency. This system provides a comprehensive solution for:

- **Employees**: Easy attendance marking and leave application submission
- **HR/Admin**: Centralized monitoring, approval workflows, and reporting capabilities
- **Organization**: Data-driven insights for workforce management

## ✨ System Features

### 🔐 Authentication & Authorization
- **Secure Login System**: SHA-256 password hashing
- **Role-Based Access Control (RBAC)**: Separate interfaces for Employees and Admins
- **Session Management**: Secure session handling with timeout
- **Access Control**: Route protection and unauthorized access prevention

### 👤 Employee Module
- **Personal Dashboard**: Overview of attendance and leave status
- **Attendance Management**:
  - Mark daily attendance (Present/Absent)
  - One-time daily entry with duplicate prevention
  - Real-time status updates
- **Attendance History**: 
  - Date-wise attendance records
  - Monthly filtering
  - Exportable reports
- **Leave Application**:
  - Apply for Sick/Casual/Annual leave
  - Date range selection with validation
  - Detailed reason submission
- **Leave Tracking**:
  - View application status (Pending/Approved/Rejected)
  - Admin remarks visibility
  - Application history

### 👨‍💼 Admin/HR Module
- **Comprehensive Dashboard**:
  - Total employees count
  - Daily attendance statistics (Present/Absent/Not Marked)
  - Pending leave requests counter
  - Recent activity feed
- **Employee Management**:
  - View all employees
  - Employee details and statistics
  - Search and filter capabilities
- **Attendance Monitoring**:
  - Daily attendance records
  - Date-wise filtering
  - Employee-wise tracking
- **Leave Management**:
  - Approve/Reject leave requests
  - Add administrative remarks
  - Status-wise filtering (Pending/Approved/Rejected)
- **Reports & Analytics**:
  - **Attendance Reports**: Monthly summary per employee with attendance rate
  - **Leave Reports**: Annual leave usage breakdown by type
  - Export to CSV functionality
  - Print-ready formats

### 📊 Reports & Data Visualization
- Monthly attendance summaries with percentage calculations
- Leave usage analysis by type (Sick/Casual/Annual)
- Attendance rate visualization
- Exportable data for further analysis

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **JavaScript (ES6+)**: Dynamic interactions and AJAX requests
- **Font Awesome 6**: Professional icons

### Backend
- **Python 3.8+**: Core programming language
- **Flask 2.3.3**: Lightweight web framework
- **SQLite3**: Embedded database (included with Python)

### Design
- **Figma**: UI/UX design prototyping (design concepts included)
- **Responsive Design**: Mobile-first approach

## 🗄️ Database Design

### Entity Relationship Diagram

```
┌─────────────┐         ┌─────────────┐
│   roles     │◄───────┐│    users    │
├─────────────┤        │├─────────────┤
│ role_id PK  │        ││ user_id PK  │
│ role_name   │        ││ username    │
│ description │        ││ password    │
└─────────────┘        ││ full_name   │
                       ││ email       │
                       ││ role_id FK  │
                       ││ date_joined │
                       ││ is_active   │
                       │└─────────────┘
                       │       │
                       │       │
        ┌──────────────┤       ├──────────────┐
        │              │       │              │
        ▼              │       ▼              │
┌─────────────┐       │ ┌─────────────┐      │
│ attendance  │       │ │leave_requests│      │
├─────────────┤       │ ├─────────────┤      │
│attendance_idPK      │ │ leave_id PK │      │
│ user_id FK  │◄──────┘ │ user_id FK  │◄─────┘
│attendance_dt│         │ leave_type  │
│ status      │         │ start_date  │
│ marked_at   │         │ end_date    │
│ remarks     │         │ reason      │
└─────────────┘         │ status      │
                        │ applied_at  │
                        │ reviewed_by │
                        │admin_remarks│
                        └─────────────┘
```

### Tables Structure

#### 1. **roles**
- `role_id` (INTEGER, PRIMARY KEY): Unique role identifier
- `role_name` (TEXT, UNIQUE): Role name (Admin/Employee)
- `description` (TEXT): Role description

#### 2. **users**
- `user_id` (INTEGER, PRIMARY KEY): Unique user identifier
- `username` (TEXT, UNIQUE): Login username
- `password` (TEXT): Hashed password (SHA-256)
- `full_name` (TEXT): Employee full name
- `email` (TEXT, UNIQUE): Email address
- `role_id` (INTEGER, FOREIGN KEY): References roles table
- `date_joined` (DATE): Account creation date
- `is_active` (INTEGER): Account status (1=active, 0=inactive)

#### 3. **attendance**
- `attendance_id` (INTEGER, PRIMARY KEY): Unique attendance record ID
- `user_id` (INTEGER, FOREIGN KEY): References users table
- `attendance_date` (DATE): Date of attendance
- `status` (TEXT): Present/Absent
- `marked_at` (TIMESTAMP): Timestamp of marking
- `remarks` (TEXT): Optional notes
- **UNIQUE CONSTRAINT**: (user_id, attendance_date) - Prevents duplicate entries

#### 4. **leave_requests**
- `leave_id` (INTEGER, PRIMARY KEY): Unique leave request ID
- `user_id` (INTEGER, FOREIGN KEY): References users table
- `leave_type` (TEXT): Sick/Casual/Annual
- `start_date` (DATE): Leave start date
- `end_date` (DATE): Leave end date
- `reason` (TEXT): Reason for leave
- `status` (TEXT): Pending/Approved/Rejected
- `applied_at` (TIMESTAMP): Application timestamp
- `reviewed_by` (INTEGER, FOREIGN KEY): Admin user ID
- `reviewed_at` (TIMESTAMP): Review timestamp
- `admin_remarks` (TEXT): Admin comments

### Database Constraints & Validations

- **Primary Keys**: Auto-incrementing for all tables
- **Foreign Keys**: Enforced referential integrity
- **Unique Constraints**: Prevent duplicate attendance and duplicate usernames/emails
- **Check Constraints**: 
  - Status values limited to defined options
  - Leave types restricted to Sick/Casual/Annual
- **Default Values**: Automatic timestamps and status values

## 💻 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step-by-Step Installation

1. **Extract the ZIP file**
   ```bash
   unzip attendance-system.zip
   cd attendance-system
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python database/init_db.py
   ```
   
   This will create the SQLite database and populate it with:
   - Default admin account
   - Sample employee accounts
   - Role definitions

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the system**
   - Open your browser and navigate to: `http://localhost:5000`
   - The login page will appear

### Default Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Employee Accounts:**
- Username: `john.doe` | Password: `emp123`
- Username: `jane.smith` | Password: `emp123`
- Username: `mike.johnson` | Password: `emp123`

## 📖 Usage Guide

### For Employees

1. **Login**: Use your credentials to access the employee dashboard
2. **Mark Attendance**: Click "Mark Present" or "Mark Absent" on the dashboard
3. **View History**: Navigate to "Attendance History" to see your records
4. **Apply for Leave**: 
   - Go to "Apply for Leave"
   - Select leave type, dates, and provide reason
   - Submit application
5. **Check Status**: View leave application status in "Leave Status"

### For Administrators

1. **Login**: Use admin credentials
2. **Dashboard Overview**: View real-time statistics
3. **Monitor Attendance**: Check daily attendance records
4. **Manage Leaves**: 
   - View pending requests
   - Approve or reject with remarks
5. **Generate Reports**:
   - Attendance Report: Monthly employee attendance
   - Leave Report: Annual leave usage
   - Export to CSV for further analysis

## 📁 Project Structure

```
attendance-system/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── database/
│   ├── init_db.py             # Database initialization script
│   └── attendance.db          # SQLite database (created after init)
│
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet (12KB+)
│   ├── js/
│   │   └── script.js          # JavaScript functions (12KB+)
│   └── images/
│       └── (placeholder for images)
│
└── templates/
    ├── base.html              # Base template
    ├── login.html             # Login page
    │
    ├── employee_dashboard.html     # Employee main dashboard
    ├── attendance_history.html     # Attendance records
    ├── apply_leave.html           # Leave application form
    ├── leave_status.html          # Leave status tracking
    │
    ├── admin_dashboard.html       # Admin main dashboard
    ├── view_employees.html        # Employee directory
    ├── view_attendance.html       # Daily attendance view
    ├── manage_leaves.html         # Leave management
    ├── attendance_report.html     # Attendance analytics
    ├── leave_report.html          # Leave analytics
    │
    ├── 404.html                   # Not found error
    └── 500.html                   # Server error
```

## 🔒 Security Features

1. **Password Security**:
   - SHA-256 hashing for password storage
   - No plain-text passwords in database

2. **Session Management**:
   - Secure session handling
   - Session timeout on inactivity
   - Logout functionality

3. **Access Control**:
   - Decorator-based route protection
   - Role-based authorization
   - Unauthorized access prevention

4. **Input Validation**:
   - Server-side validation for all inputs
   - SQL injection prevention (parameterized queries)
   - XSS protection (template escaping)
   - Date validation to prevent past/invalid dates

5. **Error Handling**:
   - Custom error pages (404, 500)
   - Graceful error messages
   - No sensitive information in error messages

## 🎨 UI/UX Design Features

- **Professional Corporate Theme**: Clean and modern interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Intuitive Navigation**: Easy-to-use sidebar and top navigation
- **Visual Feedback**: Loading states, success/error messages
- **Color-Coded Status**: Green for success, red for errors, yellow for warnings
- **Data Visualization**: Progress bars, badges, and statistics cards
- **Accessibility**: Semantic HTML, proper labels, keyboard navigation

## 🚀 Future Enhancements

- [ ] Email notifications for leave approvals/rejections
- [ ] Biometric integration for attendance
- [ ] Multiple location support
- [ ] Shift management
- [ ] Holiday calendar integration
- [ ] Advanced analytics and dashboards
- [ ] Mobile application
- [ ] Bulk user import/export
- [ ] Department-wise reporting
- [ ] API for third-party integrations

## 📄 License

This project is provided for educational and commercial use. Feel free to modify and distribute.

## 👨‍💻 Developer Notes

### Code Quality
- **Clean Code**: Well-organized, readable code with meaningful names
- **Comments**: Business logic explained with inline comments
- **Modular Design**: Reusable functions and components
- **Error Handling**: Comprehensive try-catch blocks

### Testing Recommendations
- Test all authentication flows
- Verify role-based access control
- Test duplicate attendance prevention
- Validate date selection logic
- Check report generation accuracy

### Deployment Considerations
- Change `app.secret_key` in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Set `debug=False` in app.run()
- Consider PostgreSQL/MySQL for production database
- Implement proper logging

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify database is initialized
