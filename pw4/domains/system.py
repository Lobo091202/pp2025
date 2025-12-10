from .student import Student
from .course import Course

class StudentMarkSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.credit_dict = {}

    def add_student(self, sid, name, dob):
        self.students.append(Student(sid, name, dob))

    def add_course(self, cid, name, credit):
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
