import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkcalendar import Calendar
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from db import Database
from PIL import Image, ImageTk
import os

# --- STANDARD TKINTER THEME ---
BG_COLOR = "#f4f7f6"
HEADER_COLOR = "#1a1a2e"
SIDEBAR_COLOR = "#2c3e50"
CARD_BG = "#ffffff"
TEXT_COLOR = "#16213e"
BTN_PRIMARY = "#0f3460"

# ACCENT COLORS
C_STUDENTS = "#3498db"
C_LECTURERS = "#2ecc71"
C_COURSES = "#e74c3c"
C_BATCHES = "#9b59b6"
C_EXAMS = "#f39c12"
C_RESULTS = "#1abc9c"
C_PAYMENTS = "#e67e22"
C_USERS = "#34495e"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Tech College Master System")
        self.root.geometry("1300x800")
        self.root.configure(bg=BG_COLOR)

        self.db = Database()
        self.current_user = None
        self.current_role = None

        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- LOGIN SCREEN ---
    def show_login(self):
        self.clear_window()
        
        try:
            pil_image = Image.open("bg.jpg")
            pil_image = pil_image.resize((1300, 800))
            self.bg_image = ImageTk.PhotoImage(pil_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Background image error: {e}")
            self.root.configure(bg=HEADER_COLOR)

        glass_frame = tk.Frame(self.root, bg="#fafafa", padx=50, pady=50, relief="flat", bd=0)
        glass_frame.place(relx=0.5, rely=0.5, anchor="center")
        frame = tk.Frame(glass_frame, bg="#fafafa", padx=40, pady=40, relief="solid", bd=1)
        frame.pack()

        tk.Label(frame, text="🏫 ETECH COLLEGE", font=("Segoe UI", 22, "bold"), bg="#fafafa", fg=HEADER_COLOR).pack(pady=(0, 5))
        tk.Label(frame, text="Enterprise Management System", font=("Segoe UI", 10), bg="#fafafa", fg="#7f8c8d").pack(pady=(0, 25))

        tk.Label(frame, text="Username", bg="#fafafa", fg=TEXT_COLOR, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.user_entry = tk.Entry(frame, width=30, font=("Segoe UI", 11), relief="solid", bd=1)
        self.user_entry.pack(pady=(0, 10))

        tk.Label(frame, text="Password", bg="#fafafa", fg=TEXT_COLOR, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.pass_entry = tk.Entry(frame, width=30, show="*", font=("Segoe UI", 11), relief="solid", bd=1)
        self.pass_entry.pack(pady=(0, 20))

        # BUTTONS
        btn_frame = tk.Frame(frame, bg="#fafafa")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Sign In", bg=BTN_PRIMARY, fg="white", font=("Segoe UI", 11, "bold"),
                  command=self.login_action, width=12, relief="flat", pady=5).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Exit", bg="#e74c3c", fg="white", font=("Segoe UI", 11, "bold"),
                  command=self.root.destroy, width=12, relief="flat", pady=5).pack(side="left", padx=5)
        
        tk.Label(frame, text="Admin: admin / admin | Staff: staff / staff", bg="#fafafa", fg="#95a5a6", font=("Segoe UI", 8)).pack(pady=(10, 0))

    def login_action(self):
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        result = self.db.fetch("SELECT Username, Role FROM Users WHERE Username = ? AND Password_Hash = ?", (user, pwd))
        if result:
            self.current_user = result[0][0]
            self.current_role = result[0][1]
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    # --- HELPER: GET COUNTS ---
    def get_live_counts(self):
        try:
            return (
                self.db.fetch("SELECT COUNT(*) FROM Student")[0][0],
                self.db.fetch("SELECT COUNT(*) FROM Lecturer")[0][0],
                self.db.fetch("SELECT COUNT(*) FROM Course")[0][0]
            )
        except: return 0, 0, 0

    # ==========================================================
    # DASHBOARD WITH ROLE-BASED SIDEBAR
    # ==========================================================
    def show_dashboard(self):
        self.clear_window()

        # --- SIDEBAR CONTAINER ---
        sidebar_container = tk.Frame(self.root, bg=SIDEBAR_COLOR, width=200)
        sidebar_container.pack(side="left", fill="y")
        sidebar_container.pack_propagate(False)

        # Title
        tk.Label(sidebar_container, text="E-TECH\nCOLLEGE", bg=SIDEBAR_COLOR, fg="white", font=("Segoe UI", 14, "bold")).pack(pady=(15, 10))

        # Scrollable Sidebar Frame
        sidebar_canvas = tk.Canvas(sidebar_container, bg=SIDEBAR_COLOR, highlightthickness=0, width=190)
        sidebar_canvas.pack(side="left", fill="both", expand=True)

        sidebar_scroll = tk.Scrollbar(sidebar_container, orient="vertical", command=sidebar_canvas.yview)
        sidebar_scroll.pack(side="right", fill="y")

        sidebar_frame = tk.Frame(sidebar_canvas, bg=SIDEBAR_COLOR)
        sidebar_frame.bind("<Configure>", lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all")))
        sidebar_canvas.create_window((0, 0), window=sidebar_frame, anchor="nw")
        sidebar_canvas.configure(yscrollcommand=sidebar_scroll.set)

        # --- ROLE-BASED MODULES ---
        if self.current_role == 'Admin':
            nav_items = [
                ("🎓 Students", C_STUDENTS, self.open_students),
                ("👨‍🏫 Lecturers", C_LECTURERS, self.open_lecturers),
                ("📚 Courses", C_COURSES, self.open_courses),
                ("📦 Batches", C_BATCHES, self.open_batches),
                ("📝 Exams", C_EXAMS, self.open_exams),
                ("📊 Results", C_RESULTS, self.open_results),
                ("💰 Payments", C_PAYMENTS, self.open_payments),
                ("📋 Assignments", "#2c3e50", self.open_assignments),
                ("👤 Users", C_USERS, self.open_users)
            ]
        else: # Staff sees only 4
            nav_items = [
                ("🎓 Students", C_STUDENTS, self.open_students),
                ("👨‍🏫 Lecturers", C_LECTURERS, self.open_lecturers),
                ("📚 Courses", C_COURSES, self.open_courses),
                ("📦 Batches", C_BATCHES, self.open_batches)
            ]

        for text, color, cmd in nav_items:
            tk.Button(sidebar_frame, text=text, bg=color, fg="white", font=("Segoe UI", 9, "bold"), relief="flat", command=cmd, anchor="w", padx=12, pady=8).pack(fill="x", padx=8, pady=3)

        # --- MAIN CONTENT AREA ---
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(side="right", fill="both", expand=True)

        # Header (With Logout Button on the Right)
        header = tk.Frame(main_frame, bg=HEADER_COLOR, height=70)
        header.pack(fill="x")
        
        # Left: Dashboard Title
        tk.Label(header, text="Dashboard", bg=HEADER_COLOR, fg="white", font=("Segoe UI", 20, "bold")).pack(side="left", padx=25, pady=20)
        
        # Right: Welcome Message + Logout Button
        right_header = tk.Frame(header, bg=HEADER_COLOR)
        right_header.pack(side="right", padx=25, pady=20)
        
        tk.Label(right_header, text=f"Welcome, {self.current_user}", bg=HEADER_COLOR, fg="white", font=("Segoe UI", 11)).pack(side="left", padx=10)
        
        # Logout Button is now in the Top-Right Header
        tk.Button(right_header, text="🚪 Logout", bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=10, pady=5, command=self.show_login).pack(side="left")

        # Content Container
        content_frame = tk.Frame(main_frame, bg=BG_COLOR)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- STATS CARDS ---
        stats_frame = tk.Frame(content_frame, bg=BG_COLOR)
        stats_frame.pack(fill="x", pady=(0, 20))

        s, l, c = self.get_live_counts()
        for title, count, color in [("🎓 Students", s, "#3498db"), ("👨‍🏫 Lecturers", l, "#2ecc71"), ("📚 Courses", c, "#e74c3c")]:
            card = tk.Frame(stats_frame, bg=color, padx=20, pady=15, relief="flat")
            card.pack(side="left", padx=10, expand=True, fill="both")
            tk.Label(card, text=title, bg=color, fg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Label(card, text=str(count), bg=color, fg="white", font=("Segoe UI", 24, "bold")).pack(anchor="w", pady=5)

        # --- RECENT STUDENTS TABLE ---
        table_frame = tk.Frame(content_frame, bg="white", relief="solid", bd=1)
        table_frame.pack(fill="both", expand=True)

        tk.Label(table_frame, text="Recent Students", bg="white", fg=HEADER_COLOR, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=15, pady=(10, 5))

        # Fetch recent students
        recent_students = self.db.fetch("SELECT TOP 5 Student_ID, First_Name, Last_Name, Email, Batch_ID FROM Student ORDER BY Student_ID DESC")
        
        if recent_students:
            columns = ("ID", "Name", "Email", "Batch")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=5)
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in recent_students:
                full_name = f"{row[1]} {row[2]}"
                tree.insert("", "end", values=(row[0], full_name, row[3], row[4]))

            tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        else:
            tk.Label(table_frame, text="No recent students found.", bg="white", fg="#7f8c8d").pack(pady=20)

    # ==========================================================
    # MODULES MANAGER
    # ==========================================================
    def build_manager(self, title, table, pk_name, columns, insert_q, insert_params, update_q, update_params, custom_query=None):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("1200x650")
        win.configure(bg=CARD_BG)

        # Split Container
        main_container = tk.Frame(win, bg=CARD_BG)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT: FORM PANEL (Compact)
        left_pane = tk.Frame(main_container, bg=CARD_BG, padx=15, pady=15, relief="solid", bd=1)
        left_pane.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left_pane, text=title, bg=CARD_BG, fg=HEADER_COLOR, font=("Segoe UI", 14, "bold")).pack(pady=(0, 10))

        entries = {}
        for label_text, key in columns:
            row_frame = tk.Frame(left_pane, bg=CARD_BG)
            row_frame.pack(fill="x", pady=3)
            tk.Label(row_frame, text=label_text, bg=CARD_BG, fg=TEXT_COLOR, font=("Segoe UI", 9, "bold"), width=15, anchor="w").pack(side="left")
            entry = tk.Entry(row_frame, width=20, font=("Segoe UI", 10), bg="white", relief="solid", bd=1)
            entry.pack(side="right", expand=True, fill="x")
            entries[key] = entry

        # BUTTONS
        btn_frame = tk.Frame(left_pane, bg=CARD_BG)
        btn_frame.pack(pady=10)

        def clear_entries():
            for e in entries.values():
                e.delete(0, 'end')

        def load_data():
            for r in tree.get_children(): tree.delete(r)
            rows = self.db.fetch(custom_query) if custom_query else self.db.fetch(f"SELECT * FROM {table}")
            for r in rows:
                tree.insert("", "end", values=list(r))

        def add_action():
            p = insert_params(entries)
            if p and self.db.execute(insert_q, p):
                load_data()
                messagebox.showinfo("Success", "Record added.")
                clear_entries()

        def update_action():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Error", "Select a record to update.")
                return
            pk_val = tree.item(selected[0])['values'][0]
            p = update_params(pk_val, entries)
            if p and self.db.execute(update_q, p):
                load_data()
                messagebox.showinfo("Success", "Record updated.")
                clear_entries()

        def delete_action():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Error", "Select a record to delete.")
                return
            pk_val = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Confirm", "Delete this record?"):
                if self.db.execute(f"DELETE FROM {table} WHERE {pk_name}=?", (pk_val,)):
                    load_data()
                    clear_entries()
                    messagebox.showinfo("Success", "Record deleted.")

        tk.Button(btn_frame, text="➕ Add", bg="#2ecc71", fg="white", width=10, relief="flat", command=add_action).pack(side="left", padx=4)
        tk.Button(btn_frame, text="✏️ Update", bg="#f39c12", fg="white", width=10, relief="flat", command=update_action).pack(side="left", padx=4)
        tk.Button(btn_frame, text="🗑️ Delete", bg="#e74c3c", fg="white", width=10, relief="flat", command=delete_action).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Clear", bg="#7f8c8d", fg="white", width=8, relief="flat", command=clear_entries).pack(side="left", padx=4)

        # RIGHT: TABLE
        right_pane = tk.Frame(main_container, bg=CARD_BG)
        right_pane.pack(side="right", fill="both", expand=True)

        tree_columns = [col[0] for col in columns]
        tree = ttk.Treeview(right_pane, columns=tree_columns, show="headings", height=15)
        for c_id in tree_columns:
            tree.heading(c_id, text=c_id)
            tree.column(c_id, width=100)

        v_scroll = ttk.Scrollbar(right_pane, orient="vertical", command=tree.yview)
        h_scroll = ttk.Scrollbar(right_pane, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        tree.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

        def fill_form(event):
            selected = tree.selection()
            if not selected: return
            vals = tree.item(selected[0])['values']
            clear_entries()
            for i, key in enumerate([col[1] for col in columns]):
                if i < len(vals):
                    entries[key].insert(0, str(vals[i]))

        tree.bind("<<TreeviewSelect>>", fill_form)
        load_data()

    # ==========================================================
    # ALL 9 MODULES
    # ==========================================================

    def open_students(self):
        self.build_manager(
            "Manage Students", "Student", "Student_ID",
            [("ID","Student_ID"), ("First Name","First_Name"), ("Last Name","Last_Name"), ("Gender","Gender"), ("DOB","Date_Of_Birth"), ("Email","Email"), ("Phone","Phone"), ("Address","Address"), ("Batch","Batch_ID"), ("Type","Student_Type")],
            "INSERT INTO Student (First_Name, Last_Name, Gender, Date_Of_Birth, Email, Phone, Address, Batch_ID, Student_Type) VALUES (?,?,?,?,?,?,?,?,?)",
            lambda e: (e["First_Name"].get(), e["Last_Name"].get(), e["Gender"].get(), e["Date_Of_Birth"].get(), e["Email"].get(), e["Phone"].get(), e["Address"].get(), e["Batch_ID"].get(), e["Student_Type"].get()),
            "UPDATE Student SET First_Name=?, Last_Name=?, Gender=?, Date_Of_Birth=?, Email=?, Phone=?, Address=?, Batch_ID=?, Student_Type=? WHERE Student_ID=?",
            lambda pk, e: (e["First_Name"].get(), e["Last_Name"].get(), e["Gender"].get(), e["Date_Of_Birth"].get(), e["Email"].get(), e["Phone"].get(), e["Address"].get(), e["Batch_ID"].get(), e["Student_Type"].get(), pk)
        )

    def open_lecturers(self):
        self.build_manager(
            "Manage Lecturers", "Lecturer", "Lecturer_ID",
            [("ID","Lecturer_ID"), ("First Name","First_Name"), ("Last Name","Last_Name"), ("Email","Email"), ("Phone","Phone"), ("Dept ID","Department_ID")],
            "INSERT INTO Lecturer (First_Name, Last_Name, Email, Phone, Department_ID) VALUES (?,?,?,?,?)",
            lambda e: (e["First_Name"].get(), e["Last_Name"].get(), e["Email"].get(), e["Phone"].get(), e["Department_ID"].get()),
            "UPDATE Lecturer SET First_Name=?, Last_Name=?, Email=?, Phone=?, Department_ID=? WHERE Lecturer_ID=?",
            lambda pk, e: (e["First_Name"].get(), e["Last_Name"].get(), e["Email"].get(), e["Phone"].get(), e["Department_ID"].get(), pk)
        )

    def open_courses(self):
        self.build_manager(
            "Manage Courses", "Course", "Course_ID",
            [("ID","Course_ID"), ("Course Name","Course_Name"), ("Duration","Duration"), ("Fee","Total_Fee"), ("Dept ID","Department_ID")],
            "INSERT INTO Course (Course_Name, Duration, Total_Fee, Department_ID) VALUES (?,?,?,?)",
            lambda e: (e["Course_Name"].get(), e["Duration"].get(), e["Total_Fee"].get(), e["Department_ID"].get()),
            "UPDATE Course SET Course_Name=?, Duration=?, Total_Fee=?, Department_ID=? WHERE Course_ID=?",
            lambda pk, e: (e["Course_Name"].get(), e["Duration"].get(), e["Total_Fee"].get(), e["Department_ID"].get(), pk)
        )

    def open_batches(self):
        self.build_manager(
            "Manage Batches", "Batch", "Batch_ID",
            [("ID","Batch_ID"), ("Batch Name","Batch_Name"), ("Start Date","Start_Date"), ("End Date","End_Date"), ("Course ID","Course_ID")],
            "INSERT INTO Batch (Batch_Name, Start_Date, End_Date, Course_ID) VALUES (?,?,?,?)",
            lambda e: (e["Batch_Name"].get(), e["Start_Date"].get(), e["End_Date"].get(), e["Course_ID"].get()),
            "UPDATE Batch SET Batch_Name=?, Start_Date=?, End_Date=?, Course_ID=? WHERE Batch_ID=?",
            lambda pk, e: (e["Batch_Name"].get(), e["Start_Date"].get(), e["End_Date"].get(), e["Course_ID"].get(), pk)
        )

    def open_exams(self):
        self.build_manager(
            "Manage Exams", "Exam", "Exam_ID",
            [("ID","Exam_ID"), ("Exam Name","Exam_Name"), ("Date","Exam_Date"), ("Subject ID","Subject_ID")],
            "INSERT INTO Exam (Exam_Name, Exam_Date, Subject_ID) VALUES (?,?,?)",
            lambda e: (e["Exam_Name"].get(), e["Exam_Date"].get(), e["Subject_ID"].get()),
            "UPDATE Exam SET Exam_Name=?, Exam_Date=?, Subject_ID=? WHERE Exam_ID=?",
            lambda pk, e: (e["Exam_Name"].get(), e["Exam_Date"].get(), e["Subject_ID"].get(), pk)
        )

    def open_results(self):
        custom_query = """
            SELECT se.Student_Exam_ID, s.First_Name + ' ' + s.Last_Name AS StudentName, 
                   e.Exam_Name, se.Marks, se.Grade_Level
            FROM Student_Exam se
            JOIN Student s ON se.Student_ID = s.Student_ID
            JOIN Exam e ON se.Exam_ID = e.Exam_ID
        """
        self.build_manager(
            "Manage Results", "Student_Exam", "Student_Exam_ID",
            [("ID","Student_Exam_ID"), ("Student ID","Student_ID"), ("Exam ID","Exam_ID"), ("Marks","Marks"), ("P/M/D","Grade_Level")],
            "INSERT INTO Student_Exam (Student_ID, Exam_ID, Marks, Grade_Level) VALUES (?,?,?,?)",
            lambda e: (e["Student_ID"].get(), e["Exam_ID"].get(), e["Marks"].get(), e["Grade_Level"].get()),
            "UPDATE Student_Exam SET Student_ID=?, Exam_ID=?, Marks=?, Grade_Level=? WHERE Student_Exam_ID=?",
            lambda pk, e: (e["Student_ID"].get(), e["Exam_ID"].get(), e["Marks"].get(), e["Grade_Level"].get(), pk),
            custom_query=custom_query
        )

    def open_payments(self):
        custom_query = """
            SELECT s.Student_ID, s.First_Name + ' ' + s.Last_Name AS StudentName,
                   c.Total_Fee AS Total_Fee,
                   ISNULL(SUM(p.Amount), 0) AS Total_Paid,
                   ISNULL(SUM(p.Discount), 0) AS Total_Discount,
                   (c.Total_Fee - ISNULL(SUM(p.Amount), 0)) AS Balance
            FROM Student s
            JOIN Batch b ON s.Batch_ID = b.Batch_ID
            JOIN Course c ON b.Course_ID = c.Course_ID
            LEFT JOIN Payment p ON s.Student_ID = p.Student_ID
            GROUP BY s.Student_ID, s.First_Name, s.Last_Name, c.Total_Fee
        """
        self.build_manager(
            "Manage Payments", "Payment", "Payment_ID",
            [("ID","Student_ID"), ("Student Name","StudentName"), ("Total Fee","Total_Fee"), ("Total Paid","Total_Paid"), ("Discount","Total_Discount"), ("Balance","Balance")],
            "INSERT INTO Payment (Student_ID, Amount, Discount, Date) VALUES (?,?,?,?)",
            lambda e: (e["StudentName"].get(), e["Total_Fee"].get(), e["Total_Discount"].get(), self.get_date("Payment Date")),
            "UPDATE Payment SET Student_ID=?, Amount=?, Discount=?, Date=? WHERE Payment_ID=?",
            lambda pk, e: (e["StudentName"].get(), e["Total_Fee"].get(), e["Total_Discount"].get(), self.get_date("Payment Date"), pk),
            custom_query=custom_query
        )

    def open_assignments(self):
        custom_query = """
            SELECT a.Assignment_ID, b.Batch_Name, a.Assignment_Name, 
                   s.First_Name + ' ' + s.Last_Name AS StudentName,
                   a.Submitted_Date, a.Is_Late
            FROM Assignment a
            LEFT JOIN Batch b ON a.Batch_ID = b.Batch_ID
            LEFT JOIN Student s ON a.Student_ID = s.Student_ID
        """
        self.build_manager(
            "Manage Assignments", "Assignment", "Assignment_ID",
            [("ID","Assignment_ID"), ("Batch","Batch_Name"), ("Assignment","Assignment_Name"), ("Student","StudentName"), ("Submitted","Submitted_Date"), ("Late","Is_Late")],
            "INSERT INTO Assignment (Batch_ID, Assignment_Name, Student_ID, Submitted_Date, Is_Late) VALUES (?,?,?,?,?)",
            lambda e: (e["Batch_Name"].get(), e["Assignment_Name"].get(), e["StudentName"].get(), self.get_date("Submit Date"), e["Is_Late"].get()),
            "UPDATE Assignment SET Batch_ID=?, Assignment_Name=?, Student_ID=?, Submitted_Date=?, Is_Late=? WHERE Assignment_ID=?",
            lambda pk, e: (e["Batch_Name"].get(), e["Assignment_Name"].get(), e["StudentName"].get(), self.get_date("Submit Date"), e["Is_Late"].get(), pk),
            custom_query=custom_query
        )

    def open_users(self):
        custom_query = "SELECT Username, Real_Name, Role, Password_Hash FROM Users"
        self.build_manager(
            "Manage Users", "Users", "Username",
            [("Username","Username"), ("Real Name","Real_Name"), ("Role","Role"), ("Password","Password_Hash")],
            "INSERT INTO Users (Username, Real_Name, Role, Password_Hash) VALUES (?,?,?,?)",
            lambda e: (e["Username"].get(), e["Real_Name"].get(), e["Role"].get(), e["Password_Hash"].get()),
            "UPDATE Users SET Real_Name=?, Role=?, Password_Hash=? WHERE Username=?",
            lambda pk, e: (e["Real_Name"].get(), e["Role"].get(), e["Password_Hash"].get(), pk),
            custom_query=custom_query
        )

    def get_date(self, title="Select Date"):
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("300x250")
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=10)
        d = None
        def pick(): nonlocal d; d = cal.get_date(); top.destroy()
        tk.Button(top, text="Confirm", command=pick).pack(pady=5)
        self.root.wait_window(top)
        return str(d) if d else None

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()