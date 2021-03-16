import tkinter as tk
import tkinter.ttk as ttk
from DAO import *
from Service import *


class ProductsApp(tk.Toplevel):

    def __init__(self, parent, service, table_to_update):
        super().__init__()
        self.service = service
        self.parent = parent
        self.table_to_update = table_to_update
        self.parent.title("Редактирование таблицы \"Товары\"")

        self.info_frame = tk.Frame(self)
        self.btn_frame = tk.Frame(self)
        self.table_frame = tk.Frame(self)

        tk.Label(self.info_frame, text="Товар", anchor=tk.W, width=23).grid(row=0, column=0)
        tk.Label(self.info_frame, text="Модель", anchor=tk.W, width=23).grid(row=1, column=0)
        tk.Label(self.info_frame, text="Наличие на складе", anchor=tk.W, width=23).grid(row=2, column=0)
        tk.Label(self.info_frame, text="Изготовитель", anchor=tk.W, width=23).grid(row=0, column=2)
        tk.Label(self.info_frame, text="Технические характеристики", anchor=tk.W, width=23).grid(row=1, column=2)
        tk.Label(self.info_frame, text="Цена", anchor=tk.W, width=23).grid(row=2, column=2)

        self.name = tk.Entry(self.info_frame)
        self.model = tk.Entry(self.info_frame)
        self.remains = tk.Entry(self.info_frame)
        self.brand = tk.Entry(self.info_frame)
        self.description = tk.Entry(self.info_frame)
        self.price = tk.Entry(self.info_frame)
        self.name.grid(row=0, column=1, pady=5, padx=(0, 5))
        self.model.grid(row=1, column=1, pady=5, padx=(0, 5))
        self.remains.grid(row=2, column=1, pady=5, padx=(0, 5))
        self.brand.grid(row=0, column=3, pady=5)
        self.description.grid(row=1, column=3, pady=5)
        self.price.grid(row=2, column=3, pady=5)

        self.table = ttk.Treeview(self.table_frame)

        self.table["columns"] = ("Код товара",
                                 "Товар",
                                 "Изготовитель",
                                 "Модель",
                                 "Технические характеристики",
                                 "Наличие на складе",
                                 "Цена")

        self.table.column("#0", width=0)
        self.table.column("Код товара", width=80, minwidth=80, anchor=tk.CENTER)
        self.table.column("Товар", width=60, minwidth=60)
        self.table.column("Изготовитель", width=85, minwidth=85)
        self.table.column("Модель", width=70, minwidth=70)
        self.table.column("Технические характеристики", width=180, minwidth=180)
        self.table.column("Наличие на складе", width=120, minwidth=120)
        self.table.column("Цена", width=120, minwidth=100)

        self.table.heading("#0", text="")
        self.table.heading("Код товара", text="Код товара", anchor=tk.CENTER)
        self.table.heading("Товар", text="Товар", anchor=tk.CENTER)
        self.table.heading("Изготовитель", text="Изготовитель", anchor=tk.CENTER)
        self.table.heading("Модель", text="Модель", anchor=tk.CENTER)
        self.table.heading("Технические характеристики", text="Технические характеристики", anchor=tk.CENTER)
        self.table.heading("Наличие на складе", text="Наличие на складе", anchor=tk.CENTER)
        self.table.heading("Цена", text="Цена", anchor=tk.CENTER)

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

        # self.table_customers.update()
        self.current = None
        self.update_table()
        ords = self.service.get_orders()

    def get_table(self):
        return self.table

    def on_closing(self):
        self.destroy()

    def update_table(self):
        for child in self.table.get_children():
            self.table.delete(child)
        products = self.service.get_products()
        for i, val in zip(products.keys(), products.values()):
            self.table.insert("", i, values=(val.get_iid(),
                                             val.get_name(),
                                             val.get_brand(),
                                             val.get_model(),
                                             val.get_description(),
                                             val.get_remains(),
                                             val.get_price()
                                             ))

    def add(self):
        self.service.add("products",
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
        self.table_to_update.update_table()

    def remove(self):
        iid = self.table.item(self.table.selection())["values"][0]
        self.service.delete("products", iid)
        self.update_table()
        self.table_to_update.update_table()

    def on_select(self, event):
        self.current = self.table.selection()

        self.clear_fields()
        values = self.table.item(self.table.selection())["values"]
        self.name.insert(0, values[1])
        self.brand.insert(0, values[2])
        self.model.insert(0, values[3])
        self.description.insert(0, values[4])
        self.remains.insert(0, values[5])
        self.price.insert(0, values[6])

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
    ProductsApp(root, serv)
    root.mainloop()