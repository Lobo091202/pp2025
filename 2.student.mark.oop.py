# OOP version of Student Mark Management

class Student:
    def __init__(self, sid, name, dob):
        self.__id = sid
        self.__name = name
        self.__dob = dob

    # encapsulation getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def input(self):
        print("Input student information:")
        self.__id = input("ID: ")
        self.__name = input("Name: ")
        self.__dob = input("Date of birth: ")

    def list(self):
        print(f"- {self.__id} | {self.__name} | {self.__dob}")


class Course:
    def __init__(self, cid, name):
        self.__id = cid
        self.__name = name

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def input(self):
        print("Input course information:")
        self.__id = input("ID: ")
        self.__name = input("Name: ")

    def list(self):
        print(f"- {self.__id} | {self.__name}")


class Mark:
    def __init__(self, student_id, course_id, value):
        self.student_id = student_id
        self.course_id = course_id
        self.value = value

    def list(self):
        print(f"{self.student_id}: {self.value}")


class Manager:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = []  # list of Mark objects

    # polymorphic .input() and .list()
    def input_students(self):
        n = int(input("Number of students: "))
        for _ in range(n):
            sid = input("Student ID: ")
            name = input("Name: ")
            dob = input("Date of birth: ")
            self.students.append(Student(sid, name, dob))

    def input_courses(self):
        n = int(input("Number of courses: "))
        for _ in range(n):
            cid = input("Course ID: ")
            name = input("Course name: ")
            self.courses.append(Course(cid, name))

    def input_marks(self):
        course_id = input("Enter course ID to input marks: ")
        # ensure course exists
        if not any(c.get_id() == course_id for c in self.courses):
            print("Course not found!")
            return

        print(f"Input marks for course {course_id}:")
        for s in self.students:
            mark_value = float(input(f"Mark for {s.get_name()} ({s.get_id()}): "))
            self.marks.append(Mark(s.get_id(), course_id, mark_value))

    def list_students(self):
        print("\nStudents:")
        for s in self.students:
            s.list()

    def list_courses(self):
        print("\nCourses:")
        for c in self.courses:
            c.list()

    def show_marks(self):
        course_id = input("Enter course ID: ")

        print(f"\nMarks for course: {course_id}")
        for m in self.marks:
            if m.course_id == course_id:
                print(f"- {m.student_id}: {m.value}")


def main():
    manager = Manager()

    while True:
        print("\n--- OOP STUDENT MARK MANAGEMENT ---")
        print("1. Input students")
        print("2. Input courses")
        print("3. Input marks")
        print("4. List students")
        print("5. List courses")
        print("6. Show marks")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            manager.input_students()
        elif choice == "2":
            manager.input_courses()
        elif choice == "3":
            manager.input_marks()
        elif choice == "4":
            manager.list_students()
        elif choice == "5":
            manager.list_courses()
        elif choice == "6":
            manager.show_marks()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
