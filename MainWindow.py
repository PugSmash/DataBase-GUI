from tkinter import *
from tkinter import messagebox as msgbx
import sqlite3


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
        self.table_label = Label(self.frame, text="Table:")
        self.table_entry = Entry(self.frame)
        self.columns_label = Label(self.frame, text="Columns:")
        self.columns_entry = Entry(self.frame)
        self.new_values_label = Label(self.frame, text="New Values:")
        self.new_values_entry = Entry(self.frame)
        self.submit_button = Button(self.frame, text="Submit", command=self.check_mode)
        self.instructions_button = Button(self.frame, text="Instructions", command=self.show_instructions)

        self.mode_label.place(x=100, y=70)
        self.mode_choice.place(x=150, y=70)
        self.table_label.place(x=100, y=120)
        self.table_entry.place(x=150, y=120)
        self.columns_label.place(x=80, y=170)
        self.columns_entry.place(x=150, y=170)
        self.new_values_label.place(x=70, y=220)
        self.new_values_entry.place(x=150, y=220)
        self.submit_button.place(x=100, y=250)
        self.instructions_button.place(x=170, y=250)


        msgbx.showinfo("", """For DELETE - Only delete single Values. The New value will be the value you intend to delete
                              For EDIT - The final value inputed into columns and new_values must be the Primary key of the table with its value
                              ONLY do one table at a time
                              IF entering multimple Values input them with a comma seperating eg - (one,two,three)
                                """)

    def check_mode(self):
        mode = self.drop_down_value.get()
        if mode == "Edit":
            self.edit_data()
        elif mode == "Add":
            self.add_data()
        else:
            self.delete_data()

    def add_data(self):
        print(self.columns_entry.get())
        sql = f"INSERT INTO {self.table_entry.get()}({self.columns_entry.get()}) VALUES({self.columns_entry.get()})"
        self.cur.execute(sql)
        self.con.commit()
        msgbx.showinfo("", "DATA SUCCESSFULLY ADDED")

    def delete_data(self):
        sql = f"DELETE FROM ? WHERE ?=?"
        data = (str(self.table_entry.get()), str(self.columns_entry.get()), str(self.new_values_entry.get()))
        try:
            self.cur.execute(sql, data)
            self.con.commit()
            msgbx.showinfo("", "DATA SUCCESSFULLY DELETED")
        except:
            msgbx.showwarning("COMMAND FAILED - TRY AGAIN")

    def edit_data(self):
        columns = str(self.columns_entry.get()).split(",")
        new_values = str(self.new_values_entry.get()).split(",")
        try:
            for i in range(len(columns) - 1):
                sql = f"UPDATE ? SET ?=? WHERE ?=?"
                self.cur.execute(sql)
                self.con.commit()
                msgbx.showinfo("", "DATA SUCCESSFULLY UPDATED")
        except:
            msgbx.showwarning("COMMAND FAILED - TRY AGAIN")


    def show_instructions(self):
        msgbx.showinfo("", """For DELETE - Only delete single Values. The New value will be the value you intend to delete
                                      For EDIT - The final value inputed into columns and new_values must be the Primary key of the table with its value
                                      ONLY do one table at a time
                                      IF entering multimple Values input them with a comma seperating eg - (one,two,three)
                                        """)