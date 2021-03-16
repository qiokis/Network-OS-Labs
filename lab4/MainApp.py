import sys
import tkinter as tk
import OrdersApp
import Service
import CustomersApp
import ProductsApp
import CreateOrderApp
import ReportApp


class MainApp(tk.Frame):
    users = {"a": "a", "vasya": "1234"}

    def authentication(self, parent, service):
        self.parent = parent
        self.parent.title("Database Login")
        self.service = service

        self.title_frame = tk.Frame(self.parent, bd=2, relief="groove")
        self.auth_frame = tk.Frame(self.parent, bd=2, relief="groove")
        self.btn_frame = tk.Frame(self.parent)

        tk.Label(self.title_frame, text="Database:", font="Times 15", anchor=tk.W, width=10).grid(row=0, column=0)
        tk.Label(self.title_frame, text="ADOConnection", font="Times 15", anchor=tk.W, width=15).grid(row=0, column=1)

        tk.Label(self.auth_frame, text="User name:", font="Times 15", anchor=tk.W, width=10).grid(row=0, column=0)
        tk.Label(self.auth_frame, text="Password:", font="Times 15", anchor=tk.W, width=10).grid(row=1, column=0)
        self.username = tk.Entry(self.auth_frame, width=15)
        self.username.grid(row=0, column=1)
        self.password = tk.Entry(self.auth_frame, width=15, show="#")
        self.password.grid(row=1, column=1)

        self.img = tk.PhotoImage(file="shrek_ok.gif")
        self.ok_btn = tk.Button(self.btn_frame, text="Ok", image=self.img, command=self.auth, width=60, height=30)
        self.img1 = tk.PhotoImage(file="shrek_cancel.gif")
        self.ok_btn.grid(row=0, column=0)
        self.cancel_btn = tk.Button(self.btn_frame, text="Cancel", image=self.img1, padx=5, width=60, height=30, command=sys.exit)
        self.cancel_btn.grid(row=0, column=1)

        self.title_frame.grid(row=0, column=0)
        self.auth_frame.grid(row=1, column=0)
        self.btn_frame.grid(row=2, column=0, pady=5)

    def auth(self):
        user = self.username.get()
        password = self.password.get()
        if user and password:
            if self.users[user] == password:
                for child in self.parent.winfo_children():
                    child.destroy()
                self.order_table = OrdersApp.OrdersApp(self.parent, self.service)
                self.order_table.grid()
                self.create_menus()
            else:
                return False

    def create_menus(self):
        self.menu = tk.Menu(self.parent)
        self.parent.config(menu=self.menu)

        self.order_menu = tk.Menu(self.menu, tearoff=0)
        self.sort_menu = tk.Menu(self.menu, tearoff=0)

        cmnd = lambda x=self.order_table, y=self.service: CreateOrderApp.CreateOrderApp(y, x)
        self.order_menu.add_command(label="Добавить заказ", command=cmnd)
        self.order_menu.add_command(label="Удалить заказ", command=self.order_table.remove)
        self.menu.add_cascade(label="Заказы", menu=self.order_menu)

        cmnd = lambda x="order", y=self.order_table: self.service.sort_orders(y, x)
        self.sort_menu.add_command(label="По номеру заказа", command=cmnd)
        cmnd = lambda x="client", y=self.order_table: self.service.sort_orders(y, x)
        self.sort_menu.add_command(label="По клиенту", command=cmnd)
        cmnd = lambda x="product", y=self.order_table: self.service.sort_orders(y, x)
        self.sort_menu.add_command(label="По товару", command=cmnd)
        self.menu.add_cascade(label="Сортировка таблицы \"Заказы\"", menu=self.sort_menu)

        cmnd = lambda x=self.parent, y=self.service, z=self.order_table: CustomersApp.CustomersApp(x, y, z)
        self.menu.add_command(label="Покупатели", command=cmnd)
        cmnd = lambda x=self.parent, y=self.service, z=self.order_table: ProductsApp.ProductsApp(x, y, z)
        self.menu.add_command(label="Товары", command=cmnd)
        cmnd = lambda x=self.parent, y=self.service: ReportApp.ReportApp(x, y)
        self.menu.add_command(label="Отчет", command=cmnd)
        self.menu.add_command(label="Выход", command=sys.exit)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.service = Service.Service()
        self.authentication(self.parent, self.service)


if __name__ == '__main__':
    root = tk.Tk()

    MainApp(root)
    root.mainloop()
