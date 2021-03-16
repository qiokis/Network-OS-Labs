import tkinter as tk
import tkinter.ttk as ttk
import datetime

import Service
from tkinter import messagebox as mb


class CreateOrderApp(tk.Toplevel):
    def __init__(self, service, update_table):
        self.update_table = update_table
        super().__init__()

        self.service = service
        self.table_customers = ttk.Treeview(self)

        self.table_customers["columns"] = ("Код покупателя",
                                           "Покупатель",
                                           "Адрес покупателя"
                                           )

        self.table_customers.column("#0", width=0)
        self.table_customers.column("Код покупателя", width=80, minwidth=80, anchor=tk.CENTER)
        self.table_customers.column("Покупатель", width=200, minwidth=200)
        self.table_customers.column("Адрес покупателя", width=300, minwidth=300)

        self.table_customers.heading("#0", text="")
        self.table_customers.heading("Код покупателя", text="Код покупателя", anchor=tk.CENTER)
        self.table_customers.heading("Покупатель", text="Покупатель", anchor=tk.CENTER)
        self.table_customers.heading("Адрес покупателя", text="Адрес покупателя", anchor=tk.CENTER)

        # self.table_customers.bind("<<TreeviewSelect>>", self.on_select, "+")
        self.table_customers.bind("<Double-1>", self.on_double_click_customers)

        self.table_customers.grid(row=0, column=0, padx=5, pady=5)

        self.table_products = ttk.Treeview(self)

        self.table_products["columns"] = ("Код товара",
                                          "Товар",
                                          "Изготовитель",
                                          "Модель",
                                          "Технические характеристики",
                                          "Наличие на складе",
                                          "Цена")

        self.table_products.column("#0", width=0)
        self.table_products.column("Код товара", width=80, minwidth=80, anchor=tk.CENTER)
        self.table_products.column("Товар", width=60, minwidth=60)
        self.table_products.column("Изготовитель", width=85, minwidth=85)
        self.table_products.column("Модель", width=70, minwidth=70)
        self.table_products.column("Технические характеристики", width=180, minwidth=180)
        self.table_products.column("Наличие на складе", width=120, minwidth=120)
        self.table_products.column("Цена", width=120, minwidth=100)

        self.table_products.heading("#0", text="")
        self.table_products.heading("Код товара", text="Код товара", anchor=tk.CENTER)
        self.table_products.heading("Товар", text="Товар", anchor=tk.CENTER)
        self.table_products.heading("Изготовитель", text="Изготовитель", anchor=tk.CENTER)
        self.table_products.heading("Модель", text="Модель", anchor=tk.CENTER)
        self.table_products.heading("Технические характеристики", text="Технические характеристики", anchor=tk.CENTER)
        self.table_products.heading("Наличие на складе", text="Наличие на складе", anchor=tk.CENTER)
        self.table_products.heading("Цена", text="Цена", anchor=tk.CENTER)

        # self.table_products.bind("<<TreeviewSelect>>", self.on_select, "+")
        self.table_products.bind("<Double-1>", self.on_double_click_products)

        self.table_products.grid(row=0, column=1)

        self.table_new_order = ttk.Treeview(self)

        self.table_new_order["columns"] = ("Код записи",
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

        self.table_new_order.column("#0", width=0)
        self.table_new_order.column("Код записи", width=80, minwidth=80, anchor=tk.CENTER)
        self.table_new_order.column("Код заказа", width=65, minwidth=65, anchor=tk.CENTER)
        self.table_new_order.column("Дата заказа", width=85, minwidth=85, anchor=tk.CENTER)
        self.table_new_order.column("Заказчик", width=140, minwidth=140)
        self.table_new_order.column("Адрес заказчика", width=230, minwidth=230)
        self.table_new_order.column("Товар", width=80, minwidth=80)
        self.table_new_order.column("Изготовитель", width=85, minwidth=85)
        self.table_new_order.column("Модель", width=80, minwidth=80)
        self.table_new_order.column("Цена", width=80, minwidth=80)
        self.table_new_order.column("Получено", width=70, minwidth=70, anchor=tk.CENTER)
        self.table_new_order.column("Сумма", width=80, minwidth=80)

        self.table_new_order.heading("#0", text="")
        self.table_new_order.heading("Код записи", text="Код записи", anchor=tk.CENTER)
        self.table_new_order.heading("Код заказа", text="Код заказа", anchor=tk.CENTER)
        self.table_new_order.heading("Дата заказа", text="Дата заказа", anchor=tk.CENTER)
        self.table_new_order.heading("Заказчик", text="Заказчик", anchor=tk.CENTER)
        self.table_new_order.heading("Адрес заказчика", text="Адрес заказчика", anchor=tk.CENTER)
        self.table_new_order.heading("Товар", text="Товар", anchor=tk.CENTER)
        self.table_new_order.heading("Изготовитель", text="Изготовитель", anchor=tk.CENTER)
        self.table_new_order.heading("Модель", text="Модель", anchor=tk.CENTER)
        self.table_new_order.heading("Цена", text="Цена", anchor=tk.CENTER)
        self.table_new_order.heading("Получено", text="Получено", anchor=tk.CENTER)
        self.table_new_order.heading("Сумма", text="Сумма", anchor=tk.CENTER)

        # self.table_new_order.bind("<<TreeviewSelect>>", self.on_select, "+")

        self.table_new_order.grid(row=1, column=0, columnspan=2)

        self.frame = tk.Frame(self)

        self.quantity = tk.Entry(self.frame)
        self.order_number = tk.Entry(self.frame)
        tk.Label(self.frame, text="Количество").grid(row=2, column=0)
        self.quantity.grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self.frame, text="Номер заказа").grid(row=2, column=2)
        self.order_number.grid(row=2, column=3, padx=10)
        tk.Button(self.frame, text="Сохранить", font="Times 20", command=self.save_order)\
            .grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.frame, text="Отправить", font="Times 20", command=self.send_order)\
            .grid(row=3, column=2, columnspan=2, pady=10)

        self.frame.grid()

        self.date = datetime.datetime.today().strftime("%Y-%m-%d")
        self.values = [0, 0, self.date, "", "", "", "", "", "", "", ""]
        self.product_id = None
        self.customer_id = None

        self.update_tables()

    def save_order(self):
        self.values[1] = self.order_number.get()
        self.values[9] = self.quantity.get()
        self.values[10] = float(self.values[9]) * float(self.values[8])
        self.update_order()

    def send_order(self):
        if self.service.subtract_products(self.product_id, self.values[9]):

            self.service.add("orders", number=self.order_number.get(),
                             date=self.date,
                             product_id=self.product_id,
                             received=self.values[9],
                             customer_id=self.customer_id)
            self.update_table.update_table()
        else:
            mb.showinfo("Ошибка", f"Извините, такое количество товара отсутствует на складе.")

    def on_double_click_customers(self, event):
        values = self.table_customers.item(self.table_customers.selection())["values"]
        self.customer_id = values[0]
        self.values[3] = values[1]
        self.values[4] = values[2]
        self.table_customers.selection_remove(self.table_customers.selection()[0])
        self.update_order()

    def on_double_click_products(self, event):
        values = self.table_products.item(self.table_products.selection())["values"]
        print(values)
        self.product_id = values[0]
        self.values[5] = values[1]
        self.values[6] = values[2]
        self.values[7] = values[3]
        self.values[8] = values[6]
        self.table_products.selection_remove(self.table_products.selection()[0])
        self.update_order()

    def update_order(self):
        for child in self.table_new_order.get_children():
            self.table_new_order.delete(child)
        self.table_new_order.insert("", 0, values=self.values)

    def update_tables(self):
        for child in self.table_products.get_children():
            self.table_products.delete(child)
        products = self.service.get_products()
        for i, val in zip(products.keys(), products.values()):
            self.table_products.insert("", i, values=(val.get_iid(),
                                                      val.get_name(),
                                                      val.get_brand(),
                                                      val.get_model(),
                                                      val.get_description(),
                                                      val.get_remains(),
                                                      val.get_price()
                                                      ))
        for child in self.table_customers.get_children():
            self.table_customers.delete(child)
        customers = self.service.get_customers()
        for i, val in zip(customers.keys(), customers.values()):
            self.table_customers.insert("", i, values=(val.get_iid(),
                                                       val.get_name(),
                                                       val.get_address()
                                                       ))


if __name__ == '__main__':
    root = tk.Tk()
    CreateOrderApp(Service.Service())
    root.mainloop()
