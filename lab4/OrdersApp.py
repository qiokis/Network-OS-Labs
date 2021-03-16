import tkinter as tk
import tkinter.ttk as ttk
from DAO import *
from Service import *
import sys
import CustomersApp
import ProductsApp
import heapq
import sys


class OrdersApp(tk.Frame):

    def __init__(self, parent, service):
        super().__init__()
        self.service = service
        self.parent = parent
        self.parent.title("Учет заказов")

        self.table = ttk.Treeview(self, height=30)

        self.current = None

        self.table["columns"] = ("Код записи",
                                 "Код заказа",
                                 "Дата заказа",
                                 "Заказчик",
                                 "Адрес заказчика",
                                 "Товар",
                                 "Изготовитель",
                                 "Модель",
                                 "Цена",
                                 "Получено",
                                 "Сумма")

        self.table.column("#0", width=0)
        self.table.column("Код записи", width=80, minwidth=80, anchor=tk.CENTER)
        self.table.column("Код заказа", width=65, minwidth=65, anchor=tk.CENTER)
        self.table.column("Дата заказа", width=85, minwidth=85, anchor=tk.CENTER)
        self.table.column("Заказчик", width=140, minwidth=140)
        self.table.column("Адрес заказчика", width=230, minwidth=230)
        self.table.column("Товар", width=80, minwidth=80)
        self.table.column("Изготовитель", width=85, minwidth=85)
        self.table.column("Модель", width=80, minwidth=80)
        self.table.column("Цена", width=80, minwidth=80)
        self.table.column("Получено", width=70, minwidth=70, anchor=tk.CENTER)
        self.table.column("Сумма", width=80, minwidth=80)

        self.table.heading("#0", text="")
        self.table.heading("Код записи", text="Код записи", anchor=tk.CENTER)
        self.table.heading("Код заказа", text="Код заказа", anchor=tk.CENTER)
        self.table.heading("Дата заказа", text="Дата заказа", anchor=tk.CENTER)
        self.table.heading("Заказчик", text="Заказчик", anchor=tk.CENTER)
        self.table.heading("Адрес заказчика", text="Адрес заказчика", anchor=tk.CENTER)
        self.table.heading("Товар", text="Товар", anchor=tk.CENTER)
        self.table.heading("Изготовитель", text="Изготовитель", anchor=tk.CENTER)
        self.table.heading("Модель", text="Модель", anchor=tk.CENTER)
        self.table.heading("Цена", text="Цена", anchor=tk.CENTER)
        self.table.heading("Получено", text="Получено", anchor=tk.CENTER)
        self.table.heading("Сумма", text="Сумма", anchor=tk.CENTER)

        self.table.bind("<<TreeviewSelect>>", self.on_select, "+")

        self.table.pack()

        self.update_table()

    def create_menu(self):
        pass

    def sort(self, type=""):
        self.service.sort("orders", type=type)

    def update_table(self):
        for child in self.table.get_children():
            self.table.delete(child)
        orders = self.service.get_orders()
        for i, val in zip(orders.keys(), orders.values()):
            self.table.insert("", i, values=(val.get_iid(),
                                             val.get_number(),
                                             val.get_date(),
                                             val.get_customer_name(),
                                             val.get_customer_address(),
                                             val.get_product_name(),
                                             val.get_brand_name(),
                                             val.get_model_name(),
                                             val.get_price(),
                                             val.get_received(),
                                             val.get_total()
                                             ))

    def add(self):
        self.service.add("orders",
                         product_name=self.name.get(),
                         brand_name=self.brand.get(),
                         model_name=self.model.get(),
                         description=self.description.get(),
                         remains=self.remains.get(),
                         price=self.price.get())
        self.update_table()

    def change(self):
        self.service.change("products",
                            self.table.item(self.table.selection())["values"][0],
                            product_name=self.name.get(),
                            brand_name=self.brand.get(),
                            model_name=self.model.get(),
                            description=self.description.get(),
                            remains=self.remains.get(),
                            price=self.price.get())
        self.update_table()

    def remove(self):
        iid = self.table.item(self.table.selection())["values"][0]
        self.service.delete("orders", iid)
        self.update_table()

    def on_select(self, event):
        self.current = self.table.selection()

    def clear_fields(self):
        self.name.delete(0, tk.END)
        self.model.delete(0, tk.END)
        self.brand.delete(0, tk.END)
        self.description.delete(0, tk.END)
        self.remains.delete(0, tk.END)
        self.price.delete(0, tk.END)

    def change_fields(self):
        self.table.delete(self.current)
        self.current = None
        self.table.insert("", 0, text="0", values=("3", "Дивядюк", "Хитачи", "FGH", "Good", "100", "200.3",))

    # def get_values(self):


if __name__ == '__main__':
    root = tk.Tk()
    root.title("asdd")
    serv = Service()
    OrdersApp(root, serv).grid()
    root.mainloop()