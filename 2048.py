import argparse
import tkinter as tk
from random import randint
from copy import deepcopy
from sys import platform


FONT = "Sans"
BOLD = True

WINDOW_BACKGROUND_COLOR = "#FAF8EF"

TITLE_TEXT_COLOR = "#776E65"
TITLE_FONT_SIZE = 70

SCORE_BACKROUND_COLOR = "#BBADA0"
SCORE_TEXT_COLOR = "#F9F6F2"
SCORE_LABEL_FONT_SIZE = 15
SCORE_FONT_SIZE = 25

BUTTON_BACKGROUND_COLOR = "#BBADA0"
BUTTON_TEXT_COLOR = "#F9F6F2"
BUTTON_FONT_SIZE = 20

BOARD_BACKGROUND_COLOR = "#BBADA0"
EMPTY_TILE_COLOR = "#D6CDC4"
TILE_COLORS = {2:"#EEE4DA", 4:"#EDE0C8", 8:"#F2B179", 16:"#F59563",
                32:"#F67C5F", 64:"#F65E3B", 128:"#EDCF72", 256:"#EDCC61",
                512:"#EDC850", 1024:"#EDC53F", 2048:"#EDC22E"}
TILE_TEXT_COLORS = {2:"#776E65", 4:"#776E65", 8:"#F9F6F2", 16:"#F9F6F2",
                    32:"#F9F6F2", 64:"#F9F6F2", 128:"#F9F6F2", 256:"#F9F6F2",
                    512:"#F9F6F2", 1024:"#F9F6F2", 2048:"#F9F6F2"}
TILE_FONT_SIZE = 30

GAME_OVER_TEXT_COLOR = "#776E65"
GAME_OVER_FONT_SIZE = 50


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
            for _ in range(3):
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
            key = input("Enter 'w' to move up, 'a' to move left, "
                        "'s' to move down, or 'd' to move right: ")
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
            if not old_board == self.board:
                self.add_tile()
            self.render_game()
            if self.game_won():
                print("Congratulations! You won!")
                break
            elif self.game_lost():
                print("Game over! You lost!")
                break


class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("2048")
        self.resizable(0,0)
        self.configure(bg=WINDOW_BACKGROUND_COLOR)

        self.name = tk.Label(text="2048", fg=TITLE_TEXT_COLOR,
                             bg=WINDOW_BACKGROUND_COLOR, font=font(TITLE_FONT_SIZE))
        self.name.grid(row=0, column=0)

        self.game = Game()
        self.old_game = self.game.copy()

        self.score_frame = tk.Frame(bg=SCORE_BACKROUND_COLOR)
        self.score_frame.grid(row=0, column=1, padx=(0,25))
        self.score_label = tk.Label(self.score_frame, text="SCORE",
                                    fg=SCORE_TEXT_COLOR,
                                    bg=SCORE_BACKROUND_COLOR,
                                    font=font(SCORE_LABEL_FONT_SIZE))
        self.score_label.grid()
        self.score_text = tk.Label(self.score_frame, text=self.game.score,
                                   fg=SCORE_TEXT_COLOR,
                                   bg=SCORE_BACKROUND_COLOR,
                                   width=7,font=font(SCORE_FONT_SIZE))
        self.score_text.grid()

        self.undo_button = tk.Label(text="UNDO", fg=BUTTON_TEXT_COLOR,
                                    bg=BUTTON_BACKGROUND_COLOR, width=9,
                                    font=font(BUTTON_FONT_SIZE), pady=7)
        self.undo_button.grid(row=1, column=0, pady=3)
        self.undo_button.bind("<Button-1>", self.undo)

        self.restart_button = tk.Label(text="RESTART", fg=BUTTON_TEXT_COLOR,
                                       bg=BUTTON_BACKGROUND_COLOR, width=9,
                                       font=font(BUTTON_FONT_SIZE), pady=7)
        self.restart_button.grid(row=1, column=1, padx=(0,25), pady=3)
        self.restart_button.bind("<Button-1>", self.restart)

        self.tiles = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.board_frame = tk.Frame(bg=BOARD_BACKGROUND_COLOR, padx=4, pady=4)
        self.board_frame.grid(row=2, columnspan=2, padx=15, pady=25)
        self.create_board()

        self.bind("<Key>", self.move)

        self.game_over_frame = tk.Frame(bg=WINDOW_BACKGROUND_COLOR,
                                        padx=100, pady=100)

        self.mainloop()

    def create_board(self):
        for i in range(4):
            for j in range(4):
                self.create_tile(i, j, self.game.board[i][j])
    
    def create_tile(self, x, y, value):
        if value == 0:
            tile = tk.Label(self.board_frame, bg=EMPTY_TILE_COLOR, width=4,
                            height=2, font=font(TILE_FONT_SIZE))
        else:
            tile = tk.Label(self.board_frame, text=str(value), 
                            fg=TILE_TEXT_COLORS[value], 
                            bg=TILE_COLORS[value], width=4,
                            height=2, font=font(TILE_FONT_SIZE))
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
        self.update_board()
        self.update_score()
        if self.game.game_won():
            self.game_over_frame.after(500, self.game_over, "won")
        elif self.game.game_lost():
            self.game_over_frame.after(500, self.game_over, "lost")
    
    def undo(self, event):
        self.game = self.old_game
        self.update_board()
        self.update_score()

    def restart(self, event):
        del self.game
        self.game = Game()
        self.old_game = self.old_game.copy()
        self.update_board()
        self.update_score()
    
    def play_again(self, event):
        self.game_over_frame.place(x=1000, y=1000)
        self.bind("<Key>", self.move)
        self.restart(event)

    def quit(self, event):
        self.destroy()
    
    def game_over(self, state):
        if state == "won":
            text = "Congratulations!\nYou won!"
        elif state == "lost":
            text = "Game over!\nYou lost!"
        self.game_over_text = tk.Label(self.game_over_frame, text=text,
                                       fg=GAME_OVER_TEXT_COLOR,
                                       bg=WINDOW_BACKGROUND_COLOR,
                                       font=font(GAME_OVER_FONT_SIZE))
        self.game_over_text.grid(pady=10)
        self.play_again_button = tk.Label(self.game_over_frame,
                                          text="PLAY AGAIN",
                                          fg=BUTTON_TEXT_COLOR,
                                          bg=BUTTON_BACKGROUND_COLOR, 
                                          width=11, 
                                          font=font(BUTTON_FONT_SIZE),
                                          pady=10)
        self.play_again_button.grid(pady=10)
        self.play_again_button.bind("<Button-1>", self.play_again)
        self.quit_button = tk.Label(self.game_over_frame, text="QUIT",
                                    fg=BUTTON_TEXT_COLOR,
                                    bg=BUTTON_BACKGROUND_COLOR,
                                    width=11, font=font(BUTTON_FONT_SIZE), 
                                    pady=10)
        self.quit_button.grid(pady=10)
        self.quit_button.bind("<Button-1>", self.quit)
        self.game_over_frame.place(anchor="center", relx=0.5, rely=0.55)
        self.unbind("<Key>")


def font(size):
    if BOLD:
        return (FONT, size, "bold")
    else:
        return (FONT, size)


def main():
    parser = argparse.ArgumentParser(description="2048 in Python")
    parser.add_argument("-t", "--terminal", 
                        help="play terminal version of 2048",
                        action="store_true")
    args = parser.parse_args()
    if args.terminal:
        game = Game()
        game.play()
    else:
        Window()


if __name__ == "__main__":
    main()