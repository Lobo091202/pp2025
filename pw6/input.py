def input_student_data():
    sid = input("Student ID: ").strip()
    name = input("Name: ").strip()
    dob = input("Date of Birth: ").strip()
    return sid, name, dob

def input_course_data():
    cid = input("Course ID: ").strip()
    name = input("Course name: ").strip()
    while True:
        try:
            credit = float(input("Credit (numeric): "))
            break
        except ValueError:
            print("Invalid credit. Enter a number.")
    return cid, name, credit
