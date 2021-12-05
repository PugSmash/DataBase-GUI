from tkinter import *
from tkinter import messagebox as msgbx
import sqlite3
import random


class EditingPage(Tk):
    def __init__(self, *args, **kwargs):
        """
         - The innit function is used to define key values such as width and height of the window
        - It also involves defining the connection and cursor, which allow the accessing and executing of cammands on the
          database
        - The other main function of the __init__ function is to define and place all the gui widget
        - there is also an information message sent to the user, advising

        """
        super().__init__(*args, **kwargs)
        self.geometry = "400x400"
        self.title("Db GUI")
        self.con = sqlite3.connect("CoffeeShop.db")
        self.cur = self.con.cursor()
        # options contains the three options for the user
        self.options = ["Add", "Edit", "Delete"]
        self.drop_down_value = StringVar(self)
        self.drop_down_value.set("Edit")
        self.count = 0

        # base frame
        self.frame = Frame(self, width=400, height=400)
        self.frame.pack()
        # widgets for the gui
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
        # the placements for the widgets
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

        # information for the user on how to use the program
        msgbx.showinfo("", """For ADD - Enter the username and password that you want to add, leave the customer ID blank as it will be generated for you 
                                      - seperate multiple values with commas
                              FOR EDIT - ENTER updated username and password and enter the Customer ID of the row you want to change
                              FOr Delete - enter the customer ID of the row to  be deleted""")

    # checks the mode that the user wants to use
    def check_mode(self):
        """
        - this function is run when the submit button is pressed
        - it will run a function based on the option selected by the user
        """
        mode = self.drop_down_value.get()
        if mode == "Edit":
            self.edit_data()
        elif mode == "Add":
            self.add_data()
        else:
            self.delete_data()

    # Adding Data
    def add_data(self):
        """
        - this function adds data to the table UserLogin
        - it has a try, except clause to allow for multiple insertions at once separated by commas
        - this allows an error from the split() function to be caught and for the single entry code to be applied
        - each triplet of data is added iteratively to the database

        """
        try:
            sql = f"INSERT INTO UserLogin(Username, Password, CustomerID) Values(?,?,?)"
            # this pulls the data from the inputs and converts it to strings to allow for string manipulation
            data = (str(self.Username_entry.get()), str(self.Password_entry.get()), random.randint(1, 1000000000000))
            # this creates lists of each username and password inputted by the user
            usernames = data[0].split(",")
            passwords = data[1].split(",")
            # this loops through, inputting each row in the tables
            for i in range(len(usernames)):
                data = (str(usernames[(i-1)]), str(passwords[i-1]), random.randint(1, 1000000000000))
                self.cur.execute(sql, data)
        except Exception:
            # this inputs a single row into the table
            sql = f"INSERT INTO UserLogin(Username, Password, CustomerID) Values(?,?,?)"
            data = (str(self.Username_entry.get()), str(self.Password_entry.get()), random.randint(1, 1000000000000))
            self.cur.execute(sql, data)
        self.con.commit()
        msgbx.showinfo("", "DATA SUCCESSFULLY ADDED")

    # Deleting Data
    def delete_data(self):
        """
        - this function allows the deleting of rows of data
        - it takes the customer ID (primary key) and deletes the corresponding rows
        - it can handle both single and multiple row deletions using the try, execpt clause
        """
        try:
            # used for multiple deletions
            sql = f"DELETE FROM UserLogin WHERE CustomerID=?"
            # the customer ID is retrieved from the input and is converted to a string
            data = (str(self.CustomerID_entry.get()))
            # a list of customer IDs is created
            Customer_IDs = data.split(",")
            # each customer ID is iterated over and the row is deleted
            for i in range(len(Customer_IDs)):
                data = (str(Customer_IDs[(i-1)]),)
                self.cur.execute(sql, data)
        except Exception:
            # used for single deletioncs
            sql = f"DELETE FROM UserLogin WHERE CustomerID=?"
            data = (str(self.CustomerID_entry.get()),)
            self.cur.execute(sql, data)
        self.con.commit()
        msgbx.showinfo("", "DATA SUCCESSFULLY DELETED")

    # Edit data
    def edit_data(self):
        """
        - this function allows for the editing of multiple rows
        - you can change the username and password of a user by inputting the username, password and customer ID
        - it can handle multiple or single updates
        - this is enabled by the try and except clause
        """
        try:
            sql = "UPDATE UserLogin SET Username=?, Password=? WHERE CustomerID=?"
            # this retrieves the data and converts each one to a string
            data = (str(self.Username_entry.get()), str(self.Password_entry.get()), str(self.CustomerID_entry.get()))
            # these create lists of the Username, Password and CustomerID
            usernames = data[0].split(",")
            passwords = data[1].split(",")
            Customer_IDs = data[2].split(",")
            # each set of values is iterated over and the rows are each updated
            for i in range(len(usernames)):
                data = (str(usernames[(i-1)]), str(passwords[i-1]), str(Customer_IDs[i-1]))
                self.cur.execute(sql, data)
        except Exception:
            # this handles the single row updates
            sql = "UPDATE UserLogin SET Username=?, Password=? WHERE CustomerID=?"
            data = (str(self.Username_entry.get()), str(self.Password_entry.get()), self.CustomerID_entry.get())
            self.cur.execute(sql, data)
        self.con.commit()
        msgbx.showinfo("", "DATA SUCCESSFULLY UPDATED")

    def show_instructions(self):
        """
        - this function creates a messagebox to instruct the user on how to user the program
        """
        msgbx.showinfo("", """For ADD - Enter the username and password that you want to add, leave the customer ID blank as it will be generated for you
                              FOR EDIT - ENTER updated username and password and enter the Customer ID of the row you want to change
                              FOr Delete - enter the customer ID of the row to  be deleted
                                        """)
