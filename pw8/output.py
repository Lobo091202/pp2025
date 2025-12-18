def print_summary(sms):
    print("=== SUMMARY ===")
    if not sms.students:
        print("No students.")
    else:
        for s in sms.students:
            gpa = s.get_gpa()
            gpa_str = f"{gpa:.2f}" if gpa is not None else "N/A"
            print(f"- {s.get_id()} | {s.get_name()} | GPA: {gpa_str}")

    print("\nCourses:")
    if not sms.courses:
        print("No courses.")
    else:
        for c in sms.courses:
            print(f"- {c.get_id()} | {c.get_name()} | credits: {c.get_credit()}")

def curses_ui(stdscr, sms):
    import curses
    stdscr.clear()
    stdscr.addstr(0, 2, "PW8 Student Mark System (Background Saver)")
    stdscr.addstr(2, 2, f"Students: {len(sms.students)}")
    stdscr.addstr(3, 2, f"Courses : {len(sms.courses)}")
    stdscr.addstr(5, 2, "Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()
