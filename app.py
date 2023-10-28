import tkinter as tk
from tkinter import scrolledtext, ttk

import configparser

# Создаем объект конфигурации
config = configparser.ConfigParser()
# Прочтите конфигурационный файл
config.read('config.ini', encoding='utf-8')
windowName = config.get('WINDOW', 'name')  # IP WEB API для ссылки: http://{ipWebServ}:8000/buttons/{factory}


# Глобальные переменные для интерфейса tkinter
root = tk.Tk()
root.title(f"Bot TCP Server [{windowName}]")  # Наименование Окна
# Устанавливаем размеры окна
root.geometry("800x400")  # Здесь "400x300" - ширина x высота в пикселях
root.iconbitmap("trt.ico")
# Отключаем возможность изменения размера окна
root.resizable(False, False)  # Первый аргумент - отключение изменения ширины, второй - высоты

# Виджет ScrolledText для вывода сообщений
log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled")
log_text.pack(expand=True, fill="both")


def copy_text(event):
    """
    Функия для копирования текста из лога программы
    :param event:
    :return:
    """
    selected_text = log_text.selection_get()
    root.clipboard_clear()
    root.clipboard_append(selected_text)


log_text.bind("<Control-c>", copy_text)  # Комбинация для копирования текста ил лога вывода программы


def update_log_text(message, color):
    """
    Метод вывода сообщеий в лог программы
    :param message:
    :param color:
    :return:
    """
    log_text.config(state="normal")
    log_text.tag_configure(color, foreground=color)
    log_text.insert(tk.END, message + "\n", color)
    # log_text.see(tk.END)  # Перемещаем виджет к концу текста
    log_text.config(state="disabled")  # Отключение редактирования окна с выводом


# Обработка события закрытия окна
def on_closing():
    root.iconify()  # Свернуть окно при закрытии
