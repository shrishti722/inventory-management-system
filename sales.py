from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector
import os
from datetime import datetime

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System | Sales")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()

        # Database Configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'your_username',
            'password': 'C@sper123',
            'database': 'inventory_management'
        }

        self.bill_list = []
        self.var_invoice = StringVar()

        # Title
        lbl_title = Label(
            self.root,
            text="View Customer Bills",
            font=("goudy old style", 30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE
        ).pack(side=TOP, fill=X, padx=10, pady=20)
        
        # Search Frame
        SearchFrame = Frame(self.root, bg="white")
        SearchFrame.place(x=50, y=100, width=600, height=40)
        
        # Invoice Search
        lbl_invoice = Label(
            SearchFrame,
            text="Invoice No.",
            font=("times new roman", 15),
            bg="white"
        ).place(x=0, y=5)
        
        txt_invoice = Entry(
            SearchFrame,
            textvariable=self.var_invoice,
            font=("times new roman", 15),
            bg="lightyellow"
        ).place(x=110, y=5, width=180, height=28)

        # Buttons
        btn_search = Button(
            SearchFrame,
            text="Search",
            command=self.search,
            font=("times new roman", 15, "bold"),
            bg="#2196f3",
            fg="white",
            cursor="hand2"
        ).place(x=310, y=5, width=120, height=28)
        
        btn_clear = Button(
            SearchFrame,
            text="Clear",
            command=self.clear,
            font=("times new roman", 15, "bold"),
            bg="lightgray",
            cursor="hand2"
        ).place(x=440, y=5, width=120, height=28)

        # Bill List Frame
        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=140, width=200, height=330)

        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sales_List = Listbox(
            sales_Frame,
            font=("goudy old style", 15),
            bg="white",
            yscrollcommand=scrolly.set
        )
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        # Bill Area Frame
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=410, height=330)
        
        lbl_title2 = Label(
            bill_Frame,
            text="Customer Bill Area",
            font=("goudy old style", 20),
            bg="orange"
        ).pack(side=TOP, fill=X)
        
        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area = Text(
            bill_Frame,
            bg="lightyellow",
            yscrollcommand=scrolly2.set
        )
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        # Image
        try:
            self.bill_photo = Image.open("images/cat2.jpg")
            self.bill_photo = self.bill_photo.resize((450, 300))
            self.bill_photo = ImageTk.PhotoImage(self.bill_photo)
            lbl_image = Label(self.root, image=self.bill_photo, bd=0)
            lbl_image.place(x=700, y=110)
        except Exception as ex:
            print(f"Error loading image: {str(ex)}")
            
        # Load initial data
        self.show()

    def get_db_connection(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            return connection
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(err)}")
            return None

    def show(self):
        self.bill_list.clear()
        self.Sales_List.delete(0, END)
        bill_directory = 'bill'
        
        # Create bill directory if it doesn't exist
        if not os.path.exists(bill_directory):
            os.makedirs(bill_directory)
            
        for i in os.listdir(bill_directory):
            if i.split('.')[-1] == 'txt':
                self.Sales_List.insert(END, i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self, ev):
        try:
            index_ = self.Sales_List.curselection()
            file_name = self.Sales_List.get(index_)
            self.bill_area.delete('1.0', END)
            
            with open(f'bill/{file_name}', 'r') as fp:
                self.bill_area.insert(END, fp.read())
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading bill: {str(ex)}")

    def search(self):
        if not self.var_invoice.get():
            messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)
            return
            
        if self.var_invoice.get() in self.bill_list:
            try:
                with open(f'bill/{self.var_invoice.get()}.txt', 'r') as fp:
                    self.bill_area.delete('1.0', END)
                    self.bill_area.insert(END, fp.read())
            except Exception as ex:
                messagebox.showerror("Error", f"Error reading bill: {str(ex)}")
        else:
            messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0', END)
        self.var_invoice.set('')

if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()