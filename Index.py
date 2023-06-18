from tkinter import *
from tkinter import messagebox
import mysql.connector


def login():
    username = user.get()
    password = code.get()

    mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = mycursor.fetchone()
    if username == '' or password == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    elif result:
        root.destroy()
        import mainForm
    else:
        messagebox.showerror("Login Error", "Incorrect username or password.")


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Registration",
)
mycursor = mydb.cursor()

# --------------------------------------------------------
root = Tk()
root.title('Login Page')
root.geometry('925x500+300+200')
root.config(bg='#fff')
root.resizable(False, False)

img = PhotoImage(file='login_components//login.png')
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=480, y=70)

heading = Label(frame, text='SIGN IN', fg='#4491e3', bg='white',
                font=('Terminal', 23))
heading.place(x=100, y=30)


# --------------------------------------------------------
def on_enter(e):
    user.delete(0, 'end')


def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')


usernameImage = PhotoImage(file='login_components//user.png')
usernameLabel = Label(frame, image=usernameImage, compound=LEFT, border=0)
usernameLabel.place(x=0, y=80)

user = Entry(frame, width=25, fg='black', border=0,
             bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=50, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=50, y=107)


# -------------------------------------------------------
def on_enter(e):
    code.delete(0, 'end')


def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')


passwordImage = PhotoImage(file='login_components//password.png')
passwordLabel = Label(frame, image=passwordImage, compound=LEFT, border=0)
passwordLabel.place(x=0, y=150)

code = Entry(frame, width=25, fg='black', border=0,
             bg='white', font=('Microsoft YaHei UI Light', 11))
code.place(x=50, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=50, y=177)

# ----------------------------------------------------------
Button(frame, width=45, pady=7, text='Sign in', anchor='center',
       bg='#57a1f8', fg='white', border=0, command=login).place(x=45, y=204)

root.mainloop()
