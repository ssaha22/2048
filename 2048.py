from random import randint
from copy import deepcopy

def add_tile(board):
    x = randint(1,10)
    if x == 10:
        tile = 4
    else:
        tile = 2
    while True:
        a, b = randint(0,3), randint(0,3)
        if board[a][b] == 0:
            board[a][b] = tile
            break
    return board

def new_board():
    board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    board = add_tile(board)
    board = add_tile(board)
    return board

def flip_horizontal(board):
    for i in range(4):
        board[i][0], board[i][3] = board[i][3], board[i][0]
        board[i][1], board[i][2] = board[i][2], board[i][1]
    return board

def transpose(board):
    for i in range(3):
        board[i][0], board[0][i] =  board[0][i], board[i][0]
        board[i][3], board[3][i] =  board[3][i], board[i][3]
    board[1][2], board[2][1] =  board[2][1], board[1][2]
    return board

def shift_row_right(row):
    for i in range(2,-1,-1):
        if row[i+1] == 0:
                row[i+1], row[i] = row[i], 0
    return row

def merge(row, score):
    for i in range(2,-1,-1):
            if row[i+1] == row[i]:
                row[i+1] *= 2
                score += row[i+1]
                row[i] = 0
    return row, score

def right(board, score=0):
    for row in board:
        for i in range(3):
            row = shift_row_right(row)
        row, score = merge(row, score)
        row = shift_row_right(row)
    return board, score

def left(board, score=0):
    board = flip_horizontal(board)
    board, score = right(board, score)
    board = flip_horizontal(board)
    return board, score

def down(board, score=0):
    board = transpose(board)
    board, score = right(board, score)
    board = transpose(board)
    return board, score

def up(board, score=0):
    board = transpose(board)
    board, score = left(board, score)
    board = transpose(board)
    return board, score

def move(board, score):
    directions = {'w': up, 'a': left, 's': down, 'd': right}
    while True:
        key = input("Enter 'w' to move up, 'a' to move left, 's' to move down, or 'd' to move right: ")
        key = key.lower()
        if key in directions:
            return directions[key](board, score)
        print("Invalid input. Please try again.")

def game_won(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 2048:
                return True
    return False

def game_lost(board):
    right_board = right(deepcopy(board))[0]
    left_board = left(deepcopy(board))[0]
    up_board = up(deepcopy(board))[0]
    down_board = down(deepcopy(board))[0]
    return(right_board == board and left_board == board and up_board == board and down_board == board)

def render_board(board):
    def render_number(n):
        if n == 0:
            return "      "
        elif len(str(n)) == 1:
            return f"   {n}  "
        elif len(str(n)) == 2:
            return f"  {n}  "
        elif len(str(n)) == 3:
            return f"  {n} "
        elif len(str(n)) == 4:
            return f" {n} "
    print("-----------------------------")
    for i in range(4):
        print("|      |      |      |      |")
        print("|", end="")
        for j in range(4):
            print(render_number(board[i][j]), end="|")
        print("\n|      |      |      |      |")
        print("-----------------------------")

def main():
    score = 0
    board = new_board()
    render_board(board)
    while True:
        old_board = deepcopy(board)
        board,score = move(board, score)
        if not old_board == board:
            board = add_tile(board)
        render_board(board)
        print("Score:", score)
        if game_won(board):
            print("Congratulations! You won!")
            break
        elif game_lost(board):
            print("Game over! You lost!")
            break

if __name__ == "__main__":
    main()