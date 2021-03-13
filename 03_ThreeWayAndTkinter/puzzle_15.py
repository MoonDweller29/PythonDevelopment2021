import tkinter as tk
import numpy as np
from tkinter.constants import *

class GameBoardWidget(tk.Frame):
    def __init__(self, master=None, size=(4,4)):
        tk.Frame.__init__(self, master)
        self.size = size
        for i in range(4):
            self.grid_rowconfigure(i, weight=1, uniform="_")
            self.grid_columnconfigure(i, weight=1, uniform="_")

        self.chip_buttons = [
            [tk.Button(self, text=str(i*size[1] + j), command=self.quit) for j in range(1, size[1]+1)]
            for i in range(0, size[0])
        ]

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
        self.grid_rowconfigure(1, weight=1, uniform="_")
        for i in range(4):
            self.grid_columnconfigure(i, weight=1, uniform="_")

        self.createWidgets()
        self.game_board_widget = GameBoardWidget(self, (4,4))
        self.game_board_widget.grid(columnspan=4, sticky="nswe")
        self.game_board = np.array([
            [ 1, 2, 3, 4],
            [ 5, 6, 7, 8],
            [ 9,10,11,12],
            [13,14,15,16],
        ])
        self.game_board_widget.draw(self.game_board)

    def createWidgets(self):
        self.moveCountLabelText = tk.StringVar()
        self.moveCountLabelText.set("Move count: 0")
        self.moveCountLabel = tk.Label(self, textvariable=self.moveCountLabelText)
        self.restartButton = tk.Button(self, text='Restart', command=self.quit)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)

        self.restartButton.grid(row=0, column=0, sticky="nswe")
        self.moveCountLabel.grid(row=0, column=1, columnspan=2, sticky="nswe")
        self.quitButton.grid(row=0, column=3, sticky="nswe")


app = Application(tk.Tk())
app.master.title('Puzzle of 15')
app.mainloop()
