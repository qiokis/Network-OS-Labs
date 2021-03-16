from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import re
import sys

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


def open_file():
    file_name = fd.askopenfilename(filetypes=(("TXT filex", "*.txt"), ))
    return file_name


def create_table(path=""):
    if not path:
        path = open_file()

    if path == "":
        return

    with open(path, "r") as f:

        for i in table_frame.winfo_children():
            i.destroy()

        for i in chart_frame.winfo_children():
            i.destroy()

        main_menu.delete(4)
        main_menu.delete(3)
        main_menu.add_command(label=f.readline())
        string = f.readline()
        global charts
        charts = []

        while not re.search("[|]", string):
            charts.append(string.strip())
            string = f.readline()

        chart_values = []
        for i in range(len(charts) + 1):
            chart_values.append([])

        counter = 0
        for symbol in string:
            if symbol == "|":
                counter += 1

        columns = [str(i) for i in range(counter - 1, 0, -1)]
        columns.append("№ п/п")
        columns = columns[::-1]

        table = ttk.Treeview(table_frame, columns=columns)

        for i, j in enumerate(columns):
            table.column("#" + str(i), width=60, minwidth=40)

        for i, j in enumerate(columns):
            table.heading("#" + str(i), text=j, anchor=W)

        while string:
            for i, j in enumerate(string.split("|")[1:-1]):
                chart_values[i].append(float(j))
            number, values = string.split("|")[0], string.split("|")[1:]
            table.insert("", END, values=values, text=number)
            string = f.readline()

        table.pack(fill=BOTH, expand=True)

        nb.pack()

        create_chart(charts, chart_values)


def create_chart(names, values):
    if len(names) > len(values) - 2:
        temp = [i for i in range(len(values[0]))]
        for i in range(len(values) - len(names)):
            values.insert(0, temp)
    chart_types = ["r^", "b-", "g-", "r-", "y-", "k-", "m-", "c-", "r-", "b--", "g--", "r--", "y--"]
    current_type = 0
    fig = Figure(figsize=(5, 5), dpi=100)
    a = fig.add_subplot(111)
    for i in values[2:]:
        if not i:
            continue
        a.plot(values[0], i, chart_types[current_type])
        plt.plot(values[0], i, chart_types[current_type])
        current_type += 1
    plt.legend(charts)
    can = FigureCanvasTkAgg(fig, master=chart_frame)
    can.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    main_menu.add_command(label="Масштабируемая диаграмма", command=scaling_tab)


def scaling_tab():
    plt.show()


root = Tk()
root.title("Построение графика функций")
root.geometry("1000x400")
root.resizable(False, False)

main_menu = Menu(root)
root.config(menu=main_menu)
main_menu.add_command(label="Открыть файл", command=create_table)
main_menu.add_command(label="Сохранить график в буфере ММО")

nb = ttk.Notebook(root)

chart_frame = Frame(nb)
table_frame = Frame(nb)

nb.add(chart_frame, text="Графики")
nb.add(table_frame, text="Таблица")

nb.pack(fill="both", expand="yes")

if len(sys.argv) != 1:
    path = " ".join(sys.argv[1:])
    create_table(path)

charts = []

root.mainloop()
