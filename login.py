import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
import os

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x600+500+100")
        self.root.title("Inventory Management System - Login")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        
        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'C@sper123', 
            'database': 'inventory_management'
        }
        
        # Variables
        self.employee_id = tk.StringVar()
        self.password = tk.StringVar()
        
        # Create Database and Table if not exists
        self.create_database()
        
        # Login Frame
        self.create_login_frame()
        
        # Signup Frame
        self.create_signup_frame()
    
    def get_db_connection(self):
        return mysql.connector.connect(**self.db_config)
    
    def create_database(self):
        try:
            # First connect without database to create it
            initial_config = self.db_config.copy()
            initial_config.pop('database')
            conn = mysql.connector.connect(**initial_config)
            cursor = conn.cursor()
            
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
            conn.commit()
            conn.close()
            
            # Now connect with database and create table
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Create employee table matching the schema from create_db.py
            cursor.execute('''CREATE TABLE IF NOT EXISTS employee (
                eid VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                gender VARCHAR(10),
                contact VARCHAR(20),
                dob VARCHAR(20),
                doj VARCHAR(20),
                pass VARCHAR(255),
                utype VARCHAR(50),
                address TEXT,
                salary VARCHAR(20)
            )''')
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to initialize database: {err}")
    
    def create_login_frame(self):
        login_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg="white")
        login_frame.place(x=50, y=50, width=400, height=250)

        title = tk.Label(login_frame, text="Login", font=("goudy old style", 20, "bold"), bg="white")
        title.place(x=0, y=0, width=400, height=40)
        
        # Employee ID
        tk.Label(login_frame, text="Employee ID", font=("goudy old style", 15, "bold"), bg="white").place(x=50, y=60)
        tk.Entry(login_frame, textvariable=self.employee_id, font=("goudy old style", 15), bg="lightgray").place(x=50, y=90, width=300, height=30)
        
        # Password
        tk.Label(login_frame, text="Password", font=("goudy old style", 15, "bold"), bg="white").place(x=50, y=130)
        tk.Entry(login_frame, textvariable=self.password, show="*", font=("goudy old style", 15), bg="lightgray").place(x=50, y=160, width=300, height=30)
        
        # Login Button
        tk.Button(login_frame, text="Login", font=("goudy old style", 15, "bold"), 
                  bg="#0f4d7d", fg="white", cursor="hand2", command=self.login).place(x=50, y=200, width=300, height=40)
    
    def create_signup_frame(self):
        signup_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg="white")
        signup_frame.place(x=50, y=350, width=400, height=200)

        title = tk.Label(signup_frame, text="Signup", font=("goudy old style", 20, "bold"), bg="white")
        title.place(x=0, y=0, width=400, height=40)
        
        # Signup Button for Employee
        tk.Button(signup_frame, text="Employee Signup", font=("goudy old style", 15, "bold"), 
                  bg="#0f4d7d", fg="white", cursor="hand2", command=self.employee_signup).place(x=50, y=80, width=300, height=40)
        
        # Signup Button for Admin
        tk.Button(signup_frame, text="Admin Signup", font=("goudy old style", 15, "bold"), 
                  bg="#0f4d7d", fg="white", cursor="hand2", command=self.admin_signup).place(x=50, y=140, width=300, height=40)
    
    def employee_signup(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Employee Signup")
        signup_window.geometry("400x500")
        signup_window.config(bg="white")

        # Signup form fields
        tk.Label(signup_window, text="Employee Signup", font=("goudy old style", 20, "bold"), bg="white").pack(pady=20)
        
        name_var = tk.StringVar()
        id_var = tk.StringVar()
        email_var = tk.StringVar()
        password_var = tk.StringVar()
        confirm_password_var = tk.StringVar()

        # Create entry fields
        fields = [
            ("Name", name_var),
            ("Employee ID", id_var),
            ("Email", email_var),
            ("Password", password_var, "*"),
            ("Confirm Password", confirm_password_var, "*")
        ]
        
        for field_info in fields:
            tk.Label(signup_window, text=field_info[0], bg="white", font=("goudy old style", 12)).pack(pady=5)
            if len(field_info) > 2:
                tk.Entry(signup_window, textvariable=field_info[1], show=field_info[2], 
                        font=("goudy old style", 12)).pack(pady=5)
            else:
                tk.Entry(signup_window, textvariable=field_info[1], 
                        font=("goudy old style", 12)).pack(pady=5)

        def submit_signup():
            if not all([name_var.get().strip(), id_var.get().strip(), 
                       email_var.get().strip(), password_var.get().strip(), 
                       confirm_password_var.get().strip()]):
                messagebox.showerror("Error", "All Fields are Required")
                return

            if password_var.get() != confirm_password_var.get():
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO employee (eid, name, email, pass, utype) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_var.get(), name_var.get(), email_var.get(), 
                      password_var.get(), "Employee"))
                conn.commit()
                messagebox.showinfo("Success", "Employee registered successfully")
                signup_window.destroy()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Employee ID already exists")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

        tk.Button(signup_window, text="Submit", command=submit_signup, 
                 font=("goudy old style", 15, "bold"), bg="#0f4d7d", fg="white").pack(pady=20)
    
    def admin_signup(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Admin Signup")
        signup_window.geometry("400x500")
        signup_window.config(bg="white")

        tk.Label(signup_window, text="Admin Signup", font=("goudy old style", 20, "bold"), bg="white").pack(pady=20)
        
        name_var = tk.StringVar()
        id_var = tk.StringVar()
        email_var = tk.StringVar()
        password_var = tk.StringVar()
        confirm_password_var = tk.StringVar()

        # Create entry fields
        fields = [
            ("Name", name_var),
            ("Admin ID", id_var),
            ("Email", email_var),
            ("Password", password_var, "*"),
            ("Confirm Password", confirm_password_var, "*")
        ]
        
        for field_info in fields:
            tk.Label(signup_window, text=field_info[0], bg="white", font=("goudy old style", 12)).pack(pady=5)
            if len(field_info) > 2:
                tk.Entry(signup_window, textvariable=field_info[1], show=field_info[2], 
                        font=("goudy old style", 12)).pack(pady=5)
            else:
                tk.Entry(signup_window, textvariable=field_info[1], 
                        font=("goudy old style", 12)).pack(pady=5)

        def submit_signup():
            if not all([name_var.get().strip(), id_var.get().strip(), 
                       email_var.get().strip(), password_var.get().strip(), 
                       confirm_password_var.get().strip()]):
                messagebox.showerror("Error", "All Fields are Required")
                return

            if password_var.get() != confirm_password_var.get():
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO employee (eid, name, email, pass, utype) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_var.get(), name_var.get(), email_var.get(), 
                      password_var.get(), "Admin"))
                conn.commit()
                messagebox.showinfo("Success", "Admin registered successfully")
                signup_window.destroy()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Admin ID already exists")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

        tk.Button(signup_window, text="Submit", command=submit_signup, 
                 font=("goudy old style", 15, "bold"), bg="#0f4d7d", fg="white").pack(pady=20)
    
    def login(self):
        if not self.employee_id.get() or not self.password.get():
            messagebox.showerror("Error", "All Fields are Required")
            return
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT utype FROM employee 
                WHERE eid=%s AND pass=%s
            """, (self.employee_id.get(), self.password.get()))
            user = cursor.fetchone()
            
            if user is None:
                messagebox.showerror("Error", "Invalid Username or Password")
            else:
                self.root.destroy()
                if user[0] == "Admin":
                    os.system("python dashboard.py")
                else:
                    os.system("python billing.py")
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    obj = LoginSystem(root)
    root.mainloop()