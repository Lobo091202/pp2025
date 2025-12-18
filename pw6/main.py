import os
import curses
from domains.system import StudentMarkSystem
from input import input_student_data, input_course_data
from output import print_summary, curses_ui

DATA_PATH = os.path.join("data", "system.dat")

def main():
    # Try to load existing system
    sms = StudentMarkSystem.load_data(DATA_PATH)
    if sms is None:
        print("No saved system found. Starting fresh.")
        sms = StudentMarkSystem()
    else:
        print(f"Loaded system from {DATA_PATH}")

    # --- interactive flow ---
    try:
        n = int(input("How many students to add now? (0 for none): "))
    except ValueError:
        n = 0

    for _ in range(n):
        sid, name, dob = input_student_data()
        try:
            sms.add_student(sid, name, dob)
        except ValueError as e:
            print(e)

    try:
        c = int(input("How many courses to add now? (0 for none): "))
    except ValueError:
        c = 0

    for _ in range(c):
        cid, name, credit = input_course_data()
        try:
            sms.add_course(cid, name, credit)
        except ValueError as e:
            print(e)

    # Input marks for each course
    if sms.courses and sms.students:
        print("\nNow input marks for each course:")
        for course in sms.courses:
            print(f"--- Course {course.get_id()} : {course.get_name()} ---")
            sms.input_marks_for_course(course.get_id())

    # Calculate GPA and sort
    sms.calculate_all_gpa()
    sms.sort_students_by_gpa_desc()

    # Show summary (console)
    print_summary(sms)

    # Optional: curses UI (uncomment if you want)
    # try:
    #     curses.wrapper(curses_ui, sms)
    # except Exception as e:
    #     print("Curses UI unavailable:", e)

    # Save before exit
    os.makedirs("data", exist_ok=True)
    sms.save_data(DATA_PATH)
    print(f"System saved to {DATA_PATH}")

if __name__ == "__main__":
    main()
