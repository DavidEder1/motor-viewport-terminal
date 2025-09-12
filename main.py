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
        h, w = stdscr.getmaxyx()
        if y < 0 or y >= h or x < 0 or x + len(string) > w:
            return
        
        maxLen = w - x

        if maxLen <= 0:
            return
        stdscr.addstr(y, x, string[:maxLen])
    except curses.error:
        pass

