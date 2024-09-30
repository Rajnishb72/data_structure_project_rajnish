import tkinter as tk
from tkinter import messagebox, ttk, Menu
import heapq

class PriorityQueue:
    def __init__(self):
        self.items = []
        self.history = []  # To track actions for undo

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item, priority):
        heapq.heappush(self.items, (priority, item))
        self.history.append(("enqueue", item, priority))  # Track the enqueue action

    def dequeue(self):
        if self.is_empty():
            return None
        item = heapq.heappop(self.items)[1]
        self.history.append(("dequeue", item))  # Track the dequeue action
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self.items[0][1]

    def size(self):
        return len(self.items)

    def traverse(self):
        return sorted(self.items)  # Sort items by priority

    def undo(self):
        """Undo the last action."""
        if not self.history:
            return

        action = self.history.pop()
        if action[0] == "enqueue":
            # Remove the last enqueued item
            self.items.remove((action[2], action[1]))  # Remove item by value
            heapq.heapify(self.items)  # Restore heap property
        elif action[0] == "dequeue":
            self.enqueue(action[1], 0)  # Reinsert item with a low priority (0)

class PriorityQueueApp:
    def __init__(self, root):
        self.queue = PriorityQueue()
        self.root = root

        self.root.title("Priority Queue Operations")
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

        # Queue display frame
        self.create_queue_display()

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
        file_menu.add_command(label="Reset", command=self.reset_queue)
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
        title = tk.Label(title_frame, text="Priority Queue Operations", font=("Arial", 30, "bold"), bg='#2980b9', fg='white', padx=20)
        title.pack()

    def create_input_frame(self):
        """Creates the input frame for enqueue actions."""
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=20)

        self.item_entry = ttk.Entry(input_frame, width=20, font=("Arial", 16))
        self.item_entry.grid(row=0, column=0, padx=20)

        self.priority_entry = ttk.Entry(input_frame, width=20, font=("Arial", 16))
        self.priority_entry.grid(row=1, column=0, padx=20)

        enqueue_button = ttk.Button(input_frame, text="Enqueue", command=self.enqueue_item)
        enqueue_button.grid(row=0, column=1, padx=10)

        dequeue_button = ttk.Button(input_frame, text="Dequeue", command=self.dequeue_item)
        dequeue_button.grid(row=1, column=1, padx=10)

        peek_button = ttk.Button(input_frame, text="Peek", command=self.peek_item)
        peek_button.grid(row=2, column=0, columnspan=2, pady=10)

    def create_queue_display(self):
        """Creates the frame for displaying the priority queue."""
        display_frame = ttk.Frame(self.root)
        display_frame.pack(pady=20)

        self.queue_display = tk.Label(display_frame, text="Priority Queue: []", font=("Arial", 16), bg='#bdc3c7', fg='#2c3e50')
        self.queue_display.pack()

        # Canvas for visualization
        self.canvas = tk.Canvas(self.root, bg="#e0e0e0", height=200)
        self.canvas.pack(pady=10)

    def create_info_buttons(self):
        """Creates buttons for queue operations like Undo and Size."""
        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=20)

        undo_button = ttk.Button(info_frame, text="Undo", command=self.undo_action)
        undo_button.grid(row=0, column=0, padx=20)

        size_button = ttk.Button(info_frame, text="Size", command=self.show_size)
        size_button.grid(row=0, column=1, padx=20)

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

    def enqueue_item(self):
        item = self.item_entry.get()
        try:
            priority = int(self.priority_entry.get())
            if item:
                self.queue.enqueue(item, priority)
                self.item_entry.delete(0, tk.END)
                self.priority_entry.delete(0, tk.END)
                self.update_queue_display()
                self.set_status(f"Enqueued: {item} with priority {priority}")
            else:
                messagebox.showerror("Input Error", "Please enter an item to enqueue.")
        except ValueError:
            messagebox.showerror("Input Error", "Priority must be an integer.")

    def dequeue_item(self):
        item = self.queue.dequeue()
        if item is None:
            messagebox.showerror("Queue Error", "Priority Queue is empty.")
        else:
            messagebox.showinfo("Dequeued", f"Dequeued item: {item}")
            self.update_queue_display()

    def peek_item(self):
        item = self.queue.peek()
        if item is None:
            messagebox.showerror("Queue Error", "Priority Queue is empty.")
        else:
            messagebox.showinfo("Peek", f"Next item to dequeue: {item}")

    def show_size(self):
        size = self.queue.size()
        messagebox.showinfo("Queue Size", f"Priority Queue Size: {size}")

    def undo_action(self):
        """Undo the last action."""
        self.queue.undo()
        self.update_queue_display()
        self.set_status("Last action undone.")

    def update_queue_display(self):
        """Updates the priority queue display and visualization."""
        self.queue_display.config(text="Priority Queue: " + str(self.queue.traverse()))
        self.visualize_queue()

    def visualize_queue(self):
        """Visualizes the priority queue in the canvas."""
        self.canvas.delete("all")
        elements = self.queue.traverse()
        x = 10
        for priority, item in elements:
            self.canvas.create_rectangle(x, 50, x + 100, 100, fill="lightblue", outline="black")
            self.canvas.create_text(x + 50, 75, text=f"{item} (P: {priority})", font=("Arial", 12, "bold"))
            x += 110  # Spacing between elements

    def reset_queue(self):
        """Resets the priority queue to an empty state."""
        self.queue = PriorityQueue()
        self.update_queue_display()
        self.set_status("Priority queue has been reset.")

    def show_about_info(self):
        """Displays the about information."""
        messagebox.showinfo("About", "Priority Queue Operations Application v1.0\nBy Your Name")

    def exit_app(self):
        """Closes the application."""
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    pq_app = PriorityQueueApp(root)
    root.mainloop()
