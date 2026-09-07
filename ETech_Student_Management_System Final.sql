CREATE DATABASE ETech_Technical_College_db;
GO

USE ETech_Technical_College_db;
GO

USE ETech_Technical_College_db;
GO

CREATE TABLE Department
(
    Department_ID INT PRIMARY KEY IDENTITY(1,1),
    Department_Name VARCHAR(100) NOT NULL
);

SELECT * FROM Department;
INSERT INTO Department (Department_Name)
VALUES
('Computing'),
('Business'),
('Engineering'),
('Hospitality'),
('English');

USE ETech_Technical_College_db;
GO

CREATE TABLE Course
(
    Course_ID INT PRIMARY KEY IDENTITY(1,1),
    Course_Name VARCHAR(100) NOT NULL,
    Duration VARCHAR(50),
    Department_ID INT NOT NULL,

    FOREIGN KEY (Department_ID)
    REFERENCES Department(Department_ID)
);

INSERT INTO Course (Course_Name, Duration, Department_ID)
VALUES
('Higher National Diploma in Computing', '2 Years', 1),
('Diploma in Business Management', '1 Year', 2),
('Higher National Diploma in Engineering', '2 Years', 3),
('Diploma in Hospitality Management', '1 Year', 4),
('English Language Course', '6 Months', 5);

SELECT * FROM Course;

USE ETech_Technical_College_db;
GO

CREATE TABLE Batch
(
    Batch_ID INT PRIMARY KEY IDENTITY(1,1),
    Batch_Name VARCHAR(100) NOT NULL,
    Start_Date DATE,
    End_Date DATE,
    Course_ID INT NOT NULL,

    FOREIGN KEY (Course_ID)
    REFERENCES Course(Course_ID)
);
INSERT INTO Batch (Batch_Name, Start_Date, End_Date, Course_ID)
VALUES
('HNDC-2026-A', '2026-01-15', '2027-12-15', 1),
('DBM-2026-A', '2026-02-01', '2027-01-31', 2),
('HNDE-2026-A', '2026-03-01', '2028-02-28', 3),
('DHM-2026-A', '2026-04-01', '2027-03-31', 4),
('ENG-2026-A', '2026-05-01', '2026-10-31', 5);

SELECT * FROM Batch;
USE ETech_Technical_College_db;
GO

CREATE TABLE Classroom
(
    Classroom_ID INT PRIMARY KEY IDENTITY(1,1),
    Room_No VARCHAR(20) NOT NULL,
    Location VARCHAR(100) NOT NULL
);
INSERT INTO Classroom (Room_No, Location)
VALUES
('A101', 'Ground Floor'),
('A102', 'Ground Floor'),
('B201', 'First Floor'),
('C301', 'Second Floor'),
('Lab01', 'Computer Laboratory');
SELECT * FROM Classroom;

USE ETech_Technical_College_db;
GO

CREATE TABLE Lecturer
(
    Lecturer_ID INT PRIMARY KEY IDENTITY(1,1),
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    Department_ID INT NOT NULL,

    FOREIGN KEY (Department_ID)
    REFERENCES Department(Department_ID)
);
INSERT INTO Lecturer
(First_Name, Last_Name, Email, Phone, Department_ID)
VALUES
('Nimal', 'Perera', 'nimal.perera@etech.edu', '0711234567', 1),
('Kamal', 'Silva', 'kamal.silva@etech.edu', '0722345678', 2),
('Sunil', 'Fernando', 'sunil.fernando@etech.edu', '0773456789', 3),
('Ayesha', 'Peris', 'ayesha.peris@etech.edu', '0764567890', 4),
('Dilani', 'Jayasinghe', 'dilani.j@etech.edu', '0755678901', 5);
SELECT * FROM Lecturer;

UPDATE Student
SET First_Name = 'Kasun'
WHERE Student_ID = 2;

USE ETech_Technical_College_db;
GO

DELETE FROM Student
WHERE Student_ID = 1;

