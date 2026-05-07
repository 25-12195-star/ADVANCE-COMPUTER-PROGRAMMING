from ast import pattern
import datetime
from tkinter import *
from tkinter import messagebox
from turtle import title, width
from PIL import Image, ImageTk  # pip install Pillow
from tkinter import ttk
import sqlite3
from tkinter import Label
from tkvideo import tkvideo  # pip install tkvideo
import time
import math
from PIL import ImageDraw
import re


def create_db():
    con = sqlite3.connect(database="rms.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            s_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            sr_code TEXT,
            section TEXT,
            program TEXT,
            gender TEXT
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_name TEXT,
        prelim REAL,
        midterm REAL,
        finals REAL,
        FOREIGN KEY(student_id) REFERENCES student(s_id)
        )
        """)
    
    
    
    con.commit()
    con.close()

class SearchStudent:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Student")
        self.root.geometry("1000x600+200+100")
        self.root.config(bg="white")

        self.var_search = StringVar()

        # TITLE
        title = Label(
            self.root,
            text="Search Student",
            font=("goudy old style", 25, "bold"),
            bg="#00117c",
            fg="white"
        )
        title.pack(fill=X)

        # SEARCH LABEL
        Label(
            self.root,
            text="Enter Name or SR Code",
            font=("times new roman", 15, "bold"),
            bg="white"
        ).place(x=20, y=70)

        # SEARCH ENTRY
        Entry(
            self.root,
            textvariable=self.var_search,
            font=("times new roman", 15),
            bg="#AAADAE"
        ).place(x=250, y=70, width=250)

        # SEARCH BUTTON
        Button(
            self.root,
            text="Search",
            font=("times new roman", 13, "bold"),
            bg="#00117c",
            fg="white",
            command=self.search_student
        ).place(x=520, y=68, width=120, height=35)

        # TABLE FRAME
        frame = Frame(self.root, bd=2, relief=RIDGE)
        frame.place(x=20, y=130, width=950, height=430)

        scroll_y = Scrollbar(frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.table = ttk.Treeview(
            frame,
            columns=("id","no", "name", "sr", "section", "program", "gender"),
            show="headings",
            yscrollcommand=scroll_y.set
        )

        scroll_y.config(command=self.table.yview)

        # HEADINGS
        self.table.heading("id", text="ID")
        self.table.column("id", width=0, stretch=NO)
        self.table.heading("no", text="No.")
        self.table.heading("name", text="Student Name")
        self.table.heading("sr", text="SR Code")
        self.table.heading("section", text="Section")
        self.table.heading("program", text="Program")
        self.table.heading("gender", text="Gender")

        # CENTER
        for col in ("id", "no", "name", "sr", "section", "program", "gender"):
            self.table.heading(col, anchor=CENTER)
            self.table.column(col, anchor=CENTER)

        self.table.pack(fill=BOTH, expand=1)

    def search_student(self):

        key = self.var_search.get()

        con = sqlite3.connect("rms.db")
        cur = con.cursor()

        cur.execute("""
        SELECT s_id, name, sr_code, section, program, gender
        FROM student
        WHERE name LIKE ? OR sr_code LIKE ?
        """, (f"%{key}%", f"%{key}%"))

        rows = cur.fetchall()

        self.table.delete(*self.table.get_children())

        for i, row in enumerate(rows, start=1):
                self.table.insert("", END, values=(
                        row[0],   # hidden id
                        i,        # No.
                        row[1],   # name
                        row[2],   # sr_code
                        row[3],   # section
                        row[4],   # program
                        row[5]    # gender
    ))

        con.close()

class ViewStudentResult:
        def __init__(self, root):
                self.root = root
                self.root.title("View Student Result")
                self.root.geometry("1500x850+0+0")
                self.root.config(bg="white")

                title = Label(self.root, text="View Student Result",
                      font=("goudy old style", 25, "bold"),
                      bg="#0e186c", fg="white")
                title.pack(fill=X)
                
        # VARIABLES
                self.var_program = StringVar()
                self.var_section = StringVar()
                self.var_search = StringVar()

                Label(self.root, text="Search (Name / SR Code)",
                        font=("times new roman", 14, "bold"),
                        bg="white").place(x=800, y=60)

                Entry(self.root, textvariable=self.var_search,
                        font=("times new roman", 14),
                        bg="#AAADAE").place(x=1020, y=60, width=200)

                Button(self.root, text="Search",
                        font=("times new roman", 12, "bold"),
                        bg="#00117c",
                        fg="white",
                        command=self.search_student).place(x=1230, y=60, width=100, height=30)

        # PROGRAM
                Label(self.root, text="Program", font=("times new roman", 14, "bold"),bg="white").place(x=20, y=60)
                self.cmb_program = ttk.Combobox(self.root, textvariable=self.var_program, state="readonly")
                self.cmb_program.place(x=100, y=60, width=200)
                self.cmb_program.bind("<<ComboboxSelected>>", self.load_section)

        # SECTION
                Label(self.root, text="Section", font=("times new roman", 14, "bold"),bg="white").place(x=450, y=60)
                self.cmb_section = ttk.Combobox(self.root, textvariable=self.var_section, state="readonly")
                self.cmb_section.place(x=520, y=60, width=200)
                self.cmb_section.bind("<<ComboboxSelected>>", self.load_students)

        # TABLE
                frame = Frame(self.root, bd=2, relief=RIDGE)
                frame.place(x=20, y=120, width=1450, height=650)

                scroll_y = Scrollbar(frame, orient=VERTICAL)
                scroll_y.pack(side=RIGHT, fill=Y)       

                self.table = ttk.Treeview(frame,
                columns=("no", "name", "sr","prelim", "midterm", "finals", "avg", "remarks"),
                show="headings",
                yscrollcommand=scroll_y.set)

                scroll_y.config(command=self.table.yview)

                self.table.heading("no", text="No.")
                self.table.heading("name", text="Student Name")
                self.table.heading("sr", text="SR Code")
                self.table.heading("prelim", text="Prelim")
                self.table.heading("midterm", text="Midterm")
                self.table.heading("finals", text="Finals")
                self.table.heading("avg", text="Average")
                self.table.heading("remarks", text="Remarks")
                
                # CENTER TABLE TEXT
                for col in ("no", "name", "sr", "prelim", "midterm", "finals", "avg", "remarks"):
                        self.table.column(col, anchor=CENTER)

# CENTER HEADINGS
                for col in ("no", "name", "sr", "prelim", "midterm", "finals", "avg", "remarks"):
                        self.table.heading(col, anchor=CENTER)

                self.table.column("no", width=50)
                self.table.column("name", width=200)
                self.table.column("sr", width=120)
                self.table.column("prelim", width=100)
                self.table.column("midterm", width=100)
                self.table.column("finals", width=100)
                self.table.column("avg", width=100)
                self.table.column("remarks", width=100)

                self.table.pack(fill=BOTH, expand=1)

                self.load_programs()
                
                
    # LOAD PROGRAMS
        def load_programs(self):
                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                cur.execute("SELECT DISTINCT program FROM student")
                rows = cur.fetchall()

                self.cmb_program["values"] = [i[0] for i in rows]
                con.close()

    # LOAD SECTION
        def load_section(self, event):
                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                cur.execute("SELECT DISTINCT section FROM student WHERE program=?",
                    (self.var_program.get(),))
                rows = cur.fetchall()

                self.cmb_section["values"] = [i[0] for i in rows]
                con.close()

                # LOAD STUDENTS + RESULT
                
        def load_students(self, event):
                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                cur.execute("""
                SELECT s.name, s.sr_code,
                c.prelim, c.midterm, c.finals
                FROM student s
                LEFT JOIN course c ON s.s_id = c.student_id
                WHERE s.program=? AND s.section=?
                """, (self.var_program.get(), self.var_section.get()))

                rows = cur.fetchall()
                con.close()

                self.table.delete(*self.table.get_children())

                for i, row in enumerate(rows, start=1):

                        p = row[2]
                        m = row[3]
                        f = row[4]

                        grades = [g for g in [p, m, f] if g is not None]

                        if grades:
                                avg = sum(grades) / len(grades)
                        else:
                                avg = 0

                        if avg == 0:
                                remarks = "No Grade"
                        elif avg >= 75:
                                remarks = "Passed"
                        else:
                                remarks = "Failed"

                        self.table.insert("", END, values=(
                                i,
                                row[0],
                                row[1],
                                round(p, 2) if p else "-",
                                round(m, 2) if m else "-",
                                round(f, 2) if f else "-",
                                round(avg, 2),
                                remarks
                        ))
                        
        def search_student(self):
                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                key = self.var_search.get()

                cur.execute("""
        SELECT s.name, s.sr_code,
        c.prelim, c.midterm, c.finals
        FROM student s
        LEFT JOIN course c ON s.s_id = c.student_id
        WHERE s.name LIKE ? OR s.sr_code LIKE ?
    """, (f"%{key}%", f"%{key}%"))

                rows = cur.fetchall()
                con.close()

                self.table.delete(*self.table.get_children())

                for i, row in enumerate(rows, start=1):
                        p, m, f = row[2], row[3], row[4]
                        grades = [g for g in [p, m, f] if g is not None]

                        avg = sum(grades)/len(grades) if grades else 0

                        remarks = "No Grade" if avg == 0 else ("Passed" if avg >= 75 else "Failed")

                        self.table.insert("", END, values=(
                                i,
                                row[0],
                                row[1],
                                p if p else "-",
                                m if m else "-",
                                f if f else "-",
                                round(avg, 2),
                                remarks
                        ))

class ViewStudentList:
        def __init__(self, root):
                self.root = root
                self.root.title("View Student List")
                self.root.geometry("1500x850+0+0")
                self.root.config(bg="white")

                title = Label(self.root, text="View Student List",
                      font=("goudy old style", 25, "bold"),
                      bg="#00117c", fg="white")
                title.pack(fill=X)
        
        # VARIABLES
                self.var_program = StringVar()
                self.var_section = StringVar()
                self.var_search = StringVar()

        # PROGRAM DROPDOWN
                Label(self.root, text="Program", font=("times new roman", 14, "bold"),bg="white").place(x=20, y=60)
                self.cmb_program = ttk.Combobox(self.root, textvariable=self.var_program, state="readonly")
                self.cmb_program.place(x=100, y=60, width=200)
                self.cmb_program.bind("<<ComboboxSelected>>", self.load_section)
                
        # SECTION DROPDOWN
                Label(self.root, text="Section", font=("times new roman", 14, "bold"),bg="white").place(x=450, y=60)
                self.cmb_section = ttk.Combobox(self.root, textvariable=self.var_section, state="readonly")
                self.cmb_section.place(x=520, y=60, width=200)
                self.cmb_section.bind("<<ComboboxSelected>>", self.load_students)
                # SEARCH
                Label(self.root, text="Search (Name / SR Code)", 
                font=("times new roman", 14, "bold"),
                bg="white").place(x=800, y=60)

                self.txt_search = Entry(        
                self.root,
                textvariable=self.var_search,
                font=("times new roman", 14),
                bg="#AAADAE"
                )
                self.txt_search.place(x=1020, y=60, width=200)

                Button(
                        self.root,
                        text="Search",
                        font=("times new roman", 12, "bold"),
                        bg="#00117c",
                        fg="white",
                        command=self.search_student
                ).place(x=1230, y=60, width=100, height=30)     
        # TABLE
                self.table = ttk.Treeview(self.root,
                columns=("no", "name", "sr_code", "gender"),
                show="headings")

                self.table.heading("no", text="No.")
                self.table.heading("name", text="Name")
                self.table.heading("sr_code", text="SR Code")
                self.table.heading("gender", text="Gender")
                
                # CENTER TABLE TEXT
                for col in ("no", "name", "sr_code", "gender"):
                        self.table.column(col, anchor=CENTER)

# CENTER HEADINGS
                for col in ("no", "name", "sr_code", "gender"):
                        self.table.heading(col, anchor=CENTER)

                self.table.place(x=50, y=120, width=1400, height=650)

                self.load_programs()        
                
        # LOAD PROGRAMS
        def load_programs(self):
                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                cur.execute("SELECT DISTINCT program FROM student")
                rows = cur.fetchall()

                self.cmb_program["values"] = [row[0] for row in rows]
                con.close()        

        # LOAD SECTIONS BASED ON PROGRAM
        def load_section(self, event):
                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                cur.execute("SELECT DISTINCT section FROM student WHERE program=?", (self.var_program.get(),))
                rows = cur.fetchall()

                self.cmb_section["values"] = [row[0] for row in rows]
                con.close()
                
         # LOAD STUDENTS BASED ON SECTION
        def load_students(self, event):
                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                cur.execute("""SELECT name, sr_code, gender FROM student WHERE program=? AND section=?""", (self.var_program.get(), self.var_section.get()))

                rows = cur.fetchall()
                con.close()

                self.table.delete(*self.table.get_children())

                for i, row in enumerate(rows, start=1):
                        self.table.insert("", END, values=(
                        i,
                        row[0],
                        row[1],
                        row[2]
                ))
                        
        def search_student(self):
                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                key = self.var_search.get()

                query = """
        SELECT name, sr_code, gender 
        FROM student 
        WHERE name LIKE ? OR sr_code LIKE ?
    """

                cur.execute(query, (f"%{key}%", f"%{key}%"))
                rows = cur.fetchall()

                self.table.delete(*self.table.get_children())

                for i, row in enumerate(rows, start=1):
                        self.table.insert("", END, values=(
                                i,
                                row[0],
                                row[1],
                                row[2]
                        ))

                con.close()

class CourseClass:
        def __init__(self, root):
                self.root = root
                self.root.title("Course Management")
                self.root.geometry("1500x850+0+0")

                self.var_search = StringVar()
                self.var_course = StringVar()
                self.var_prelim = StringVar()
                self.var_midterm = StringVar()
                self.var_finals = StringVar()
                self.student_id = StringVar()
                

                Label(self.root, text="Student Section",
                        font=("goudy old style", 20, "bold"),
                        bg="white").pack(pady=20)
        
         # Title
                title = Label(
                        self.root,
                        text="Add Student Course Details",
                        font=("goudy old style", 30, "bold"),
                        bg="#00117c",
                        fg="white"
                 )
                title.place(x=0, y=0, relwidth=1, height=50)
                
                self.var_id = StringVar()
                self.var_course = StringVar()
                self.var_prelim = StringVar()
                self.var_midterm = StringVar()
                self.var_finals = StringVar()

        # SEARCH STUDENT
                Label(self.root, text="SR Code / Name", font=("Times New Roman", 15)).place(x=10, y=80)
                Entry(self.root, textvariable=self.var_search).place(x=200, y=80, width=200, height=25)

                Button(self.root, text="Find Student", font=("Times New Roman", 12), command=self.find_student).place(x=410, y=80, height=25)

        # RESULT LABEL
                self.lbl_student = Label(self.root, text="No Student Selected", font=("Times New Roman", 15, "bold"))
                self.lbl_student.place(x=10, y=120)

        # COURSE INPUT
                Label(self.root, text="Course Name", font=("Times New Roman", 15)).place(x=10, y=170)
                Entry(self.root, textvariable=self.var_course).place(x=200, y=170, width=200, height=25)

                Label(self.root, text="Prelim", font=("Times New Roman", 15)).place(x=10, y=200)
                Entry(self.root, textvariable=self.var_prelim).place(x=200, y=200, width=200, height=25)

                Label(self.root, text="Midterm", font=("Times New Roman", 15)).place(x=10, y=230)
                Entry(self.root, textvariable=self.var_midterm).place(x=200, y=230, width=200, height=25)

                Label(self.root, text="Finals", font=("Times New Roman", 15)).place(x=10, y=260)
                Entry(self.root, textvariable=self.var_finals).place(x=200, y=260, width=200, height=25)

                self.btn_add = Button(self.root, text="Add",font=("goudy old style", 15, "bold"),bg="#00117c", fg="white", cursor="hand2",command=self.add_course)
                self.btn_add.place(x=50, y=325, width=110, height=40)

                self.btn_update = Button(self.root, text="Update",font=("goudy old style", 15, "bold"),bg="#00117c", fg="white", cursor="hand2",command=self.update_course)
                self.btn_update.place(x=170, y=325, width=110, height=40)

                self.btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#00117c", fg="white", cursor="hand2",  command=self.delete_course)
                self.btn_delete.place(x=290, y=325, width=110, height=40)

                Button(self.root, text="Exit", font=("goudy old style", 15, "bold" ), bg="#00117c", fg="white", cursor="hand2", command=self.root.destroy).place(x=410, y=325, width=110, height=40)

        # TABLE
                self.table = ttk.Treeview(self.root,
                columns=("no", "course","prelim", "midterm", "finals", "avg", "id"),
                show="headings")

                self.table.heading("no", text="No.")
                self.table.heading("course", text="Course")
                self.table.heading("prelim", text="Prelim")
                self.table.heading("midterm", text="Midterm")
                self.table.heading("finals", text="Finals")
                self.table.heading("avg", text="Average")
                self.table.heading("id", text="ID")
                # CENTER TABLE TEXT
                for col in ("no", "course", "prelim", "midterm", "finals", "avg", "id"):
                        self.table.column(col, anchor=CENTER)

# CENTER HEADINGS
                for col in ("no", "course", "prelim", "midterm", "finals", "avg", "id"):
                        self.table.heading(col, anchor=CENTER)
                
                self.table.column("id", width=0, stretch=NO)
                self.table.bind("<ButtonRelease-1>", self.get_data)
                self.table.place(x=550, y=80, width=900, height=500)
                
        def get_data(self, event):
                selected = self.table.focus()
                data = self.table.item(selected)
                row = data["values"]
                
                if not row:
                        return
                
                self.var_id.set(row[6])  # 👉 IMPORTANT (database id)
                self.var_course.set(row[1])
                self.var_prelim.set(row[2])
                self.var_midterm.set(row[3])
                self.var_finals.set(row[4])

        def find_student(self):
                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                key = self.var_search.get()

                cur.execute("""
                SELECT s_id, name, sr_code FROM student
                WHERE name=? OR sr_code=?
                """, (key, key))

                row = cur.fetchone()
                con.close()

                if row is None:
                        messagebox.showerror("Error", "Student not found")
                else:
                        self.student_id = row[0]
                        self.lbl_student.config(text=f"{row[1]} | {row[2]}")
                        self.load_courses()
                        
        def add_course(self):
                if self.student_id is None:
                        messagebox.showerror("Error", "Select a student first")
                        return

                try:
                        p = float(self.var_prelim.get()) if self.var_prelim.get() else None
                        m = float(self.var_midterm.get()) if self.var_midterm.get() else None
                        f = float(self.var_finals.get()) if self.var_finals.get() else None

        # VALIDATION 1–100
                        for grade in [p, m, f]:
                                if grade is not None and not (1 <= grade <= 100):
                                        messagebox.showerror("Error", "Grades must be 1–100 only")
                                        return

                except ValueError:
                        messagebox.showerror("Error", "Invalid input")
                        return

                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                cur.execute("""
                INSERT INTO course(student_id, course_name, prelim, midterm, finals)
                VALUES(?,?,?,?,?)
                """, (self.student_id, self.var_course.get(), p, m, f))

                con.commit()
                con.close()

                messagebox.showinfo("Success", "Course Added")
                self.load_courses()

    # ONLY clear inputs (NOT close window)
                self.var_course.set("")
                self.var_prelim.set("")
                self.var_midterm.set("")
                self.var_finals.set("")
                self.var_id.set("")

                self.load_courses()


                
        def load_courses(self):
                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                cur.execute("""
                SELECT id, course_name, prelim, midterm, finals 
                FROM course WHERE student_id=?
                """, (self.student_id,))

                rows = cur.fetchall()
                con.close()

                self.table.delete(*self.table.get_children())

                for i, row in enumerate(rows, start=1):
                        grades = [g for g in row[2:] if g is not None]

                        if grades:
                                avg = sum(grades) / len(grades)
                        else:
                                avg = 0

                        self.table.insert("", END, values=(
                                i,
                                row[1],
                                row[2] if row[2] else "-",
                                row[3] if row[3] else "-",
                                row[4] if row[4] else "-",
                                round(avg, 2),
                                row[0]
                        ))
                        
        def update_course(self):
                if self.var_id.get() =="":
                        messagebox.showerror("Error", "Select course to update")
                        return

                try:
                        p = float(self.var_prelim.get()) if self.var_prelim.get() else None
                        m = float(self.var_midterm.get()) if self.var_midterm.get() else None
                        f = float(self.var_finals.get()) if self.var_finals.get() else None
                except ValueError:
                        messagebox.showerror("Error", "Invalid input")
                        return

                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                cur.execute("""
                UPDATE course
                SET course_name=?, prelim=?, midterm=?, finals=?
                WHERE id=?
                """, (
                        self.var_course.get(),
                        p, m, f,
                        self.var_id.get()
                ))

                con.commit()
                con.close()

                messagebox.showinfo("Success", "Course Updated")
                self.load_courses()
                
        def delete_course(self):
                if self.var_id.get() == "":
                        messagebox.showerror("Error", "Select course to delete")
                        return

                con = sqlite3.connect("rms.db")
                cur = con.cursor()

                cur.execute("DELETE FROM course WHERE id=?", (self.var_id.get(),))

                con.commit()
                con.close()

                messagebox.showinfo("Success", "Course Deleted")
                self.load_courses()

    # clear fields
                self.var_id.set("")
                self.var_course.set("")
                self.var_prelim.set("")
                self.var_midterm.set("")
                self.var_finals.set("")

class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management")
        self.root.geometry("1500x850+0+0")
        self.root.config(bg="white")
        self.root.focus_force()
        

        Label(self.root, text="Student Section",
              font=("goudy old style", 20, "bold"),
              bg="white").pack(pady=20)
        
         # Title
        title = Label(
            self.root,
            text="Add Student Details",
            font=("goudy old style", 30, "bold"),
            bg="#00117c",
            fg="white"
        )
        title.place(x=0, y=0, relwidth=1, height=50)

#variables
        
        self.var_studentName = StringVar()
        self.var_srCode = StringVar()
        self.var_section = StringVar()
        self.var_program = StringVar()
        self.var_gender = StringVar()
        self.selected_id = None
        
        #WIDGET
        lbl_studentName=Label(self.root, text="Student Name", font=("goudy old style", 15, "bold"),bg="white", fg="black").place(x=10, y=60)
        lbl_srCode=Label(self.root, text="SR Code", font=("goudy old style", 15, "bold"), bg="white", fg="black").place(x=10, y=100)
        lbl_section=Label(self.root, text="Section", font=("goudy old style", 15, "bold"), bg="white", fg="black", ).place(x=10, y=140)
        lbl_program=Label(self.root, text="Program", font=("goudy old style", 15, "bold"), bg="white", fg="black").place(x=10, y=180)
        Label(self.root, text="Gender", font=("goudy old style", 15, "bold"),bg="white").place(x=10, y=220)

       #entry field
        self.txt_studentName=Entry(self.root,textvariable=self.var_studentName,font=("goudy old style", 15, "bold"), bg="#AAADAE", fg="white", relief=RIDGE)
        self.txt_studentName.place(x=150, y=60, width=200, height=30)
        self.txt_srCode=Entry(self.root, textvariable=self.var_srCode, font=("goudy old style", 15, "bold"), bg="#AAADAE", fg="white", relief=RIDGE).place(x=150, y=100, width=200, height=30)
        self.txt_section=Entry(self.root, textvariable=self.var_section,  font=("goudy old style", 15, "bold"), bg="#AAADAE", fg="white", relief=RIDGE).place(x=150, y=140, width=200, height=30)
        self.txt_program=Text(self.root, font=("goudy old style", 15, "bold"), bg="#AAADAE", fg="white", relief=RIDGE)
        self.txt_program.place(x=150, y=180, width=200, height=30)
        ttk.Combobox(self.root, textvariable=self.var_gender,values=["Male", "Female"], state="readonly").place(x=150, y=220, width=200)

#buttons
        self.btn_add=Button(self.root, text="Save", font=("goudy old style   ", 15, "bold"), bg="#00117c", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=150, y=325, width=110, height=40)
        self.btn_update=Button(self.root, text="Update", font=("goudy old style   ", 15, "bold"), bg="#00117c", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=270, y=325, width=110, height=40)
        self.btn_delete=Button(self.root, text="Delete", font=("goudy old style   ", 15, "bold"), bg="#00117c", fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=390, y=325, width=110, height=40)
        self.btn_clear=Button(self.root, text="Clear", font=("goudy old style   ", 15, "bold"), bg="#00117c", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=510, y=325, width=110, height=40)

#search panel
        self.var_search=StringVar()
        lbl_search_student=Label(self.root, text="Student Name", font=("goudy old style", 15, "bold"), bg="white", fg="black").place(x=700, y=60)
        txt_search_studentName=Entry(self.root,textvariable=self.var_search,font=("goudy old style", 15, "bold"), bg="#AAADAE", fg="white", relief=RIDGE).place(x=825, y=60, width=180)
        btn_search=Button(self.root, text="Search", font=("goudy old style   ", 15, "bold"), bg="#00117c", fg="white", cursor="hand2", command=self.search).place(x=1010, y=60, width=100, height=30)
        
#Content
        self.C_Frame=Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=650, y=100, width=800, height=600)
        
        
        scroll_y = Scrollbar(self.C_Frame, orient=VERTICAL)
        scroll_x = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.StudentTable=ttk.Treeview(self.C_Frame, 
                columns=("id","no", "name", "sr_code", "section", "program", "gender"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.StudentTable.yview)
        scroll_x.config(command=self.StudentTable.xview)
        
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.StudentTable.heading("id", text="ID")
        self.StudentTable.column("id", width=0, stretch=NO)
        self.StudentTable.heading("no", text="No.")
        self.StudentTable.heading("name", text="Student Name")
        self.StudentTable.heading("sr_code", text="SR Code")
        self.StudentTable.heading("section", text="Section")
        self.StudentTable.heading("program", text="Program")
        self.StudentTable.heading("gender", text="Gender")
        self.StudentTable["show"] = "headings"
                # CENTER TABLE TEXT
        for col in ("no", "name", "sr_code", "section", "program", "gender"):
                self.StudentTable.column(col, anchor=CENTER)

# CENTER HEADINGS
        for col in ("no", "name", "sr_code", "section", "program", "gender"):
                self.StudentTable.heading(col, anchor=CENTER)
        self.StudentTable.bind("<ButtonRelease-1>", self.get_data)
        self.StudentTable.pack(fill=BOTH, expand=1)
        self.show()
        
    def clear(self):
        self.show()
        self.var_studentName.set("")
        self.var_srCode.set("")
        self.var_section.set("")
        self.var_gender.set("")
        self.var_search.set("")
        self.txt_program.delete("1.0", END)
        self.txt_studentName.config(state=NORMAL)  # Disable the Entry widget to prevent text insertion
        
    def get_data(self, event):
        r = self.StudentTable.focus()
        content = self.StudentTable.item(r)
        row = content.get("values")

        if not row:
                return

        self.var_studentName.set(row[2])
        self.var_srCode.set(row[3])
        self.var_section.set(row[4])
        self.txt_program.delete("1.0", END)
        self.txt_program.insert(END, row[5])
        self.var_gender.set(row[6])
        self.selected_id = row[0]  # Store the selected student's ID
        
    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
                if self.var_studentName.get() == "":
                        messagebox.showerror("Error", "Student Name is Required", parent=self.root)
                        return

        # ✅ SR CODE VALIDATION (ILAGAY DITO)
                pattern = r'^\d{2}-\d{5}$'
                if not re.match(pattern, self.var_srCode.get()):
                        messagebox.showerror("Error", "Invalid SR Code format (e.g. 25-12345)")
                        return

        # CHECK DUPLICATE
                cur.execute("select * from student where name=?", (self.var_studentName.get(),))
                row = cur.fetchone()

                if row != None:
                         messagebox.showerror("Error", "Student Name already present, try different", parent=self.root)
                else:
                        cur.execute("""
                                INSERT INTO student(name, sr_code, section, program, gender)
                                VALUES(?,?,?,?,?)
                                """, (
                                self.var_studentName.get().strip(),
                                self.var_srCode.get().strip(),
                                self.var_section.get().strip(),
                                self.txt_program.get("1.0", END).strip(),
                                self.var_gender.get()
                        ))
                        con.commit()
                        messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
                        self.show()

        except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}")

        finally:
                con.close()
    
    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
                cur.execute("SELECT * FROM student")
                rows = cur.fetchall()

                self.StudentTable.delete(*self.StudentTable.get_children())

                for i, row in enumerate(rows, start=1):
                        self.StudentTable.insert("", END, values=(
                                row[0],   # hidden database ID
                                i,        # display number
                                row[1],
                                row[2],
                                row[3],
                                row[4],
                                row[5]
                        ))

        except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}")

        finally:
                con.close()


    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
                if self.selected_id is None:
                        messagebox.showerror("Error", "Select a student from the table first", parent=self.root)
                        return

                op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)

                if op == True:
                        cur.execute("DELETE FROM student WHERE s_id=?", (self.selected_id,))
                        con.commit()

                        messagebox.showinfo("Success", "Student Deleted Successfully", parent=self.root)

                        self.show()
                        self.clear()
                        self.selected_id = None

        except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}")

        finally:
                con.close()

    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
                if self.var_studentName.get() == "":
                        messagebox.showerror("Error", "Student Name is Required", parent=self.root)
                else:
                        cur.execute("SELECT * FROM student WHERE name=?", (self.var_studentName.get(),))
                        row = cur.fetchone()

                        if row is None:
                                messagebox.showerror("Error", "Select Student from list", parent=self.root)
                        else:
                                cur.execute("""
                                UPDATE student 
                                SET sr_code=?, section=?, program=?, gender=?
                                WHERE name=?
                                """, (
                                        self.var_srCode.get(),
                                        self.var_section.get(),
                                        self.txt_program.get("1.0", END).strip(),
                                        self.var_gender.get(),
                                        self.var_studentName.get()
                                ))

                        con.commit()
                        messagebox.showinfo("Success", "Student Updated Successfully", parent=self.root)
                        self.show()

        except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}")
        finally:
                con.close()
                        
    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
                if self.var_search.get()=="":
                        self.show()
                else:
                        cur.execute("SELECT * FROM student where name LIKE ?", ('%'+self.var_search.get()+'%',))
                        rows = cur.fetchall()
                        self.StudentTable.delete(*self.StudentTable.get_children())
                       
                        for i, row in enumerate(rows, start=1):
                                self.StudentTable.insert("", END, values=(
                                        row[0],
                                        i,
                                        row[1],
                                        row[2],
                                        row[3],
                                        row[4],
                                        row[5]
                                ))
                        
                        else:
                                messagebox.showerror("Error", "No record found", parent=self.root)
        except  Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}")
        finally:
                con.close()

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record System")
        self.root.geometry("1300x700+0+0")
        self.root.config(bg="White")
        self.dark_mode = False

        
        # Icon
        logo = Image.open("RMS/images/logologo.jpg")  # open the file
        logo = logo.resize((40, 40))  # resize to 40x40
        mask = Image.new("L", logo.size, 0)  # create a mask# create a drawing context
        self.logo_dash = ImageTk.PhotoImage(logo) 
        
        mask = Image.new("L", (40, 40), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 40, 40), fill=255)

# APPLY MASK (MAKE CIRCLE)
        logo.putalpha(mask)

# CONVERT TO TKINTER IMAGE
        self.logo_dash = ImageTk.PhotoImage(logo)
       
       # DIGITAL CLOCK FRAME
        clock_frame = Frame(self.root, bg="#00117c", bd=5, relief=RIDGE)
        clock_frame.place(x=20, y=690, width=350, height=150)

# TIME
        self.lbl_time = Label(clock_frame,
                      font=("digital-7", 28, "bold"),
                      bg="#00117c",
                      fg="white")
        self.lbl_time.pack(pady=5)

# DAY
        self.lbl_day = Label(clock_frame,
                     font=("Orbitron", 28, "bold"),
                     bg="#00117c",
                     fg="white")
        self.lbl_day.pack()

# DATE
        self.lbl_date = Label(clock_frame,
                      font=("Orbitron", 12, "bold"),
                      bg="#00117c",
                      fg="white")
        self.lbl_date.pack()
        

# START CLOCK
        self.digital_clock()

        # Title
        title = Label(
            self.root,
            text="Student Record System",
            image=self.logo_dash,
            compound=LEFT,  # makes image + text appear nicely
            font=("times new roman", 30, "bold"),
            bg="#00117c",
            fg="white"
        )
        title.place(x=5, y=0, relwidth=1, height=50)

        #MENU
        M_Frame = LabelFrame(self.root,text="Menus",font=("times new roman", 15,), bg="white")
        M_Frame.place(x=10, y=70, width=1510, height=80)
        
        btn_add_student=Button(M_Frame, text="Add Student", font=("goudy old style", 15, "bold"), bg="#00117c", fg="white", cursor="hand2", command=self.add_student).place(x=100, y=5, width=200, height=40)
        btn_add_course=Button(M_Frame, text="Add Course", font=("goudy old style", 15, "bold"), bg="#00117c", fg="white", cursor="hand2", command=self.add_course).place(x=320, y=5, width=200, height=40)
        btn_view_student_list=Button(M_Frame, text="View Student List", font=("goudy old style", 15, "bold"), bg="#00117c", fg="white", cursor="hand2", command=self.view_student_list).place(x=540, y=5, width=200, height=40)
        btn_view_result=Button(M_Frame, text="View Student Result", font=("goudy old style", 15, "bold"), bg="#00117c", fg="white", cursor="hand2", command=self.view_result).place(x=760, y=5, width=200, height=40)
        self.btn_theme = Button(
                M_Frame,
                text="Search Student",
                font=("goudy old style", 15, "bold"),
                bg="#00117c",
                fg="white",
                cursor="hand2",
               command=self.search_student_window
        )

        self.btn_theme.place(x=980, y=5, width=200, height=40)
        btn_exit=Button(M_Frame, text="Exit", font=("goudy old style", 15, "bold"), bg="#00117c", fg="white", cursor="hand2", command=self.exit_app).place(x=1200, y=5, width=200, height=40)
        
        # VIDEO
        video_label = Label(self.root)
        video_label.place(x=15, y=160, width=1500, height=520)

        player = tkvideo("RMS/images/video.mp4", video_label, loop=1, size=(1500, 520))
        player.play()
        
        # ================= DASHBOARD =================
        self.lbl_student = Label(self.root, text="Total Students\n[ 0 ]",
            font=("goudy old style", 18, "bold"),
            bg="#3E4447", fg="white", bd=5, relief=RIDGE)
        self.lbl_student.place(x=400, y=690, width=350, height=150)

        self.lbl_pass = Label(self.root, text="Total Passes\n[ 0 ]",
            font=("goudy old style", 18, "bold"),
            bg="#3E4447", fg="white", bd=5, relief=RIDGE)
        self.lbl_pass.place(x=780, y=690, width=350, height=150)

        self.lbl_fail = Label(self.root, text="Total Fails\n[ 0 ]",
            font=("goudy old style", 18, "bold"),
            bg="#3E4447", fg="white", bd=5, relief=RIDGE)
        self.lbl_fail.place(x=1160, y=690, width=350, height=150)
        
        self.update_dashboard()
# Title footer
        footer = Label(
            self.root,
            text="SRS - Student Record System\nContact Us for any Technical Issue: 09123456789",
            
              # makes image + text appear nicely
            font=("times new roman", 12) ,
            bg="#262626",
            fg="white"
        )
        footer.pack(side=BOTTOM, fill=X)
        
   
    def search_student_window(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SearchStudent(self.new_win)

        # START CLOCK          
    def digital_clock(self):
        now = datetime.datetime.now()

    # TIME (HH:MM:SS)
        time_str = now.strftime("%H:%M:%S")

    # DAY (Monday, Tuesday, etc.)
        day_str = now.strftime("%A")

    # DATE (optional but recommended)
        date_str = now.strftime("%B %d, %Y")

    # UPDATE LABELS
        self.lbl_time.config(text=time_str)
        self.lbl_day.config(text=day_str)
        self.lbl_date.config(text=date_str)
        
    def update_dashboard(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()

        # TOTAL STUDENTS
        cur.execute("SELECT COUNT(*) FROM student")
        total_students = cur.fetchone()[0]

        # PASS / FAIL
        cur.execute("""
        SELECT 
        AVG(
        (IFNULL(c.prelim,0) + IFNULL(c.midterm,0) + IFNULL(c.finals,0)) /
        (CASE 
            WHEN c.prelim IS NOT NULL AND c.midterm IS NOT NULL AND c.finals IS NOT NULL THEN 3
            WHEN (c.prelim IS NOT NULL AND c.midterm IS NOT NULL) OR 
                 (c.prelim IS NOT NULL AND c.finals IS NOT NULL) OR 
                 (c.midterm IS NOT NULL AND c.finals IS NOT NULL) THEN 2
            ELSE 1
        END)
        )
        FROM student s
        LEFT JOIN course c ON s.s_id = c.student_id
        GROUP BY s.s_id
        """)
        rows = cur.fetchall()

        total_pass = 0
        total_fail = 0

        for row in rows:
            avg = float(row[0])

            if avg >= 75:
                total_pass += 1
            elif avg > 0:
                total_fail += 1

        # AUTO REFRESH
        self.root.after(1000, self.update_dashboard)

        # UPDATE LABELS
        self.lbl_student.config(text=f"Total Students\n[ {total_students} ]")
        self.lbl_pass.config(text=f"Total Passes\n[ {total_pass} ]")
        self.lbl_fail.config(text=f"Total Fails\n[ {total_fail} ]")

        con.close()
    # SMOOTH UPDATE every 200ms (mas smooth kaysa 1000ms)
        self.root.after(200, self.digital_clock)
#update details
        #self.lbl_student = Label(self.root, text="Total Students\n[ 0 ]",
                #font=("goudy old style", 18, "bold"),
                #bg="#3E4447", fg="white", bd=5, relief=RIDGE)

        #self.lbl_student.place(x=400, y=690, width=350, height=150)
        #self.lbl_pass=Label(self.root, text="Total Passes\n[ 0 ]", font=("goudy old style", 18, "bold"), bg="#3E4447", fg="white",bd=5,relief=RIDGE).place(x=780, y=690, width=350, height=150)
        #self.lbl_fail=Label(self.root, text="Total Fails\n[ 0 ]", font=("goudy old style", 18, "bold"), bg="#3E4447", fg="white",bd=5,relief=RIDGE).place(x=1160, y=690, width=350, height=150)
        
    def exit_app(self):
        op = messagebox.askyesno("Confirm", "Do you really want to exit?")
        if op:
                self.root.destroy()
                
    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)
        self.new_win.grab_set()
        self.new_win.focus_force()

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = StudentClass(self.new_win)
        
    def view_student_list(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ViewStudentList(self.new_win)
        
    def view_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ViewStudentResult(self.new_win)
        

if __name__ == "__main__":
    root = Tk()
     # TABLE STYLE
    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "Treeview.Heading",
        font=("goudy old style", 12, "bold")
    )

    style.configure(
        "Treeview",
        font=("goudy old style", 11)
    )
    
    style.configure(
        "Rounded.TButton",
        font=("goudy old style", 12, "bold"),
        padding=10
   )
    
    create_db()
    obj = RMS(root)
      # Call the function to create the database and table
    root.mainloop()