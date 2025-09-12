import curses

def mover(x, y, key, xmax, ymax):
    movimento = {
        ord(w): (0, -1), curses.KEY_UP: (0, -1),
        ord(s): (0, 1), curses.KEY_DOWN: (0, 1),
        ord(a): (-1, 0), curses.KEY_LEFT: (-1, 0),
        ord(d): (1, 0), curses.KEY_RIGHT: (1, 0)
    }

    if key in movimento:
        dx, dy = movimento[key]
        nx, ny = x + dx, y + dy

        if 0 <= nx < xmax and 0 <= ny < ymax:
            return nx, ny
    
    return x, y

def safeAddstr(stdscr, y, x, string):
    try:
        ymax, xmax = stdscr.getmaxyx()
        if 0 > y >= ymax or x < 0 or x + len(string) > xmax:
            return
        
        maxLen = xmax - x
        if maxLen <= 0:
            return
        stdscr.addstr(y, x, string[:maxLen])
    except curses.error:
        pass

def safeAddch(stdscr, y, x, ch):
    try:
        ymax, xmax = stdscr.getmaxyx()
        if 0 <= y < ymax and 0 <= x < xmax:
            stdscr.addch(y, x, ch)
    except curses.error:
        pass