from domains.system import StudentMarkSystem
from input import input_student_data, input_course_data
from output import curses_ui
import curses

def main():
    sms = StudentMarkSystem()

    # Add students
    for _ in range(2):
        sid, name, dob = input_student_data()
        sms.add_student(sid, name, dob)

    # Add courses
    for _ in range(2):
        cid, name, credit = input_course_data()
        sms.add_course(cid, name, credit)

    # Input marks
    for c in sms.courses:
        sms.input_marks(c.get_id())

    # GPA
    sms.calculate_all_gpa()
    sms.sort_by_gpa()

    curses.wrapper(curses_ui, sms)


if __name__ == "__main__":
    main()
