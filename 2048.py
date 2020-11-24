import tkinter as tk
from random import randint
from copy import deepcopy


WINDOW_BACKGROUND_COLOR = "#FAF8EF"

TITLE_TEXT_COLOR = "#776E65"
TITLE_FONT = ("Clear Sans", 70, "bold")

SCORE_BACKROUND_COLOR = "#BBADA0"
SCORE_TEXT_COLOR = "#F9F6F2"
SCORE_LABEL_FONT = ("Clear Sans", 15, "bold")
SCORE_FONT = font=("Clear Sans", 25, "bold")

BOARD_BACKGROUND_COLOR = "#BBADA0"
EMPTY_TILE_COLOR = "#D6CDC4"
TILE_COLORS = {2:"#EEE4DA", 4:"#EDE0C8", 8:"#F2B179", 16:"#F59563",
                32:"#F67C5F", 64:"#F65E3B", 128:"#EDCF72", 256:"#EDCC61",
                512:"#EDC850", 1024:"#EDC53F", 2048:"#EDC22E"}
TILE_TEXT_COLORS = {2:"#776E65", 4:"#776E65", 8:"#F9F6F2", 16:"#F9F6F2",
                    32:"#F9F6F2", 64:"#F9F6F2", 128:"#F9F6F2", 256:"#F9F6F2",
                    512:"#F9F6F2", 1024:"#F9F6F2", 2048:"#F9F6F2"}
TILE_FONT = ("Clear Sans", 30, "bold")


class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("2048")
        self.geometry("410x500")
        self.resizable(0,0)
        self.configure(bg=WINDOW_BACKGROUND_COLOR)

        self.name = tk.Label(text="2048", fg=TITLE_TEXT_COLOR, bg=WINDOW_BACKGROUND_COLOR, font=TITLE_FONT)
        self.name.grid(row=0, column=0)

        self.game = Game()
        self.old_game = self.game.copy()

        self.score_frame = tk.Frame(bg=SCORE_BACKROUND_COLOR)
        self.score_frame.grid(row=0, column=1)
        self.score_label = tk.Label(self.score_frame, text="SCORE",
                                    fg=SCORE_TEXT_COLOR, bg=SCORE_BACKROUND_COLOR,
                                    font=SCORE_LABEL_FONT)
        self.score_label.grid()
        self.score_text = tk.Label(self.score_frame, text=self.game.score,
                                    fg=SCORE_TEXT_COLOR, bg=SCORE_BACKROUND_COLOR, width=7, 
                                    font=SCORE_FONT)
        self.score_text.grid()

        self.tiles = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

        self.board_frame = tk.Frame(bg=BOARD_BACKGROUND_COLOR)
        self.board_frame.grid(row=1, columnspan=2, padx=9, pady=9)
        self.create_board()

        self.bind("<Key>", self.move)

        self.mainloop()

    def create_board(self):
        for i in range(4):
            for j in range(4):
                self.create_tile(i, j, self.game.board[i][j])
    
    def create_tile(self, x, y, value):
        if value == 0:
            tile = tk.Label(self.board_frame, bg=EMPTY_TILE_COLOR, width=4, 
                            height=2, font=TILE_FONT)
        else:
            tile = tk.Label(self.board_frame, text=str(value), 
                            fg=TILE_TEXT_COLORS[value], 
                            bg=TILE_COLORS[value], width=4, height=2,
                            font=TILE_FONT)
        tile.grid(row=x, column=y, padx=4, pady=4, ipadx=2, ipady=6)
        self.tiles[x][y] = tile
    
    def update_board(self):
        for i in range(4):
            for j in range(4):
                self.update_tile(i, j, self.game.board[i][j])

    def update_tile(self, x, y, value):
        if value == 0:
            self.tiles[x][y].config(text="", bg=EMPTY_TILE_COLOR)
        else:
            self.tiles[x][y].config(text=str(value), 
                                    fg=TILE_TEXT_COLORS[value],
                                    bg=TILE_COLORS[value])
    
    def update_score(self):
        self.score_text.config(text=self.game.score)
    
    def move(self, event):
        arrow_keys = {'Up':'w', 'Left':'a', 'Down':'s', 'Right': 'd'}
        key = event.keysym
        if key in arrow_keys:
            key = arrow_keys[key]
        if key in ['w', 'a', 's', 'd']:
            temp_game = self.game.copy()
            old_board = deepcopy(self.game.board)
            self.game.move(key)
            if self.game.board != old_board:
                self.game.add_tile()
                self.old_game = temp_game
        elif key == 'u':
            self.undo()
        elif key == 'r':
            self.restart()
        self.update_board()
        self.update_score()
    
    def undo(self):
        self.game = self.old_game

    def restart(self):
        del self.game
        self.game = Game()
        self.old_game = self.old_game.copy()


