def print_summary(sms):
    print("=== SUMMARY ===")
    print("Students:")
    for s in sms.students:
        print(f" - {s.get_id()} | {s.get_name()} | GPA: {s.get_gpa():.2f}" if s.get_gpa() is not None else f" - {s.get_id()} | {s.get_name()} | GPA: N/A")
    print("\nCourses:")
    for c in sms.courses:
        print(f" - {c.get_id()} | {c.get_name()} | credits: {c.get_credit()}")

# Optional curses UI (use with caution on Windows).
def curses_ui(stdscr, sms):
    import curses
    stdscr.clear()
    stdscr.addstr(0, 2, "PW6 Student Mark System")
    stdscr.addstr(2, 2, f"Students: {len(sms.students)}")
    stdscr.addstr(3, 2, f"Courses : {len(sms.courses)}")
    stdscr.addstr(5, 2, "Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()
