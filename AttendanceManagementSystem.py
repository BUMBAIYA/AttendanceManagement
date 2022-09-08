from tkinter import *
from tkinter import ttk
import sqlite3 as sq
import time
from datetime import date
from tkinter import messagebox
import os
from EngineeringSubjects import Subjects


class Login:
    """This class is for login window"""
    username = ''
    user_pass = ''
    category = ''
    dept = ''
    year = 0
    PROJECT_DIR = ""

    def __init__(self):
        """Initiating all the widgets in the login window"""
        self.PROJECT_DIR = os.getcwd()
        today_date = date.today()
        self.d2 = today_date.strftime("%B %d,%Y")
        t = time.localtime()
        self.t2 = time.strftime("%H:%M", t)
        self.window = Tk()
        self.window.geometry("800x490")
        self.window.title("Attendance Management System")
        self.window.resizable(0, 0)

        # All variable initialize
        self.username = ''
        self.user_pass = ''
        self.dept = ''
        self.category = ''
        self.error = 0

        self.img = PhotoImage(file="./assets/images/LoginPageImage.png")
        self.login_btn_img = PhotoImage(file="./assets/images/login_btn.png")

        self.canvas = Canvas(self.window, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack(fill="both", expand="yes")

        self.canvas.create_image(0, 0, image=self.img, anchor="nw")

        self.ent1 = Entry(self.canvas, font=('Helvetica', 24), width=12, bg="white")
        self.ent1.place(x=290, y=150)

        self.ent2 = Entry(self.canvas, font=('Arial', 24), show="*", width=12, bg="white")
        self.ent2.place(x=290, y=218)

        self.btn = Button(self.canvas, image=self.login_btn_img, bd=0, bg="#57E186", command=self.password_check)
        self.btn.place(x=318, y=320)

        self.window.mainloop()

    def password_check(self):
        """This function checks all the input is proper or not"""
        self.username = self.ent1.get()
        self.user_pass = self.ent2.get()
        if self.username and self.user_pass == "":
            messagebox.showerror("Error", "Input cannot be empty!!")
        else:
            conn = sq.connect("./demo.db")
            cur = conn.cursor()
            for row in cur.execute(f"SELECT * FROM users"):
                if self.username == row[0] and self.user_pass == row[1]:
                    self.category = row[2]
                    self.dept = row[3]
                    self.year = row[4]
                    cur.execute(f"INSERT INTO login_log (username,pass,category,time,date,dept,year) "
                                f"VALUES ('{self.username}','{self.user_pass}','{self.category}',"
                                f"'{self.t2}','{self.d2}','{self.dept}', '{self.year}')")
                    conn.commit()
                    self.error = 1
                    self.category_check()
            if self.error == 0:
                messagebox.showerror("Login failed", "User or password do not match")

    def category_check(self):
        if self.category == "admin":
            self.window.destroy()
            AdminPage()
        else:
            self.window.destroy()
            Student()


class AdminPage:
    """This class is for admin page"""
    sem = ()
    subjects = ()
    user_year = 0
    department = ''
    user_name = ''
    sem_choice = ''
    d2 = ''
    log_error = 0
    sub = ''
    roll_count = 0
    roll = []
    zeros = []
    data = {}
    new_pass = ''
    PROJECT_DIR = ""

    def __init__(self):
        """Initializing the admin page"""
        today_date = date.today()
        self.d2 = today_date.strftime("%B %d,%Y")
        self.window = Tk()
        self.window.geometry("800x510")
        self.window.title("Attendance Management System : Admin page")
        self.window.config(bg="#dbffdb")
        self.window.resizable(0, 0)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.map("Treeview", background=[('selected', "#c0c0ff")])

        self.conn = sq.connect("./demo.db")
        self.cur = self.conn.cursor()
        result = self.cur.execute(f"SELECT * FROM login_log ORDER BY sr DESC LIMIT 1")
        for row in result:
            self.user_name = row[1]
            self.user_year = row[7]
            self.department = row[6]

        self.log_error = 0
        self.roll_count = 0
        self.subjects = ()
        self.sem_choice = ''
        self.sub = ''
        self.new_pass = ''
        self.roll = []
        self.zeros = []
        self.data = {}

        if self.user_year == 1:
            self.sem = ('I', 'II')
        elif self.user_year == 2:
            self.sem = ('III', 'IV')
        elif self.user_year == 3:
            self.sem = ('V', 'VI')
        elif self.user_year == 4:
            self.sem = ('VII', 'VIII')

        self.user_info = LabelFrame(self.window, text="User info", font='Arial 9 bold', bg="#dbffdb")
        self.user_info.pack(fill='x', expand="yes", padx=10, pady=5)

        self.lbl1 = Label(self.user_info, text=f"Username : {self.user_name}", bg="#dbffdb")
        self.lbl1.grid(row=0, column=0, padx=15, pady=3)

        self.lbl2 = Label(self.user_info, text=f"Department : {self.department}", bg="#dbffdb")
        self.lbl2.grid(row=0, column=1, padx=15, pady=3)

        self.lbl3 = Label(self.user_info, text=f"Year : {self.user_year}", bg="#dbffdb")
        self.lbl3.grid(row=0, column=2, padx=15, pady=3)

        self.mark_att = LabelFrame(self.window, text="Mark Attendance", font='Arial 9 bold', bg="#dbffdb")
        self.mark_att.pack(fill='x', expand="yes", padx=10, pady=5)

        self.choose_sem_frame = LabelFrame(self.mark_att, text="Semester", font='Arial 9 bold', bg="#dbffdb")
        self.choose_sem_frame.pack(fill='x', expand="yes", padx=10, pady=5)

        self.sem1_btn = Button(self.choose_sem_frame, text=f"Semester {self.sem[0]}", command=self.sem1_btn_click)
        self.sem1_btn.grid(row=0, column=0, padx=10, pady=10)

        self.sem2_btn = Button(self.choose_sem_frame, text=f"Semester {self.sem[1]}", command=self.sem2_btn_click)
        self.sem2_btn.grid(row=0, column=1, padx=10, pady=10)

        self.choose_sub_frame = LabelFrame(self.mark_att, text="Subject", font='Arial 9 bold', bg="#dbffdb")
        self.choose_sub_frame.pack(fill='x', expand="yes", padx=10, pady=5)

        self.lbl4 = Label(self.choose_sub_frame, text="Choose Subject", bg="#dbffdb")
        self.lbl4.grid(row=0, column=0, pady=10, padx=10)

        # combobox  creation of the subjects
        self.var = StringVar()
        self.subject_choice = ttk.Combobox(self.choose_sub_frame, width=40, textvariable=self.var,
                                           font='Helvetica 10', state='readonly')
        self.subject_choice['values'] = self.subjects
        self.subject_choice.grid(row=0, column=1, padx=15)

        self.Mark_att_info = LabelFrame(self.mark_att, text="Mark Attendance info", font='Arial 9 bold', bg="#dbffdb")
        self.Mark_att_info.pack(fill='x', expand="yes", padx=10, pady=10)

        self.lbl5 = Label(self.Mark_att_info, bg="#dbffdb")
        self.lbl5.grid(row=0, column=0, pady=5, padx=5)

        self.change_pass_frame = LabelFrame(self.window, text="Change Password", bg="#dbffdb", font='Arial 9 bold')
        self.change_pass_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        self.lbl6 = Label(self.change_pass_frame, text="Enter Old password", bg="#dbffdb")
        self.lbl6.grid(row=0, column=0, pady=5, padx=5)
        self.ent1 = Entry(self.change_pass_frame, width=30, bg="#c0c0ff")
        self.ent1.grid(row=0, column=1, padx=20)

        self.lbl7 = Label(self.change_pass_frame, text="Enter new password", bg="#dbffdb")
        self.lbl7.grid(row=1, column=0, pady=5, padx=5)
        self.ent2 = Entry(self.change_pass_frame, width=30, bg="#c0c0ff")
        self.ent2.grid(row=1, column=1, padx=20)

        self.lbl8 = Label(self.change_pass_frame, text="Confirm new password", bg="#dbffdb")
        self.lbl8.grid(row=2, column=0, pady=5, padx=5)
        self.ent3 = Entry(self.change_pass_frame, width=30, bg="#c0c0ff")
        self.ent3.grid(row=2, column=1, padx=20)

        self.change_pass_btn = Button(self.change_pass_frame, text="Change Password", bg="azure3",
                                      command=self.check_old_pass)
        self.change_pass_btn.grid(row=2, column=3, sticky=E, padx=30)

        self.commands = LabelFrame(self.window, text="Commands", font='Arial 9 bold', bg="#dbffdb")
        self.commands.pack(fill='x', expand="yes", padx=10, pady=10)

        self.mark_att_btn = Button(self.commands, text="Mark Attendance", bg="azure3",
                                   command=self.check_input_subject)
        self.mark_att_btn.grid(row=0, column=1, padx=10, pady=10)

        self.att_log_btn = Button(self.commands, text="Attendance Log", bg="azure3", command=self.attendance_log)
        self.att_log_btn.grid(row=0, column=2, padx=10, pady=10)

        self.logout_btn = Button(self.commands, text="Logout", bg="azure3", command=self.logout)
        self.logout_btn.grid(row=0, column=3, padx=10, pady=10)

        self.initialize_app()

        self.window.mainloop()

    def initialize_app(self):
        self.sem1_btn.config(bg="SeaGreen1", fg="black")
        self.sem2_btn.config(bg="white", fg="black")
        self.lbl4.config(text=f"Select subject from semester {self.sem[0]}")
        self.lbl5.config(text=f"Mark Attendance for {self.d2}, Semester {self.sem[0]}")
        self.sem_choice = self.sem[0]
        self.subjects = Subjects.subject_choose(self.sem[0], self.user_year, self.department)
        self.check_box()

    def check_box(self):
        self.subject_choice['values'] = self.subjects
        self.subject_choice.current(0)

    def sem1_btn_click(self):
        self.sem1_btn.config(bg="SeaGreen1", fg="black")
        self.sem2_btn.config(bg="white", fg="black")
        self.lbl4.config(text=f"Select subject from semester {self.sem[0]}")
        self.lbl5.config(text=f"Mark Attendance for {self.d2}, Semester {self.sem[0]}")
        self.subjects = Subjects.subject_choose(self.sem[0], self.user_year, self.department)
        self.sem_choice = self.sem[0]
        self.check_box()

    def sem2_btn_click(self):
        self.sem2_btn.config(bg="SeaGreen1", fg="black")
        self.sem1_btn.config(bg="white", fg="black")
        self.lbl4.config(text=f"Select subject from semester {self.sem[1]}")
        self.lbl5.config(text=f"Mark Attendance for {self.d2}, Semester {self.sem[1]}")
        self.subjects = Subjects.subject_choose(self.sem[1], self.user_year, self.department)
        self.sem_choice = self.sem[1]
        self.check_box()

    def attendance_log(self):
        self.window.destroy()
        AdminLog(self.user_year, self.department, self.sem)

    def logout(self):
        result = messagebox.askyesno("logout", "Do you want to logout?")
        if result:
            self.window.destroy()
            Login()

    def check_old_pass(self):
        """This function is used to check the old password"""
        if self.ent1.get() != '' and self.ent2.get() != '' and self.ent3.get() != '':
            temp = ''
            result = self.cur.execute(f"SELECT * FROM login_log ORDER BY sr DESC LIMIT 1")
            for row in result:
                temp = row[2]
            if temp == self.ent1.get():
                self.save_new_password()
            else:
                messagebox.showerror("Error", "Old password is wrong!!!")
        else:
            messagebox.showerror("Input Error", "Input cannot be empty!!!")

    def save_new_password(self):
        """This function is used to change the password of user"""
        if self.ent1.get() != '' and self.ent2.get() != '' and self.ent3.get() != '':
            if self.ent2.get() == self.ent3.get():
                self.new_pass = self.ent3.get()
                try:
                    self.cur.execute(f"UPDATE users SET user_pass='{self.new_pass}' WHERE user_name='{self.user_name}'")
                    self.cur.execute(f"UPDATE login_log SET pass='{self.new_pass}' WHERE username='{self.user_name}'")
                    self.conn.commit()
                    messagebox.showinfo("Successful", "Password changed successfully")
                    self.ent1.delete(0, END)
                    self.ent2.delete(0, END)
                    self.ent3.delete(0, END)
                except sq.OperationalError:
                    messagebox.showerror("Error", "Database is not connected to the system!!!")
            else:
                messagebox.showerror("Password Error", "New password do not match!!!")
        else:
            messagebox.showerror("Input error", "Input cannot be empty!!!")

    def check_input_subject(self):
        """This function checks the input for choose subject frame"""
        self.log_error = 0
        if self.var.get() != "":
            if self.var.get() in self.subjects:
                self.sub = self.var.get()
                self.check_attendance_log()
            else:
                messagebox.showerror("Input error", "Choose correct subject!")
        else:
            messagebox.showerror("Input error", "Input cannot be empty")

    def check_attendance_log(self):
        """Checks if attendance for the day is already marked"""
        try:
            for row in self.cur.execute(f"SELECT * FROM '{self.user_year}{self.department}attendance'"):
                if row[0] == self.d2 and row[2] == self.sub:
                    self.log_error = 1
                    messagebox.showerror("Error", f"Attendance is already marked\n{self.d2}, {self.sub}")
            if self.log_error == 0:
                self.window.destroy()
                MarkAttendance(self.user_year, self.department, self.sem_choice, self.sub)
        except Exception as e:
            messagebox.showerror(f"Database Error", {e})


class MarkAttendance:
    roll = []
    roll_count = 1
    counter = 0
    department = ''
    sem = ''
    sub = ''
    user_year = 0

    def __init__(self, a, b, c, d):
        today_date = date.today()
        self.d2 = today_date.strftime("%B %d,%Y")
        self.window = Tk()
        self.window.geometry("800x560")
        self.window.title("Admin Page: Mark Attendance")
        self.window.config(bg="#dbffdb")
        self.window.resizable(0, 0)

        self.conn = sq.connect("./demo.db")
        self.cur = self.conn.cursor()

        self.department = b
        self.sem = c
        self.sub = d
        self.user_year = a
        self.roll = []
        self.roll_count = 1
        self.counter = 0

        self.checked = PhotoImage(file="./assets/images/checked.png")
        self.unchecked = PhotoImage(file="./assets/images/unchecked.png")

        self.style = ttk.Style()

        self.style.theme_use('clam')

        # treeview color
        self.style.configure("Treeview", background="white", foreground="black",
                             rowheight=30, fieldbackground="#c2c2d6")

        # change color theme
        self.style.map("Treeview", background=[('selected', 'invalid', "#7fbacc")], foreground=[('selected', 'black')])

        self.att_info = LabelFrame(self.window, text="Attendance info", font='Arial 9 bold', bg="#dbffdb")
        self.att_info.pack(fill='x', expand="yes", pady=5, padx=10)

        self.lbl1 = Label(self.att_info, text=f"Department: {self.department}", bg="#dbffdb")
        self.lbl1.grid(row=0, column=0, padx=5, pady=10)

        self.lbl2 = Label(self.att_info, text=f"Date: {self.d2}", bg="#dbffdb")
        self.lbl2.grid(row=0, column=3)

        self.lbl1 = Label(self.att_info, text=f"Subject: {self.sub}", bg="#dbffdb")
        self.lbl1.grid(row=1, column=1, padx=5, pady=5)

        self.lbl1 = Label(self.att_info, text=f"Semester: {self.sem}", bg="#dbffdb")
        self.lbl1.grid(row=1, column=0)

        self.lbl1 = Label(self.att_info, text=f"Year: 2", bg="#dbffdb")
        self.lbl1.grid(row=0, column=1)

        self.mark_att = LabelFrame(self.window, text="Mark Attendance", font='Arial 9 bold', bg="#dbffdb")
        self.mark_att.pack(pady=5, padx=10)

        # treeview frame
        self.tree_frame = Frame(self.mark_att)
        self.tree_frame.pack(padx=5, pady=5)

        # create treeview scrollbar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # create treeview
        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
        self.my_tree.pack()

        # create tag for strips
        self.my_tree.tag_configure('checked', image=self.checked, background="#9dff9d")
        self.my_tree.tag_configure('unchecked', image=self.unchecked, background="#ffa7a7")

        # configure scrollbar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define our Column
        self.my_tree['columns'] = ("Roll no", "Name")

        # formatting the columns
        self.my_tree.column("#0", width=150, anchor=W)
        self.my_tree.column("Roll no", anchor=CENTER, width=200)
        self.my_tree.column("Name", anchor=W, width=410)

        # create heading
        self.my_tree.heading("#0", text="Check if present", anchor=CENTER)
        self.my_tree.heading("#1", anchor=CENTER, text="Roll no")
        self.my_tree.heading("#2", anchor=CENTER, text="Name")

        for record in self.cur.execute(f"SELECT * FROM '{self.user_year}{self.department}'"):
            self.my_tree.insert(parent='', index='end', iid=self.counter,
                                values=(f'{record[0]}', f'{record[3]}'), tags='unchecked')
            self.counter += 1

        self.command = LabelFrame(self.window, text="Commands", font='Arial 9 bold', bg="#dbffdb")
        self.command.pack(fill=X, expand="yes", padx=10, pady=10)

        self.abort_btn = Button(self.command, text="Abort", bg="#ff8566", font='Helvetica 9 bold',
                                command=self.abort)
        self.abort_btn.grid(row=0, column=0, pady=10, padx=10)

        self.save_btn = Button(self.command, text="Save Attendance", font='Helvetica 9 bold',
                               bg="#9999ff", command=self.save)
        self.save_btn.grid(row=0, column=1, pady=10, padx=30)

        self.my_tree.bind('<Button 1>', self.toggle_check)

        self.window.mainloop()

    def abort(self):
        """This function is to abort the marking attendance process"""
        result = messagebox.askyesno("Confirm exit", "Do you want to abort\nMarking attendance")
        if result:
            self.window.destroy()
            self.roll.clear()
            AdminPage()

    def toggle_check(self, event):
        """This function toggles the tag of the row"""
        try:
            rowid = self.my_tree.identify_row(event.y)
            tag = self.my_tree.item(rowid, "tags")[0]
            tags = list(self.my_tree.item(rowid, "tags"))
            tags.remove(tag)
            self.my_tree.item(rowid, tags=tags)
            if tag == "checked":
                self.my_tree.item(rowid, tags="unchecked")
            else:
                self.my_tree.item(rowid, tags="checked")
        except Exception as e:
            print(e)

    def save(self):
        """Save the present roll numbers according to their tags"""
        result = messagebox.askyesno("Confirm", "Do you want to mark attendance")
        if result:
            for line in self.my_tree.get_children():
                for value in self.my_tree.item(line)['tags']:
                    if value == "checked":
                        self.roll.append(self.roll_count)
                    self.roll_count += 1
            self.check_if_empty()

    def check_if_empty(self):
        """Checks is no student is checked present"""
        if not self.roll:
            result = messagebox.askyesno("Caution", "No student marked present\nPress Yes to proceed")
            if result:
                self.save_to_database()
        else:
            self.save_to_database()

    def save_to_database(self):
        """This function saves the present roll no into database"""
        try:
            self.roll = ','.join(map(str, self.roll))
            self.cur.execute(
                f"INSERT INTO '{str(self.user_year)}{self.department}attendance' (date,sem,subject,rollno) "
                f"VALUES ('{self.d2}','{self.sem}','{self.sub}','{self.roll}')")
            self.conn.commit()
            messagebox.showinfo("Success", "Attendance marked successfully!!!")
            self.window.destroy()
            AdminPage()
        except Exception as e:
            messagebox.showerror(f"Error", {e})


class AdminLog:
    """student log"""
    count = 0
    sem = ()
    user_year = 0
    department = ''
    sem_choice = ''
    subjects = ()
    selected = ''
    values = []
    selected_subject = ''
    selected_date = ''
    max_roll = 0
    roll = []
    input_error = 0

    def __init__(self, a, b, c):
        """to initialize all the widgets"""
        self.window = Tk()
        self.window.title("Attendance Management System : Admin Log")
        self.window.geometry("800x575")
        self.window.config(bg="#dbffdb")
        self.window.resizable(0, 0)

        self.conn = sq.connect("./demo.db")

        self.sem = c
        self.user_year = a
        self.department = b
        self.sem_choice = ''
        self.count = 0
        self.max_roll = 0
        self.input_error = 0
        self.var = StringVar()
        self.subjects = ()
        self.selected = ''
        self.values = []
        self.roll = []
        self.selected_date = ''
        self.selected_subject = ''

        self.style = ttk.Style()

        # theme
        self.style.theme_use('clam')

        self.style.configure("Treeview", foreground="black",
                             rowheight=25)

        # change color theme
        self.style.map("Treeview", background=[('selected', "#347083")])

        # treeview frame
        self.tree_frame = Frame(self.window)

        # create treeview scrollbar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # create treeview
        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
        self.my_tree.pack()

        # create tag for strips
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="#bebeff")

        # configure scrollbar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define our Column
        self.my_tree['columns'] = ("Date", "Subject", "Present Roll no")

        # formatting the columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Date", anchor=W, width=150)
        self.my_tree.column("Subject", anchor=W, width=250)
        self.my_tree.column("Present Roll no", anchor=W, width=360)

        # create heading
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("Date", anchor=W, text="Date")
        self.my_tree.heading("Subject", anchor=W, text="Subject")
        self.my_tree.heading("Present Roll no", anchor=W, text="Present Roll no")

        self.button_frame = LabelFrame(self.window, text="Semester", font='Arial 9 bold')
        self.button_frame.config(bg="#dbffdb")
        self.button_frame.pack(fill="x", expand="yes", padx=10)

        self.sem1_btn = Button(self.button_frame, text=f"Semester {self.sem[0]}", command=self.sem1_btn_click)
        self.sem1_btn.grid(row=0, column=0, padx=10, pady=10)

        self.sem2_btn = Button(self.button_frame, text=f"Semester {self.sem[1]}", command=self.sem2_btn_click)
        self.sem2_btn.grid(row=0, column=1, padx=10, pady=10)

        self.back_btn = Button(self.button_frame, text="Back", bg="azure3", command=self.back_button)
        self.back_btn.grid(row=0, column=2, padx=10, pady=10)

        self.choose_sub = LabelFrame(self.window, text="Subject", font='Arial 9 bold')
        self.choose_sub.config(bg="#dbffdb")
        self.choose_sub.pack(fill="x", expand="yes", padx=10)

        self.lbl1 = Label(self.choose_sub, font='Helvetica 10', bg="#dbffdb")
        self.lbl1.grid(row=0, column=0, padx=10)

        # combobox  creation of the subjects
        self.subject_choice = ttk.Combobox(self.choose_sub, width=40, textvariable=self.var,
                                           font='Helvetica 10', state='readonly')
        self.subject_choice['values'] = self.subjects
        self.subject_choice.grid(row=0, column=1, padx=15)

        self.enter_btn = Button(self.choose_sub, text="Refresh Table", bg="azure3", command=self.input_check)
        self.enter_btn.grid(row=0, column=3, padx=10, pady=10)

        # edit label frame
        self.edit_frame = LabelFrame(self.window, text=f"Edit Data",
                                     font='Helvetica 9 bold')
        self.edit_frame.config(bg="#dbffdb")

        self.note_lbl = Label(self.edit_frame, bg="#dbffdb", text="Note:", font="Helvetica 9 bold")
        self.note_lbl.grid(row=0, column=0, pady=10)

        self.lbl = Label(self.edit_frame, bg="#dbffdb", text="Double Click the log to edit")
        self.lbl.grid(row=0, column=1, pady=10)

        self.entry = Entry(self.edit_frame, width=60)
        self.entry.grid(row=0, column=2, padx=40)

        # commands label frame
        self.user_commands = LabelFrame(self.window, text="Commands", font='Helvetica 9 bold', bg="#dbffdb")

        self.edit_button = Button(self.user_commands, text="Edit Roll No", bg="azure3", command=self.check_empty_entry)
        self.edit_button.grid(row=0, column=0, padx=10, pady=10)

        self.delete_row = Button(self.user_commands, text="Delete data", bg="azure3", command=self.remove_row)
        self.delete_row.grid(row=0, column=1, padx=10)

        self.cur = self.conn.cursor()
        for _ in self.cur.execute(f"SELECT * FROM '{self.user_year}{self.department}'"):
            self.max_roll += 1

        self.initialize_app()

        self.my_tree.bind('<Button 1>', self.select_record)

        self.window.mainloop()

    def initialize_app(self):
        self.sem1_btn.config(bg="SeaGreen1", fg="black")
        self.sem2_btn.config(bg="white", fg="black")
        self.lbl1.config(text=f"Select subject from semester {self.sem[0]}")
        self.sem_choice = self.sem[0]
        self.subjects = Subjects.subject_choose(self.sem[0], self.user_year, self.department)
        for record in self.cur.execute(
                f"SELECT * FROM '{self.user_year}{self.department}attendance' "
                f"WHERE sem='{self.sem_choice}' AND subject='{self.subjects[0]}'"):
            if self.count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=self.count, text='',
                                    values=(record[0], record[2], record[3]), tag=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=self.count, text='',
                                    values=(record[0], record[2], record[3]), tag=('oddrow',))
            self.count += 1
        self.tree_frame.pack(pady=10)
        self.edit_frame.pack(fill="x", expand="yes", padx=10)
        self.user_commands.pack(fill='x', expand="yes", padx=10)
        self.check_box()

    def back_button(self):
        self.window.destroy()
        AdminPage()

    def check_box(self):
        # combobox  creation of the year
        self.subject_choice['values'] = self.subjects
        self.subject_choice.grid(row=0, column=1, padx=15)
        self.subject_choice.current(0)

    def sem1_btn_click(self):
        self.sem1_btn.config(bg="SeaGreen1", fg="black")
        self.sem2_btn.config(bg="white", fg="black")
        self.lbl1.config(text=f"Select subject from semester {self.sem[0]}")
        self.subjects = Subjects.subject_choose(self.sem[0], self.user_year, self.department)
        self.sem_choice = self.sem[0]
        self.check_box()

    def sem2_btn_click(self):
        self.sem2_btn.config(bg="SeaGreen1", fg="black")
        self.sem1_btn.config(bg="white", fg="black")
        self.lbl1.config(text=f"Select subject from semester {self.sem[1]}")
        self.subjects = Subjects.subject_choose(self.sem[1], self.user_year, self.department)
        self.sem_choice = self.sem[1]
        self.check_box()

    def remove_row(self):
        result = messagebox.askyesno("Confirm deleting process", "Data will be permanently deleted!\nProceed carefully")
        if result:
            x = self.my_tree.selection()
            for record in x:
                self.my_tree.delete(record)
            self.cur.execute(f"DELETE FROM '{self.user_year}{self.department}attendance' "
                             f"WHERE date='{self.selected_date}' AND subject='{self.selected_subject}'")
            self.conn.commit()

    def input_check(self):
        if self.var.get() != '':
            if self.var.get() in self.subjects:
                self.refresh_button()
            else:
                messagebox.showerror("Input error", "Choose correct subject!")
        else:
            messagebox.showerror("Input error", "Subject input cannot be empty!\nChoose correct subject!")

    def refresh_button(self):
        self.tree_frame.pack(pady=10)
        self.count = 0
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)
        for record in self.cur.execute(
                f"SELECT * FROM '{self.user_year}{self.department}attendance' "
                f"WHERE sem='{self.sem_choice}' AND subject='{self.var.get()}'"):
            if self.count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=self.count, text='',
                                    values=(record[0], record[2], record[3]), tag=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=self.count, text='',
                                    values=(record[0], record[2], record[3]), tag=('oddrow',))
            self.count += 1
        self.tree_frame.pack(pady=10)

    def select_record(self, e):
        try:
            # clear record
            self.entry.delete(0, END)

            # Grab record
            self.selected = self.my_tree.focus()

            # Grab values record
            self.values = self.my_tree.item(self.selected, 'values')

            # Enter the value to entry box
            self.entry.insert(0, self.values[2])
            self.selected_subject = self.values[1]
            self.selected_date = self.values[0]

            self.lbl.config(text=f"{self.values[0]}, {self.var.get()}")
            self.note_lbl.config(text="")
        except:
            pass

    def check_empty_entry(self):
        if self.entry.get() == '':
            result = messagebox.askyesno("Caution",
                                         f"Proceed carefully!\nNo student will be marked present for"
                                         f"\n{self.selected_date}, {self.selected_subject}")
            if result:
                self.roll_check()
        else:
            self.roll_check()

    def roll_check(self):
        self.input_error = 0
        self.roll = []
        temp = self.entry.get().split(",")
        if self.entry.get() != '':
            try:
                for i in range(len(temp)):
                    temp[i] = int(temp[i])
                    if temp[i] > self.max_roll:
                        messagebox.showerror(f"Input error", f"Entered roll no {temp[i]} does not exist in class"
                                                             f"\nClass has only {self.max_roll} students")
                        self.input_error = 1
                [self.roll.append(x) for x in temp if x not in self.roll]
                self.roll.sort()
                self.edit_database()
            except ValueError:
                messagebox.showerror("Input error", "Check input!\nAlphabet not allowed in edit entry")
        else:
            self.cur.execute(f"UPDATE '{self.user_year}{self.department}attendance' SET rollno='' "
                             f"WHERE date='{self.selected_date}' AND subject='{self.selected_subject}'")
            self.conn.commit()
            self.refresh_button()

    def edit_database(self):
        if self.input_error == 0:
            roll = ','.join(map(str, self.roll))
            try:
                self.cur.execute(f"UPDATE '{self.user_year}{self.department}attendance' SET rollno='{roll}' "
                                 f"WHERE date='{self.selected_date}' AND subject='{self.selected_subject}'")
                self.conn.commit()
                messagebox.showinfo("Success", f"Successfully Edited the present roll"
                                               f"\nFor {self.selected_date},{self.selected_subject}")
                self.refresh_button()
            except Exception as e:
                print(e)


