# E-Tech Technical College Student Management System

A comprehensive desktop-based Student Management System developed for **E-Tech Technical College** using **Python, Tkinter, and Microsoft SQL Server**. The system provides a centralized and user-friendly platform for managing important academic and administrative activities.

## Project Overview

The E-Tech Student Management System is designed to improve the efficiency of college administration by replacing manual record management with a computerized system. It provides role-based access and dedicated modules for managing students, lecturers, courses, batches, examinations, results, payments, assignments, and system users.

## Main Features

- **Student Management** – Add, update, delete, and view student records.
- **Lecturer Management** – Manage lecturer information and department details.
- **Course Management** – Maintain course information, duration, fees, and departments.
- **Batch Management** – Manage student batches and course schedules.
- **Exam Management** – Create and maintain examination records.
- **Result Management** – Record and manage student examination results and grades.
- **Payment Management** – Track course fees, payments, discounts, and outstanding balances.
- **Assignment Management** – Manage assignments, submissions, and late submissions.
- **User Management** – Manage system users and roles.
- **Role-Based Access** – Provides different access levels for Admin and Staff users.
- **Dashboard** – Displays key information and recent student records in an easy-to-use interface.
- **SQL Server Database** – Stores and manages the system's data using Microsoft SQL Server.

## Technologies Used

- **Python**
- **Tkinter** – Graphical User Interface
- **Microsoft SQL Server / LocalDB** – Database management
- **pyodbc** – Python database connectivity
- **Pillow (PIL)** – Image handling
- **tkcalendar** – Date selection
- **ReportLab** – PDF generation

## Project Files

```text
ETech-Student-Management-System/
├── main.py
├── db.py
├── ETech_Student_Management_System_Final.sql
├── bg.jpg
└── README.md
```

## Database

The SQL database script is included in:

`ETech_Student_Management_System_Final.sql`

The application is configured to connect to the SQL Server LocalDB database:

`ETech_Technical_College_db`

## How to Run

1. Install Python on your computer.
2. Install the required Python packages:

```bash
pip install pyodbc pillow tkcalendar reportlab
```

3. Install and configure Microsoft SQL Server LocalDB and the required ODBC driver.
4. Execute `ETech_Student_Management_System_Final.sql` in SQL Server to create the database and tables.
5. Keep `main.py`, `db.py`, and `bg.jpg` in the same project folder.
6. Open the project in Visual Studio Code or another Python IDE.
7. Run `main.py`.
8. Sign in using a valid user account created in the database.

## System Purpose

The main purpose of this project is to provide E-Tech Technical College with an organized, reliable, and easy-to-use system for handling student and academic information. By integrating a graphical interface with a relational SQL Server database, the system helps reduce manual work, improve data organization, and support efficient academic administration.

## Author

**Mohamed Irfan Mohamed Insaf**

Student Management System – E-Tech Technical College