CREATE TABLE Student
(
    Student_ID INT PRIMARY KEY IDENTITY(1,1),
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Gender VARCHAR(10),
    Date_Of_Birth DATE,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    Address VARCHAR(255),
    Batch_ID INT NOT NULL,

    FOREIGN KEY (Batch_ID)
    REFERENCES Batch(Batch_ID)
);

SELECT s.First_Name, c.Course_Name
FROM Student s
INNER JOIN Course c
ON c.Course_ID = c.Course_ID;

SELECT *
FROM Student
WHERE Student_ID = 1;

SELECT Student_ID, COUNT(*) AS StudentCount
FROM Student
GROUP BY Student_ID
HAVING COUNT(*) > 5;

SELECT Student_ID, COUNT(*) AS StudentCount
FROM Student
GROUP BY Student_ID;

SELECT *
FROM Student
ORDER BY First_Name ASC;

INSERT INTO Student
(First_Name, Last_Name, Gender, Date_Of_Birth, Email, Phone, Address, Batch_ID)
VALUES
('Kasun', 'Perera', 'Male', '2004-05-10', 'kasun.perera@gmail.com', '0712345678', 'Colombo', 1),
('Nadeesha', 'Silva', 'Female', '2003-09-22', 'nadeesha.silva@gmail.com', '0723456789', 'Kandy', 2),
('Sahan', 'Fernando', 'Male', '2004-01-15', 'sahan.fernando@gmail.com', '0774567890', 'Galle', 3),
('Ishara', 'Peris', 'Female', '2005-03-18', 'ishara.peris@gmail.com', '0765678901', 'Kurunegala', 4),
('Tharindu', 'Jayasinghe', 'Male', '2004-11-30', 'tharindu.j@gmail.com', '0756789012', 'Matara', 5);
SELECT * FROM Student;

ALTER TABLE Student
DROP COLUMN DOB;

USE ETech_Technical_College_db;
GO

CREATE TABLE Subject
(
    Subject_ID INT PRIMARY KEY IDENTITY(1,1),
    Subject_Name VARCHAR(100) NOT NULL,
    Credits INT NOT NULL,
    Course_ID INT NOT NULL,

    FOREIGN KEY (Course_ID)
    REFERENCES Course(Course_ID)
);
INSERT INTO Subject
(Subject_Name, Credits, Course_ID)
VALUES
('Programming Fundamentals', 4, 1),
('Database Systems', 4, 1),
('Business Communication', 3, 2),
('Engineering Mathematics', 4, 3),
('Hospitality Operations', 3, 4);
SELECT * FROM Subject;

USE ETech_Technical_College_db;
GO

CREATE TABLE Exam
(
    Exam_ID INT PRIMARY KEY IDENTITY(1,1),
    Exam_Name VARCHAR(100) NOT NULL,
    Exam_Date DATE NOT NULL,
    Subject_ID INT NOT NULL,

    FOREIGN KEY (Subject_ID)
    REFERENCES Subject(Subject_ID)
);
INSERT INTO Exam
(Exam_Name, Exam_Date, Subject_ID)
VALUES
('Programming Fundamentals Final', '2026-06-15', 1),
('Database Systems Mid', '2026-07-10', 2),
('Business Communication Final', '2026-08-05', 3),
('Engineering Mathematics Final', '2026-09-20', 4),
('Hospitality Operations Practical', '2026-10-12', 5);
SELECT * FROM Exam;

USE ETech_Technical_College_db;
GO

CREATE TABLE Student_Exam
(
    Student_Exam_ID INT PRIMARY KEY IDENTITY(1,1),
    Student_ID INT NOT NULL,
    Exam_ID INT NOT NULL,
    Marks DECIMAL(5,2),
    Grade VARCHAR(5),

    FOREIGN KEY (Student_ID)
    REFERENCES Student(Student_ID),

    FOREIGN KEY (Exam_ID)
    REFERENCES Exam(Exam_ID)
);
INSERT INTO Student_Exam
(Student_ID, Exam_ID, Marks, Grade)
VALUES
(1, 1, 85.50, 'A'),
(2, 2, 78.00, 'B+'),
(3, 3, 91.25, 'A+'),
(4, 4, 69.50, 'B'),
(5, 5, 88.75, 'A');
SELECT * FROM Student_Exam;

