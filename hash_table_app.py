import tkinter as tk
from tkinter import messagebox

class HashTableApp:
    def __init__(self, root, size):
        self.root = root
        self.size = size
        self.hash_set = [None] * size
        self.root.geometry("1200x700")
        self.root.configure(bg="#D3D3D3")
        root.title("Hash Set GUI")

        self.header_label = tk.Label(root, text="RAJNISH BHARDWAJ S073", font=("Arial", 30, "bold"),
                                      bg="#D3D3D3", fg="black")
        self.header_label.pack(pady=40)

        self.hash_set_frame = tk.Frame(root, bg="#D3D3D3")
        self.hash_set_frame.pack(pady=15)
        self.hash_set_labels = [tk.Label(self.hash_set_frame, text=f"{i} :", font=("Arial", 20),
                                          bg="#D3D3D3", fg="black") for i in range(self.size)]
        for i, label in enumerate(self.hash_set_labels):
            label.grid(row=i, column=0, sticky=tk.W, padx=40)

        self.container = tk.Frame(root, bg="#A9A9A9")
        self.container.pack(pady=40)

        self.entry = tk.Entry(self.container, font=("Arial", 20), width=18)
        self.entry.grid(row=0, column=0, padx=15, pady=15)

        self.button_frame = tk.Frame(self.container, bg="#A9A9A9")
        self.button_frame.grid(row=1, column=0, padx=10, pady=10)

        button_style = {
            "font": ("Arial", 18),
            "bg": "#696969",
            "fg": "white",
            "width": 10
        }

        self.contains_button = tk.Button(self.button_frame, text="contains()", **button_style,
                                          command=self.contains)
        self.contains_button.grid(row=0, column=0, padx=15)

        self.add_button = tk.Button(self.button_frame, text="add()", **button_style,
                                    command=self.add)
        self.add_button.grid(row=0, column=1, padx=15)

        self.remove_button = tk.Button(self.button_frame, text="remove()", **button_style,
                                       command=self.remove)
        self.remove_button.grid(row=0, column=2, padx=15)

        self.size_button = tk.Button(self.button_frame, text="size()", **button_style,
                                     command=self.size_func)
        self.size_button.grid(row=0, column=3, padx=15)

    def ascii_hash_function(self, key):
        ascii_sum = sum(ord(char) for char in key)
        return ascii_sum % self.size

    def contains(self):
        key = self.entry.get()
        index = self.ascii_hash_function(key)
        if self.hash_set[index] is not None and key in self.hash_set[index]:
            messagebox.showinfo("Result", f"'{key}' is in the hash set.")
        else:
            messagebox.showinfo("Result", f"'{key}' is NOT in the hash set.")

    def add(self):
        key = self.entry.get()
        if not key:
            messagebox.showwarning("Warning", "Please enter a value to add.")
            return
        index = self.ascii_hash_function(key)
        if self.hash_set[index] is None:
            self.hash_set[index] = []
        if key not in self.hash_set[index]:
            self.hash_set[index].append(key)
            self.update_display()
        else:
            messagebox.showwarning("Warning", f"'{key}' already exists.")

    def remove(self):
        key = self.entry.get()
        if not key:
            messagebox.showwarning("Warning", "Please enter a value to remove.")
            return
        index = self.ascii_hash_function(key)
        if self.hash_set[index] and key in self.hash_set[index]:
            self.hash_set[index].remove(key)
            if len(self.hash_set[index]) == 0:
                self.hash_set[index] = None
            self.update_display()
        else:
            messagebox.showwarning("Warning", f"'{key}' is not in the hash set.")

    def size_func(self):
        size = sum(len(bucket) for bucket in self.hash_set if bucket is not None)
        messagebox.showinfo("Size", f"The size of the hash set is: {size}")

    def update_display(self):
        for i, label in enumerate(self.hash_set_labels):
            values = ", ".join(self.hash_set[i]) if self.hash_set[i] else ""
            label.config(text=f"{i} : {values}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HashTableApp(root, size=10)
    root.mainloop()
