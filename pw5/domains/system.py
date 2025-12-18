from .student import Student
from .course import Course
import pickle, zlib, os

class StudentMarkSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.credit_dict = {}   # for GPA

    # ------------------------
    # Data input
    # ------------------------
    def add_student(self, sid, name, dob):
        self.students.append(Student(sid, name, dob))

    def add_course(self, cid, name, credit):
        self.courses.append(Course(cid, name, credit))
        self.credit_dict[cid] = credit

    def input_marks(self, cid):
        for s in self.students:
            s.input_mark(cid)

    # ------------------------
    # GPA
    # ------------------------
    def calculate_all_gpa(self):
        for s in self.students:
            s.calculate_gpa(self.credit_dict)

    def sort_by_gpa(self):
        self.students.sort(key=lambda x: x.get_gpa(), reverse=True)

    # ------------------------
    # TEXT FILE OUTPUT (PW5)
    # ------------------------
    def save_text_files(self):
        # Students
        with open("students.txt", "w") as f:
            for s in self.students:
                f.write(f"{s.get_id()},{s.get_name()},{s.get_dob()}\n")

        # Courses
        with open("courses.txt", "w") as f:
            for c in self.courses:
                f.write(f"{c.get_id()},{c.get_name()},{c.get_credit()}\n")

        # Marks
        with open("marks.txt", "w") as f:
            for s in self.students:
                for cid, mark in s.get_all_marks().items():
                    f.write(f"{s.get_id()},{cid},{mark}\n")

    # ------------------------
    # COMPRESS -> students.dat
    # ------------------------
    def compress_all(self):
        data = {}

        for filename in ["students.txt", "courses.txt", "marks.txt"]:
            if os.path.exists(filename):
                with open(filename, "rb") as f:
                    data[filename] = f.read()

        raw = pickle.dumps(data)
        compressed = zlib.compress(raw)

        with open("students.dat", "wb") as f:
            f.write(compressed)

    # ------------------------
    # LOAD FROM .dat
    # ------------------------
    def load_if_exist(self):
        if not os.path.exists("students.dat"):
            print("No previous data found.")
            return

        print("Loading previous data from students.dat ...")

        with open("students.dat", "rb") as f:
            compressed = f.read()

        raw = zlib.decompress(compressed)
        data = pickle.loads(raw)

        # rewrite extracted data into the text files
        for filename, content in data.items():
            with open(filename, "wb") as f:
                f.write(content)

        # now load the text files into objects
        self.students = []
        self.courses = []
        self.credit_dict = {}

        # load students
        with open("students.txt") as f:
            for line in f:
                sid, name, dob = line.strip().split(",")
                self.add_student(sid, name, dob)

        # load courses
        with open("courses.txt") as f:
            for line in f:
                cid, name, credit = line.strip().split(",")
                self.add_course(cid, name, int(credit))

        # load marks
        with open("marks.txt") as f:
            for line in f:
                sid, cid, mark = line.strip().split(",")
                for st in self.students:
                    if st.get_id() == sid:
                        st.set_mark(cid, float(mark))
