import math
import numpy as np

class Student:
    def __init__(self, sid, name, dob):
        self.__id = sid
        self.__name = name
        self.__dob = dob
        self.__marks = {}   # {course_id: mark}
        self.__gpa = None

    # getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def get_mark(self, cid):
        return self.__marks.get(cid)

    def get_all_marks(self):
        return dict(self.__marks)

    def get_gpa(self):
        return self.__gpa

    # used when loading from storage
    def set_mark(self, cid, mark):
        self.__marks[cid] = mark

    # input mark (round down to 1 decimal using floor)
    def input_mark(self, course_id):
        while True:
            try:
                val = input(f"Enter mark for {self.__name} ({self.__id}) in {course_id}: ")
                score = float(val)
                break
            except ValueError:
                print("Invalid number. Try again.")
        score = math.floor(score * 10) / 10
        self.__marks[course_id] = score

    # calculate GPA weighted by credits (using numpy)
    def calculate_gpa(self, credit_dict):
        if not self.__marks:
            self.__gpa = 0.0
            return self.__gpa

        marks = []
        credits = []
        for cid, mark in self.__marks.items():
            credit = credit_dict.get(cid)
            if credit is None:
                continue
            marks.append(mark)
            credits.append(credit)

        if not credits:
            self.__gpa = 0.0
            return self.__gpa

        marks = np.array(marks, dtype=float)
        credits = np.array(credits, dtype=float)
        self.__gpa = float(np.sum(marks * credits) / np.sum(credits))
        return self.__gpa
