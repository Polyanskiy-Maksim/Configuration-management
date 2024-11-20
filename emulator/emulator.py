import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import tarfile
import argparse

class ShellEmulator:
    def __init__(self, master, virtual_fs_path):
        self.master = master
        self.master.title("Shell Emulator")
        self.current_path = "/"
        self.history = []

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.username = os.getlogin()
        self.virtual_fs_path = virtual_fs_path

        self.label = tk.Label(master, text=f"{self.username}")
        self.label.pack(padx=10, pady=5)

        self.entry = tk.Entry(master)
        self.entry.pack(padx=10, pady=10, fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)

        self.extract_virtual_fs()

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Запуск эмулятора командной строки vshell.')
        parser.add_argument('--script', type=str, help='Имя файла со скриптом команд.')
        parser.add_argument('virtual_fs', type=str, help='Путь к образу файловой системы (tar или zip).')

        args = parser.parse_args()

        if not os.path.exists(args.virtual_fs):
            parser.error(f"Файл виртуальной файловой системы '{args.virtual_fs}' не найден.")

        return args

    def extract_virtual_fs(self):
        if not os.path.exists(self.virtual_fs_path):
            messagebox.showerror("Ошибка", "Файл виртуальной файловой системы не найден.")
            return

        with tarfile.open(self.virtual_fs_path) as tar:
            tar.extractall(path="virtual_fs", filter=tarfile.data_filter)

    def execute_command(self, event):
        command = self.entry.get().strip()
        if not command:
            self.entry.delete(0, tk.END)
            return

        self.history.append(command)

        # Выводим команду в текстовое поле для отображения
        self.text_area.insert(tk.END, f"$ {command}\n")

        command_dict = {
            "ls": self.list_files,
            "cd": lambda: self.change_directory(command[3:].strip()),
            "pwd": self.print_working_directory,
            "cat": lambda: self.cat_file(command[4:].strip()),
            "exit": self.master.quit,
            "history": self.show_history,
            "touch": lambda: self.touch_file(command[6:].strip()),
            "find": lambda: self.find(command[5:].strip()),
            "uname": self.uname,
            "mkdir": lambda: self.mkdir(command[6:].strip())
        }

        cmd_func = command_dict.get(command.split()[0], None)

        if cmd_func:
            cmd_func()
        else:
            self.text_area.insert(tk.END, f"{self.username}: команда не найдена\n")

        self.entry.delete(0, tk.END)

    def list_files(self):
        try:
            # Получаем список файлов из текущей директории
            files = os.listdir(f"virtual_fs{self.current_path}")
            output = "\n".join(files) if files else "Пустая директория\n"
            self.text_area.insert(tk.END, f"{output}\n")
        except FileNotFoundError:
            self.text_area.insert(tk.END, "Директория не найдена\n")

    def change_directory(self, path):
        if not path:
            # Если команда "cd" без аргументов, возвращаем в корень
            self.current_path = "/"
            return

        if path == "..":
            # Переход в родительскую директорию
            if self.current_path != "/":
                parts = self.current_path.strip("/").split("/")
                parts.pop()  # Убираем последний сегмент пути
                self.current_path = "/" + "/".join(parts) if parts else "/"
            return

        new_path = os.path.join(f"virtual_fs{self.current_path}", path)
        if os.path.isdir(new_path):
            # Если директория существует, переходим в нее
            self.current_path = new_path.replace("virtual_fs", "")
        else:
            self.text_area.insert(tk.END, "Директория не найдена\n")

    def print_working_directory(self):
        current_dir = f"{self.username}:{self.current_path}\n"
        self.text_area.insert(tk.END, current_dir)

    def cat_file(self, filename):
        try:
            with open(os.path.join(f"virtual_fs{self.current_path}", filename), 'r') as file:
                content = file.read()
                self.text_area.insert(tk.END, f"{content}\n")
        except FileNotFoundError:
            self.text_area.insert(tk.END, "Файл не найден\n")

    def touch_file(self, filename):
        try:
            file_path = os.path.join(f"virtual_fs{self.current_path}", filename.strip())
            with open(file_path, 'a'):
                pass
            self.text_area.insert(tk.END, f"Файл '{filename}' создан.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"Ошибка при создании файла '{filename}': {str(e)}\n")

    def show_history(self):
        history_output = "\n".join(self.history) or "История пуста\n"
        self.text_area.insert(tk.END, f"История команд:\n{history_output}\n")

    def find(self, name):
        results = []

        def recursive_search(directory):
            try:
                for entry in os.listdir(directory):
                    entry_path = os.path.join(directory, entry)
                    if name in entry:
                        results.append(entry_path.replace("virtual_fs", ""))
                    if os.path.isdir(entry_path):
                        recursive_search(entry_path)
            except Exception as e:
                self.text_area.insert(tk.END, f"Ошибка при поиске: {e}\n")

        current_dir = f"virtual_fs{self.current_path}"
        recursive_search(current_dir)
        if results:
            self.text_area.insert(tk.END, "\n".join(results) + "\n")
        else:
            self.text_area.insert(tk.END, "Ничего не найдено\n")

    def uname(self):
        import platform
        os_name = platform.system()
        self.text_area.insert(tk.END, f"Операционная система: {os_name}\n")

    def mkdir(self, dirname):
        if not dirname.strip():
            self.text_area.insert(tk.END, "Укажите имя директории для создания\n")
            return
        dir_path = os.path.join(f"virtual_fs{self.current_path}", dirname.strip())
        try:
            os.makedirs(dir_path, exist_ok=True)
            self.text_area.insert(tk.END, f"Директория '{dirname.strip()}' создана.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"Ошибка при создании директории: {e}\n")

if __name__ == "__main__":
    args = ShellEmulator.parse_arguments()
    root = tk.Tk()
    app = ShellEmulator(root, args.virtual_fs)

    if args.script:
        app.load_script(args.script)

    root.mainloop()
