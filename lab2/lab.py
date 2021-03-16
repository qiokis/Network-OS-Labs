import math
import random
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageDraw


class MyApp(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Frames
        self.parent_image = tk.Frame(self)
        self.draw_box = tk.Frame(self)
        self.memo_box = tk.Frame(self)
        self.paint_box = tk.Frame(self)
        self.image_box = tk.Frame(self.parent_image)

        # draw box content
        cmnd = lambda: self.clear("memo2")
        self.clear_memo2_btn = tk.Button(self.draw_box, text="Очистить Memo2", command=cmnd)
        cmnd = lambda: self.clear("memo1")
        self.clear_memo1_btn = tk.Button(self.draw_box, text="Очистить Memo1", command=cmnd)
        self.rewrite_memo_btn = tk.Button(self.draw_box, text="Переписать из Memo1 в Memo2", command=self.transfer_memo)
        self.blue_scale = ttk.Scale(self.draw_box, from_=0, to="255", command=self.change_blue)
        self.green_scale = ttk.Scale(self.draw_box, from_=0, to="255", command=self.change_green)
        self.red_scale = ttk.Scale(self.draw_box, from_=0, to="255", command=self.change_red)
        self.size_scale = ttk.Scale(self.draw_box, from_=1, to="100", command=self.draw_brush)
        self.blue_label = tk.Label(self.draw_box, text=f"Blue={0}")
        self.green_label = tk.Label(self.draw_box, text=f"Green={0}")
        self.red_label = tk.Label(self.draw_box, text=f"Red={0}")
        self.size_label = tk.Label(self.draw_box, text=f"Size={0}")
        self.rewrite_edit_btn = tk.Button(self.draw_box, text="Переписать из Edit1 в Edit2", command=self.transfer_edit)
        self.edit2 = tk.Entry(self.draw_box)
        self.edit1 = tk.Entry(self.draw_box)
        self.edit1.insert(0, "Edit1")

        # memo box content
        self.memo2 = tk.Text(self.memo_box, heigh=15, width=30)
        self.memo1 = tk.Text(self.memo_box, heigh=15, width=30)

        # Paint box options
        self.color = {"red": 0, "green": 0, "blue": 0}
        self.brush_size = 10

        # Menus
        self.menu = tk.Menu(self)
        self.mmo_buffer = tk.Menu(self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)

        # ImageBox
        self.load = Image.open("fill.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.img = tk.Label(self.image_box, image=self.render, width=400, heigh=400)

        # Paint Canvas
        self.canvas = tk.Canvas(self.paint_box, bg="white", width=400, height=400)

        # Brush
        self.brush_canvas = tk.Canvas(self.draw_box, bg="white", width=200, height=200)

        self.bitmap_buffer = None

        self.default_size = self.load.size

        self.initUI()

    def initUI(self):
        self.parent_image.grid(row=0, column=1)
        self.image_box.pack()
        self.paint_box.grid(row=0, column=0)
        self.memo_box.grid(row=1, column=1)
        self.draw_box.grid(row=1, column=0)

        self.parent.config(menu=self.menu)

        cmnd = lambda: self.set_picture("paint")
        self.file_menu.add_command(label="Загрузить в PaintBox", command=cmnd)
        cmnd = lambda: self.set_picture("image")
        self.file_menu.add_command(label="Загрузить в ImageBox", command=cmnd)
        self.file_menu.add_command(label="Загрузить в Bitmap", command=self.load_to_buffer)
        self.menu.add_cascade(label="Работа с файлами", menu=self.file_menu)

        # self.mmo_buffer.add_command(label="Сохранить Bitmap в буфере MMO")
        cmnd = lambda: self.set_pic_from_buffer("paint", self.bitmap_buffer)
        self.mmo_buffer.add_command(label="Считать из буфера ММО в PaintBox", command=cmnd)
        cmnd = lambda: self.set_pic_from_buffer("image", self.bitmap_buffer)
        self.mmo_buffer.add_command(label="Считать из буфера ММО в ImageBox", command=cmnd)
        self.menu.add_cascade(label="Работа с буфером MMO", menu=self.mmo_buffer)

        cmnd = lambda: self.resize(1.2)
        self.menu.add_command(label="Увеличить Image в 1.2 раза", command=self.resize)
        cmnd = lambda: self.resize(0.85)
        self.menu.add_command(label="Уменшить Image в 0.85 раза", command=cmnd)
        cmnd = lambda: self.resize(1)
        self.menu.add_command(label="Масштаб Image 1x1", command=cmnd)

        self.menu.add_command(label="Test func", command=self.test)

        # Frame with 2 Text fields
        self.memo1.grid(row=0, column=0, pady=5, padx=5)
        self.memo2.grid(row=0, column=1, pady=5, padx=5)

        # Frame with Buttons
        self.edit1.grid(row=0, column=0, pady=5, padx=5)
        self.edit2.grid(row=0, column=3, pady=5, padx=5)
        self.rewrite_edit_btn.grid(row=0, column=1, pady=5, padx=5, columnspan=2)

        self.size_label.grid(row=1, column=0)
        self.red_label.grid(row=2, column=0)
        self.green_label.grid(row=3, column=0)
        self.blue_label.grid(row=4, column=0)

        self.size_scale.grid(row=1, column=1)
        self.red_scale.grid(row=2, column=1)
        self.green_scale.grid(row=3, column=1)
        self.blue_scale.grid(row=4, column=1)

        self.brush_canvas.grid(row=1, column=2, rowspan=4, padx=5)

        self.rewrite_memo_btn.grid(row=1, column=3, pady=(5, 5))
        self.clear_memo1_btn.grid(row=2, column=3, pady=(5, 5))
        self.clear_memo2_btn.grid(row=3, column=3, pady=(5, 5))

        # Frame with picture
        self.img.pack(pady=5)

        # Frame with paint box
        self.canvas.pack(pady=5)

        self.canvas.bind("<B1-Motion>", self.draw)

        self.draw_brush(-1)

    def draw(self, event):
        self.canvas.create_oval(event.x - self.brush_size,
                                event.y - self.brush_size,
                                event.x + self.brush_size,
                                event.y + self.brush_size,
                                fill='#%02x%02x%02x' % (self.color["red"], self.color["green"], self.color["blue"]),
                                outline='#%02x%02x%02x' % (self.color["red"], self.color["green"], self.color["blue"]))

    def resize(self):
        self.resizable = self.load
        print(self.resizable)
        self.resizable.resize((250, 250), Image.ANTIALIAS)
        print(self.resizable)
        self.load = self.resizable
        self.render = ImageTk.PhotoImage(self.load)
        self.img["image"] = self.render
        # if size == 1:
        #     self.resizable.thumbnail(self.default_size, Image.ANTIALIAS)
        # else:
        #     width, height = self.resizable.size
        #     new_width, new_height = int(width * size), int(height * size)
        #     print(width, height)
        #     print(self.resizable.size)
        #     print(new_width, new_height)
        #     self.resizable.resize((new_width, new_height))
        #     print(self.resizable.size)
        #     self.load = self.resizable
        #     self.render = ImageTk.PhotoImage(self.load)
        #     self.img["image"] = self.render

    def set_pic_from_buffer(self, window, img=""):
        if img:
            if window == "image":
                self.render = ImageTk.PhotoImage(img)
                self.img.configure(image=self.render)
            else:
                self.render_paint = ImageTk.PhotoImage(img)
                self.canvas.create_image((self.paint_box.winfo_width() // 2, self.paint_box.winfo_height() // 2),
                                         image=self.render_paint)

    def set_picture(self, window):
        path = fd.askopenfilename()
        if not path:
            return -1
        if window == "image":
            self.load = Image.open(path)
            self.default_size = self.load.size
            self.render = ImageTk.PhotoImage(self.load)
            self.img.configure(image=self.render)
        else:
            self.load_paint = Image.open(path)
            self.render_paint = ImageTk.PhotoImage(self.load_paint)
            self.canvas.create_image((self.paint_box.winfo_width() // 2, self.paint_box.winfo_height() // 2),
                                     image=self.render_paint)

    def load_to_buffer(self):
        path = fd.askopenfilename()
        if not path:
            return -1
        self.bitmap_buffer = Image.open(path)

    def transfer_edit(self):
        text = self.edit1.get()
        self.edit2.delete(0, tk.END)
        self.edit2.insert(0, text)
        self.memo1.insert(0.1, f"Переписано из Edit1:\n{text}\n")

    def transfer_memo(self):
        text = self.memo1.get(0.1, tk.END)
        self.memo2.insert(tk.END, text)

    def clear(self, field):
        if field == "memo1":
            self.memo1.delete(0.1, tk.END)
        else:
            self.memo2.delete(0.1, tk.END)

    def draw_brush(self, size=-1):
        if size == -1:
            size = self.brush_size
        size = int(float(size))
        self.size_label["text"] = f"Size={size}"
        self.brush_canvas.delete("all")
        self.brush_size = size
        self.brush_canvas.create_oval(self.brush_canvas.winfo_width() // 2 - self.brush_size,
                                      self.brush_canvas.winfo_height() // 2 - self.brush_size,
                                      self.brush_canvas.winfo_width() // 2 + self.brush_size,
                                      self.brush_canvas.winfo_height() // 2 + self.brush_size,
                                      fill='#%02x%02x%02x' % (self.color["red"], self.color["green"], self.color["blue"]),
                                      outline='#%02x%02x%02x' % (self.color["red"], self.color["green"], self.color["blue"]))

    def change_red(self, color):
        color = int(float(color))
        self.red_label["text"] = f"Red={color}"
        self.color["red"] = color
        self.draw_brush()

    def change_green(self, color):
        color = int(float(color))
        self.green_label["text"] = f"Green={color}"
        self.color["green"] = color
        self.draw_brush()

    def change_blue(self, color):
        color = int(float(color))
        self.blue_label["text"] = f"Blue={color}"
        self.color["blue"] = color
        self.draw_brush()

    def test(self):
        image = self.bitmap_buffer
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        counter = 0
        max = 1
        # for x in range(width):
        #     for y in range(height):
        #         if counter == max:
        #             r = 0
        #             g = 0
        #             b = 0
        #             counter = 0
        #             max += 1
        #         else:
        #             r = pix[x, y][0]
        #             g = pix[x, y][1]
        #             b = pix[x, y][2]
        #             counter += 1
        #         draw.point((x, y), (r, g, b))
        for x in range(width):
            for y in range(height):
                rand = random.randint(-50, 50)
                r = pix[x, y][0] + rand
                g = pix[x, y][0] + rand
                b = pix[x, y][0] + rand
                if r < 0:
                    r = 0
                if g < 0:
                    g = 0
                if b < 0:
                    b = 0
                if r > 255:
                    r = 255
                if g > 255:
                    g = 255
                if b > 255:
                    b = 255
                sr = (r + g + b) // 3
                draw.point((x, y), (r, g, b))
        self.bitmap_buffer = image


if __name__ == "__main__":
    root = tk.Tk()
    MyApp(root).pack()
    root.mainloop()
