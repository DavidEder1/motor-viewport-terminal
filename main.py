import curses

def mover(x, y, key, grid_cols, grid_rows):
    # Dicionário que relaciona teclas com deslocamento (dx, dy)
    # dx altera coluna (x), dy altera linha (y)
    movimento = {
        ord('w'): (0, -1), ord('W'): (0, -1), curses.KEY_UP: (0, -1),
        ord('s'): (0, 1),  ord('S'): (0, 1),  curses.KEY_DOWN: (0, 1),
        ord('a'): (-1, 0), ord('A'): (-1, 0), curses.KEY_LEFT: (-1, 0),
        ord('d'): (1, 0),  ord('D'): (1, 0),  curses.KEY_RIGHT: (1, 0),
    }

    # Se a tecla está no dicionário, calcula nova posição
    if key in movimento:
        dx, dy = movimento[key]
        nx, ny = x + dx, y + dy
        # Garante que não saia da grid
        if 0 <= nx < grid_cols and 0 <= ny < grid_rows:
            return nx, ny
    # Se a tecla não é válida ou sai dos limites, mantém posição
    return x, y

def safeAddstr(stdscr, y, x, string):
    try:
        rows, cols = stdscr.getmaxyx()
        # Verifica se a posição é válida dentro da tela
        if y < 0 or y >= rows or x < 0 or x >= cols:
            return
        # Calcula quantos caracteres ainda cabem na linha
        maxLen = cols - x
        if maxLen <= 0:
            return
        # Escreve o texto limitado ao espaço disponível
        stdscr.addstr(y, x, string[:maxLen])
    except curses.error:
        pass  # Ignora erros do curses quando não dá pra escrever

def safeAddch(stdscr, y, x, ch):
    try:
        rows, cols = stdscr.getmaxyx()
        # Só escreve se estiver dentro da tela
        if 0 <= y < rows and 0 <= x < cols:
            # ch deve ser apenas um caractere
            stdscr.addch(y, x, ch)
    except curses.error:
        pass

def safeTerminalSize(stdscr, min_rows, min_cols, rows, cols):
    # Verifica se o terminal atende os requisitos mínimos
    if rows < min_rows or cols < min_cols:
        # Se for muito pequeno, mostra mensagens adaptadas
        if rows < 3:
            if rows >= 1 and cols >= 20:
                safeAddstr(stdscr, 0, 0, "TERMINAL MUITO PEQUENO!")
            if rows >= 2 and cols >= 15:
                safeAddstr(stdscr, 1, 0, f"{rows}L x {cols}C - AUMENTE O TERMINAL!")
        else:
            # Mostra informações mais completas quando tem mais linhas
            safeAddstr(stdscr, 0, 0, '=' * min(40, cols))
            if rows >= 2:
                safeAddstr(stdscr, 1, 0, 'TERMINAL MUITO PEQUENO!')
            if rows >= 3:
                safeAddstr(stdscr, 2, 0, f'Min: {min_rows}L x {min_cols}C')
            if rows >= 4:
                safeAddstr(stdscr, 3, 0, f'Atual: {rows}L x {cols}C')
            if rows >= 5:
                safeAddstr(stdscr, 4, 0, 'Aumente o terminal ou Q para sair')
        # Retorna True para indicar que não dá pra rodar o jogo
        return True
    return False

def main(stdscr):
    # Configurações do curses
    curses.curs_set(0)       # Esconde o cursor
    stdscr.nodelay(True)     # Não bloqueia esperando tecla
    stdscr.timeout(100)      # Tempo máximo de espera (ms)
    stdscr.keypad(True)      # Habilita setas e outras teclas especiais

    # Define tamanho da grid do jogo
    grid_cols, grid_rows = 19, 9
    # Posição inicial do jogador (meio da grid)
    x, y = grid_cols // 2, grid_rows // 2

    # Tamanho mínimo do terminal para rodar o jogo
    min_rows_needed = grid_rows + 3
    min_cols_needed = grid_cols * 2  # cada coluna ocupa 2 caracteres na tela

    while True:
        stdscr.clear()
        rows, cols = stdscr.getmaxyx()

        # Verifica se o terminal é grande o suficiente
        if safeTerminalSize(stdscr, min_rows_needed, min_cols_needed, rows, cols):
            stdscr.refresh()
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')):
                break
            continue  # volta ao início do loop

        # Desenha a grid
        for i in range(grid_rows):
            for j in range(grid_cols):
                col = j * 2  # espaço extra entre colunas
                if i == y and j == x:
                    safeAddch(stdscr, i, col, '+')  # jogador
                else:
                    safeAddch(stdscr, i, col, '.')  # espaço vazio

        # Mostra informações abaixo da grid
        infoY1 = grid_rows
        infoY2 = grid_rows + 1
        safeAddstr(stdscr, infoY1, 0, f'Posição: ({x}, {y}) Tamanho Terminal: {rows}L x {cols}C')
        safeAddstr(stdscr, infoY2, 0, 'Use W/A/S/D ou setas para mover. Q para sair.')

        stdscr.refresh()
        # Captura uma tecla por iteração
        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            break
        # Atualiza posição do jogador
        x, y = mover(x, y, key, grid_cols, grid_rows)

if __name__ == "__main__":
    # Inicia o programa no modo curses
    curses.wrapper(main)
ds