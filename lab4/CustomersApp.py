import tkinter as tk
import tkinter.ttk as ttk
from DAO import *
from Service import *


class CustomersApp(tk.Toplevel):

    def __init__(self, parent, service, table_to_update):
        super().__init__()
        self.service = service
        self.parent = parent
        self.table_to_update = table_to_update
        self.parent.title("Редактирование таблицы \"Покупатель\"")

        self.info_frame = tk.Frame(self)
        self.btn_frame = tk.Frame(self)
        self.table_frame = tk.Frame(self)

        tk.Label(self.info_frame, text="Покупатель", anchor=tk.W, width=23).grid(row=0, column=0)
        tk.Label(self.info_frame, text="Адрес покупателя", anchor=tk.W, width=23).grid(row=0, column=2)

        self.name = tk.Entry(self.info_frame, width=30)
        self.address = tk.Entry(self.info_frame, width=40)
        self.name.grid(row=0, column=1, pady=5, padx=(0, 5))
        self.address.grid(row=0, column=3, pady=5)

        self.table = ttk.Treeview(self.table_frame)

        self.table["columns"] = ("Код покупателя",
                                 "Покупатель",
                                 "Адрес покупателя"
                                 )

        self.table.column("#0", width=0)
        self.table.column("Код покупателя", width=80, minwidth=80, anchor=tk.CENTER)
        self.table.column("Покупатель", width=200, minwidth=200)
        self.table.column("Адрес покупателя", width=300, minwidth=300)

        self.table.heading("#0", text="")
        self.table.heading("Код покупателя", text="Код покупателя", anchor=tk.CENTER)
        self.table.heading("Покупатель", text="Покупатель", anchor=tk.CENTER)
        self.table.heading("Адрес покупателя", text="Адрес покупателя", anchor=tk.CENTER)

        self.table.bind("<<TreeviewSelect>>", self.on_select, "+")

        self.table.pack()

        self.edit = tk.Button(self.btn_frame, text="Изменить", width=10, command=self.change)
        self.add = tk.Button(self.btn_frame, text="Добавить", width=10, command=self.add)
        self.delete = tk.Button(self.btn_frame, text="Удалить", width=10, command=self.remove)
        self.exit = tk.Button(self.btn_frame, text="Выход", width=10, command=self.on_closing)
        self.edit.grid(row=0, column=0, padx=5, pady=5)
        self.add.grid(row=1, column=0, padx=5, pady=5)
        self.delete.grid(row=2, column=0, padx=5, pady=5)
        self.exit.grid(row=3, column=0, padx=5, pady=5)

        self.info_frame.grid(row=0, column=0, columnspan=4)
        self.table_frame.grid(row=1, column=0, columnspan=3)
        self.btn_frame.grid(row=1, column=3)

        self.update_table()

    def get_table(self):
        return self.table

    def update_table(self):
        for child in self.table.get_children():
            self.table.delete(child)
        customers = self.service.get_customers()
        for i, val in zip(customers.keys(), customers.values()):
            self.table.insert("", i, values=(val.get_iid(),
                                             val.get_name(),
                                             val.get_address()
                                             ))

    def on_closing(self):
        self.destroy()

    def add(self):
        self.service.add("customers",
                         name=self.name.get(),
                         address=self.address.get()
                         )
        self.update_table()

    def change(self):
        self.service.change("customers",
                            self.table.item(self.table.selection())["values"][0],
                            name=self.name.get(),
                            address=self.address.get()
                            )
        self.update_table()
        self.table_to_update.update_table()

    def remove(self):
        iid = self.table.item(self.table.selection())["values"][0]
        self.service.delete("customers", iid)
        self.update_table()
        self.table_to_update.update_table()

    def on_select(self, event):
        self.service.get_orders()
        self.current = self.table.selection()

        self.clear_fields()
        values = self.table.item(self.table.selection())["values"]
        self.name.insert(0, values[1])
        self.address.insert(0, values[2])

    def clear_fields(self):
        self.name.delete(0, tk.END)
        self.address.delete(0, tk.END)

    def change_fields(self):
        self.table.delete(self.current)
        self.current = None
        self.table.insert("", 0, text="0", values=("3", "Дивядюк", "Хитачи", "FGH", "Good", "100", "200.3",))

    # def get_values(self):





if __name__ == '__main__':
    root = tk.Tk()
    root.title("asdd")
    serv = Service()
    CustomersApp(root, serv, )
    root.mainloop()