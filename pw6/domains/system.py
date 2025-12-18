import os
import pickle
import zlib

from .student import Student
from .course import Course

DATA_DIR = "data"
DATA_PATH = os.path.join(DATA_DIR, "system.dat")

class StudentMarkSystem:
    def __init__(self):
        self.students = []      # list of Student objects
        self.courses = []       # list of Course objects
        self.credit_dict = {}   # course_id -> credit

    # --------- helpers ----------
    def find_student(self, sid):
        for s in self.students:
            if s.get_id() == sid:
                return s
        return None

    def find_course(self, cid):
        for c in self.courses:
            if c.get_id() == cid:
                return c
        return None

    # --------- add data ----------
    def add_student(self, sid, name, dob):
        if self.find_student(sid):
            raise ValueError(f"Student id {sid} already exists")
        self.students.append(Student(sid, name, dob))

    def add_course(self, cid, name, credit):
        if self.find_course(cid):
            raise ValueError(f"Course id {cid} already exists")
        self.courses.append(Course(cid, name, credit))
        self.credit_dict[cid] = credit

    def input_marks_for_course(self, cid):
        if self.find_course(cid) is None:
            raise ValueError(f"Course {cid} not found")
        for s in self.students:
            s.input_mark(cid)

    # --------- GPA ----------
    def calculate_all_gpa(self):
        for s in self.students:
            s.calculate_gpa(self.credit_dict)

    def sort_students_by_gpa_desc(self):
        self.students.sort(key=lambda x: x.get_gpa() if x.get_gpa() is not None else 0.0, reverse=True)

    # --------- persistence using pickle + compression ----------
    def save_data(self, path=DATA_PATH):
        # ensure data dir exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # pickle the whole object (self)
        raw = pickle.dumps(self)
        compressed = zlib.compress(raw)
        with open(path, "wb") as f:
            f.write(compressed)
        return path

    @staticmethod
    def load_data(path=DATA_PATH):
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            compressed = f.read()
        raw = zlib.decompress(compressed)
        obj = pickle.loads(raw)
        return obj
