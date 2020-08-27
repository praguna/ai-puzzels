import random as r
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from tic_tac_toe.algorithm import get_symbol, find_best_move, update_state, is_draw

sys.setrecursionlimit(10000)


def build_gui(dim):
    root = tk.Tk()
    App(root, dim).pack(side="top", fill="both", expand=True)
    root.mainloop()


class App(tk.Frame):
    def __init__(self, parent, dim, **kw):
        super().__init__(parent, **kw)
        parent.minsize(dim[0], dim[1])
        parent.title("Tic Tac Toe")
        self.define_display_widgets()
        messagebox.showinfo("Info", "Welcome to Tic Tac Toe Game ")
        self.ttt_grid = Grid(self, {"tile_color": "red", "text": "Puzzle Grid"})

    def define_display_widgets(self):
        self.label = tk.Label(self, text="Let's play Tic Tac Toe", font=('Verdana', 15, 'bold'))
        self.label.pack(side=tk.TOP)
        self.reset = tk.Button(self, text="Reset", bg="grey", fg="white", command=self.reset_all)
        self.reset.pack(side=tk.LEFT, anchor=tk.N)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(after=self.label, fill=tk.X)

    def reset_all(self):
        self.ttt_grid.disable_or_reset(disable=False)


class Grid(tk.Frame):

    def __init__(self, parent, config, **kw):
        super().__init__(parent, **kw)
        self.b = [[], [], []]
        self.config = config
        self.draw_grid()
        tk.Label(parent, text=config["text"], font=('Verdana', 20, 'bold'), pady=5).pack()
        self.score = tk.Label(parent, text="", font=('Verdana', 10, 'bold'), pady=2)
        self.score.pack()
        self.pack(pady=15)
        self.set_algo()

    def draw_grid(self):
        for i in range(3):
            for j in range(3):
                self.b[i].append(self.button())
                self.b[i][j].config(command=lambda row=i, col=j: self.fill(row, col))
                self.b[i][j].grid(row=i, column=j)

    def button(self):
        return tk.Button(self, bd=5, width=2, font=('arial', 50, 'bold'))

    def fill(self, i, j):
        self.b[i][j].config(text=get_symbol(self.turn), state=tk.DISABLED, bg="black", fg="white")
        self.algo_value[i * 3 + j] = get_symbol(self.turn)
        status  = self.check_if_game_ended("Player")
        if status: return
        self.turn = update_state(self.algo_value, i, j, self.turn)
        self.ai_move()

    def ai_move(self, start=None):
        if start:
            move, s = start, 0
        else:
            move, s = find_best_move(self.algo_value, True, self.turn)
        self.score.config(text="current minimax score {}".format(s))
        index = 0
        for i in range(9):
            if self.algo_value[i] != move[i]:
                index = i
                break
        self.algo_value = move
        self.b[index // 3][index % 3].config(text=get_symbol(self.turn), state=tk.DISABLED, fg="white", bg="red")
        self.turn = not self.turn
        self.check_if_game_ended("Computer")

    def check_if_game_ended(self, player):
        if is_draw(self.algo_value):
            messagebox.showinfo("Info", "Game is drawn !!")
            return True
        is_own, v = self.has_won()
        if is_own:
            messagebox.showinfo("Info", "{} has won !".format(player))
            self.highlight(v)
            return True
        return False

    def highlight(self, v):
        for x in v:
            self.b[x // 3][x % 3].config(fg="black", bg="blue")
        self.disable_or_reset()

    def disable_or_reset(self, disable=True):
        for i in range(3):
            for j in range(3):
                if disable:
                    self.b[i][j].config(state=tk.DISABLED)
                else:
                    self.b[i][j].config(text="", bg=self.cget('bg'), fg="black", state=tk.NORMAL)
        if not disable: self.set_algo()

    def set_algo(self):
        val = messagebox.askquestion("Info", "Do you want me to start ?")
        self.algo_value = [-1] * 9
        self.turn = True
        if val == "yes":
            i = r.choice([2, 0, 6, 8, 1, 3, 5, 7])
            m = self.algo_value[:]
            m[i] = 'X'
            self.ai_move(m)

    def has_won(self):
        curr = self.algo_value
        for i in range(3):
            if curr[3 * i] == curr[3 * i + 1] == curr[3 * i + 2] != -1:
                return True, (3 * i, 3 * i + 1, 3 * i + 2)
            if curr[0 + i] == curr[3 + i] == curr[6 + i] != -1:
                return True, (0 + i, 3 + i, 6 + i)
        if curr[0] == curr[4] == curr[8] != -1:
            return True, (0, 4, 8)
        if curr[2] == curr[4] == curr[6] != -1:
            return True, (2, 4, 6)
        return False, None
