# winpe_utility_tkinter.py
import os
import tkinter as tk
from tkinter import messagebox


class WinPEUtility:
    def __init__(self, root):
        self.root = root
        self.root.title("Выключение VladWinPE")
        self.root.geometry("300x70")
        self.root.resizable(False, False)

        # Центрирование окна
        self.center_window()

        self.create_widgets()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Основной frame
        main_frame = tk.Frame(self.root, padx=5)
        main_frame.pack(expand=True, fill='both')

        # Кнопка выключения
        shutdown_btn = tk.Button(main_frame,
                                 text="Выключить",
                                 bg="#e74c3c",
                                 fg="white",
                                 width=50,
                                 command=self.shutdown)
        shutdown_btn.pack(pady=5)

        # Кнопка перезагрузки
        restart_btn = tk.Button(main_frame,
                                text="Перезагрузить",
                                bg="#3498db",
                                fg="white",
                                width=50,
                                command=self.restart)
        restart_btn.pack()

    def shutdown(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите выключить компьютер?"):
            try:
                os.system("wpeutil shutdown")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось выключить компьютер: {str(e)}")

    def restart(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите перезагрузить компьютер?"):
            try:
                os.system("wpeutil reboot")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось перезагрузить компьютер: {str(e)}")


def main():
    root = tk.Tk()
    app = WinPEUtility(root)
    root.mainloop()


if __name__ == "__main__":
    main()