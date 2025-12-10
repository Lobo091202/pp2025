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

    def input_mark(self, course_id):
        score = float(input(f"Enter mark for {self.__name} in course {course_id}: "))
        score = math.floor(score * 10) / 10
        self.__marks[course_id] = score

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
