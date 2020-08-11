import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


def build_gui(dim):
    root = tk.Tk()
    App(root, dim).pack(side="top", fill="both", expand=True)
    root.mainloop()


class App(tk.Frame):
    def __init__(self, parent, dim, **kw):
        super().__init__(parent, **kw)
        parent.minsize(dim[0], dim[1])
        parent.title("8 puzzle problem")
        self.label = tk.Label(self, text="Let's solve the eight puzzle Problem", font=('Verdana', 15, 'bold'))
        self.label.pack(side=tk.TOP)
        self.puzzle_src = Puzzle(self, {"tile_color":"red", "text":"Source Configuration"})
        self.puzzle_dest = Puzzle(self, {"tile_color":"red", "text":"Destination Configuration"})
        self.draw_separator()

    def draw_separator(self):
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(after=self.label, fill=tk.X)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(after=self.puzzle_src, fill=tk.X)


class Puzzle(tk.Frame):
    def __init__(self, parent, config, **kw):
        super().__init__(parent, **kw)
        self.b = [[], [], []]
        self.algo_value = [-1] * 9
        self.index = 1
        self.config = config
        self.draw_puzzle()
        tk.Label(parent, text=config["text"], font=('Verdana', 10, 'bold'), pady = 10).pack()
        self.pack(pady=40)

    def draw_puzzle(self):
        for i in range(3):
            for j in range(3):
                self.b[i].append(self.button())
                self.b[i][j].config(command=lambda row=i, col=j: self.fill(row, col))
                self.b[i][j].grid(row=i, column=j)

    def set_state(self, move:list):
        curr_row, curr_col = self.get_corr(self.algo_value.index(-1))
        new_row, new_col = self.get_corr(move.index(-1))
        self.b[curr_row][curr_col], self.b[new_row][new_col] = self.b[new_row][new_col], self.b[curr_row][curr_col]
        self.algo_value = move[:]

    def mark_tile(self):
        index = self.algo_value.index(-1)
        row, col = self.get_corr(index)
        self.b[row][col].config(bg=self.config["tile_color"], state=tk.DISABLED)

    def button(self):
        return tk.Button(self, bd=5, width=2, font=('arial', 30, 'bold'))

    def fill(self, i, j):
        self.b[i][j].config(text=self.index, state = tk.DISABLED, bg="black", fg="white")
        self.algo_value[i * 3 + j] = self.index
        self.index += 1
        if self.index == 9:
            self.mark_tile()
            messagebox.showinfo("Value input to algorithm set to : ",str(self.algo_value))

    def get_corr(self, index):
        return index // 3, index % 3

    def is_set(self):
        return self.index == 9