SELECT name
FROM sys.tables
ORDER BY name;

EXEC sp_help 'Student';

SELECT * FROM Batch

USE ETech_Technical_College_db;
GO

CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) UNIQUE,
    Password_Hash NVARCHAR(100) -- In production, store hash. Use plain text for assignment.
);

INSERT INTO Users (Username, Password_Hash) VALUES ('admin', 'admin');
GO

USE ETech_Technical_College_db;
GO

CREATE TABLE Users (
    Username NVARCHAR(50) PRIMARY KEY,
    Password_Hash NVARCHAR(50)
);

SELECT * FROM Users;

INSERT INTO Users (Username, Password_Hash) VALUES ('admin', 'admin');
GO

USE ETech_Technical_College_db;
GO

INSERT INTO Subject (Subject_Name, Credits, Course_ID) VALUES ('Python Programming', 4, 1);
GO

USE ETech_Technical_College_db;
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Student' AND COLUMN_NAME = 'First_Name')
BEGIN
    ALTER TABLE Student ADD First_Name VARCHAR(50);
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Student' AND COLUMN_NAME = 'Last_Name')
BEGIN
    ALTER TABLE Student ADD Last_Name VARCHAR(50);
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Student' AND COLUMN_NAME = 'DOB')
BEGIN
    ALTER TABLE Student ADD DOB DATE;
END
GO

UPDATE Student SET First_Name = 'Test' WHERE First_Name IS NULL;
UPDATE Student SET Last_Name = 'User' WHERE Last_Name IS NULL;
GO

USE ETech_Technical_College_db;
GO

DELETE FROM Student;
DELETE FROM Batch;
DELETE FROM Lecturer;
DELETE FROM Course;
DELETE FROM Department;
GO

INSERT INTO Department (Department_Name) VALUES 
('Computing'), 
('Business'), 
('Engineering'), 
('Hospitality'), 
('English');
GO

INSERT INTO Course (Course_Name, Duration, Department_ID) VALUES 
('HND in Computing', '2 Years', 1), 
('Diploma in Business', '1 Year', 2), 
('HND in Engineering', '2 Years', 3), 
('Diploma in Hospitality', '1 Year', 4), 
('English Course', '6 Months', 5);
GO

INSERT INTO Batch (Batch_Name, Start_Date, End_Date, Course_ID) VALUES 
('HNDC-2026-A', '2026-01-15', '2027-12-15', 1),
('DBM-2026-A', '2026-02-01', '2027-01-31', 2),
('HNDE-2026-A', '2026-03-01', '2028-02-28', 3),
('DHM-2026-A', '2026-04-01', '2027-03-31', 4),
('ENG-2026-A', '2026-05-01', '2026-10-31', 5);
GO

SELECT * FROM Batch

USE ETech_Technical_College_db;
GO
DROP TABLE IF EXISTS Student;
GO
CREATE TABLE Student (
    Student_ID INT PRIMARY KEY IDENTITY(1,1),
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Gender VARCHAR(10),
    Date_Of_Birth DATE,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    Address VARCHAR(255),
    Batch_ID INT NOT NULL,
    FOREIGN KEY (Batch_ID) REFERENCES Batch(Batch_ID)
);
GO

USE ETech_Technical_College_db;
GO
CREATE TABLE Payment (
    Payment_ID INT IDENTITY(1,1) PRIMARY KEY,
    Student_ID INT NOT NULL,
    Amount DECIMAL(10,2),
    Date DATE,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
);
GO

USE ETech_Technical_College_db;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Payment')
BEGIN
    CREATE TABLE Payment (
        Payment_ID INT IDENTITY(1,1) PRIMARY KEY,
        Student_ID INT NOT NULL,
        Amount DECIMAL(10,2),
        Date DATE,
        FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
    );
END
GO

