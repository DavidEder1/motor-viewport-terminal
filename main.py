import curses

def mover(x, y, key, xmax, ymax):
    movimento = {
        ord('w'): (0, -1),  curses.KEY_UP: (0, -1),
        ord('s'): (0, 1),   curses.KEY_DOWN: (0, 1),
        ord('a'): (-1, 0),  curses.KEY_LEFT: (-1, 0),
        ord('d'): (1, 0),   curses.KEY_RIGHT: (1, 0)
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
        pass # Adicionar erros em um log

def safeAddch(stdscr, y, x, ch):
    try:
        ymax, xmax = stdscr.getmaxyx()
        if 0 <= y < ymax and 0 <= x < xmax:
            stdscr.addch(y, x, ch) # Adicionar cores futuramente
    except curses.error:
        pass

def safeTerminalSize(stdscr, minRows, minCols, ymax, xmax):
    if ymax < minRows or xmax < minCols:
        if ymax < 3:  # Terminal minúsculo
            if ymax >= 1 and xmax >= 20:
                safeAddstr(stdscr, 0, 0, "TERMINAL MUITO PEQUENO!")
            if ymax >= 2 and xmax >= 15:
                safeAddstr(stdscr, 1, 0, f"{ymax}L x {xmax}C - AUMENTE O TERMINAL!")
        else:  # Terminal pequeno, mas dá pra mostrar algumas mensagens
            if ymax >= 1:
                safeAddstr(stdscr, 0, 0, '=' * min(40, xmax))  # Linha de separação
            if ymax >= 2:
                safeAddstr(stdscr, 1, 0, 'TERMINAL MUITO PEQUENO!')
            if ymax >= 3:
                safeAddstr(stdscr, 2, 0, f'Min: {minRows}L x {minCols}C')
            if ymax >= 4:
                safeAddstr(stdscr, 3, 0, f'Atual: {ymax}L x {xmax}C')
            if ymax >= 5:
                safeAddstr(stdscr, 4, 0, 'Aumente o terminal ou Q para sair')
        if softQuit(stdscr):
                return True

    return False

def softQuit(stdscr):
    stdscr.refresh()
    key = stdscr.getch()  # Captura tecla do usuário
    if key in (ord('Q'), ord('q')):
        return True
    return False


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    x, y = 10, 10
    xmax, ymax = stdscr.getmaxyx()

    minRowsNeeded = ymax + 3 # Espaço para debug da localização e instruções de movimento
    minColsNeeded = xmax * 2 # Espaçamento entre as colunas

    while True:
        stdscr.clear()
        alturamax, larguramax = stdscr.getmaxyx()

        if safeTerminalSize(stdscr, minRowsNeeded, minColsNeeded, alturamax, larguramax):
            break

        else:
            for i in range(ymax):
                for j in range(xmax):
                    col = j * 2
                    if i == y and j == x:
                        safeAddch(stdscr, i, col, '+')
                    else:
                        safeAddch(stdscr, i, col, '.')

            
            infoY1 = ymax + 1
            infoY2 = ymax + 2
            safeAddstr(stdscr, infoY1, 0, f'Posição: ({x}, {y}) Tamanho Terminal: {alturamax}L x {larguramax}C')
            safeAddstr(stdscr, infoY2, 0, 'Use W/A/S/D ou setas para mover. Q para sair.')

            stdscr.refresh()

            if softQuit(stdscr):
                break

            key = stdscr.getch()
            x, y = mover(x, y, key, xmax, ymax)

curses.wrapper(main)