import numpy as np
import random
import tkinter as tk
from tkinter.constants import *

class GameBoard:
    def __init__(self, gui, size=(4,4)):
        self.gui = gui
        self.board = np.zeros(size).astype(np.uint8)
        self.__random_board_fill()

        self.move_count = 0

    def __random_board_fill(self):
        l = list(range(1, self.board.size + 1))
        random.shuffle(l)

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                self.board[i,j] = l[i*self.board.shape[1] + j]

    def get_board(self):
        return self.board

    def get_move_count(self):
        return self.move_count

    def restart(self):
        self.__random_board_fill()
        self.move_count = 0

class GameBoardWidget(tk.Frame):
    def __init__(self, core, master=None, size=(4,4)):
        tk.Frame.__init__(self, master)
        self.core = core
        self.size = size
        for i in range(4):
            self.grid_rowconfigure(i, weight=1, uniform="_")
            self.grid_columnconfigure(i, weight=1, uniform="_")

        self.chip_buttons = [
            [tk.Button(self, text=str(i*size[1] + j), command=self.quit) for j in range(1, size[1]+1)]
            for i in range(0, size[0])
        ]

    def __click_callback(self, i, j):
        pass

    def draw(self, arr):
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                self.chip_buttons[i][j].grid(row=i, column=j, sticky="nswe")
                if (arr[i,j] != 16):
                    self.chip_buttons[i][j].configure(text=str(arr[i,j]))
                else:
                    self.chip_buttons[i][j].grid_forget()



class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack(fill=BOTH, expand=1)

        self.game_board = GameBoard(self, (4,4))
        self.createWidgets()

        self.draw()

    def restart(self):
        self.game_board.restart()
        self.game_board_widget.draw(self.game_board.get_board())

    def update_move_count_label(self):
        self.moveCountLabelText.set("Move count: {}".format(self.game_board.get_move_count()))

    def createWidgets(self):
        self.grid_rowconfigure(1, weight=1, uniform="_")
        for i in range(4):
            self.grid_columnconfigure(i, weight=1, uniform="_")

        self.moveCountLabelText = tk.StringVar()
        self.moveCountLabel = tk.Label(self, textvariable=self.moveCountLabelText)
        self.restartButton = tk.Button(self, text='Restart', command=self.restart)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.game_board_widget = GameBoardWidget(self.game_board, self, (4,4))

    def draw(self):
        self.update_move_count_label()
        self.restartButton.grid(row=0, column=0, sticky="nswe")
        self.moveCountLabel.grid(row=0, column=1, columnspan=2, sticky="nswe")
        self.quitButton.grid(row=0, column=3, sticky="nswe")

        self.game_board_widget.grid(columnspan=4, sticky="nswe")
        self.game_board_widget.draw(self.game_board.get_board())


app = Application(tk.Tk())
app.master.title('Puzzle of 15')
app.mainloop()