INSERT INTO Student (First_Name, Last_Name, Gender, Date_Of_Birth, Email, Phone, Address, Batch_ID) VALUES 

('M.I.M.', 'Insaf', 'Male', '2002-01-15', 'mim.insaf@student.etech.edu', '0771234567', 'No. 55, Galle Road, Colombo 05, Sri Lanka', 1),
('Nimal', 'Perera', 'Male', '2003-05-10', 'nimal.perera@gmail.com', '0711111111', 'No. 12, Temple Road, Kandy, Sri Lanka', 1),
('Nadeesha', 'Silva', 'Female', '2004-09-22', 'nadeesha.silva@gmail.com', '0722222222', 'No. 8, Sea Street, Galle, Sri Lanka', 2),
('Sahan', 'Fernando', 'Male', '2005-01-15', 'sahan.fernando@gmail.com', '0773333333', 'No. 45, Hospital Road, Jaffna, Sri Lanka', 3),
('Ishara', 'Peris', 'Female', '2004-03-18', 'ishara.peris@gmail.com', '0764444444', 'No. 21, Lake View, Kurunegala, Sri Lanka', 4),
('Tharindu', 'Jayasinghe', 'Male', '2005-11-30', 'tharindu.j@gmail.com', '0755555555', 'No. 7, Beach Road, Matara, Sri Lanka', 5),
('Kavindi', 'Wickramasinghe', 'Female', '2003-07-12', 'kavindi.w@gmail.com', '0706666666', 'No. 33, Church Street, Negombo, Sri Lanka', 1),
('Sajith', 'Rajapaksa', 'Male', '2004-02-28', 'sajith.r@gmail.com', '0767777777', 'No. 10, New Town, Anuradhapura, Sri Lanka', 2),
('Amali', 'Gunasekara', 'Female', '2004-06-05', 'amali.g@gmail.com', '0718888888', 'No. 19, Hill Street, Nuwara Eliya, Sri Lanka', 3),
('Ranil', 'Wickramasinghe', 'Male', '2003-12-20', 'ranil.w@gmail.com', '0779999999', 'No. 4, Fort Road, Galle, Sri Lanka', 4),
('Sanduni', 'Weerasinghe', 'Female', '2005-08-14', 'sanduni.w@gmail.com', '0720000000', 'No. 60, Lake Road, Polonnaruwa, Sri Lanka', 5);
GO

INSERT INTO Payment (Student_ID, Amount, Date) VALUES 
(1, 25000.00, '2026-01-10'),  -- M.I.M. Insaf
(1, 25000.00, '2026-06-01'),
(2, 15000.00, '2026-02-05'),  -- Nimal Perera
(3, 35000.00, '2026-03-12'),  -- Nadeesha Silva
(3, 35000.00, '2026-07-05'),
(4, 12000.00, '2026-04-20'),  -- Sahan Fernando
(5, 22000.00, '2026-05-15'),  -- Ishara Peris
(6, 18000.00, '2026-06-10'),  -- Tharindu Jayasinghe
(7, 30000.00, '2026-07-20'),  -- Kavindi Wickramasinghe
(8, 25000.00, '2026-08-01'),  -- Sajith Rajapaksa
(9, 15000.00, '2026-08-15'),  -- Amali Gunasekara
(10, 32000.00, '2026-09-05'); -- Ranil Wickramasinghe
GO

INSERT INTO Student_Exam (Student_ID, Exam_ID, Marks, Grade) VALUES 
(1, 2, 92.00, 'A+'),  -- M.I.M. Insaf
(2, 1, 65.00, 'B'),   -- Nimal Perera
(3, 3, 88.00, 'A'),   -- Nadeesha Silva
(4, 4, 55.00, 'C'),   -- Sahan Fernando
(5, 1, 95.00, 'A+'),  -- Ishara Peris
(6, 2, 70.00, 'B+');  -- Tharindu Jayasinghe
GO


SELECT * FROM Student ORDER BY Student_ID DESC;
SELECT * FROM Payment;
SELECT * FROM Student_Exam;
GO

