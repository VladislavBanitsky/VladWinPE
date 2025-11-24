import tkinter as tk
from tkinter import ttk
import json
import os
from PIL import Image, ImageTk


class WinPETaskbar:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.load_config()
        self.create_taskbar()
        self.setup_taskbar_position()

    def setup_window(self):
        # Сделать окно поверх всех других окон
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)  # Убрать заголовок окна
        self.root.attributes('-alpha', 1)  # Полупрозрачность
        self.root.configure(bg='#2b2b2b')

    def load_config(self):
        config_file = 'taskbar_config.json'
        if not os.path.exists(config_file):
            # Создать конфиг по умолчанию если файл не существует
            self.create_default_config(config_file)

        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    def create_default_config(self, config_file):
        default_config = {
            "taskbar": {
                "position": "bottom",
                "height": 60,
                "width": 290,
                "corner_radius": 15,
                "background_color": "#1F85DE",
                "opacity": 0.9
            },
            "apps": [
                {
                    "name": "Проводник",
                    "executable": "X:/Windows/_internal/explorer++/explorer++.exe",
                    "icon_path": "X:/Windows/_internal/icons/explorer.svg.png",
                    "icon_index": 3,
                    "working_directory": ""
                },
                {
                    "name": "Командная строка",
                    "executable": "cmd.exe",
                    "icon_path": "X:/Windows/_internal/icons/cmd.svg.png",
                    "icon_index": 0,
                    "working_directory": ""
                },
                {
                    "name": "Блокнот",
                    "executable": "notepad.exe",
                    "icon_path": "X:/Windows/_internal/icons/notepad.png",
                    "icon_index": 0,
                    "working_directory": ""
                },
                {
                    "name": "CrystalDiskInfo",
                    "executable": "X:/Windows/_internal/cdi/DiskInfo64.exe",
                    "icon_path": "X:/Windows/_internal/icons/cdi.png",
                    "icon_index": 0,
                    "working_directory": ""
                },
                {
                    "name": "CrystalDiskMark",
                    "executable": "X:/Windows/_internal/cdm/DiskMark64.exe",
                    "icon_path": "X:/Windows/_internal/icons/cdm.png",
                    "icon_index": 0,
                    "working_directory": ""
                },
                {
                    "name": "AIDA64 Extreme",
                    "executable": "X:/Windows/_internal/aida64/aida64.exe",
                    "icon_path": "X:/Windows/_internal/icons/aida64.png",
                    "icon_index": 0,
                    "working_directory": ""
                }
            ]
        }

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)

    def create_taskbar(self):
        # Получить настройки панели задач
        taskbar_config = self.config.get('taskbar', {})
        height = taskbar_config.get('height', 60)
        width = taskbar_config.get('width', 800)
        bg_color = taskbar_config.get('background_color', '#2b2b2b')

        # Установить размер окна
        self.root.geometry(f'{width}x{height}')

        # Создать основной фрейм с закруглёнными углами
        self.main_frame = tk.Frame(self.root, bg=bg_color, relief='flat')
        self.main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Создать стиль для кнопок
        self.setup_styles()

        # Добавить приложения на панель задач
        self.create_app_buttons()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Стиль для кнопок приложений
        style.configure('App.TButton',
                        background='#3c3c3c',
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        padding=(10, 5))

        style.map('App.TButton',
                  background=[('active', '#4a4a4a'),
                              ('pressed', '#5a5a5a')])

    def create_app_buttons(self):
        apps = self.config.get('apps', [])

        for app in apps:
            self.create_app_button(app)

    def create_app_button(self, app_config):
        name = app_config.get('name', 'Unknown')
        executable = app_config.get('executable', '')
        icon_path = app_config.get('icon_path', '')
        icon_index = app_config.get('icon_index', 0)
        working_dir = app_config.get('working_directory', '')

        # Создать фрейм для кнопки
        button_frame = tk.Frame(self.main_frame, bg=self.main_frame['bg'])
        button_frame.pack(side='left', padx=5, pady=5)

        try:
            # Загрузить иконку
            icon = self.load_icon(icon_path, icon_index)
            if icon:
                icon_label = tk.Label(button_frame, image=icon, bg=button_frame['bg'])
                icon_label.image = icon  # Сохранить ссылку
                icon_label.pack()

                # Привязать события клика к иконке
                icon_label.bind('<Button-1>', lambda e, exe=executable, wd=working_dir: self.launch_app(exe, wd))
        except Exception as e:
            print(f"Ошибка загрузки иконки для {name}: {e}")

        # Создать кнопку
        button = ttk.Button(button_frame,
                            width=1,
                            text=name,
                            style='App.TButton',
                            command=lambda exe=executable, wd=working_dir: self.launch_app(exe, wd))
        button.pack(fill='x')

    def load_icon(self, icon_path, icon_index=0):
        """Загрузить иконку из файла или ресурсов"""
        if not os.path.exists(icon_path):
            return None
        try:
            # Для обычных файлов изображений
            image = Image.open(icon_path)
            image = image.resize((32, 32), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)

        except Exception as e:
            print(f"Ошибка загрузки иконки {icon_path}: {e}")

        return None

    def launch_app(self, executable, working_directory=""):
        """Запустить приложение"""
        try:
            if working_directory and os.path.exists(working_directory):
                os.chdir(working_directory)

            # Использовать os.system для простоты в WinPE
            os.system(f'start "" "{executable}"')

        except Exception as e:
            print(f"Ошибка запуска приложения {executable}: {e}")

    def setup_taskbar_position(self):
        """Установить позицию панели задач"""
        taskbar_config = self.config.get('taskbar', {})
        position = taskbar_config.get('position', 'bottom')
        width = taskbar_config.get('width', 800)
        height = taskbar_config.get('height', 60)

        # Получить размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Вычислить позицию
        if position == 'bottom':
            x = (screen_width - width) // 2
            y = screen_height - height - 10
        elif position == 'top':
            x = (screen_width - width) // 2
            y = 10
        elif position == 'left':
            x = 10
            y = (screen_height - height) // 2
        elif position == 'right':
            x = screen_width - width - 10
            y = (screen_height - height) // 2
        else:  # center
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2

        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()


if __name__ == "__main__":
    taskbar = WinPETaskbar()
    taskbar.run()