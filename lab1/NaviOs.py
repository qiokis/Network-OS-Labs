import _io
import atexit
import subprocess
from datetime import datetime
from threading import Timer
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import os
import re
import time

import win32gui


def get_mouse_pos():
    x, y = win32gui.GetCursorInfo()[2]
    x_field.config(text=x)
    y_field.config(text=y)
    global global_counter
    if writing_status:
        f.write("{}|{:.4f}|{}|{}|\n".format(global_counter,
                                            time.perf_counter() - start_time, x, y))
        global_counter += 1
    global t
    t = Timer(0.01, get_mouse_pos)
    t.start()


def update_file_list():
    for children in table.get_children():
        table.delete(children)

    values = []
    counter = 1
    for path in os.listdir():
        if re.search(r"\w+[.]txt", path):
            values.append([counter, path, os.stat(path).st_size, datetime.fromtimestamp(os.stat(path).st_mtime)])
            counter += 1

    for number, vals in enumerate(values):
        table.insert("", number, text=f"Line {number}", values=vals)


def on_select(event):
    to_memo(table.item(table.selection())["values"][1])


def to_notepad():
    path = open_file()
    if not path:
        return
    subprocess.call("notepad.exe {}".format(path))


def to_memo(path=""):
    memo.delete(1.0, END)
    if not path:
        path = open_file()
    if not path:
        return
    with open(path, "r") as file:
        string = file.readline()
        while string:
            memo.insert(END, string)
            string = file.readline()


def open_file():
    temp = fd.askopenfilename(filetypes=(("TXT filex", "*.txt"), ))
    if not temp:
        return False
    new_dir = temp
    for i in reversed(new_dir):
        if i == "/":
            new_dir = new_dir[:-1]
            break
        new_dir = new_dir[:-1]
    name_dir.configure(text=new_dir)
    os.chdir(new_dir)
    update_file_list()
    match = re.search(r"\w+[.]txt", temp)
    entry_field.configure(text=match[0])
    return temp


def create_chart():
    path = open_file()
    if not path:
        return
    # Абсолютный путь
    subprocess.call("python "
                    r"lab1\MyChart.py "
                    "{}".format(path))


def start_writing():
    global f
    global writing_status
    global start_time
    start_time = time.perf_counter()
    f = open(writing_file.get(), "w")
    f.write("Хроника движения мыши\nГрафик 1\nГрафик 2\n")
    writing_status = True


def stop_writing():
    global writing_status
    writing_status = False
    f.close()


def on_exit():
    global t
    t.cancel()
    exit(1)


if __name__ == '__main__':

    root = Tk()
    root.title("NaviOS")
    root.resizable(False, False)
    # root.overrideredirect(1)

    table_frame = Frame(root)
    table_frame.grid(row=0, column=1)

    table = ttk.Treeview(table_frame)

    table["columns"] = ("№ п/п", "Имя файла", "Размер", "Дата создания")

    table.column("#0", width=0)
    table.column("№ п/п", width=20, minwidth=40, anchor=CENTER)
    table.column("Имя файла", width=100, minwidth=40)
    table.column("Размер", width=100, minwidth=40)
    table.column("Дата создания", width=120, minwidth=120)

    table.heading("#0", text="")
    table.heading("№ п/п", text="№ п/п", anchor=CENTER)
    table.heading("Имя файла", text="Имя файла", anchor=CENTER)
    table.heading("Размер", text="Размер", anchor=CENTER)
    table.heading("Дата создания", text="Дата создания", anchor=CENTER)

    table.bind("<<TreeviewSelect>>", on_select, "+")

    table.pack()

    update_file_list()

    functional_frame = Frame(root)
    functional_frame.grid(row=0, column=0)

    Label(root, text="Переменная NameDir:").grid(row=1, column=0, columnspan=2)
    name_dir = Label(root, text=os.getcwd(), relief="sunken")
    name_dir.grid(row=2, column=0, columnspan=2)

    memo_frame = Frame(functional_frame)
    btns_frame = Frame(functional_frame)

    memo_frame.grid(row=0, column=1)
    btns_frame.grid(row=0, column=0)

    read_into_notepad = Button(btns_frame, text="Прочитать файл в notepad", width=25, command=to_notepad)
    read_into_notepad.grid(row=0, column=0, columnspan=4, pady=4, padx=10)

    read_into_memo = Button(btns_frame, text="Прочитать в мемополе", width=25, command=to_memo)
    read_into_memo.grid(row=1, column=0, columnspan=4, pady=4, padx=10)

    create_chart = Button(btns_frame, text="Построить график", width=25, command=create_chart)
    create_chart.grid(row=2, column=0, columnspan=4, pady=4, padx=10)

    Label(btns_frame, text="Открываемый файл", justify=LEFT)\
        .grid(row=3, column=0, columnspan=4, pady=4, padx=10)

    entry_field = Label(btns_frame, relief="sunken", bg="white", width=20)
    entry_field.grid(row=4, column=0, columnspan=4, pady=4, padx=10)

    Label(btns_frame, text="X").grid(row=5, column=1)
    Label(btns_frame, text="Y").grid(row=6, column=1)

    x_field = Label(btns_frame, width=5, relief="sunken", bg="white")
    x_field.grid(row=5, column=2)

    y_field = Label(btns_frame, width=5, relief="sunken", bg="white")
    y_field.grid(row=6, column=2)

    Label(btns_frame, text="Записываемый файл:").grid(row=7, column=2)
    writing_file = Entry(btns_frame)
    writing_file.grid(row=8, column=2)
    start_write_file_btn = Button(btns_frame, text="Начать запись", command=start_writing, width=15)
    start_write_file_btn.grid(row=9, column=2, pady=5)
    stop_write_file_btn = Button(btns_frame, text="Остановить запись", command=stop_writing, width=15)
    stop_write_file_btn.grid(row=10, column=2, pady=5)
    cancel_btn = Button(btns_frame, text="Выход", command=on_exit, width=15)
    cancel_btn.grid(row=11, column=2, pady=5)


    f: _io.TextIOWrapper
    writing_status = False
    global_counter = 0
    start_time: float

    Label(memo_frame, text="Текст в файле:").grid(row=0, column=0)
    memo = Text(memo_frame, width=30, height=17)
    memo.grid(row=1, column=0, padx=10, pady=4)

    t = Timer(0.01, get_mouse_pos)
    t.start()

    root.mainloop()
