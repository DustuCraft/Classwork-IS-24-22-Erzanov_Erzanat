import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from PIL import Image, ImageTk

DATA_FILE = "products.json"


# ------------------ Модель ------------------
class Product:
    def __init__(self, name, genre, price, image_path):
        self.name = name
        self.genre = genre
        self.price = price
        self.image_path = image_path

    def to_dict(self):
        return {
            "name": self.name,
            "genre": self.genre,
            "price": self.price,
            "image_path": self.image_path
        }


class Catalog:
    def __init__(self):
        self.items = []
        self.load()

    def add(self, product):
        self.items.append(product)
        self.save()

    def remove(self, name):
        self.items = [p for p in self.items if p.name != name]
        self.save()

    def search(self, query):
        query = query.lower()
        return [p for p in self.items if query in p.name.lower()]

    def save(self):
        data = [p.to_dict() for p in self.items]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                self.items.append(Product(
                    item["name"], item["genre"], item["price"], item.get("image_path", "")
                ))


# ------------------ UI ------------------
class App:
    def __init__(self, root):
        self.catalog = Catalog()
        self.loaded_image = None

        # ==== ОКНО ====
        root.title("Мини-каталог товаров")
        root.geometry("820x600")
        root.configure(bg="#000000")  # полностью черный фон

        self.fade_in(root)

        # ==== СТИЛИ ====
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton",
                        background="#2b2b2b",
                        foreground="white",
                        padding=8,
                        relief="flat",
                        font=("Segoe UI", 11))
        style.map("TButton",
                  background=[("active", "#3d3d3d")])

        # ----------------------------------------
        #               ЗАГОЛОВОК
        # ----------------------------------------
        title = tk.Label(root, text="Mini Catalog",
                         bg="#000", fg="#00b4ff",
                         font=("Segoe UI", 24, "bold"))
        title.pack(pady=10)

        # ----------------------------------------
        #                 ПОИСК
        # ----------------------------------------
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(root, textvariable=self.search_var, width=40,
                                font=("Segoe UI", 13),
                                bg="#111", fg="#fff", insertbackground="white",
                                relief="flat")
        search_entry.pack(pady=5)
        search_entry.bind("<KeyRelease>", self.update_list)

        # ----------------------------------------
        #     ГЛАВНЫЙ БЛОК (СПИСОК + КАРТИНКА)
        # ----------------------------------------
        main_frame = tk.Frame(root, bg="#000")
        main_frame.pack(pady=10)

        # список товаров
        left_frame = tk.Frame(main_frame, bg="#000")
        left_frame.grid(row=0, column=0, padx=15)

        self.listbox = tk.Listbox(left_frame, width=45, height=18,
                                  bg="#111", fg="#fff",
                                  font=("Segoe UI", 12),
                                  highlightthickness=0, bd=0,
                                  selectbackground="#00b4ff")
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.show_image)

        # картинка
        right_frame = tk.Frame(main_frame, bg="#000")
        right_frame.grid(row=0, column=1, padx=20)

        self.image_label = tk.Label(right_frame, bg="#000")
        self.image_label.pack()

        # ----------------------------------------
        #                 ФОРМА
        # ----------------------------------------
        form_frame = tk.Frame(root, bg="#000")
        form_frame.pack(pady=10)

        def add_label(text, row):
            return tk.Label(form_frame, text=text,
                            bg="#000", fg="#fff",
                            font=("Segoe UI", 11)).grid(row=row, column=0, sticky="e", pady=3)

        add_label("Название:", 0)
        add_label("Жанр:", 1)
        add_label("Цена:", 2)
        add_label("Картинка:", 3)

        self.name_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.image_path_var = tk.StringVar()

        def entry(var, row):
            return tk.Entry(form_frame, textvariable=var,
                            bg="#111", fg="#fff", insertbackground="white",
                            relief="flat").grid(row=row, column=1, pady=3, padx=5)

        entry(self.name_var, 0)
        entry(self.genre_var, 1)
        entry(self.price_var, 2)

        tk.Entry(form_frame, textvariable=self.image_path_var,
                 width=25, bg="#111", fg="#fff",
                 relief="flat", insertbackground="white").grid(row=3, column=1)

        ttk.Button(form_frame, text="Файл", command=self.pick_image).grid(row=3, column=2, padx=5)

        # ----------------------------------------
        #                 КНОПКИ
        # ----------------------------------------
        btn_frame = tk.Frame(root, bg="#000")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Добавить", width=18,
                   command=self.add_product).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Удалить", width=18,
                   command=self.remove_product).grid(row=0, column=1, padx=10)

        self.update_list()

    # ------------------ АНИМАЦИЯ ОКНА ------------------
    def fade_in(self, win):
        alpha = win.attributes("-alpha")
        if alpha < 1:
            alpha += 0.05
            win.attributes("-alpha", alpha)
            win.after(20, lambda: self.fade_in(win))

    # ------------------ Выбор файла ------------------
    def pick_image(self):
        filename = filedialog.askopenfilename(
            title="Выберите картинку",
            filetypes=[("Images", "*.jpg *.png *.jpeg *.gif *.bmp")]
        )
        if filename:
            self.image_path_var.set(filename)

    # ------------------ Показ картинки ------------------
    def show_image(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            return

        name = self.listbox.get(selection[0]).split("|")[0].strip()
        item = next((p for p in self.catalog.items if p.name == name), None)

        if not item or not item.image_path or not os.path.exists(item.image_path):
            self.image_label.config(image="", text="Нет изображения", fg="white")
            return

        img = Image.open(item.image_path)
        img = img.resize((260, 260), Image.LANCZOS)
        self.loaded_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.loaded_image)

    # ------------------ Обновление списка ------------------
    def update_list(self, event=None):
        query = self.search_var.get()
        products = self.catalog.search(query)

        self.listbox.delete(0, tk.END)
        for p in products:
            self.listbox.insert(tk.END, f"{p.name} | {p.genre} | {p.price} ₸")

    # ------------------ Добавление ------------------
    def add_product(self):
        name = self.name_var.get().strip()
        genre = self.genre_var.get().strip()
        price = self.price_var.get().strip()
        image_path = self.image_path_var.get().strip()

        if not name or not genre or not price:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            float(price)
        except:
            messagebox.showerror("Ошибка", "Цена должна быть числом!")
            return

        self.catalog.add(Product(name, genre, price, image_path))
        self.update_list()

        self.name_var.set("")
        self.genre_var.set("")
        self.price_var.set("")
        self.image_path_var.set("")

    # ------------------ Удаление ------------------
    def remove_product(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showerror("Ошибка", "Выберите товар!")
            return

        name = self.listbox.get(sel[0]).split("|")[0].strip()
        self.catalog.remove(name)
        self.update_list()
        self.image_label.config(image="", text="")


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-alpha", 0)  # старт с прозрачности
    App(root)
    root.mainloop()