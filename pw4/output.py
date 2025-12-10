import curses

def curses_ui(stdscr, sms):
    stdscr.clear()
    stdscr.addstr(1, 2, "=== Student Mark System (Curses UI) ===")
    stdscr.addstr(3, 2, "Students Loaded: " + str(len(sms.students)))
    stdscr.addstr(4, 2, "Courses Loaded : " + str(len(sms.courses)))
    stdscr.addstr(6, 2, "Press any key to exit")
    stdscr.refresh()
    stdscr.getch()
