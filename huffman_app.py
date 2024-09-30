import tkinter as tk
from tkinter import messagebox, ttk, Menu
import heapq
from collections import defaultdict

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanApp:
    def __init__(self):
        self.huffman_tree = None
        self.codes = {}

    def calculate_frequencies(self, text):
        frequency = defaultdict(int)
        for char in text:
            frequency[char] += 1
        return frequency

    def build_huffman_tree(self, text):
        frequency = self.calculate_frequencies(text)
        heap = [Node(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)

        self.huffman_tree = heap[0]
        self.build_codes(self.huffman_tree, "")

    def build_codes(self, node, current_code):
        if node:
            if node.char is not None:
                self.codes[node.char] = current_code
            self.build_codes(node.left, current_code + "0")
            self.build_codes(node.right, current_code + "1")

    def encode(self, text):
        return ''.join(self.codes[char] for char in text)

    def decode(self, encoded_text):
        current_node = self.huffman_tree
        decoded_output = ""
        for bit in encoded_text:
            current_node = current_node.left if bit == '0' else current_node.right
            if current_node.char:
                decoded_output += current_node.char
                current_node = self.huffman_tree
        return decoded_output

class HuffmanCodingApp:
    def __init__(self, root):
        self.huffman_coding = HuffmanCoding()
        self.root = root
        self.root.title("Huffman Coding Application")
        self.root.geometry("750x500")
        self.center_window(750, 500)
        self.root.configure(bg='#bdc3c7')

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 14), padding=10)
        self.style.configure("TFrame", background='#A9A9A9')

        # Menu bar
        self.create_menu_bar()

        # Title
        self.create_title_label()

        # Input frame
        self.create_input_frame()

        # Output display frame
        self.create_output_display()

        # Exit button
        self.create_exit_button()

        # Status bar
        self.create_status_bar()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_menu_bar(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Adding File Menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reset", command=self.reset_app)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)

        # Adding Help Menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_info)

    def create_title_label(self):
        title_frame = tk.Frame(self.root, bg='#2980b9', bd=5, relief=tk.RAISED)
        title_frame.pack(pady=10, fill=tk.X)
        title = tk.Label(title_frame, text="Huffman Coding Application", font=("Arial", 30, "bold"), bg='#2980b9', fg='white', padx=20)
        title.pack()

    def create_input_frame(self):
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=20)

        self.input_text = tk.Text(input_frame, width=50, height=5, font=("Arial", 12))
        self.input_text.grid(row=0, column=0, padx=20)

        encode_button = ttk.Button(input_frame, text="Encode", command=self.encode_text)
        encode_button.grid(row=0, column=1, padx=10)

        decode_button = ttk.Button(input_frame, text="Decode", command=self.decode_text)
        decode_button.grid(row=0, column=2, padx=10)

    def create_output_display(self):
        output_frame = ttk.Frame(self.root)
        output_frame.pack(pady=20)

        self.output_label = tk.Label(output_frame, text="Output: ", font=("Arial", 16), bg='#bdc3c7', fg='#2c3e50')
        self.output_label.pack()

        self.output_display = tk.Label(output_frame, text="", font=("Arial", 14), bg='#bdc3c7', fg='black')
        self.output_display.pack()

    def create_exit_button(self):
        exit_button = ttk.Button(self.root, text="Exit", command=self.exit_app)
        exit_button.pack(pady=20)

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 12), bg='#16a085', fg='white')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.set_status("Ready")

    def set_status(self, message):
        self.status_var.set(message)

    def encode_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if text:
            self.huffman_coding.build_huffman_tree(text)
            encoded_text = self.huffman_coding.encode(text)
            self.output_display.config(text=encoded_text)
            self.set_status("Text encoded successfully.")
        else:
            messagebox.showerror("Input Error", "Please enter text to encode.")

    def decode_text(self):
        encoded_text = self.output_display.cget("text").strip()
        if encoded_text:
            decoded_text = self.huffman_coding.decode(encoded_text)
            self.output_display.config(text=decoded_text)
            self.set_status("Text decoded successfully.")
        else:
            messagebox.showerror("Input Error", "Please encode text first.")

    def reset_app(self):
        self.input_text.delete("1.0", tk.END)
        self.output_display.config(text="")
        self.huffman_coding = HuffmanCoding()
        self.set_status("Application has been reset.")

    def show_about_info(self):
        messagebox.showinfo("About", "Huffman Coding Application v1.0\nBy Your Name")

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
