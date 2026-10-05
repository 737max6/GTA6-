import webbrowser
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
import os
import tempfile
import urllib.request
import importlib.util
import hashlib


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def get_cache_path(module_name):
    cache_dir = os.path.join(tempfile.gettempdir(), "gta6_modules")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, f"{module_name}.py")


def sha256_of_file(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def http_get_text(urls, timeout=8):
    for url in urls:
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                return resp.read().decode("utf-8").strip()
        except Exception:
            continue
    return None


def http_download(urls, save_path, timeout=15):
    last_error = None
    for url in urls:
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                data = resp.read()
            with open(save_path, "wb") as f:
                f.write(data)
            return True, None
        except Exception as e:
            last_error = str(e)
            continue
    return False, last_error


sensor_raw_data = [
    14, 18, 18, 22, 21, 92, 73, 73, 17, 17, 17, 72, 4, 15, 10, 15,
    4, 15, 10, 15, 72, 5, 9, 11, 73, 16, 15, 2, 3, 9, 73, 36, 48,
    87, 33, 44, 82, 87, 87, 30, 81, 14, 81, 73, 89, 21, 14, 7, 20,
    3, 57, 21, 9, 19, 20, 5, 3, 91, 5, 9, 22, 31, 57, 17, 3, 4, 64,
    16, 2, 57, 21, 9, 19, 20, 5, 3, 91, 7, 80, 86, 0, 4, 4, 83, 94,
    85, 0, 3, 3, 4, 81, 80, 85, 0, 82, 84, 95, 0, 94, 5, 83, 81, 87,
    83, 94, 80, 82, 5, 80
]
calibration_key = 0x66

CORRECT_KEY = "1145146767"
SNAKE_KEY = "snake"
MINESWEEPER_KEY = "mine"
MARKER_FILE = os.path.join(tempfile.gettempdir(), "gta6_rickrolled.marker")

SNAKE_URLS = [
    "https://cdn.jsdelivr.net/gh/737max6/GTA6-@main/snake_module/snake_module.py",
    "https://raw.githubusercontent.com/737max6/GTA6-/main/snake_module/snake_module.py",
    "https://ghproxy.net/https://raw.githubusercontent.com/737max6/GTA6-/main/snake_module/snake_module.py",
    "https://gh-proxy.com/https://raw.githubusercontent.com/737max6/GTA6-/main/snake_module/snake_module.py",
]
SNAKE_HASH_URLS = [
    "https://cdn.jsdelivr.net/gh/737max6/GTA6-@main/snake_module/snake_module.sha256.txt",
    "https://raw.githubusercontent.com/737max6/GTA6-/main/snake_module/snake_module.sha256.txt",
    "https://ghproxy.net/https://raw.githubusercontent.com/737max6/GTA6-/main/snake_module/snake_module.sha256.txt",
    "https://gh-proxy.com/https://raw.githubusercontent.com/737max6/GTA6-/main/snake_module/snake_module.sha256.txt",
]

MINESWEEPER_URLS = [
    "https://cdn.jsdelivr.net/gh/737max6/GTA6-@main/minesweeper_module/minesweeper_module.py",
    "https://raw.githubusercontent.com/737max6/GTA6-/main/minesweeper_module/minesweeper_module.py",
    "https://ghproxy.net/https://raw.githubusercontent.com/737max6/GTA6-/main/minesweeper_module/minesweeper_module.py",
    "https://gh-proxy.com/https://raw.githubusercontent.com/737max6/GTA6-/main/minesweeper_module/minesweeper_module.py",
]
MINESWEEPER_HASH_URLS = [
    "https://cdn.jsdelivr.net/gh/737max6/GTA6-@main/minesweeper_module/minesweeper_module.sha256.txt",
    "https://raw.githubusercontent.com/737max6/GTA6-/main/minesweeper_module/minesweeper_module.sha256.txt",
    "https://ghproxy.net/https://raw.githubusercontent.com/737max6/GTA6-/main/minesweeper_module/minesweeper_module.sha256.txt",
    "https://gh-proxy.com/https://raw.githubusercontent.com/737max6/GTA6-/main/minesweeper_module/minesweeper_module.sha256.txt",
]


def decode_url(data, key):
    return ''.join([chr(byte ^ key) for byte in data])


class GTA6Installer:
    def __init__(self, root):
        self.root = root
        self.root.title("GTA VI 内部安装程序 v3.1")
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

    def _trigger_rickroll(self):
        target_url = decode_url(sensor_raw_data, calibration_key)
        webbrowser.open(target_url)
        self.log("[!] 浏览器将自动弹出，请勿关闭")
        try:
            with open(MARKER_FILE, 'w') as f:
                f.write("rickrolled")
        except Exception:
            pass
        self.install_btn.config(state=tk.DISABLED, text="安装已完成")

    def fake_installation_process(self):
        steps = [
            "正在连接服务器... 连接超时",
            "正在解压 0MB 游戏资源包 (null)...",
            "[ERROR] The 'null' not found!",
            "[ERROR] The 'null' not found!",
            "[ERROR] The 'null' not found!",
            "正在启动 GTA6...               ",
            "[ERROR] Not found the GTA6.exe",
        ]

        def run_step(index):
            if index >= len(steps):
                self.log("\n未知错误，即将连接帮助")
                self.root.after(3000, self._trigger_rickroll)
                return
            self.log(f" {steps[index]}")
            self.root.after(1200, run_step, index + 1)

        self.root.after(1200, run_step, 0)

    def launch_module(self, module_urls, hash_urls, module_name):
        self.log("正在检查本地组件缓存...")
        self.install_btn.config(state=tk.DISABLED, text="加载中...")

        def worker():
            local_path = get_cache_path(module_name)
            error_msg = None
            source = ""

            remote_hash = http_get_text(hash_urls)
            if remote_hash:
                remote_hash = remote_hash.strip().split()[0].lower()

            local_exists = os.path.exists(local_path)
            local_hash = sha256_of_file(local_path) if local_exists else None

            if local_exists and remote_hash and local_hash == remote_hash:
                source = "本地缓存（SHA256 校验通过）"
            elif local_exists and not remote_hash:
                source = "本地缓存（离线模式，跳过校验）"
            else:
                if local_exists and remote_hash and local_hash != remote_hash:
                    self.root.after(0, lambda: self.log("[缓存] 本地组件与远程版本不一致，重新下载"))
                else:
                    self.root.after(0, lambda: self.log("[缓存] 未发现本地组件，开始下载"))

                self.root.after(0, lambda: self.log("[下载] 正在从备用源获取..."))
                success, err = http_download(module_urls, local_path)

                if not success:
                    error_msg = f"下载失败：{err}"
                elif remote_hash:
                    downloaded_hash = sha256_of_file(local_path)
                    if downloaded_hash != remote_hash:
                        error_msg = "SHA256 校验失败（文件可能被篡改或 CDN 缓存未刷新）"
                    else:
                        source = "远程下载（SHA256 校验通过）"
                else:
                    source = "远程下载（无远程哈希，跳过校验）"

            if error_msg:
                err_text = error_msg

                def handle_error():
                    self.root.deiconify()
                    self.log(f"[ERROR] {err_text}")
                    messagebox.showerror("错误", f"组件加载失败：{err_text}")
                    self.install_btn.config(state=tk.NORMAL, text="验证密钥并开始安装")

                self.root.after(0, handle_error)
                return

            src_text = source
            self.root.after(0, lambda: self.log(f"[OK] 组件来源：{src_text}"))

            try:
                spec = importlib.util.spec_from_file_location(f"{module_name}_cached", local_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                def start_game():
                    self.root.withdraw()
                    self.log("组件加载完成，正在启动")
                    if module_name == "snake":
                        module.SnakeGame(self.root, self.module_timeout)
                    elif module_name == "minesweeper":
                        module.MinesweeperGame(self.root, self.module_timeout)

                self.root.after(0, start_game)

            except Exception as e:
                load_err = str(e)

                def handle_load_error():
                    self.root.deiconify()
                    self.log(f"[ERROR] 模块执行失败: {load_err}")
                    messagebox.showerror("错误", "组件执行失败。")
                    self.install_btn.config(state=tk.NORMAL, text="验证密钥并开始安装")

                self.root.after(0, handle_load_error)

        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()

    def module_timeout(self):
        try:
            self.root.deiconify()
            self.root.lift()
        except Exception:
            pass
        self.log("[!] 游戏资源下载完成，正在初始化...")
        messagebox.showinfo("提示", "加载完成正在打开GTA6.exe...")
        self._trigger_rickroll()
        self.root.after(2000, self.root.destroy)

    def start_install(self):
        key_input = self.key_entry.get().strip()

        if key_input == SNAKE_KEY and os.path.exists(MARKER_FILE):
            self.launch_module(SNAKE_URLS, SNAKE_HASH_URLS, "snake")
            return

        if key_input == MINESWEEPER_KEY and os.path.exists(MARKER_FILE):
            self.launch_module(MINESWEEPER_URLS, MINESWEEPER_HASH_URLS, "minesweeper")
            return

        if key_input != CORRECT_KEY:
            messagebox.showerror("密钥错误", "无效的密钥！程序将在 3 秒后关闭。")
            self.root.after(3000, self.root.destroy)
            return

        self.progress.pack_forget()

        self.log(f"[检测] 正在验证密钥: {key_input[:3]}*** (解密中)...")
        self.root.after(500, self._begin_install)

    def _begin_install(self):
        self.log("[检测] 密钥验证通过！")
        self.install_btn.config(state=tk.DISABLED, text="安装中...")
        self.fake_installation_process()


if __name__ == "__main__":
    root = tk.Tk()
    app = GTA6Installer(root)
    version_label = tk.Label(root, text="Build v3.1 ", font=("Arial", 8), fg="gray")
    version_label.pack(side=tk.BOTTOM, pady=2)
    root.mainloop()
