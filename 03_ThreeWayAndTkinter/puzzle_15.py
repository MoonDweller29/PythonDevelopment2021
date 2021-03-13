import numpy as np
import random
import tkinter as tk
from tkinter.constants import *
from tkinter import messagebox
from functools import partial

class GameBoard:
    def __init__(self, gui, size=(4,4)):
        self.gui = gui
        self.empty_num = size[0]*size[1]
        print(self.empty_num)
        self.board = np.zeros(size).astype(np.uint8)
        self.__random_board_fill()

        self.move_count = 0

    def __random_board_fill(self):
        l = list(range(1, self.board.size + 1))
        random.shuffle(l)

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                self.board[i,j] = l[i*self.board.shape[1] + j]
                # self.board[i,j] = i*self.board.shape[1] + j + 1

    def get_board(self):
        return self.board

    def get_move_count(self):
        return self.move_count

    def __get_num(self, i, j):
        i, j = self.__clip(i, j)
        return self.board[i,j]

    def __clip(self, i, j):
        i = np.clip(i, 0, self.board.shape[0]-1)
        j = np.clip(j, 0, self.board.shape[1]-1)
        return (i, j)

    def __find_empty(self, i, j):
        if (self.__get_num(i-1, j) == self.empty_num):
            return self.__clip(i-1, j)
        if (self.__get_num(i+1, j) == self.empty_num):
            return self.__clip(i+1, j)
        if (self.__get_num(i, j-1) == self.empty_num):
            return self.__clip(i, j-1)
        if (self.__get_num(i, j+1) == self.empty_num):
            return self.__clip(i, j+1)

        return (-1, -1)

    def move(self, i, j):
        pos_empty = self.__find_empty(i,j)
        if (pos_empty[0] < 0):
            return
        self.board[pos_empty] = self.board[i,j]
        self.board[i,j] = self.empty_num

        self.move_count+=1
        self.gui.draw()
        self.__check_win_condition()

    def __check_win_condition(self):
        is_win = True
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i,j] != i*self.board.shape[1] + j + 1 :
                    is_win = False

        if is_win:
            messagebox.showinfo("WIN", "You finished puzzle in {} moves".format(self.move_count))
            self.restart()


    def restart(self):
        self.__random_board_fill()
        self.move_count = 0
        self.gui.draw()

class GameBoardWidget(tk.Frame):
    def __init__(self, core, master=None, size=(4,4)):
        tk.Frame.__init__(self, master)
        self.core = core
        self.size = size
        self.empty_num = size[0]*size[1]
        for i in range(4):
            self.grid_rowconfigure(i, weight=1, uniform="_")
            self.grid_columnconfigure(i, weight=1, uniform="_")

        self.chip_buttons = [
            [
                tk.Button(self, text=str(i*size[1] + j+1), command=partial(self.__click_callback, i, j))
                for j in range(size[1])
            ]
            for i in range(size[0])
        ]

    def __click_callback(self, i, j):
        self.core.move(i,j)

    def draw(self, arr):
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                self.chip_buttons[i][j].grid(row=i, column=j, sticky="nswe")
                if (arr[i,j] != self.empty_num):
                    self.chip_buttons[i][j].configure(text="\n{}\n".format(arr[i,j]))
                else:
                    self.chip_buttons[i][j].grid_forget()



class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack(fill=BOTH, expand=1)
        self.board_size = (2,2)

        self.game_board = GameBoard(self, self.board_size)
        self.createWidgets()

        self.draw()

    def restart(self):
        self.game_board.restart()

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
        self.game_board_widget = GameBoardWidget(self.game_board, self, self.board_size)

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