USE ETech_Technical_College_db;
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Users' AND COLUMN_NAME = 'Role')
BEGIN
    ALTER TABLE Users ADD Role VARCHAR(20) DEFAULT 'Staff';
END
GO

UPDATE Users SET Role = 'Admin' WHERE Username = 'admin';
GO

INSERT INTO Users (Username, Password_Hash, Role) VALUES ('staff', 'staff', 'Staff');
GO

SELECT * FROM Users;
GO

SELECT * FROM Student;

USE ETech_Technical_College_db;
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Users' AND COLUMN_NAME = 'Role')
BEGIN
    ALTER TABLE Users ADD Role VARCHAR(20) DEFAULT 'Staff';
END
GO

UPDATE Users SET Role = 'Admin' WHERE Username = 'admin';
UPDATE Users SET Role = 'Staff' WHERE Username = 'staff';
GO

IF NOT EXISTS (SELECT 1 FROM Users WHERE Username = 'staff')
BEGIN
    INSERT INTO Users (Username, Password_Hash, Role) VALUES ('staff', 'staff', 'Staff');
END
GO

SELECT * FROM Users; 
GO

USE ETech_Technical_College_db;
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Course' AND COLUMN_NAME = 'Total_Fee')
BEGIN
    ALTER TABLE Course ADD Total_Fee DECIMAL(10,2) DEFAULT 0;
END
GO

UPDATE Course SET Total_Fee = 250000.00 WHERE Course_ID = 1; -- Computing
UPDATE Course SET Total_Fee = 180000.00 WHERE Course_ID = 2; -- Business
UPDATE Course SET Total_Fee = 300000.00 WHERE Course_ID = 3; -- Engineering
UPDATE Course SET Total_Fee = 150000.00 WHERE Course_ID = 4; -- Hospitality
UPDATE Course SET Total_Fee = 100000.00 WHERE Course_ID = 5; -- English
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Student_Exam' AND COLUMN_NAME = 'Grade_Level')
BEGIN
    ALTER TABLE Student_Exam ADD Grade_Level VARCHAR(5);
END
GO

UPDATE Student_Exam SET Grade_Level = 'D' WHERE Marks >= 75;
UPDATE Student_Exam SET Grade_Level = 'M' WHERE Marks >= 60 AND Marks < 75;
UPDATE Student_Exam SET Grade_Level = 'P' WHERE Marks >= 40 AND Marks < 60;
UPDATE Student_Exam SET Grade_Level = 'F' WHERE Marks < 40;
GO

CREATE TABLE Assignment (
    Assignment_ID INT IDENTITY(1,1) PRIMARY KEY,
    Assignment_Name VARCHAR(100),
    Due_Date DATE,
    Course_ID INT,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
);
GO

INSERT INTO Assignment (Assignment_Name, Due_Date, Course_ID) VALUES 
('Python Final Project', '2026-08-15', 1),
('Database Design Report', '2026-09-01', 1),
('Business Plan Presentation', '2026-08-20', 2),
('Engineering Bridge Design', '2026-09-10', 3),
('Customer Service Roleplay', '2026-08-25', 4);
GO

SELECT * FROM Student

USE ETech_Technical_College_db;
GO

ALTER TABLE Student_Exam ALTER COLUMN Grade VARCHAR(10);
GO

USE ETech_Technical_College_db;
GO

ALTER TABLE Student ADD Student_Type VARCHAR(20) DEFAULT 'Internal';
GO

ALTER TABLE Payment ADD Discount DECIMAL(10,2) DEFAULT 0;
GO

ALTER TABLE Users ADD Real_Name VARCHAR(100);
GO

ALTER TABLE Assignment ADD Batch_ID INT, Student_ID INT, Submitted_Date DATE, Is_Late VARCHAR(10) DEFAULT 'No';
ALTER TABLE Assignment ADD CONSTRAINT FK_Assign_Batch FOREIGN KEY (Batch_ID) REFERENCES Batch(Batch_ID);
ALTER TABLE Assignment ADD CONSTRAINT FK_Assign_Student FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID);
GO

