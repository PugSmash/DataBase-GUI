import random
from tkinter import *
from tkinter import messagebox as msgbx
from EditingWindow import EditingPage
import sqlite3


class LoginWindow(Tk):

    def __init__(self, *args, **kwargs):
        """
        - The innit function is used to define key values such as width and height of the window
        - It also involves defining the connection and cursor, which allow the accessing and executing of cammands on the
          database
        - The other main function of the __init__ function is to define and place all the gui widget
        """
        super().__init__(*args, **kwargs)  # this initialises the inherited gui class
        self.geometry = "400x400"  # this defines the WidthxHeight
        self.title("Db GUI")  # the title of the gui
        self.con = sqlite3.connect("CoffeeShop.db")  # connection to the database
        self.cur = self.con.cursor()  # the object used to execute sql commands

        # the base frame of the first window

        self.frame = Frame(self, width=400, height=400)  # defining the frame
        self.frame.pack()  # placing the frame

        # Defining each widget

        self.Title_label = Label(self.frame, text="Welcome To The Coffee Shop Db")
        self.username_label = Label(self.frame, text="username:")
        self.username_entry = Entry(self.frame)
        self.password_label = Label(self.frame, text="password:")
        self.password_entry = Entry(self.frame)
        self.login_button = Button(self.frame, text="login", command=self.sign_in)
        self.sign_up_button = Button(self.frame, text="sign up", command=self.sign_up)

        # this is the placing of the widgets

        self.Title_label.place(x=100, y=50)
        self.username_label.place(x=50, y=100)
        self.username_entry.place(x=140, y=100)
        self.password_label.place(x=50, y=150)
        self.password_entry.place(x=140, y=150)
        self.sign_up_button.place(x=30, y=300)
        self.login_button.place(x=300, y=300)

    def sign_up(self):
        """
        - this functions main goal is to handle the signing up of users
        - it is the function called by pressing the sign_up_button
        - First, it checks if either the username entry or the password entry are empty
          if so, it will cause a message box to pop up displaying an error
        - then the username and password are inserted into the database
        """
        if self.username_entry.get() == "" or self.password_entry.get() == "":
            # error message being shown
            msgbx.showerror("", "The Username or Password is blank - please retry")
        else:
            # sql command being executed
            self.cur.execute(
                f"INSERT INTO UserLogin(Username, Password, CustomerID) VALUES (?,?,?)",
                (self.username_entry.get(), self.password_entry.get(), random.randint(1, 1000000)))
            self.con.commit()
            msgbx.showinfo("", "You Are Signed Up")

    def sign_in(self):
        """
        - this function handles the signing in of a user
        - it does an initial check of both inputs to check if they are not empty
        - then, all the entries in the UserLogin table are retrieved
        - they are iteratively compared to the Username and Password
        - if there is a match, the user passes authentication and a new window is created
        -  if there is no match, a message is sent to the user, saying that they have been denied
        """
        if self.username_entry.get() == "" or self.password_entry.get() == "":
            # error message being displayed
            msgbx.showerror("", "The Username or Password is blank - please retry")
        else:
            self.checkInDb(username=self.username_entry.get(), password=self.password_entry.get())

    def checkInDb(self, username, password):
        # selecting all rows in user login and looping through them
        for row in self.cur.execute("SELECT * FROM UserLogin"):
            # indexing the list returned from the the line above to access the username and password
            if row[1] == username and row[2] == password:
                msgbx.showinfo("", "SIGN IN SUCCESSFUL")
                self.con.close()
                edit = EditingPage()
                edit.mainloop()
            else:
                pass
        msgbx.showinfo("", "SIGN IN DENIED")


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
