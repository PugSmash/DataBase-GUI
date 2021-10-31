from tkinter import *
from tkinter import messagebox as msgbx
import sqlite3
import random


class EditingPage(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry = "400x400"
        self.title("Db GUI")
        self.con = sqlite3.connect("CoffeeShop.db")
        self.cur = self.con.cursor()
        self.options = ["Add", "Edit", "Delete"]
        self.drop_down_value = StringVar(self)
        self.drop_down_value.set("Edit")
        self.count = 0

        self.frame = Frame(self, width=400, height=400)
        self.frame.pack()

        self.mode_label = Label(self.frame, text="Mode:")
        self.mode_choice = OptionMenu(self.frame, self.drop_down_value, *self.options)
        self.Username_label = Label(self.frame, text="Username:")
        self.Username_entry = Entry(self.frame)
        self.Password_label = Label(self.frame, text="Password:")
        self.Password_entry = Entry(self.frame)
        self.CustomerID_label = Label(self.frame, text="CustomerID:")
        self.CustomerID_entry = Entry(self.frame)
        self.submit_button = Button(self.frame, text="Submit", command=self.check_mode)
        self.instructions_button = Button(self.frame, text="Instructions", command=self.show_instructions)

        self.mode_label.place(x=100, y=70)
        self.mode_choice.place(x=150, y=70)
        self.Username_label.place(x=80, y=120)
        self.Username_entry.place(x=150, y=120)
        self.Password_label.place(x=80, y=170)
        self.Password_entry.place(x=150, y=170)
        self.CustomerID_label.place(x=70, y=220)
        self.CustomerID_entry.place(x=150, y=220)
        self.submit_button.place(x=100, y=250)
        self.instructions_button.place(x=170, y=250)

        msgbx.showinfo("", """For ADD - Enter the username and password that you want to add, leave the customer ID blank as it will be generated for you
                              FOR EDIT - ENTER updated username and password and enter the Customer ID of the row you want to change
                              FOr Delete - enter the customer ID of the row to  be deleted""")

    def check_mode(self):
        mode = self.drop_down_value.get()
        if mode == "Edit":
            self.edit_data()
        elif mode == "Add":
            self.add_data()
        else:
            self.delete_data()

    def add_data(self):
        print(self.Password_entry.get())
        sql = f"INSERT INTO UserLogin(CustomerID, Username, Password) Values(?,?,?)"
        data = (str(self.Username_entry.get()), str(self.Password_entry.get()), random.randint(1, 1000000))
        self.cur.execute(sql, data)
        self.con.commit()
        msgbx.showinfo("", "DATA SUCCESSFULLY ADDED")

    def delete_data(self):
        sql = f"DELETE FROM UserLogin WHERE CustomerID=?"
        data = (str(self.CustomerID_entry.get()))
        self.cur.execute(sql, data)
        self.con.commit()
        msgbx.showinfo("", "DATA SUCCESSFULLY DELETED")

    def edit_data(self):
        sql = "UPDATE UserLogin SET Username=?, Password=? WHERE CustomerID=?"
        data = (str(self.Username_entry.get()), str(self.Password_entry.get()), self.CustomerID_entry.get())
        self.cur.execute(sql, data)
        self.con.commit()
        msgbx.showinfo("", "DATA SUCCESSFULLY UPDATED")
        msgbx.showwarning("COMMAND FAILED - TRY AGAIN")

    def show_instructions(self):
        msgbx.showinfo("", """For DELETE - Only delete single Values. The New value will be the value you intend to delete
                                      For EDIT - The final value inputed into columns and new_values must be the Primary key of the table with its value
                                      ONLY do one table at a time
                                      IF entering multimple Values input them with a comma seperating eg - (one,two,three)
                                        """)
