import tkinter as tk
from tkinter import messagebox, ttk


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.history = []  # Track actions for undo

    def is_empty(self):
        return self.head is None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.history.append(("insert", data))  # Track the action

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.history.append(("insert", data))  # Track the action

    def delete_at_beginning(self):
        if self.is_empty():
            return None
        deleted_node = self.head
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.history.append(("delete", deleted_node.data))  # Track the action
        return deleted_node.data

    def delete_at_end(self):
        if self.is_empty():
            return None
        deleted_node = self.tail
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.history.append(("delete", deleted_node.data))  # Track the action
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
        if action == "insert":
            self.delete_node(item)
        elif action == "delete":
            self.insert_at_end(item)

    def delete_node(self, data):
        """Delete a node by value."""
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:  # Adjust head if necessary
                    self.head = current.next
                if current == self.tail:  # Adjust tail if necessary
                    self.tail = current.prev
                return
            current = current.next


class DoublyLinkedListApp:
    def __init__(self, root, main_app=None):  # Accept main_app as an optional parameter
        self.dll = DoublyLinkedList()
        self.root = root
        self.main_app = main_app  # Store the reference to the main app if needed
        self.root.title("Doubly Linked List Operations")
        self.root.geometry("750x500")
        self.center_window(750, 500)
        self.root.configure(bg='#bdc3c7')


        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 14), padding=10, relief=tk.RAISED)
        self.style.configure("TFrame", background='#A9A9A9')

        # Title
        self.create_title_label()

        # Input frame
        self.create_input_frame()

        # DLL display
        self.create_dll_display()

        # Delete buttons
        self.create_delete_buttons()

        # Undo and Reset buttons
        self.create_undo_reset_buttons()

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

    def create_title_label(self):
        """Creates the title label."""
        title_frame = tk.Frame(self.root, bg='#2980b9', bd=5, relief=tk.RAISED)
        title_frame.pack(pady=10, fill=tk.X)
        title = tk.Label(title_frame, text="Doubly Linked List Operations", font=("Arial", 30, "bold"), bg='#2980b9', fg='white', padx=20)
        title.pack()

    def create_input_frame(self):
        """Creates the input frame for insert actions."""
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=20)

        self.entry = ttk.Entry(input_frame, width=20, font=("Arial", 16))
        self.entry.grid(row=0, column=0, padx=20)

        insert_beg_button = ttk.Button(input_frame, text="Insert at Beginning", command=self.insert_at_beginning)
        insert_beg_button.grid(row=0, column=1, padx=10)

        insert_end_button = ttk.Button(input_frame, text="Insert at End", command=self.insert_at_end)
        insert_end_button.grid(row=0, column=2, padx=10)

    def create_dll_display(self):
        """Creates the frame for displaying the doubly linked list."""
        display_frame = ttk.Frame(self.root)
        display_frame.pack(pady=20)

        self.dll_display = tk.Label(display_frame, text="Doubly Linked List: []", font=("Arial", 16), bg='#bdc3c7', fg='#2c3e50')
        self.dll_display.pack()

    def create_delete_buttons(self):
        """Creates buttons for delete operations."""
        delete_frame = ttk.Frame(self.root)
        delete_frame.pack(pady=20)

        delete_beg_button = ttk.Button(delete_frame, text="Delete at Beginning", command=self.delete_at_beginning)
        delete_beg_button.grid(row=0, column=0, padx=20)

        delete_end_button = ttk.Button(delete_frame, text="Delete at End", command=self.delete_at_end)
        delete_end_button.grid(row=0, column=1, padx=20)

    def create_undo_reset_buttons(self):
        """Creates buttons for undo and reset operations."""
        undo_reset_frame = ttk.Frame(self.root)
        undo_reset_frame.pack(pady=20)

        undo_button = ttk.Button(undo_reset_frame, text="Undo", command=self.undo_action)
        undo_button.grid(row=0, column=0, padx=20)

        reset_button = ttk.Button(undo_reset_frame, text="Reset", command=self.reset_list)
        reset_button.grid(row=0, column=1, padx=20)

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
        item = self.entry.get()
        if item:
            self.dll.insert_at_beginning(item)
            self.update_dll_display()
            self.set_status(f"Inserted at beginning: {item}")
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter an item.")

    def insert_at_end(self):
        item = self.entry.get()
        if item:
            self.dll.insert_at_end(item)
            self.update_dll_display()
            self.set_status(f"Inserted at end: {item}")
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter an item.")

    def delete_at_beginning(self):
        deleted_item = self.dll.delete_at_beginning()
        if deleted_item is not None:
            self.update_dll_display()
            self.set_status(f"Deleted item: {deleted_item}")
            messagebox.showinfo("Deleted", f"Deleted item: {deleted_item}")
        else:
            messagebox.showwarning("Deletion Error", "The list is empty.")

    def delete_at_end(self):
        deleted_item = self.dll.delete_at_end()
        if deleted_item is not None:
            self.update_dll_display()
            self.set_status(f"Deleted item: {deleted_item}")
            messagebox.showinfo("Deleted", f"Deleted item: {deleted_item}")
        else:
            messagebox.showwarning("Deletion Error", "The list is empty.")

    def undo_action(self):
        """Undo the last insertion or deletion."""
        self.dll.undo()
        self.update_dll_display()
        self.set_status("Last action undone.")

    def reset_list(self):
        """Clear the entire list."""
        self.dll = DoublyLinkedList()  # Reset the DLL
        self.update_dll_display()
        self.set_status("List has been reset.")

    def update_dll_display(self):
        """Update the display of the doubly linked list."""
        self.dll_display.config(text="Doubly Linked List: " + str(self.dll.traverse()))

    def exit_app(self):
        """Exit the application."""
        self.root.quit()


# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    app = DoublyLinkedListApp(root)
    root.mainloop()
