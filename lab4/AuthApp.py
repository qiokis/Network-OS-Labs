import sys
import tkinter as tk
import OrdersApp
import Service


class AuthApp(tk.Frame):

    users = {"a": "a", "vasya": "1234"}

    def __init__(self, parent, service):

        super().__init__()
        self.parent = parent
        self.parent.title("Database Login")
        self.service = service
        # self.parent.geometry("250x80")

        self.title_frame = tk.Frame(bd=2, relief="groove")
        self.auth_frame = tk.Frame(bd=2, relief="groove")
        self.btn_frame = tk.Frame()

        tk.Label(self.title_frame, text="Database:", font="Times 15", anchor=tk.W, width=10).grid(row=0, column=0)
        tk.Label(self.title_frame, text="ADOConnection", font="Times 15", anchor=tk.W, width=15).grid(row=0, column=1)

        tk.Label(self.auth_frame, text="User name:", font="Times 15", anchor=tk.W, width=10).grid(row=0, column=0)
        tk.Label(self.auth_frame, text="Password:", font="Times 15", anchor=tk.W, width=10).grid(row=1, column=0)
        self.username = tk.Entry(self.auth_frame, width=15)
        self.username.grid(row=0, column=1)
        self.password = tk.Entry(self.auth_frame, width=15, show="#")
        self.password.grid(row=1, column=1)

        self.img = tk.PhotoImage(file="shrek_ok.gif")
        self.ok_btn = tk.Button(self.btn_frame, text="Ok", image=self.img, command=self.auth)
        self.ok_btn.grid(row=0, column=0)
        self.cancel_btn = tk.Button(self.btn_frame, text="Cancel", padx=5, width=10, command=sys.exit)
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
                OrdersApp.OrdersApp(self.parent, self.service).grid()
            else:
                return False


if __name__ == '__main__':
    root = tk.Tk()
    AuthApp(root).grid()
    root.mainloop()