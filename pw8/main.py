import os
from domains.system import StudentMarkSystem
from input import input_student_data, input_course_data
from output import print_summary, curses_ui
import curses

DATA_PATH = os.path.join("data", "system.dat")

def main():
    # Try load existing pickled state (no saver started)
    sms = StudentMarkSystem.load_data(DATA_PATH)
    if sms is None:
        print("No saved system found. Starting fresh.")
        sms = StudentMarkSystem()
    else:
        print(f"Loaded system from {DATA_PATH}")

    # Start background saver
    sms.start_background_saver(DATA_PATH)
    print("Background saver started.")

    try:
        # Interactive flow
        try:
            n = int(input("How many students to add now? (0 for none): ") or "0")
        except ValueError:
            n = 0

        for _ in range(n):
            sid, name, dob = input_student_data()
            try:
                sms.add_student(sid, name, dob)
            except ValueError as e:
                print(e)
            # request async save
            sms.request_save()

        try:
            c = int(input("How many courses to add now? (0 for none): ") or "0")
        except ValueError:
            c = 0

        for _ in range(c):
            cid, name, credit = input_course_data()
            try:
                sms.add_course(cid, name, credit)
            except ValueError as e:
                print(e)
            sms.request_save()

        # Input marks for all courses if possible
        if sms.courses and sms.students:
            print("\nNow input marks for each course:")
            for course in sms.courses:
                print(f"--- Course {course.get_id()} : {course.get_name()} ---")
                sms.input_marks_for_course(course.get_id())
            sms.calculate_all_gpa()
            sms.sort_students_by_gpa_desc()
            sms.request_save()

        # Show summary (console)
        print_summary(sms)

        # Optional curses UI - commented by default (uncomment to use)
        # try:
        #     curses.wrapper(curses_ui, sms)
        # except Exception as e:
        #     print("Curses UI unavailable:", e)

        input("\nPress Enter to exit (background saver will flush pending saves)...")

    finally:
        # stop background saver and wait
        print("\nStopping background saver and waiting for pending saves...")
        sms.stop_background_saver(wait=True)
        print("Background saver stopped. Exiting.")

if __name__ == "__main__":
    main()
