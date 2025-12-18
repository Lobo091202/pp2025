from domains.system import StudentMarkSystem
from input import input_student_data, input_course_data
from output import curses_ui
import curses

def main():
    sms = StudentMarkSystem()

    # Step 1 — load old data if exists
    sms.load_if_exist()

    # Step 2 — input new students
    n = int(input("Number of students to add: "))
    for _ in range(n):
        sid, name, dob = input_student_data()
        sms.add_student(sid, name, dob)

    # Step 3 — input new courses
    c = int(input("Number of courses to add: "))
    for _ in range(c):
        cid, name, credit = input_course_data()
        sms.add_course(cid, name, credit)

    # Step 4 — input marks for every course
    for course in sms.courses:
        print(f"Input marks for course {course.get_id()}:")
        sms.input_marks(course.get_id())

    # Step 5 — calculate GPA + sort
    sms.calculate_all_gpa()
    sms.sort_by_gpa()

    # Step 6 — save .txt files
    sms.save_text_files()

    # Step 7 — compress all into students.dat
    sms.compress_all()

    print("All data saved & compressed into students.dat !")

    # Step 8 — optional curses UI
    curses.wrapper(curses_ui, sms)


if __name__ == "__main__":
    main()
