import logging
from tkinter import *
from tkinter import messagebox as msgbx
from MainWindow import EditingPage
import sqlite3


class LoginWindow(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry = "400x400"
        self.title("Db GUI")
        self.con = sqlite3.connect("CoffeeShop.db")
        self.cur = self.con.cursor()

        self.frame = Frame(self, width=400, height=400)
        self.frame.pack()

        self.Title_label = Label(self.frame, text="Welcome To The Coffee Shop Db")
        self.username_label = Label(self.frame, text="username:")
        self.username_entry = Entry(self.frame)
        self.password_label = Label(self.frame, text="password:")
        self.password_entry = Entry(self.frame)
        self.login_button = Button(self.frame, text="login", command=self.sign_in)
        self.sign_up_button = Button(self.frame, text="sign up", command=self.sign_up)

        self.Title_label.place(x=100, y=50)
        self.username_label.place(x=50, y=100)
        self.username_entry.place(x=140, y=100)
        self.password_label.place(x=50, y=150)
        self.password_entry.place(x=140, y=150)
        self.sign_up_button.place(x=30, y=300)
        self.login_button.place(x=300, y=300)

    def sign_up(self):
        if self.username_entry.get() == "" or self.password_entry.get() == "":
            msgbx.showerror("", "The Username or Password is blank - please retry")
        else:
            self.cur.execute(
                f"INSERT INTO UserLogin(Username, Password) VALUES (?,?)",
                (self.username_entry.get(), self.password_entry.get()))
            self.con.commit()
            msgbx.showinfo("", "You Are Signed Up")

    def sign_in(self):
        if self.username_entry.get() == "" or self.password_entry.get() == "":
            msgbx.showerror("", "The Username or Password is blank - please retry")
        else:
            self.checkInDb(username=self.username_entry.get(), password=self.password_entry.get())

    def checkInDb(self, username, password):
        for row in self.cur.execute("SELECT * FROM UserLogin"):
            if row[1] == username and row[2] == password:
                msgbx.showinfo("", "SIGN IN SUCCESSFUL")
                edit = EditingPage()
                edit.mainloop()
            else:
                pass
        msgbx.showinfo("", "SIGN IN DENIED")


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
