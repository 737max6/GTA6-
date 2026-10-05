import tkinter as tk
import random
import time

class MinesweeperGame:
    def __init__(self, root, on_timeout):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("小彩蛋-扫雷")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.window.configure(bg="black")

        self.GRID = 9
        self.MINES = 10
        self.CELL = 40
        self.TIMEOUT = 120

        self.mines = set()
        self.revealed = set()
        self.flags = set()
        self.game_over = False
        self.first_click = True
        self.on_timeout = on_timeout
        self.start_time = time.time()
        self.timeout_called = False

        self.info_label = tk.Label(self.window, text="", font=("Consolas", 12), bg="black", fg="#00FFD9")
        self.info_label.pack(pady=5)

        self.canvas = tk.Canvas(self.window, width=self.GRID * self.CELL, height=self.GRID * self.CELL,
                                bg="#A9A9A9", highlightthickness=0)
        self.canvas.pack(padx=10, pady=5)

        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        self.draw()
        self.check_timeout()

    def _trigger_timeout(self):
        if self.timeout_called:
            return
        self.timeout_called = True
        try:
            self.window.destroy()
        except Exception:
            pass
        self.on_timeout()

    def _on_close(self):
        self._trigger_timeout()

    def generate_mines(self, safe_r, safe_c):
        safe_zone = set()
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                safe_zone.add((safe_r + dr, safe_c + dc))
        available = [(r, c) for r in range(self.GRID) for c in range(self.GRID)
                     if (r, c) not in safe_zone]
        self.mines = set(random.sample(available, self.MINES))

    def count_adjacent(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if (r + dr, c + dc) in self.mines:
                    count += 1
        return count

    def reveal(self, r, c):
        if not (0 <= r < self.GRID and 0 <= c < self.GRID):
            return
        if (r, c) in self.revealed or (r, c) in self.flags:
            return
        self.revealed.add((r, c))
        if (r, c) in self.mines:
            self.game_over = True
            self.draw()
            self.window.after(3000, self._trigger_timeout)
            return
        count = self.count_adjacent(r, c)
        if count == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    self.reveal(r + dr, c + dc)

    def on_left_click(self, event):
        if self.game_over or self.timeout_called:
            return
        c = event.x // self.CELL
        r = event.y // self.CELL
        if not (0 <= r < self.GRID and 0 <= c < self.GRID):
            return
        if self.first_click:
            self.generate_mines(r, c)
            self.first_click = False
        self.reveal(r, c)
        self.draw()
        self.check_win()

    def on_right_click(self, event):
        if self.game_over or self.timeout_called:
            return
        c = event.x // self.CELL
        r = event.y // self.CELL
        if not (0 <= r < self.GRID and 0 <= c < self.GRID):
            return
        if (r, c) in self.revealed:
            return
        if (r, c) in self.flags:
            self.flags.remove((r, c))
        else:
            self.flags.add((r, c))
        self.draw()

    def check_win(self):
        if len(self.revealed) == self.GRID * self.GRID - self.MINES:
            self.game_over = True
            self.draw()
            self.window.after(3000, self._trigger_timeout)

    def draw(self):
        self.canvas.delete("all")
        colors = ["", "#0000FF", "#008000", "#FF0000", "#000080", "#800000", "#008080", "#000000", "#808080"]

        for r in range(self.GRID):
            for c in range(self.GRID):
                x1 = c * self.CELL
                y1 = r * self.CELL
                x2 = x1 + self.CELL
                y2 = y1 + self.CELL

                if (r, c) in self.revealed:
                    if (r, c) in self.mines:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FF4444", outline="black")
                        self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="X", fill="white", font=("Arial", 16, "bold"))
                    else:
                        count = self.count_adjacent(r, c)
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#D3D3D3", outline="black")
                        if count > 0:
                            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(count),
                                                    fill=colors[count], font=("Arial", 14, "bold"))
                elif (r, c) in self.flags:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FFD700", outline="black")
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="F", fill="red", font=("Arial", 16, "bold"))
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#A9A9A9", outline="black")

        if self.game_over:
            for (r, c) in self.mines:
                if (r, c) not in self.revealed:
                    x1 = c * self.CELL
                    y1 = r * self.CELL
                    x2 = x1 + self.CELL
                    y2 = y1 + self.CELL
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FF8888", outline="black")
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="X", fill="white", font=("Arial", 16, "bold"))

        remaining = max(0, self.TIMEOUT - int(time.time() - self.start_time))
        self.info_label.config(text=f"剩余时间: {remaining}s    剩余雷数: {self.MINES - len(self.flags)}")

    def check_timeout(self):
        if self.timeout_called:
            return
        if time.time() - self.start_time >= self.TIMEOUT:
            self._trigger_timeout()
            return
        self.draw()
        self.window.after(1000, self.check_timeout)