import math
import numpy as np

class Student:
    def __init__(self, sid, name, dob):
        self.__id = sid
        self.__name = name
        self.__dob = dob
        self.__marks = {}   # {course_id: mark}
        self.__gpa = None

    def get_id(self): return self.__id
    def get_name(self): return self.__name
    def get_dob(self): return self.__dob
    def get_mark(self, cid): return self.__marks.get(cid)
    def get_gpa(self): return self.__gpa

    # Add mark
    def input_mark(self, course_id):
        score = float(input(f"Enter mark for {self.__name} in {course_id}: "))
        score = math.floor(score * 10) / 10
        self.__marks[course_id] = score

    # Calculate GPA
    def calculate_gpa(self, credit_dict):
        if not self.__marks:
            self.__gpa = 0
            return 0

        marks = []
        credits = []

        for cid, mark in self.__marks.items():
            marks.append(mark)
            credits.append(credit_dict[cid])

        marks = np.array(marks)
        credits = np.array(credits)

        self.__gpa = np.sum(marks * credits) / np.sum(credits)
        return self.__gpa

    # For PW5 loading marks directly
    def set_mark(self, cid, mark):
        self.__marks[cid] = mark

    def get_all_marks(self):
        return self.__marks
