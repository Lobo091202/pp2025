import math
import numpy as np
import curses
import time

# -----------------------------
# Classes
# -----------------------------

class Student:
    def __init__(self, sid, name, dob):
        self.__id = sid
        self.__name = name
        self.__dob = dob
        self.__marks = {}   # {course_id: mark}
        self.__gpa = None

    # Encapsulation getters
    def get_id(self): return self.__id
    def get_name(self): return self.__name
    def get_dob(self): return self.__dob
    def get_mark(self, cid): return self.__marks.get(cid)
    def get_gpa(self): return self.__gpa

    # Input mark with rounding
    def input_mark(self, course_id):
        score = float(input(f"Enter mark for {self.__name} in course {course_id}: "))
        score = math.floor(score * 10) / 10
        self.__marks[course_id] = score

    # Calculate GPA using numpy
    def calculate_gpa(self, credit_dict):
        marks = []
        credits = []

        for cid, mark in self.__marks.items():
            marks.append(mark)
            credits.append(credit_dict[cid])

        marks = np.array(marks)
        credits = np.array(credits)

        self.__gpa = np.sum(marks * credits) / np.sum(credits)
        return self.__gpa


class Course:
    def __init__(self, cid, name, credit):
        self.__id = cid
        self.__name = name
        self.__credit = credit

    def get_id(self): return self.__id
    def get_name(self): return self.__name
    def get_credit(self): return self.__credit


# -----------------------------
# Manager class
# -----------------------------

class StudentMarkSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.credit_dict = {}   # {course_id: credit}

    def add_student(self):
        sid = input("Student ID: ")
        name = input("Name: ")
        dob = input("DoB: ")
        self.students.append(Student(sid, name, dob))

    def add_course(self):
        cid = input("Course ID: ")
        name = input("Course name: ")
        credit = int(input("Credit: "))
        self.courses.append(Course(cid, name, credit))
        self.credit_dict[cid] = credit

    def input_marks(self, cid):
        for s in self.students:
            s.input_mark(cid)

    def calculate_all_gpa(self):
        for s in self.students:
            s.calculate_gpa(self.credit_dict)

    def sort_by_gpa(self):
        self.students.sort(key=lambda s: s.get_gpa(), reverse=True)

    def list_students(self):
        for s in self.students:
            print(f"{s.get_id():<10} {s.get_name():<20} GPA = {s.get_gpa():.2f}")


# --------------------------------
# Curses-based minimal UI
# --------------------------------

def curses_ui(stdscr, sms: StudentMarkSystem):
    stdscr.clear()
    stdscr.addstr(1, 2, "=== Student Mark System (Curses UI) ===")
    stdscr.addstr(3, 2, "Students Loaded: " + str(len(sms.students)))
    stdscr.addstr(4, 2, "Courses Loaded : " + str(len(sms.courses)))
    stdscr.addstr(6, 2, "Press any key to exit")
    stdscr.refresh()
    stdscr.getch()


# -----------------------------
# Main
# -----------------------------

def main():
    sms = StudentMarkSystem()

    # test flow
    sms.add_student()
    sms.add_student()
    sms.add_course()
    sms.add_course()

    # Input marks
    for c in sms.courses:
        sms.input_marks(c.get_id())

    # GPA
    sms.calculate_all_gpa()
    sms.sort_by_gpa()

    # Show UI
    curses.wrapper(curses_ui, sms)


if __name__ == "__main__":
    main()
