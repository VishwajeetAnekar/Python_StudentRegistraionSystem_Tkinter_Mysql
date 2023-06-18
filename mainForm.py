from tkinter import *
from PIL import ImageTk
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas


# Exit Button
def exit_program():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass


# Export Data
def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pandas.DataFrame(newlist,
                             columns=['Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Date',
                                      'Added Time'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is saved successfully')


def toplevel_data(title, button_text, command):
    global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, genderEntry, dobEntry, screen
    screen = Toplevel(bg='#dff0ee')
    screen.title(title)
    screen.grab_set()

    screen.resizable(False, False)
    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)

    if title == 'Update Student':
        indexing = studentTable.focus()

        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])


# Update data
def update_data():
    query = 'update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query, (nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                             genderEntry.get(), dobEntry.get(), date, currenttime, idEntry.get()))
    con.commit()
    messagebox.showinfo('Success', f'Id {idEntry.get()} is modified successfully', parent=screen)
    screen.destroy()
    show_student()


# Display Data
def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


# Delete Data
def delete_student():
    indexing = studentTable.focus()
    print(indexing)
    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('Deleted', f'Id {content_id} is deleted succesfully')
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


# Search Data
def search_data():
    query = 'select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query, (
        idEntry.get(), nameEntry.get(), emailEntry.get(), phoneEntry.get(), addressEntry.get(), genderEntry.get(),
        dobEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)


# Add Data
def add_data():
    if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
        messagebox.showerror('Error', 'All Feilds are required', parent=screen)

    else:
        try:
            query = 'insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,
                             (idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                              genderEntry.get(), dobEntry.get(), date, currenttime))
            con.commit()
            result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clean the form?',
                                         parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error', 'Id cannot be repeated', parent=screen)
            return

        query = 'select *from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('', END, values=data)


# Database Connection
def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(
                host=hostEntry.get(),
                user=usernameEntry.get(),
                password=passwordEntry.get()
            )
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Invalid Details', parent=connectWindow)
            return

        # Create the database if it doesn't exist
        query = f"CREATE DATABASE IF NOT EXISTS {databaseEntry.get()}"
        mycursor.execute(query)

        # Use the database
        query = f"USE {databaseEntry.get()}"
        mycursor.execute(query)

        # Create the table if it doesn't exist
        query = 'CREATE TABLE IF NOT EXISTS student(id INT NOT NULL PRIMARY KEY, name VARCHAR(30), mobile VARCHAR(' \
                '10), email VARCHAR(30), address VARCHAR(100), gender VARCHAR(20), dob VARCHAR(20), date VARCHAR(50), ' \
                'time VARCHAR(50))'
        mycursor.execute(query)

        connectWindow.destroy()
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)

    connectWindow = Toplevel(bg='#dff0ee')
    connectWindow.grab_set()
    connectWindow.geometry('450x350+500+200')

    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0)

    hostnameLabel = Label(connectWindow, text='Host Name', font=('Garamond', 16), border=0)
    hostnameLabel.grid(row=0, column=0, padx=20)

    hostEntry = Entry(connectWindow, font=('Garamond', 15), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 16))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('Garamond', 15), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 16))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('Garamond', 15), show='*', bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    databaseLabel = Label(connectWindow, text='Database', font=('arial', 16))
    databaseLabel.grid(row=3, column=0, padx=20)

    databaseEntry = Entry(connectWindow, font=('Garamond', 15), bd=2)
    databaseEntry.grid(row=3, column=1, padx=40, pady=20)

    connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=4, columnspan=2)


count = 0
text = ''


def clock():
    global date, currenttime
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)


# Theme User Interface
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('vista')
backgroundImage = ImageTk.PhotoImage(file='MainForm_Component//background.jpg')
bgLabel = Label(root, image=backgroundImage)
bgLabel.place(x=0, y=0)

# screen Size and title
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.resizable(0, 0)
root.title('Registration Form')

datetimeLabel = Label(root, font=('Terminal', 14, 'italic'))
datetimeLabel.place(x=0, y=20)
clock()

heading = Label(root, text='Registration Form(CRUD Application)', font=('Terminal', 28), width=50, bg='#23968a',
                fg='white')
heading.place(x=350, y=20)

# Connect Button
connectButton = ttk.Button(root, text='Connect database', command=connect_database, style='Custom.TButton')
connectButton.place(x=1350, y=20, width=150, height=43)

# left Frame
leftFrame = Frame(root, bg='#b9f0e9')
leftFrame.place(x=10, y=80, width=350, height=700)
logo_image = PhotoImage(file='MainForm_Component//boy.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0, pady=20)

addstudentButton = ttk.Button(leftFrame, text='Add Student', width=30, state=DISABLED,
                              command=lambda: toplevel_data('Add Student', 'Add', add_data), padding=(10, 10))
addstudentButton.grid(row=1, column=0, pady=15, padx=75)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=30, state=DISABLED,
                                 command=lambda: toplevel_data('Search Student', 'Search', search_data),
                                 padding=(10, 10))
searchstudentButton.grid(row=2, column=0, pady=15)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=30, state=DISABLED, command=delete_student,
                                 padding=(10, 10))
deletestudentButton.grid(row=3, column=0, pady=15)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=30, state=DISABLED,
                                 command=lambda: toplevel_data('Update Student', 'Update', update_data),
                                 padding=(10, 10))
updatestudentButton.grid(row=4, column=0, pady=15)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=30, state=DISABLED, command=show_student,
                               padding=(10, 10))
showstudentButton.grid(row=5, column=0, pady=15)

exportstudentButton = ttk.Button(leftFrame, text='Export data', width=30, state=DISABLED, command=export_data,
                                 padding=(10, 10))
exportstudentButton.grid(row=6, column=0, pady=15)

exitButton = ttk.Button(leftFrame, text='Exit', width=30, command=exit_program, padding=(10, 10))
exitButton.grid(row=7, column=0, pady=15)

# Right Frame
rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=1180, height=700)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender',
                                                 'D.O.B', 'Added Date', 'Added Time'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(expand=1, fill=BOTH)

studentTable.heading('Id', text='Id')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile', text='Mobile No')
studentTable.heading('Email', text='Email Address')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Added Date', text='Added Date')
studentTable.heading('Added Time', text='Added Time')

studentTable.column('Id', width=50, anchor=CENTER)
studentTable.column('Name', width=200, anchor=CENTER)
studentTable.column('Email', width=300, anchor=CENTER)
studentTable.column('Mobile', width=200, anchor=CENTER)
studentTable.column('Address', width=150, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('D.O.B', width=200, anchor=CENTER)
studentTable.column('Added Date', width=200, anchor=CENTER)
studentTable.column('Added Time', width=200, anchor=CENTER)

style = ttk.Style()

style.configure('Treeview', rowheight=40, font=('Roboto', 12), fieldbackground='white',
                background='#e6f2f1', )
style.configure('Treeview.Heading', font=('Penna', 16), foreground='#002e28')
style.configure('Custom.TButton', background='#112e2b', foreground='red')

studentTable.config(show='headings')

root.mainloop()
