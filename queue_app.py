import tkinter as tk
from tkinter import messagebox, ttk, Menu

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("Queue is empty, cannot dequeue.")

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        else:
            raise IndexError("Queue is empty, cannot peek.")

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class QueueApp:
    def __init__(self, root, main_app):
        self.queue = Queue()
        self.root = root
        self.main_app = main_app  # Reference to the main application
        self.root.title("Queue Operations Application")
        self.root.geometry("750x500")
        self.center_window(750, 500)
        self.root.configure(bg='#2c3e50')  # Set background color

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 14), padding=10, relief=tk.RAISED)
        self.style.configure("TFrame", background='#A9A9A9')  # Frame background color

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
        file_menu.add_command(label="Exit", command=self.exit_queue_app)

        # Adding Help Menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_info)

    def create_title_label(self):
        """Creates the title label."""
        title_frame = tk.Frame(self.root, bg='#2980b9', bd=5, relief=tk.RAISED)
        title_frame.pack(pady=10, fill=tk.X)
        title = tk.Label(title_frame, text="Queue Operations", font=("Arial", 30, "bold"), bg='#2980b9', fg='white', padx=20)
        title.pack()

    def create_input_frame(self):
        """Creates the input frame for enqueue and dequeue actions."""
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=20)

        self.entry = ttk.Entry(input_frame, width=20, font=("Arial", 16))
        self.entry.grid(row=0, column=0, padx=20)

        enqueue_button = ttk.Button(input_frame, text="Enqueue", command=self.enqueue_item)
        enqueue_button.grid(row=0, column=1, padx=10)

        dequeue_button = ttk.Button(input_frame, text="Dequeue", command=self.dequeue_item)
        dequeue_button.grid(row=0, column=2, padx=10)

    def create_queue_display(self):
        """Creates the frame for displaying the queue."""
        display_frame = ttk.Frame(self.root)
        display_frame.pack(pady=20)

        self.queue_display = tk.Label(display_frame, text="Queue: []", font=("Arial", 16), bg='#000000', fg='#ecf0f1')
        self.queue_display.pack()

        # Graphical visualization of the queue
        self.queue_visual_frame = ttk.Frame(self.root)
        self.queue_visual_frame.pack(pady=10)

    def create_info_buttons(self):
        """Creates buttons for queue operations like Peek and Size."""
        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=20)

        peek_button = ttk.Button(info_frame, text="Peek", command=self.peek_item)
        peek_button.grid(row=0, column=0, padx=20)

        size_button = ttk.Button(info_frame, text="Size", command=self.get_size)
        size_button.grid(row=0, column=1, padx=20)

    def create_exit_button(self):
        """Creates the exit button."""
        exit_button = ttk.Button(self.root, text="Exit", command=self.exit_queue_app)
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
        """Handles the enqueue operation."""
        item = self.entry.get()
        if item:
            self.queue.enqueue(item)
            self.update_queue_display()
            self.entry.delete(0, tk.END)
            self.set_status(f"Enqueued: {item}")
        else:
            messagebox.showwarning("Input Error", "Please enter an item to enqueue.")

    def dequeue_item(self):
        """Handles the dequeue operation."""
        try:
            dequeued_item = self.queue.dequeue()
            messagebox.showinfo("Dequeued", f"Dequeued item: {dequeued_item}")
            self.update_queue_display()
            self.set_status(f"Dequeued: {dequeued_item}")
        except IndexError as e:
            messagebox.showerror("Queue Error", str(e))
            self.set_status("Queue is empty, cannot dequeue.")

    def peek_item(self):
        """Displays the front item of the queue."""
        try:
            peek_item = self.queue.peek()
            messagebox.showinfo("Peek", f"Front item: {peek_item}")
            self.set_status(f"Peeked: {peek_item}")
        except IndexError as e:
            messagebox.showerror("Queue Error", str(e))
            self.set_status("Queue is empty, cannot peek.")

    def get_size(self):
        """Displays the size of the queue."""
        size = self.queue.size()
        messagebox.showinfo("Size", f"Queue size: {size}")
        self.set_status(f"Queue size: {size}")

    def update_queue_display(self):
        """Updates the queue display and visualization."""
        self.queue_display.config(text="Queue: " + str(self.queue))

        # Clear the previous queue visualization
        for widget in self.queue_visual_frame.winfo_children():
            widget.destroy()

        # Visualize the queue items
        for item in self.queue.items:
            item_label = tk.Label(self.queue_visual_frame, text=item, font=("Arial", 16), bg='#000000', fg='#ecf0f1', padx=10, pady=5, relief=tk.SOLID)
            item_label.pack(side=tk.LEFT, padx=5)

    def reset_queue(self):
        """Resets the queue to an empty state."""
        self.queue = Queue()
        self.update_queue_display()
        self.set_status("Queue has been reset.")

    def show_about_info(self):
        """Displays the about information."""
        messagebox.showinfo("About", "Queue Operations Application v1.0\nBy Rajnish Bhardwaj")

    def exit_queue_app(self):
        """Closes the application and shows the main application window."""
        self.root.destroy()  # Close the current window
        self.main_app.deiconify()  # Show the main window

# Main application class placeholder (for context)
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")
        self.root.geometry("500x300")
        self.center_window(500, 300)

        self.label = tk.Label(self.root, text="Main Application", font=("Arial", 24))
        self.label.pack(pady=50)

        self.open_queue_app_button = ttk.Button(self.root, text="Open Queue App", command=self.open_queue_app)
        self.open_queue_app_button.pack(pady=10)

    def center_window(self, width, height):
        """Center the application window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def open_queue_app(self):
        """Opens the Queue application."""
        self.root.withdraw()  # Hide the main application window
        queue_root = tk.Toplevel(self.root)  # Create a new window for the queue app
        app = QueueApp(queue_root, self.root)  # Pass the main application reference

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    main_app = MainApp(root)
    root.mainloop()
