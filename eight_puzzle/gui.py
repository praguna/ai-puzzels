import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
from time import sleep
from tkinter import messagebox

from eight_puzzle.algorithm import possible_moves, h


def build_gui(dim):
    root = tk.Tk()
    App(root, dim).pack(side="top", fill="both", expand=True)
    root.mainloop()


class App(tk.Frame):
    def __init__(self, parent, dim, **kw):
        super().__init__(parent, **kw)
        parent.minsize(dim[0], dim[1])
        parent.title("8 puzzle problem")
        self.stop = False
        self.done = False
        self.speed = 0.5
        self.define_display_widgets()
        self.define_puzzle()
        self.start_background_task()
        messagebox.showinfo("Info", "Welcome to 8 puzzle Demo:\n\nClick on the tiles to provide input and explore !")

    def start_background_task(self):
        self.t1 = Thread(target=self.algo_update)
        self.t1.setDaemon(True)
        self.t1.start()

    def stop_animation(self):
        self.stop = True
        self.done = False
        self.score.config(text="")
        self.reset_puzzle()

    def reset_puzzle(self):
        self.puzzle_src.reset()
        self.puzzle_dest.reset()

    def define_puzzle(self):
        self.puzzle_src = Puzzle(self, {"tile_color": "red", "text": "Start Configuration"})
        self.puzzle_dest = Puzzle(self, {"tile_color": "blue", "text": "Destination Configuration"})
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(after=self.puzzle_src, fill=tk.X, expand=True)

    def set_score(self, score, step):
        self.score.config(text="Score : {} , Steps : {}".format(score, step))

    def algo_update(self):
        while True:
            while not (self.puzzle_src.is_set() and self.puzzle_dest.is_set()) or self.done:
                if self.stop is True: self.done = False
            self.stop = False
            visited_states = []
            res = self.gui_search(self.puzzle_src.algo_value, self.puzzle_dest.algo_value, visited_states)
            if self.stop is True:
                messagebox.showinfo("Debug", "Resetting Widgets")
                self.reset_puzzle()
            elif res is True:
                messagebox.showinfo("Debug", "solution is reached !!")
            elif not res:
                messagebox.showinfo("Debug", "solution does not exist")
            self.done = True

    def gui_search(self, src, target, visited_states, g=0):
        if src == target or self.stop:
            self.puzzle_src.set_state(target, self.speed)
            return True
        visited_states.append(src)
        adj = possible_moves(src, visited_states)
        scores = []
        selected_moves = []
        for move in adj: scores.append(h(move) + g)
        if len(scores) == 0:
            min_score = 0
        else:
            min_score = min(scores)
        for i in range(len(adj)):
            if scores[i] == min_score: selected_moves.append(adj[i])
        for move in selected_moves:
            self.set_score(min_score, g + 1)
            self.puzzle_src.set_state(move, self.speed)
            if self.gui_search(move, target, visited_states, g + 1): return True
        return False

    def define_display_widgets(self):
        self.label = tk.Label(self, text="Let's solve the eight puzzle Problem", font=('Verdana', 15, 'bold'))
        self.label.pack(side=tk.TOP)
        self.score = tk.Label(self, text=" ", font=('Verdana', 10, 'bold'))
        self.score.pack(side=tk.TOP, anchor=tk.NE)
        self.reset = tk.Button(self, text="Reset", bg="grey", fg="white", command=self.stop_animation)
        self.reset.pack(side=tk.LEFT, anchor=tk.N)
        self.increase_speed = tk.Button(self, text="inc_speed", bg="grey", fg="white", command=self.inc_speed)
        self.increase_speed.pack(side=tk.RIGHT, anchor=tk.N)
        self.decrease_speed = tk.Button(self, text="dec_speed", bg="grey", fg="white", command=self.dec_speed)
        self.decrease_speed.pack(side=tk.RIGHT, anchor=tk.N)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(after=self.label, fill=tk.X)

    def inc_speed(self):
        self.speed /= 2

    def dec_speed(self):
        self.speed *= 2


class Puzzle(tk.Frame):
    def __init__(self, parent, config, **kw):
        super().__init__(parent, **kw)
        self.b = [[], [], []]
        self.config = config
        self.init_algo()
        self.draw_puzzle()
        tk.Label(parent, text=config["text"], font=('Verdana', 10, 'bold'), pady=5).pack()
        self.val = tk.Label(parent, text="", font=('Verdana', 10, 'bold'), pady=2)
        self.val.pack()
        self.pack(pady=15)

    def init_algo(self):
        self.algo_value = [-1] * 9
        self.index = 1

    def draw_puzzle(self):
        for i in range(3):
            for j in range(3):
                self.b[i].append(self.button())
                self.b[i][j].config(command=lambda row=i, col=j: self.fill(row, col))
                self.b[i][j].grid(row=i, column=j)

    def set_state(self, move: list, speed: float):
        curr_row, curr_col = self.get_corr(self.algo_value.index(-1))
        new_row, new_col = self.get_corr(move.index(-1))
        b1, b2 = self.b[curr_row][curr_col], self.b[new_row][new_col]
        prop1, prop2 = self.get_prop(b1), self.get_prop(b2)
        self.set_prop(prop2, b1)
        self.set_prop(prop1, b2)
        self.algo_value = move[:]
        self.update()
        sleep(speed)

    def get_prop(self, b):
        return b.cget("text"), b.cget("bg")

    def set_prop(self, prop, b):
        b.config(text=prop[0], bg=prop[1])

    def mark_tile(self):
        index = self.algo_value.index(-1)
        row, col = self.get_corr(index)
        self.b[row][col].config(bg=self.config["tile_color"], state=tk.DISABLED)

    def button(self):
        return tk.Button(self, bd=5, width=2, font=('arial', 30, 'bold'))

    def fill(self, i, j):
        self.b[i][j].config(text=self.index, state=tk.DISABLED, bg="black", fg="white")
        self.algo_value[i * 3 + j] = self.index
        self.index += 1
        if self.index == 9:
            self.mark_tile()
            self.val.config(text=str(self.algo_value))

    def get_corr(self, index):
        return index // 3, index % 3

    def is_set(self):
        return self.index == 9

    def reset(self):
        self.init_algo()
        self.val.config(text="")
        for i in range(3):
            for j in range(3):
                self.b[i][j].config(text="", bg=self.cget('bg'), fg="black", state=tk.NORMAL)
