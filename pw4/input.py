def input_student_data():
    sid = input("Student ID: ")
    name = input("Name: ")
    dob = input("DoB: ")
    return sid, name, dob


def input_course_data():
    cid = input("Course ID: ")
    name = input("Course name: ")
    credit = int(input("Credit: "))
    return cid, name, credit
