import sys
import tkinter as tk
import tkinter.ttk as ttk
import Service


class ReportApp(tk.Toplevel):

    def __init__(self, parent, service):
        super(ReportApp, self).__init__()

        self.parent = parent
        self.service = service

        self.btn_frame = tk.Frame(self)
        self.quantity_frame = tk.Frame(self)
        self.total_price_frame = tk.Frame(self)
        self.btn_frame.pack()
        self.quantity_frame.pack()
        self.total_price_frame.pack()

        self.general_btn = tk.Button(self.btn_frame, text="Общие заказы", command=self.update_info)
        self.model_btn = tk.Button(self.btn_frame, text="По моделям", command=self.select_model)
        self.model_combo = ttk.Combobox(self.btn_frame, state="readonly")
        self.exit_btn = tk.Button(self.btn_frame, text="Выход", command=self.destroy)
        self.models = []
        self.customer_list = []
        self.customers = {}
        self.orders = self.service.get_orders()
        self.service.get_customers()
        self.serv_customers = self.service.get_customers()
        self.serv_products = self.service.get_products()

        for key, value in zip(self.serv_customers.keys(), self.serv_customers.values()):
            customer = value.get_name()
            if customer not in self.customer_list:
                self.customer_list.append(customer)
        for key, value in zip(self.serv_products.keys(), self.serv_products.values()):
            model = value.get_model()
            if model not in self.models:
                self.models.append(model)

        self.model_combo["values"] = self.models
        self.model_combo.current(0)

        self.general_btn.grid(row=0, column=0, padx=5, pady=5)
        self.model_btn.grid(row=0, column=1, padx=5, pady=5)
        self.model_combo.grid(row=0, column=2, padx=5, pady=5)
        self.exit_btn.grid(row=0, column=3, padx=5, pady=5)

        self.quantity_table = ttk.Treeview(self.quantity_frame)

        self.quantity_table["columns"] = ("Покупатель",
                                          "Всего",
                                          "2021 год",
                                          "2020 год",
                                          "2019 год",
                                          "2018 год",
                                          "2017 год")

        self.quantity_table.column("#0", width=0)
        self.quantity_table.column("Покупатель", width=150, minwidth=150, anchor=tk.W)
        self.quantity_table.column("Всего", width=100, minwidth=100, anchor=tk.W)
        self.quantity_table.column("2021 год", width=70, minwidth=70, anchor=tk.W)
        self.quantity_table.column("2020 год", width=70, minwidth=70, anchor=tk.W)
        self.quantity_table.column("2019 год", width=70, minwidth=70, anchor=tk.W)
        self.quantity_table.column("2018 год", width=70, minwidth=70, anchor=tk.W)
        self.quantity_table.column("2017 год", width=70, minwidth=70, anchor=tk.W)

        self.quantity_table.heading("#0", text="")
        self.quantity_table.heading("Покупатель", text="Покупатель", anchor=tk.CENTER)
        self.quantity_table.heading("Всего", text="Всего", anchor=tk.CENTER)
        self.quantity_table.heading("2021 год", text="2021 год", anchor=tk.CENTER)
        self.quantity_table.heading("2020 год", text="2020 год", anchor=tk.CENTER)
        self.quantity_table.heading("2019 год", text="2019 год", anchor=tk.CENTER)
        self.quantity_table.heading("2018 год", text="2018 год", anchor=tk.CENTER)
        self.quantity_table.heading("2017 год", text="2017 год", anchor=tk.CENTER)

        self.quantity_table.pack(padx=10, pady=10)

        self.total_price_table = ttk.Treeview(self.total_price_frame)

        self.total_price_table["columns"] = ("Покупатель",
                                             "Всего",
                                             "2021 год",
                                             "2020 год",
                                             "2019 год",
                                             "2018 год",
                                             "2017 год")

        self.total_price_table.column("#0", width=0)
        self.total_price_table.column("Покупатель", width=150, minwidth=150, anchor=tk.W)
        self.total_price_table.column("Всего", width=100, minwidth=100, anchor=tk.W)
        self.total_price_table.column("2021 год", width=70, minwidth=70, anchor=tk.W)
        self.total_price_table.column("2020 год", width=70, minwidth=70, anchor=tk.W)
        self.total_price_table.column("2019 год", width=70, minwidth=70, anchor=tk.W)
        self.total_price_table.column("2018 год", width=70, minwidth=70, anchor=tk.W)
        self.total_price_table.column("2017 год", width=70, minwidth=70, anchor=tk.W)

        self.total_price_table.heading("#0", text="")
        self.total_price_table.heading("Покупатель", text="Покупатель", anchor=tk.CENTER)
        self.total_price_table.heading("Всего", text="Всего", anchor=tk.CENTER)
        self.total_price_table.heading("2021 год", text="2021 год", anchor=tk.CENTER)
        self.total_price_table.heading("2020 год", text="2020 год", anchor=tk.CENTER)
        self.total_price_table.heading("2019 год", text="2019 год", anchor=tk.CENTER)
        self.total_price_table.heading("2018 год", text="2018 год", anchor=tk.CENTER)
        self.total_price_table.heading("2017 год", text="2017 год", anchor=tk.CENTER)

        self.total_price_table.pack(padx=10, pady=10)

        self.update_info()

    def create_customers(self):
        self.customers = {}

        self.customers.update({"Итого": {"total": {"price": 0,
                                                   "quantity": 0},
                                         "2021": {"price": 0,
                                                  "quantity": 0},
                                         "2020": {"price": 0,
                                                  "quantity": 0},
                                         "2019": {"price": 0,
                                                  "quantity": 0},
                                         "2018": {"price": 0,
                                                  "quantity": 0},
                                         "2017": {"price": 0,
                                                  "quantity": 0},
                                         }})

        for customer in self.customer_list:
            self.customers.update({customer: {"total": {"price": 0,
                                                        "quantity": 0},
                                              "2021": {"price": 0,
                                                       "quantity": 0},
                                              "2020": {"price": 0,
                                                       "quantity": 0},
                                              "2019": {"price": 0,
                                                       "quantity": 0},
                                              "2018": {"price": 0,
                                                       "quantity": 0},
                                              "2017": {"price": 0,
                                                       "quantity": 0},
                                              }})

    def update_info(self, model=""):

        self.create_customers()

        if model == "":
            for key, value in zip(self.orders.keys(), self.orders.values()):
                customer = value.get_customer_name()
                year = str(value.get_date().year)
                self.customers["Итого"]["total"]["price"] += self.orders[key].get_total()
                self.customers["Итого"]["total"]["quantity"] += self.orders[key].get_received()
                self.customers[customer]["total"]["price"] += self.orders[key].get_total()
                self.customers[customer]["total"]["quantity"] += self.orders[key].get_received()
                if year in list(self.customers[customer].keys()):
                    self.customers[customer][year]["price"] += self.orders[key].get_total()
                    self.customers[customer][year]["quantity"] += self.orders[key].get_received()
                    self.customers["Итого"][year]["price"] += self.orders[key].get_total()
                    self.customers["Итого"][year]["quantity"] += self.orders[key].get_received()

        else:
            for key, value in zip(self.orders.keys(), self.orders.values()):
                customer = value.get_customer_name()
                year = str(value.get_date().year)
                if model == value.get_model_name():
                    self.customers[customer]["total"]["price"] += self.orders[key].get_total()
                    self.customers[customer]["total"]["quantity"] += self.orders[key].get_received()
                    self.customers["Итого"]["total"]["price"] += self.orders[key].get_total()
                    self.customers["Итого"]["total"]["quantity"] += self.orders[key].get_received()
                    if year in list(self.customers[customer].keys()):
                        self.customers[customer][year]["price"] += self.orders[key].get_total()
                        self.customers[customer][year]["quantity"] += self.orders[key].get_received()
                        self.customers["Итого"][year]["price"] += self.orders[key].get_total()
                        self.customers["Итого"][year]["quantity"] += self.orders[key].get_received()

        self.update_tables()

    def select_model(self):
        self.update_info(model=self.model_combo.get())

    def update_tables(self):

        for child in self.quantity_table.get_children():
            self.quantity_table.delete(child)

        for child in self.total_price_table.get_children():
            self.total_price_table.delete(child)

        for customer in self.customers:
            self.quantity_table.insert("", 0, values=(customer,
                                                      self.customers[customer]["total"]["quantity"],
                                                      self.customers[customer]["2021"]["quantity"],
                                                      self.customers[customer]["2020"]["quantity"],
                                                      self.customers[customer]["2019"]["quantity"],
                                                      self.customers[customer]["2018"]["quantity"],
                                                      self.customers[customer]["2017"]["quantity"]))
            self.total_price_table.insert("", 0, values=(customer,
                                                         self.customers[customer]["total"]["price"],
                                                         self.customers[customer]["2021"]["price"],
                                                         self.customers[customer]["2020"]["price"],
                                                         self.customers[customer]["2019"]["price"],
                                                         self.customers[customer]["2018"]["price"],
                                                         self.customers[customer]["2017"]["price"]))


if __name__ == '__main__':
    root = tk.Tk()
    ReportApp(root, Service.Service())
    root.mainloop()
