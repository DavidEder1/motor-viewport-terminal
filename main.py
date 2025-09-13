import curses

def mover(x, y, key, grid_cols, grid_rows):
    # dx,dy onde dx altera coluna (x) e dy altera linha (y)
    movimento = {
        ord('w'): (0, -1), ord('W'): (0, -1), curses.KEY_UP: (0, -1),
        ord('s'): (0, 1),  ord('S'): (0, 1),  curses.KEY_DOWN: (0, 1),
        ord('a'): (-1, 0), ord('A'): (-1, 0), curses.KEY_LEFT: (-1, 0),
        ord('d'): (1, 0),  ord('D'): (1, 0),  curses.KEY_RIGHT: (1, 0),
    }

    if key in movimento:
        dx, dy = movimento[key]
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_cols and 0 <= ny < grid_rows:
            return nx, ny
    return x, y

def safeAddstr(stdscr, y, x, string):
    try:
        rows, cols = stdscr.getmaxyx()
        # validações corretas (y linhas, x colunas)
        if y < 0 or y >= rows or x < 0 or x >= cols:
            return
        maxLen = cols - x
        if maxLen <= 0:
            return
        stdscr.addstr(y, x, string[:maxLen])
    except curses.error:
        pass

def safeAddch(stdscr, y, x, ch):
    try:
        rows, cols = stdscr.getmaxyx()
        if 0 <= y < rows and 0 <= x < cols:
            # espera-se ch ser um único caractere
            stdscr.addch(y, x, ch)
    except curses.error:
        pass

def safeTerminalSize(stdscr, min_rows, min_cols, rows, cols):
    # rows,cols atuais vs mínimos exigidos
    if rows < min_rows or cols < min_cols:
        # desenho adaptado ao tamanho mínimo possível
        if rows < 3:
            if rows >= 1 and cols >= 20:
                safeAddstr(stdscr, 0, 0, "TERMINAL MUITO PEQUENO!")
            if rows >= 2 and cols >= 15:
                safeAddstr(stdscr, 1, 0, f"{rows}L x {cols}C - AUMENTE O TERMINAL!")
        else:
            safeAddstr(stdscr, 0, 0, '=' * min(40, cols))
            if rows >= 2:
                safeAddstr(stdscr, 1, 0, 'TERMINAL MUITO PEQUENO!')
            if rows >= 3:
                safeAddstr(stdscr, 2, 0, f'Min: {min_rows}L x {min_cols}C')
            if rows >= 4:
                safeAddstr(stdscr, 3, 0, f'Atual: {rows}L x {cols}C')
            if rows >= 5:
                safeAddstr(stdscr, 4, 0, 'Aumente o terminal ou Q para sair')
        # Não faz getch extra aqui — deixe caller decidir. Retorna True para "fechar".
        return True
    return False

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)
    stdscr.keypad(True)  # permite curses.KEY_UP / DOWN / LEFT / RIGHT

    # grid do jogo
    grid_cols, grid_rows = 19, 9
    x, y = grid_cols // 2, grid_rows // 2  # x: coluna na grid, y: linha na grid

    # requisitos mínimos (grid + linhas de info)
    min_rows_needed = grid_rows + 3
    min_cols_needed = grid_cols * 2  # porque col = j*2 no desenho

    while True:
        stdscr.clear()
        rows, cols = stdscr.getmaxyx()

        if safeTerminalSize(stdscr, min_rows_needed, min_cols_needed, rows, cols):
            stdscr.refresh()
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')):
                break
            continue  # volta pro topo do loop, esperando resize


        # desenha grid
        for i in range(grid_rows):
            for j in range(grid_cols):
                col = j * 2
                if i == y and j == x:
                    safeAddch(stdscr, i, col, '+')
                else:
                    safeAddch(stdscr, i, col, '.')

        # informações abaixo da grid
        infoY1 = grid_rows
        infoY2 = grid_rows + 1
        safeAddstr(stdscr, infoY1, 0, f'Posição: ({x}, {y}) Tamanho Terminal: {rows}L x {cols}C')
        safeAddstr(stdscr, infoY2, 0, 'Use W/A/S/D ou setas para mover. Q para sair.')

        stdscr.refresh()
        # pegue a tecla UMA vez por iteração
        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            break
        # atualiza posição usando limites da grid (não do terminal)
        x, y = mover(x, y, key, grid_cols, grid_rows)

if __name__ == "__main__":
    curses.wrapper(main)
