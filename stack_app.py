import tkinter as tk
from tkinter import messagebox, ttk, Menu
import json
import os

class Stack:
    def __init__(self):
        self.items = []
        self.history = []  # To track actions for undo

    def is_empty(self):
        return len(self.items) == 0

    def push(self, data):
        self.items.append(data)
        self.history.append(("push", data))  # Track the push action

    def pop(self):
        if self.is_empty():
            return None
        popped_item = self.items.pop()
        self.history.append(("pop", popped_item))  # Track the pop action
        return popped_item

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def size(self):
        return len(self.items)

    def undo(self):
        """Undo the last action."""
        if self.history:
            action, item = self.history.pop()
            if action == "push":
                self.items.pop()  # Remove the last pushed item
            elif action == "pop":
                self.items.append(item)  # Add back the popped item

    def load_from_json(self, data):
        """Load stack items from JSON data."""
        self.items = data.get("items", [])
        self.history = []  # Reset history

    def save_to_json(self):
        """Save stack items to JSON format."""
        return json.dumps({"items": self.items})

    def __str__(self):
        return str(self.items)


class StackApp:
    def __init__(self, root, main_root=None):
        self.stack = Stack()
        self.root = root
        self.main_root = main_root  # Optional main window reference
        self.root.title("Stack Operations Application")
        self.root.geometry("750x500")
        self.center_window(750, 500)
        self.root.configure(bg='#bdc3c7')  # Gray background color

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 14), padding=10, relief=tk.RAISED)
        self.style.configure("TFrame", background='#A9A9A9')

        # Menu bar
        self.create_menu_bar()

        # Title
        self.create_title_label()

        # Input frame
        self.create_input_frame()

        # Stack display frame
        self.create_stack_display()

        # Info buttons frame
        self.create_info_buttons()

        # Exit button
        self.create_exit_button()

        # Status bar
        self.create_status_bar()

        # Load stack from file
        self.load_stack()

        # Bind keyboard shortcuts
        self.bind_shortcuts()

    def center_window(self, width, height):
        """Center the application window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_menu_bar(self):
        """Adds a menu bar to the application."""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Adding File Menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reset", command=self.reset_stack)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_stack_app)

        # Adding Help Menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_info)

    def create_title_label(self):
        """Creates the title label."""
        title_frame = tk.Frame(self.root, bg='#2980b9', bd=5, relief=tk.RAISED)
        title_frame.pack(pady=10, fill=tk.X)
        title = tk.Label(title_frame, text="Stack Operations", font=("Arial", 30, "bold"), bg='#2980b9', fg='white', padx=20)
        title.pack()

    def create_input_frame(self):
        """Creates the input frame for push and pop actions."""
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=20)

        self.entry = ttk.Entry(input_frame, width=20, font=("Arial", 16))
        self.entry.grid(row=0, column=0, padx=20)

        push_button = ttk.Button(input_frame, text="Push", command=self.push_item)
        push_button.grid(row=0, column=1, padx=10)

        pop_button = ttk.Button(input_frame, text="Pop", command=self.pop_item)
        pop_button.grid(row=0, column=2, padx=10)

    def create_stack_display(self):
        """Creates the frame for displaying the stack."""
        display_frame = ttk.Frame(self.root)
        display_frame.pack(pady=20)

        self.stack_display = tk.Label(display_frame, text="Stack: []", font=("Arial", 16), bg='#bdc3c7', fg='#2c3e50')
        self.stack_display.pack()

        # Graphical visualization of the stack
        self.stack_visual_frame = ttk.Frame(self.root)
        self.stack_visual_frame.pack(pady=10)

    def create_info_buttons(self):
        """Creates buttons for stack operations like Peek and Size."""
        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=20)

        peek_button = ttk.Button(info_frame, text="Peek", command=self.peek_item)
        peek_button.grid(row=0, column=0, padx=20)

        size_button = ttk.Button(info_frame, text="Size", command=self.get_size)
        size_button.grid(row=0, column=1, padx=20)

        undo_button = ttk.Button(info_frame, text="Undo", command=self.undo_action)
        undo_button.grid(row=0, column=2, padx=20)

    def create_exit_button(self):
        """Creates the exit button."""
        exit_button = ttk.Button(self.root, text="Exit", command=self.exit_stack_app)
        exit_button.pack(pady=20)

    def create_status_bar(self):
        """Creates a status bar to show live updates."""
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 12), bg='#16a085', fg='white')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.set_status("Ready")

    def set_status(self, message):
        """Updates the status bar with a message."""
        self.status_var.set(message)

    def push_item(self):
        """Handles the push operation."""
        item = self.entry.get()
        if item and len(item) <= 20:
            self.stack.push(item)
            self.update_stack_display()
            self.entry.delete(0, tk.END)
            self.set_status(f"Pushed: {item}")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid item (max 20 characters).")

    def pop_item(self):
        """Handles the pop operation."""
        popped_item = self.stack.pop()
        if popped_item is not None:
            messagebox.showinfo("Popped", f"Popped item: {popped_item}")
            self.update_stack_display()
            self.set_status(f"Popped: {popped_item}")
        else:
            messagebox.showerror("Stack Error", "Stack is empty.")

    def peek_item(self):
        """Displays the top item of the stack."""
        peek_item = self.stack.peek()
        if peek_item is not None:
            messagebox.showinfo("Peek", f"Top item: {peek_item}")
            self.set_status(f"Peeked: {peek_item}")
        else:
            messagebox.showerror("Stack Error", "Stack is empty.")

    def get_size(self):
        """Displays the size of the stack."""
        size = self.stack.size()
        messagebox.showinfo("Size", f"Stack size: {size}")
        self.set_status(f"Stack size: {size}")

    def update_stack_display(self):
        """Updates the stack display and visualization."""
        self.stack_display.config(text="Stack: " + str(self.stack))

        # Clear the previous stack visualization
        for widget in self.stack_visual_frame.winfo_children():
            widget.destroy()

        # Visualize the stack items
        for item in reversed(self.stack.items):  # Stack visualized from top to bottom
            item_label = tk.Label(self.stack_visual_frame, text=item, font=("Arial", 16), bg='#bdc3c7', fg='#2c3e50', padx=10, pady=5, relief=tk.SOLID)
            item_label.pack(pady=5)

    def reset_stack(self):
        """Resets the stack to an empty state."""
        self.stack = Stack()
        self.update_stack_display()
        self.set_status("Stack has been reset.")

    def show_about_info(self):
        """Displays the about information."""
        messagebox.showinfo("About", "Stack Operations Application v1.0\nBy Rajnish Bhardwaj")

    def exit_stack_app(self):
        """Closes the application."""
        self.save_stack()  # Save stack before exiting
        self.root.destroy()
        if self.main_root:
            self.main_root.deiconify()  # Show the main window if available

    def load_stack(self):
        """Load stack items from a file if it exists."""
        if os.path.exists("stack_data.json"):
            with open("stack_data.json", "r") as f:
                data = json.load(f)
                self.stack.load_from_json(data)
                self.update_stack_display()

    def save_stack(self):
        """Save stack items to a file."""
        with open("stack_data.json", "w") as f:
            f.write(self.stack.save_to_json())

    def undo_action(self):
        """Undo the last action."""
        self.stack.undo()
        self.update_stack_display()
        self.set_status("Last action undone.")

    def bind_shortcuts(self):
        """Bind keyboard shortcuts for stack operations."""
        self.root.bind('<Control-p>', lambda event: self.push_item())
        self.root.bind('<Control-o>', lambda event: self.pop_item())
        self.root.bind('<Control-u>', lambda event: self.undo_action())
        self.root.bind('<Control-e>', lambda event: self.exit_stack_app())

