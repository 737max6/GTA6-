import tkinter as tk
import random
import time

class SnakeGame:
    def __init__(self, root, on_timeout):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("小彩蛋-贪吃蛇")
        self.window.geometry("420x440")
        self.window.resizable(False, False)
        self.window.configure(bg="black")

        self.canvas = tk.Canvas(self.window, width=400, height=400, bg="black", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.snake = [(200, 200), (180, 200), (160, 200)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.on_timeout = on_timeout
        self.start_time = time.time()
        self.timeout_called = False

        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

        self.window.bind("<Key>", self.on_key)
        self.canvas.bind("<Key>", self.on_key)
        self.canvas.focus_set()
        self.window.focus_force()
        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.after(100, lambda: self.window.attributes('-topmost', False))

        self.draw()
        self.game_loop()
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

    def spawn_food(self):
        while True:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            if (x, y) not in self.snake:
                return (x, y)

    def on_key(self, event):
        key = event.keysym
        if key == "Up" and self.direction != "Down":
            self.next_direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.next_direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.next_direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.next_direction = "Right"

    def draw(self):
        self.canvas.delete("all")
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="#00FF00", outline="")
        fx, fy = self.food
        self.canvas.create_oval(fx, fy, fx + 20, fy + 20, fill="#FF0000", outline="")
        self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white", anchor="w", font=("Consolas", 12))
        remaining = max(0, 60 - int(time.time() - self.start_time))
        self.canvas.create_text(350, 20, text=f"Time: {remaining}s", fill="yellow", anchor="e", font=("Consolas", 12))

    def game_loop(self):
        if self.game_over or self.timeout_called:
            return
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= 20
        elif self.direction == "Down":
            head_y += 20
        elif self.direction == "Left":
            head_x -= 20
        elif self.direction == "Right":
            head_x += 20

        new_head = (head_x, head_y)

        if (head_x < 0 or head_x >= 400 or head_y < 0 or head_y >= 400 or new_head in self.snake):
            self.game_over = True
            self.canvas.create_text(200, 200, text="GAME OVER", fill="red", font=("Arial", 24, "bold"))
            self.window.after(3000, self._trigger_timeout)
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        self.draw()
        self.window.after(150, self.game_loop)

    def check_timeout(self):
        if self.timeout_called:
            return
        if time.time() - self.start_time >= 60:
            self._trigger_timeout()
            return
        self.window.after(1000, self.check_timeout)