# Student Mark Management 

students = []
courses = []
marks = {}   # key = course_id, value = list of (student_id, mark)


# ------------------------
# INPUT FUNCTIONS
# ------------------------

def input_number_of_students():
    n = int(input("Number of students: "))
    for _ in range(n):
        sid = input("Student ID: ")
        name = input("Student name: ")
        dob = input("Date of birth: ")
        students.append({
            "id": sid,
            "name": name,
            "dob": dob
        })


def input_number_of_courses():
    n = int(input("Number of courses: "))
    for _ in range(n):
        cid = input("Course ID: ")
        name = input("Course name: ")
        courses.append({
            "id": cid,
            "name": name
        })


def input_marks():
    course_id = input("Enter course ID to input marks: ")
    # check course exists
    found = False
    for c in courses:
        if c["id"] == course_id:
            found = True

    if not found:
        print("Course not found.")
        return

    print(f"Input marks for course {course_id}:")
    course_marks = []

    for s in students:
        m = float(input(f"Mark for student {s['name']} ({s['id']}): "))
        course_marks.append((s["id"], m))

    marks[course_id] = course_marks


# ------------------------
# LISTING FUNCTIONS
# ------------------------

def list_students():
    print("\nStudents:")
    for s in students:
        print(f"- {s['id']} | {s['name']} | {s['dob']}")


def list_courses():
    print("\nCourses:")
    for c in courses:
        print(f"- {c['id']} | {c['name']}")


def show_marks():
    course_id = input("Enter course ID to show marks: ")

    if course_id not in marks:
        print("No marks found for this course.")
        return

    print(f"\nMarks for course {course_id}:")
    for (sid, mark) in marks[course_id]:
        # find student name
        name = ""
        for s in students:
            if s["id"] == sid:
                name = s["name"]
        print(f"- {sid} | {name}: {mark}")


# ------------------------
# MAIN PROGRAM
# ------------------------

def main():
    print("STUDENT MARK MANAGEMENT")
    while True:
        print("\n--- MENU ---")
        print("1. Input students")
        print("2. Input courses")
        print("3. Input marks")
        print("4. List students")
        print("5. List courses")
        print("6. Show marks")
        print("0. Exit")

        choice = input("Your choice: ")

        if choice == "1":
            input_number_of_students()
        elif choice == "2":
            input_number_of_courses()
        elif choice == "3":
            input_marks()
        elif choice == "4":
            list_students()
        elif choice == "5":
            list_courses()
        elif choice == "6":
            show_marks()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
