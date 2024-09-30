import tkinter as tk
from tkinter import messagebox, ttk, Menu
import json
import os

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.history = []  # To track actions for undo

    def is_empty(self):
        return self.head is None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.history.append(("insert_beginning", data))  # Track the insert action

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.history.append(("insert_end", data))  # Track the insert action
            return
        self.tail.next = new_node
        self.tail = new_node
        self.history.append(("insert_end", data))  # Track the insert action

    def delete_at_beginning(self):
        if self.is_empty():
            return None
        deleted_node = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.history.append(("delete_beginning", deleted_node.data))  # Track the delete action
        return deleted_node.data

    def delete_at_end(self):
        if self.is_empty():
            return None
        if self.head.next is None:
            deleted_node = self.head
            self.head = None
            self.tail = None
            self.history.append(("delete_end", deleted_node.data))  # Track the delete action
            return deleted_node.data
        current = self.head
        while current.next and current.next.next:
            current = current.next
        deleted_node = current.next
        current.next = None
        self.tail = current
        self.history.append(("delete_end", deleted_node.data))  # Track the delete action
        return deleted_node.data

    def traverse(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def undo(self):
        """Undo the last action."""
        if not self.history:
            return
        
        action, item = self.history.pop()
        if action == "insert_beginning":
            self.delete_at_beginning()
        elif action == "insert_end":
            self.delete_at_end()
        elif action == "delete_beginning":
            self.insert_at_beginning(item)
        elif action == "delete_end":
            self.insert_at_end(item)

class LinkedListApp:
    def __init__(self, root):
        self.linked_list = LinkedList()
        self.root = root
        self.root.title("Linked List Operations Application")
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

        # Linked list display frame
        self.create_linked_list_display()

        # Info buttons frame
        self.create_info_buttons()

        # Exit button
        self.create_exit_button()

        # Status bar
        self.create_status_bar()

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
        file_menu.add_command(label="Reset", command=self.reset_list)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)

        # Adding Help Menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_info)

    def create_title_label(self):
        """Creates the title label."""
        title_frame = tk.Frame(self.root, bg='#2980b9', bd=5, relief=tk.RAISED)
        title_frame.pack(pady=10, fill=tk.X)
        title = tk.Label(title_frame, text="Linked List Operations", font=("Arial", 30, "bold"), bg='#2980b9', fg='white', padx=20)
        title.pack()

    def create_input_frame(self):
        """Creates the input frame for insert actions."""
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=20)

        self.entry = ttk.Entry(input_frame, width=20, font=("Arial", 16))
        self.entry.grid(row=0, column=0, padx=20)

        insert_begin_button = ttk.Button(input_frame, text="Insert at Beginning", command=self.insert_at_beginning)
        insert_begin_button.grid(row=0, column=1, padx=10)

        insert_end_button = ttk.Button(input_frame, text="Insert at End", command=self.insert_at_end)
        insert_end_button.grid(row=0, column=2, padx=10)

    def create_linked_list_display(self):
        """Creates the frame for displaying the linked list."""
        display_frame = ttk.Frame(self.root)
        display_frame.pack(pady=20)

        self.linked_list_display = tk.Label(display_frame, text="Linked List: []", font=("Arial", 16), bg='#bdc3c7', fg='#2c3e50')
        self.linked_list_display.pack()

        # Canvas for visualization
        self.canvas = tk.Canvas(self.root, bg="#e0e0e0", height=200)
        self.canvas.pack(pady=10)

    def create_info_buttons(self):
        """Creates buttons for linked list operations like Delete and Undo."""
        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=20)

        delete_begin_button = ttk.Button(info_frame, text="Delete at Beginning", command=self.delete_at_beginning)
        delete_begin_button.grid(row=0, column=0, padx=20)

        delete_end_button = ttk.Button(info_frame, text="Delete at End", command=self.delete_at_end)
        delete_end_button.grid(row=0, column=1, padx=20)

        undo_button = ttk.Button(info_frame, text="Undo", command=self.undo_action)
        undo_button.grid(row=0, column=2, padx=20)

    def create_exit_button(self):
        """Creates the exit button."""
        exit_button = ttk.Button(self.root, text="Exit", command=self.exit_app)
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

    def insert_at_beginning(self):
        data = self.entry.get()
        if data:
            self.linked_list.insert_at_beginning(data)
            self.entry.delete(0, tk.END)
            self.update_linked_list_display()
            self.set_status(f"Inserted at beginning: {data}")
        else:
            messagebox.showerror("Input Error", "Please enter data to insert.")

    def insert_at_end(self):
        data = self.entry.get()
        if data:
            self.linked_list.insert_at_end(data)
            self.entry.delete(0, tk.END)
            self.update_linked_list_display()
            self.set_status(f"Inserted at end: {data}")
        else:
            messagebox.showerror("Input Error", "Please enter data to insert.")

    def delete_at_beginning(self):
        data = self.linked_list.delete_at_beginning()
        if data is not None:
            messagebox.showinfo("Deleted Data", f"Deleted from beginning: {data}")
            self.update_linked_list_display()
            self.set_status(f"Deleted from beginning: {data}")
        else:
            messagebox.showerror("Error", "List is empty.")

    def delete_at_end(self):
        data = self.linked_list.delete_at_end()
        if data is not None:
            messagebox.showinfo("Deleted Data", f"Deleted from end: {data}")
            self.update_linked_list_display()
            self.set_status(f"Deleted from end: {data}")
        else:
            messagebox.showerror("Error", "List is empty.")

    def update_linked_list_display(self):
        """Updates the linked list display and visualization."""
        self.linked_list_display.config(text="Linked List: " + str(self.linked_list.traverse()))
        self.visualize_linked_list()

    def visualize_linked_list(self):
        """Visualizes the linked list in the canvas."""
        self.canvas.delete("all")
        elements = self.linked_list.traverse()
        x = 10
        for element in elements:
            self.canvas.create_rectangle(x, 50, x + 60, 100, fill="lightblue", outline="black")
            self.canvas.create_text(x + 30, 75, text=element, font=("Arial", 12, "bold"))
            x += 70  # Spacing between elements

    def reset_list(self):
        """Resets the linked list to an empty state."""
        self.linked_list = LinkedList()
        self.update_linked_list_display()
        self.set_status("Linked list has been reset.")

    def show_about_info(self):
        """Displays the about information."""
        messagebox.showinfo("About", "Linked List Operations Application v1.0\nBy Your Name")

    def exit_app(self):
        """Closes the application."""
        self.root.destroy()

    def undo_action(self):
        """Undo the last action."""
        self.linked_list.undo()
        self.update_linked_list_display()
        self.set_status("Last action undone.")

