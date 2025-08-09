import random

TILES = ['sword', 'shield', 'bow', 'staff', 'gold', 'heart']
SYMBOLS = {
    'sword': 'Sw',
    'shield': 'Sh',
    'bow': 'Bo',
    'staff': 'St',
    'gold': 'Go',
    'heart': 'He'
}

STOCKPILE = {tile: 0 for tile in TILES}

SIZE = 8


def random_tile():
    return random.choice(TILES)


def create_board():
    board = [[random_tile() for _ in range(SIZE)] for _ in range(SIZE)]
    # Ensure no initial matches
    while find_matches(board):
        board = [[random_tile() for _ in range(SIZE)] for _ in range(SIZE)]
    return board


def display_board(board):
    for row in board:
        print(' '.join(SYMBOLS[t] for t in row))
    print()


def find_matches(board):
    matches = []
    # Horizontal
    for r in range(SIZE):
        c = 0
        while c < SIZE:
            run = 1
            while c + run < SIZE and board[r][c] == board[r][c+run]:
                run += 1
            if run >= 3:
                matches.append({(r, c+i) for i in range(run)})
            c += run
    # Vertical
    for c in range(SIZE):
        r = 0
        while r < SIZE:
            run = 1
            while r + run < SIZE and board[r][c] == board[r+run][c]:
                run += 1
            if run >= 3:
                matches.append({(r+i, c) for i in range(run)})
            r += run
    return matches


def remove_matches(board, matches):
    for group in matches:
        # Assume all tiles in group same type
        tile = board[next(iter(group))[0]][next(iter(group))[1]]
        length = len(group)
        if length == 3:
            STOCKPILE[tile] += 3
        elif length == 4:
            STOCKPILE[tile] += 5
        else:  # 5 or more
            STOCKPILE[tile] += 8
        for r, c in group:
            board[r][c] = None


def collapse(board, direction):
    if direction == 'up':
        for c in range(SIZE):
            tiles = [board[r][c] for r in range(SIZE) if board[r][c] is not None]
            for r in range(len(tiles)):
                board[r][c] = tiles[r]
            for r in range(len(tiles), SIZE):
                board[r][c] = random_tile()
    elif direction == 'down':
        for c in range(SIZE):
            tiles = [board[r][c] for r in range(SIZE-1, -1, -1) if board[r][c] is not None]
            for i, tile in enumerate(tiles):
                board[SIZE-1-i][c] = tile
            for r in range(SIZE - len(tiles)):
                board[r][c] = random_tile()
    elif direction == 'left':
        for r in range(SIZE):
            tiles = [board[r][c] for c in range(SIZE) if board[r][c] is not None]
            for c in range(len(tiles)):
                board[r][c] = tiles[c]
            for c in range(len(tiles), SIZE):
                board[r][c] = random_tile()
    elif direction == 'right':
        for r in range(SIZE):
            tiles = [board[r][c] for c in range(SIZE-1, -1, -1) if board[r][c] is not None]
            for i, tile in enumerate(tiles):
                board[r][SIZE-1-i] = tile
            for c in range(SIZE - len(tiles)):
                board[r][c] = random_tile()


def swap(board, r, c, direction):
    dr, dc = {'up': (-1,0), 'down': (1,0), 'left': (0,-1), 'right': (0,1)}[direction]
    r2, c2 = r + dr, c + dc
    if not (0 <= r2 < SIZE and 0 <= c2 < SIZE):
        print('Swap out of bounds')
        return False
    board[r][c], board[r2][c2] = board[r2][c2], board[r][c]
    matches = find_matches(board)
    if not matches:
        board[r][c], board[r2][c2] = board[r2][c2], board[r][c]
        print('No match')
        return False
    while matches:
        remove_matches(board, matches)
        collapse(board, direction)
        matches = find_matches(board)
    return True


def main():
    board = create_board()
    while True:
        display_board(board)
        print('Stockpile:', STOCKPILE)
        move = input('Enter row col direction (up/down/left/right) or q: ')
        if move.lower() == 'q':
            break
        try:
            r, c, d = move.split()
            r, c = int(r), int(c)
            if d not in ('up','down','left','right'):
                raise ValueError
        except ValueError:
            print('Invalid input')
            continue
        swap(board, r, c, d)


if __name__ == '__main__':
    main()