class Student:
    """Displays student log window"""
    user_name = ''
    name = ''
    user_roll = ''
    user_year = ''
    department = ''
    sem = ()
    subjects = ()
    sem_choice = ''
    count = 0
    present_roll = ()
    total = 0
    present_count = 0
    absent_count = 0
    percentage = 0

    def __init__(self):
        self.window = Tk()
        self.window.geometry("800x590")
        self.window.title("Attendance Management System : Student Log")
        self.window.config(bg="#dbffdb")
        self.window.resizable(0, 0)

        self.style = ttk.Style()

        # theme
        self.style.theme_use('clam')

        # treeview color
        self.style.configure("Treeview", foreground="black",
                             rowheight=25)

        # change color theme
        self.style.map("Treeview", background=[('selected', "#347083")])

        self.conn = sq.connect("./demo.db")
        self.cur = self.conn.cursor()
        for row in self.cur.execute(f"SELECT * FROM login_log ORDER BY sr DESC LIMIT 1"):
            self.user_name = row[1]
            self.user_year = row[7]
            self.department = row[6]
        for result in self.cur.execute(f"SELECT * FROM '{self.user_year}{self.department}' "
                                       f"WHERE user_name='{self.user_name}'"):

            self.name = result[3]
            self.user_roll = result[0]
        if self.user_year == 1:
            self.sem = ('I', 'II')
        elif self.user_year == 2:
            self.sem = ('III', 'IV')
        elif self.user_year == 3:
            self.sem = ('V', 'VI')
        elif self.user_year == 4:
            self.sem = ('VII', 'VIII')

        self.sem_choice = ''
        self.count = 0
        self.total = 0
        self.present_count = 0
        self.absent_count = 0
        self.percentage = 0
        self.present_roll = ()

        self.user_info_frame = LabelFrame(self.window, text="User Info", font='Arial 9 bold', bg="#dbffdb")
        self.user_info_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        self.lbl1 = Label(self.user_info_frame, text=f"Name : {self.name}", bg="#dbffdb")
        self.lbl1.grid(row=0, column=0, padx=10, pady=5)

        self.lbl2 = Label(self.user_info_frame, text=f"Year : {self.user_year}", bg="#dbffdb")
        self.lbl2.grid(row=0, column=1, padx=10, pady=5)

        self.lbl3 = Label(self.user_info_frame, text=f"Department : {self.department}", bg="#dbffdb")
        self.lbl3.grid(row=0, column=2, padx=10, pady=5)

        self.lbl7 = Label(self.user_info_frame, text=f"Roll No.: {self.user_roll}", bg="#dbffdb")
        self.lbl7.grid(row=0, column=3, padx=10, pady=5)

        self.logout_btn = Button(self.user_info_frame, text="Logout", bg="azure3", command=self.logout)
        self.logout_btn.grid(row=0, column=5, padx=10, pady=5)

        self.button_frame = LabelFrame(self.window, text="Semester", font='Arial 9 bold')
        self.button_frame.config(bg="#dbffdb")
        self.button_frame.pack(fill="x", expand="yes", padx=10)

        self.sem1_btn = Button(self.button_frame, text=f"Semester {self.sem[0]}", command=self.sem1_btn_click)
        self.sem1_btn.grid(row=0, column=0, padx=10, pady=10)

        self.sem2_btn = Button(self.button_frame, text=f"Semester {self.sem[1]}", command=self.sem2_btn_click)
        self.sem2_btn.grid(row=0, column=1, padx=10, pady=10)

        # treeview frame
        self.tree_frame = Frame(self.window)

        # create treeview scrollbar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # create treeview
        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
        self.my_tree.pack()

        # create tag for strips
        self.my_tree.tag_configure('present', background="#9dff9d")
        self.my_tree.tag_configure('absent', background="#ffa7a7")

        # configure scrollbar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define our Column
        self.my_tree['columns'] = ("Date", "Subject", "Attendance")

        # formatting the columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Date", anchor=W, width=150)
        self.my_tree.column("Subject", anchor=W, width=250)
        self.my_tree.column("Attendance", anchor=W, width=360)

        # create heading
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("Date", anchor=W, text="Date")
        self.my_tree.heading("Subject", anchor=W, text="Subject")
        self.my_tree.heading("Attendance", anchor=W, text="Attendance")

        self.choose_sub = LabelFrame(self.window, text="Subject", font='Arial 9 bold')
        self.choose_sub.config(bg="#dbffdb")
        self.choose_sub.pack(fill="x", expand="yes", padx=10)

        self.lbl4 = Label(self.choose_sub, font='Helvetica 10', bg="#dbffdb")
        self.lbl4.grid(row=0, column=0, padx=10)

        # combobox  creation of the subjects
        self.var = StringVar()
        self.subject_choice = ttk.Combobox(self.choose_sub, width=40, textvariable=self.var,
                                           font='Helvetica 10', state='readonly')
        self.subject_choice['values'] = self.subjects
        self.subject_choice.grid(row=0, column=1, padx=15)

        self.enter_btn = Button(self.choose_sub, text="Refresh Table", bg="azure3", command=self.refresh_button)
        self.enter_btn.grid(row=0, column=3, padx=10, pady=10)

        self.att_info_frame = LabelFrame(self.window, text="Attendance Info", font='Arial 9 bold', bg="#dbffdb")

        self.lbl5 = Label(self.att_info_frame, bg="#dbffdb")
        self.lbl5.grid(row=0, column=0, pady=10)

        self.lbl6 = Label(self.att_info_frame, bg="#dbffdb")
        self.lbl6.grid(row=0, column=1, padx=10)

        self.initialize_app()

        self.window.mainloop()

    def initialize_app(self):
        self.sem1_btn.config(bg="SeaGreen1", fg="black")
        self.sem2_btn.config(bg="white", fg="black")
        self.lbl4.config(text=f"Select subject from semester {self.sem[0]}")
        self.sem_choice = self.sem[0]
        self.subjects = Subjects.subject_choose(self.sem[0], self.user_year, self.department)
        for record in self.cur.execute(
                f"SELECT * FROM '{self.user_year}{self.department}attendance' "
                f"WHERE sem='{self.sem_choice}' AND subject='{self.subjects[0]}'"):
            temp1 = record[3].split(",")
            for i in range(len(temp1)):
                temp1[i] = int(temp1[i])
                self.present_roll = tuple(temp1)
            if self.user_roll in self.present_roll:
                self.my_tree.insert(parent='', index='end', iid=self.count, text='',
                                    values=(record[0], record[2], "Present"), tag='present')
                self.present_count += 1
            else:
                self.my_tree.insert(parent='', index='end', iid=self.count, text='',
                                    values=(record[0], record[2], "Absent"), tag='absent')
                self.absent_count += 1
            self.count += 1
            self.total += 1
        self.calculate_percentage(self.present_count, self.total)
        self.tree_frame.pack(pady=10)
        self.lbl5.config(text=f"Total Lecture: {self.total}   "
                              f"Present: {self.present_count}   Absent: {self.absent_count}")
        self.att_info_frame.pack(fill="x", expand="yes", padx=10, pady=10)
        self.check_box()

    def calculate_percentage(self, a, b):
        if b != 0:
            temp = (a * 100) / b
            percentage = round(temp, 2)
            if percentage <= 35:
                self.lbl6.config(text=f"Percentage: {percentage}%", bg="#ff8181", fg="black")
            elif 35 < percentage < 75:
                self.lbl6.config(text=f"Percentage: {percentage}%", bg="#ffff32", fg="black")
            elif percentage >= 75:
                self.lbl6.config(text=f"Percentage: {percentage}%", bg="#57ff57", fg="black")
        else:
            self.lbl6.config(text="No Attendance record available", bg="#ff0000", fg="white")

    def sem1_btn_click(self):
        self.sem1_btn.config(bg="SeaGreen1", fg="black")
        self.sem2_btn.config(bg="white", fg="black")
        self.lbl4.config(text=f"Select subject from semester {self.sem[0]}")
        self.subjects = Subjects.subject_choose(self.sem[0], self.user_year, self.department)
        self.sem_choice = self.sem[0]
        self.check_box()

    def sem2_btn_click(self):
        self.sem2_btn.config(bg="SeaGreen1", fg="black")
        self.sem1_btn.config(bg="white", fg="black")
        self.lbl4.config(text=f"Select subject from semester {self.sem[1]}")
        self.subjects = Subjects.subject_choose(self.sem[1], self.user_year, self.department)
        self.sem_choice = self.sem[1]
        self.check_box()

    def check_box(self):
        # combobox  creation of the year
        self.subject_choice['values'] = self.subjects
        self.subject_choice.grid(row=0, column=1, padx=15)
        self.subject_choice.current(0)

    def logout(self):
        result = messagebox.askyesno("logout", "Do you want to logout?")
        if result:
            self.window.destroy()
            Login()

    def refresh_button(self):
        self.total = 0
        self.present_count = 0
        self.absent_count = 0
        self.tree_frame.pack(pady=10)
        self.count = 0
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)
        for record in self.cur.execute(
                f"SELECT * FROM '{self.user_year}{self.department}attendance' "
                f"WHERE sem='{self.sem_choice}' AND subject='{self.var.get()}'"):
            temp1 = record[3].split(",")
            for i in range(len(temp1)):
                temp1[i] = int(temp1[i])
                self.present_roll = tuple(temp1)
            if self.user_roll in self.present_roll:
                self.my_tree.insert(parent='', index='end', iid=self.count, text='',
                                    values=(record[0], record[2], "Present"), tag='present')
                self.present_count += 1
            else:
                self.my_tree.insert(parent='', index='end', iid=self.count, text='',
                                    values=(record[0], record[2], "Absent"), tag='absent')
                self.absent_count += 1
            self.count += 1
            self.total += 1
        self.lbl5.config(text=f"Total Lecture: {self.total}   "
                              f"Present: {self.present_count}   Absent: {self.absent_count}")
        self.tree_frame.pack(pady=10)
        self.calculate_percentage(self.present_count, self.total)


if __name__ == '__main__':
    login = Login()
