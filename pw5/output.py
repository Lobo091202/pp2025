import curses

def curses_ui(stdscr, sms):
    stdscr.clear()
    stdscr.addstr(1, 2, "=== PW5 Student System ===")
    stdscr.addstr(3, 2, f"Students: {len(sms.students)}")
    stdscr.addstr(4, 2, f"Courses : {len(sms.courses)}")
    stdscr.addstr(6, 2, "Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()