class Game:
    def __init__(self):
        self.board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.score = 0
        self.add_tile().add_tile()
    
    def add_tile(self):
        x = randint(1,10)
        if x == 10:
            tile = 4
        else:
            tile = 2
        while True:
            a, b = randint(0,3), randint(0,3)
            if self.board[a][b] == 0:
                self.board[a][b] = tile
                break
        return self

    def flip_horizontal(self):
        for i in range(4):
            self.board[i][0], self.board[i][3] = self.board[i][3], self.board[i][0]
            self.board[i][1], self.board[i][2] = self.board[i][2], self.board[i][1]
        return self
    
    def transpose(self):
        for i in range(3):
            self.board[i][0], self.board[0][i] =  self.board[0][i], self.board[i][0]
            self.board[i][3], self.board[3][i] =  self.board[3][i], self.board[i][3]
        self.board[1][2], self.board[2][1] =  self.board[2][1], self.board[1][2]
        return self
    
    def right(self):
        def shift_row_right(row):
            for i in range(2,-1,-1):
                if row[i+1] == 0:
                        row[i+1], row[i] = row[i], 0
        
        def merge(row):
            for i in range(2,-1,-1):
                if row[i+1] == row[i]:
                    row[i+1] *= 2
                    self.score += row[i+1]
                    row[i] = 0
        
        for row in self.board:
            for i in range(3):
                shift_row_right(row)
            merge(row)
            shift_row_right(row)
        return self
    
    def left(self):
        self.flip_horizontal().right().flip_horizontal()
        return self
    
    def down(self):
        self.transpose().right().transpose()
        return self
    
    def up(self):
        self.transpose().left().transpose()
        return self
    
    def get_move(self):
        while True:
            key = input("Enter 'w' to move up, 'a' to move left, 's' to move down, or 'd' to move right: ")
            key = key.lower()
            if key in ['w', 'a', 's', 'd']:
                return key
            print("Invalid input. Please try again.")
    
    def move(self, key):
        directions = {'w': self.up, 'a': self.left,
                      's': self.down, 'd': self.right}
        directions[key]()
    
    def copy(self):
        return deepcopy(self)

    def game_won(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 2048:
                    return True
        return False
    
    def game_lost(self):
        right_board = self.copy().right().board
        left_board = self.copy().left().board
        up_board = self.copy().up().board
        down_board = self.copy().down().board
        return(right_board == self.board and left_board == self.board
               and up_board == self.board and down_board == self.board)
    
    def render_game(self):
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
                print(render_number(self.board[i][j]), end="|")
            print("\n|      |      |      |      |")
            print("-----------------------------")
        print("Score:", self.score)
    
    def play(self):
        self.render_game()
        while True:
            old_board = deepcopy(self.board)
            key = self.get_move()
            self.move(key)
            if not old_board == game.board:
                self.add_tile()
            self.render_game()
            if self.game_won():
                print("Congratulations! You won!")
                break
            elif self.game_lost():
                print("Game over! You lost!")
                break


if __name__ == "__main__":
    Window()