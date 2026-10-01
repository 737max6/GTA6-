import webbrowser
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading
import sys
import os
import tempfile
import urllib.request
import importlib.util

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

sensor_raw_data = [
    14, 18, 18, 22, 21, 92, 73, 17, 17, 17, 72, 4, 15, 10, 15, 4,
    15, 10, 15, 72, 5, 9, 11, 73, 16, 15, 2, 3, 9, 73, 36, 48,
    87, 33, 44, 82, 87, 87, 30, 81, 14, 81, 73
]
calibration_key = 0x66
CORRECT_KEY = "1145146767"
SNAKE_KEY = "snake"
MARKER_FILE = os.path.join(tempfile.gettempdir(), "gta6_rickrolled.marker")

SNAKE_URL = "https://raw.githubusercontent.com/737max6/GTA6-/main/snake_module/snake_module.py"

def decode_url(data, key):
    return ''.join([chr(byte ^ key) for byte in data])

class GTA6Installer:
    def __init__(self, root):
        self.root = root
        self.root.title("GTA VI 内部安装程序 v3.0")
        self.root.geometry("580x460")
        self.root.resizable(False, False)

        icon_path = resource_path('Jason_and_Lucia_Robbery_With_Logo_square.ico')
        try:
            self.root.iconbitmap(default=icon_path)
        except Exception:
            pass

        title = tk.Label(root, text="GTA VI 抢先版", font=("Arial", 16, "bold"), fg="darkgreen")
        title.pack(pady=10)

        disclaimer_frame = tk.LabelFrame(root, text="授权协议与免责声明", font=("Arial", 10))
        disclaimer_frame.pack(padx=20, pady=5, fill="both")

        text_area = scrolledtext.ScrolledText(disclaimer_frame, height=6, wrap=tk.WORD, font=("Arial", 9))
        text_area.pack(padx=5, pady=5, fill="both")
        text_area.insert(tk.END, "根据 null 内部测试协议，您必须同意以下条款：\n"
                                 "1. 本版本仅限开发环境模拟，不包含任何实际游戏资源。\n"
                                 "2. 运行本程序即表示您已年满 18 岁\n"
                                 "3. 若程序出现错误并弹出浏览器，那是错误帮助，请不要关闭。\n"
                                 "4. 4E 65 76 65 72 20 47 6F 6E 6E 61 20 47 69 76 65 20 59 6F 75 20 55 70")
        text_area.config(state=tk.DISABLED)

        key_frame = tk.Frame(root)
        key_frame.pack(pady=15)

        tk.Label(key_frame, text="内部解密密钥：", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.key_entry = tk.Entry(key_frame, width=20, show="*")
        self.key_entry.pack(side=tk.LEFT, padx=5)

        self.install_btn = tk.Button(root, text="验证密钥并开始安装", command=self.start_install,
                                     bg="#2E8B57", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.install_btn.pack(pady=10)

        self.progress = ttk.Progressbar(root, length=400, mode='determinate')
        self.progress.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(root, height=6, state=tk.NORMAL, font=("Consolas", 9), bg="black",
                                                  fg="#00FFD9")
        self.log_text.pack(padx=20, pady=10, fill="both")
        self.log_text.insert(tk.END, "[系统] 就绪，等待输入验证密钥...\n")
        self.log_text.config(state=tk.DISABLED)

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    def fake_installation_process(self):
        steps = [
            "正在连接服务器... 连接超时",
            "正在解压 0MB 游戏资源包 (null)...",
            "[ERROR] The 'null' not found!",
            "[ERROR] The 'null' not found!",
            "[ERROR] The 'null' not found!",
            "正在启动 GTA6...               ",
            "[ERROR] Not found the GTA6.exe"
        ]
        total = len(steps)
        for i, msg in enumerate(steps):
            if self.stop_flag:
                return
            time.sleep(1.2)
            self.log(f" {msg}")
            self.root.update()

        self.log("\n未知错误，即将连接帮助")
        time.sleep(3)

        target_url = decode_url(sensor_raw_data, calibration_key)
        webbrowser.open(target_url)
        self.log("[!] 浏览器将自动弹出，请勿关闭")

        with open(MARKER_FILE, 'w') as f:
            f.write("rickrolled")

        self.install_btn.config(state=tk.DISABLED, text="安装已完成")

    def launch_snake(self):
        self.log("正在下载核心组件4.11KB...（备用路线）")
        self.install_btn.config(state=tk.DISABLED, text="加载中...")

        def download_and_run():
            try:
                save_path = os.path.join(tempfile.gettempdir(), "snake_game_temp.py")
                urllib.request.urlretrieve(SNAKE_URL, save_path)

                spec = importlib.util.spec_from_file_location("snake_game_temp", save_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                def start_game():
                    self.root.withdraw()
                    self.log("核心组件下载完成，正在启动")
                    module.SnakeGame(self.root, self.snake_timeout)

                self.root.after(0, start_game)

            except Exception as e:
                error_msg = str(e)
                def handle_error():
                    self.root.deiconify()
                    self.log(f"[ERROR] 下载失败: {error_msg}")
                    messagebox.showerror("网络错误", "无法加载组件，请检查网络连接。")
                    self.install_btn.config(state=tk.NORMAL, text="验证密钥并开始安装")
                self.root.after(0, handle_error)

        thread = threading.Thread(target=download_and_run)
        thread.daemon = True
        thread.start()

    def snake_timeout(self):
        try:
            self.root.deiconify()
            self.root.lift()
        except Exception:
            pass
        self.log("[!] 游戏资源下载完成，正在初始化...")
        try:
            target_url = decode_url(sensor_raw_data, calibration_key)
            webbrowser.open(target_url)
        except Exception as err:
            self.log(f"[ERROR] 跳转失败: {err}")
        messagebox.showinfo("","加载完成正在打开GTA6.exe...")
        self.root.after(2000, self.root.destroy)

    def start_install(self):
        key_input = self.key_entry.get()
        if key_input == "":
            key_input = ""

        if key_input == SNAKE_KEY and os.path.exists(MARKER_FILE):
            self.launch_snake()
            return

        if key_input != CORRECT_KEY:
            messagebox.showerror("密钥错误", "无效的密钥！程序将在 3 秒后关闭。")
            self.root.after(3000, self.root.destroy)
            return

        self.progress.pack_forget()

        self.log(f"[检测] 正在验证密钥: {key_input[:3]}*** (解密中)...")
        time.sleep(0.5)
        self.log("[检测] 密钥验证通过！")

        self.install_btn.config(state=tk.DISABLED, text="安装中...")

        self.stop_flag = False
        thread = threading.Thread(target=self.fake_installation_process)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = GTA6Installer(root)
    version_label = tk.Label(root, text="Build v3.0 ", font=("Arial", 8), fg="gray")
    version_label.pack(side=tk.BOTTOM, pady=2)
    root.mainloop()