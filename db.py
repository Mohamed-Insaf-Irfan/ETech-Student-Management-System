import pyodbc
import tkinter as tk
from tkinter import messagebox

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            print("🔄 Attempting to connect to LocalDB...")
            self.connection = pyodbc.connect(
                r"DRIVER={ODBC Driver 17 for SQL Server};"
                r"SERVER=(localdb)\MSSQLLocalDB;"
                r"DATABASE=ETech_Technical_College_db;"
                r"Trusted_Connection=yes;"
            )
            self.cursor = self.connection.cursor()
            print("✅ Connected to LocalDB successfully!")
        except Exception as e:
            messagebox.showerror("Fatal Error", f"Cannot connect to DB: {e}")
            print(f"❌ Connection Error: {e}")
            exit()

    def execute(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except pyodbc.IntegrityError:
            messagebox.showerror("Constraint Error", 
                "This action violates database rules (e.g., Duplicate ID, or deleting a record linked to others).")
            return False
        except pyodbc.Error as e:
            messagebox.showerror("SQL Error", f"Database error: {e}")
            return False
        except Exception as e:
            messagebox.showerror("Unknown Error", str(e))
            return False

    def fetch(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Fetch Error", str(e))
            return []