USE ETech_Technical_College_db;
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Student' AND COLUMN_NAME = 'Student_Type')
BEGIN
    ALTER TABLE Student ADD Student_Type VARCHAR(20) DEFAULT 'Internal';
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Payment' AND COLUMN_NAME = 'Discount')
BEGIN
    ALTER TABLE Payment ADD Discount DECIMAL(10,2) DEFAULT 0;
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Users' AND COLUMN_NAME = 'Real_Name')
BEGIN
    ALTER TABLE Users ADD Real_Name VARCHAR(100);
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Assignment' AND COLUMN_NAME = 'Batch_ID')
BEGIN
    ALTER TABLE Assignment ADD Batch_ID INT, Student_ID INT, Submitted_Date DATE, Is_Late VARCHAR(10) DEFAULT 'No';
    ALTER TABLE Assignment ADD CONSTRAINT FK_Assign_Batch FOREIGN KEY (Batch_ID) REFERENCES Batch(Batch_ID);
    ALTER TABLE Assignment ADD CONSTRAINT FK_Assign_Student FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID);
END
GO

UPDATE Users SET Real_Name = 'Administrator' WHERE Username = 'admin' AND Real_Name IS NULL;
GO

USE ETech_Technical_College_db;
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Student' AND COLUMN_NAME = 'Student_Type')
BEGIN
    ALTER TABLE Student ADD Student_Type VARCHAR(20) DEFAULT 'Internal';
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Payment' AND COLUMN_NAME = 'Discount')
BEGIN
    ALTER TABLE Payment ADD Discount DECIMAL(10,2) DEFAULT 0;
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Users' AND COLUMN_NAME = 'Real_Name')
BEGIN
    ALTER TABLE Users ADD Real_Name VARCHAR(100);
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Assignment' AND COLUMN_NAME = 'Batch_ID')
BEGIN
    ALTER TABLE Assignment ADD Batch_ID INT, Student_ID INT, Submitted_Date DATE, Is_Late VARCHAR(10) DEFAULT 'No';
    ALTER TABLE Assignment ADD CONSTRAINT FK_Assign_Batch FOREIGN KEY (Batch_ID) REFERENCES Batch(Batch_ID);
    ALTER TABLE Assignment ADD CONSTRAINT FK_Assign_Student FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID);
END
GO

UPDATE Users SET Real_Name = 'Administrator' WHERE Username = 'admin' AND Real_Name IS NULL;
GO

SELECT * FROM Users;

USE ETech_Technical_College_db;
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Student' AND COLUMN_NAME = 'Student_Type')
BEGIN
    ALTER TABLE Student ADD Student_Type VARCHAR(20) DEFAULT 'Internal';
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Payment' AND COLUMN_NAME = 'Discount')
BEGIN
    ALTER TABLE Payment ADD Discount DECIMAL(10,2) DEFAULT 0;
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Users' AND COLUMN_NAME = 'Real_Name')
BEGIN
    ALTER TABLE Users ADD Real_Name VARCHAR(100);
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Assignment' AND COLUMN_NAME = 'Batch_ID')
BEGIN
    ALTER TABLE Assignment ADD Batch_ID INT, Student_ID INT, Submitted_Date DATE, Is_Late VARCHAR(10) DEFAULT 'No';
    ALTER TABLE Assignment ADD CONSTRAINT FK_Assign_Batch FOREIGN KEY (Batch_ID) REFERENCES Batch(Batch_ID);
    ALTER TABLE Assignment ADD CONSTRAINT FK_Assign_Student FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID);
END
GO

UPDATE Users SET Real_Name = 'Administrator' WHERE Username = 'admin' AND Real_Name IS NULL;
GO

SELECT * FROM Student;

USE ETech_Technical_College_db;
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Payment' AND COLUMN_NAME = 'Discount')
BEGIN
    ALTER TABLE Payment ADD Discount DECIMAL(10,2) DEFAULT 0;
END
GO

UPDATE Payment SET Discount = 0 WHERE Discount IS NULL;
GO