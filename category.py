from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector
import os

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System | Category Management")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()

        # Database Configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'C@sper123',
            'database': 'inventory_management'
        }

        # Variables
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        # Title
        lbl_title = Label(
            self.root,
            text="Manage Product Category",
            font=("goudy old style", 30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE
        ).pack(side=TOP, fill=X, padx=10, pady=20)
        
        # Category Input
        lbl_name = Label(
            self.root,
            text="Enter Category Name",
            font=("goudy old style", 30),
            bg="white"
        ).place(x=50, y=100)
        
        txt_name = Entry(
            self.root,
            textvariable=self.var_name,
            font=("goudy old style", 18),
            bg="lightyellow"
        ).place(x=50, y=170, width=300)

        # Buttons
        btn_add = Button(
            self.root,
            text="ADD",
            command=self.add,
            font=("goudy old style", 15),
            bg="#4caf50",
            fg="white",
            cursor="hand2"
        ).place(x=360, y=170, width=150, height=30)
        
        btn_delete = Button(
            self.root,
            text="Delete",
            command=self.delete,
            font=("goudy old style", 15),
            bg="red",
            fg="white",
            cursor="hand2"
        ).place(x=520, y=170, width=150, height=30)

        # Category Details Table
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=380, height=100)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)
        
        self.CategoryTable = ttk.Treeview(
            cat_frame,
            columns=("cid", "name"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)
        
        self.CategoryTable.heading("cid", text="C ID")
        self.CategoryTable.heading("name", text="Name")
        self.CategoryTable["show"] = "headings"
        self.CategoryTable.column("cid", width=90)
        self.CategoryTable.column("name", width=100)
        self.CategoryTable.pack(fill=BOTH, expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)

        # Images
        try:
            self.im1 = Image.open("images/cat.jpg")
            self.im1 = self.im1.resize((500, 250))
            self.im1 = ImageTk.PhotoImage(self.im1)
            self.lbl_im1 = Label(self.root, image=self.im1, bd=2, relief=RAISED)
            self.lbl_im1.place(x=50, y=220)

            self.im2 = Image.open("images/category.jpg")
            self.im2 = self.im2.resize((500, 250))
            self.im2 = ImageTk.PhotoImage(self.im2)
            self.lbl_im2 = Label(self.root, image=self.im2, bd=2, relief=RAISED)
            self.lbl_im2.place(x=580, y=220)
        except Exception as ex:
            print(f"Error loading images: {str(ex)}")

        # Load initial data
        self.show()

    def get_db_connection(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            return connection
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(err)}")
            return None

    def add(self):
        conn = self.get_db_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name must be required", parent=self.root)
            else:
                # Check if category exists
                cursor.execute("SELECT * FROM category WHERE name = %s", (self.var_name.get(),))
                row = cursor.fetchone()
                
                if row is not None:
                    messagebox.showerror("Error", "Category already present", parent=self.root)
                else:
                    cursor.execute("INSERT INTO category (name) VALUES (%s)", (self.var_name.get(),))
                    conn.commit()
                    messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
                    self.clear()
                    self.show()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {str(err)}")
        finally:
            cursor.close()
            conn.close()

    def show(self):
        conn = self.get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM category")
            rows = cursor.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('', END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {str(err)}")
        finally:
            cursor.close()
            conn.close()

    def clear(self):
        self.var_name.set("")
        self.var_cat_id.set("")
        self.show()

    def get_data(self, ev):
        selected_row = self.CategoryTable.focus()
        content = self.CategoryTable.item(selected_row)
        row = content['values']
        if row:
            self.var_cat_id.set(row[0])
            self.var_name.set(row[1])

    def delete(self):
        conn = self.get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Select category to delete", parent=self.root)
            else:
                cursor.execute("SELECT * FROM category WHERE cid = %s", (self.var_cat_id.get(),))
                row = cursor.fetchone()
                
                if row is None:
                    messagebox.showerror("Error", "Invalid Category", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cursor.execute("DELETE FROM category WHERE cid = %s", (self.var_cat_id.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        self.clear()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {str(err)}")
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()