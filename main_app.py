import tkinter as tk
from queue_app import QueueApp  # Import QueueApp class
from stack_app import StackApp  # Import StackApp class
from priority_queue_app import PriorityQueueApp  # Import PriorityQueueApp class
from doubly_linked_list_app import DoublyLinkedListApp  # Import DoublyLinkedListApp class
from hash_table_app import HashTableApp  # Import HashTableApp class
from linked_list_app import LinkedListApp  # Import LinkedListApp class
from binary_tree_app import BinaryTreeApp  # Import BinaryTreeApp class
from graph_app import GraphApp  # Import GraphApp class
from huffman_app import HuffmanApp  # Import HuffmanApp class
from tsp_app import TSPApp  # Import TSPApp class

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Page - Rajnish Bhardwaj S073")
        self.root.geometry("400x300")
        self.root.config(bg='#2c3e50')

        # Title Label
        title = tk.Label(root, text="Data Structures", font=("Arial", 18), bg='#2c3e50', fg='white')
        title.pack(pady=20)

        # Menu Button (Hamburger Menu)
        menu_button = tk.Menubutton(root, text="☰", font=("Arial", 20), bg='#ecf0f1', fg='#2c3e50')
        menu = tk.Menu(menu_button, tearoff=0)
        menu_button.config(menu=menu)

        # Add all application commands to the menu
        menu.add_command(label="Queue Operations", command=self.open_queue_program)
        menu.add_command(label="Stack Operations", command=self.open_stack_program)
        menu.add_command(label="Priority Queue Operations", command=self.open_priority_queue_program)
        menu.add_command(label="Doubly Linked List Operations", command=self.open_doubly_linked_list_program)
        menu.add_command(label="Hash Table Operations", command=self.open_hash_table_program)
        menu.add_command(label="Linked List Operations", command=self.open_linked_list_program)
        menu.add_command(label="Binary Tree Operations", command=self.open_binary_tree_program)
        menu.add_command(label="Graph Operations", command=self.open_graph_program)
        menu.add_command(label="Huffman Encoding", command=self.open_huffman_program)
        menu.add_command(label="Traveling Salesman Problem", command=self.open_tsp_program)  # Add TSP option
        menu.add_command(label="Exit", command=root.quit)

        menu_button.pack(anchor='nw', padx=10, pady=10)

        # Welcome Label
        welcome_label = tk.Label(root, text="Welcome to the Data Structures Program", font=("Arial", 14), bg='#2c3e50', fg='white')
        welcome_label.pack(pady=20)

    def open_queue_program(self):
        self.open_new_window(QueueApp, "Queue Operations")

    def open_stack_program(self):
        self.open_new_window(StackApp, "Stack Operations")

    def open_priority_queue_program(self):
        self.open_new_window(PriorityQueueApp, "Priority Queue Operations")

    def open_doubly_linked_list_program(self):
        new_window = tk.Toplevel(self.root)  # Create a new window
        app = DoublyLinkedListApp(new_window, self)  # Pass 'self' if you want to reference the main app
        
    def open_hash_table_program(self):
        self.open_new_window(HashTableApp, "Hash Table Operations")

    def open_linked_list_program(self):
        self.open_new_window(LinkedListApp, "Linked List Operations")

    def open_binary_tree_program(self):
        self.open_new_window(BinaryTreeApp, "Binary Tree Operations")

    def open_graph_program(self):
        self.open_new_window(GraphApp, "Graph Operations")

    def open_huffman_program(self):
        self.open_new_window(HuffmanApp, "Huffman Encoding/Decoding")

    def open_tsp_program(self):
        self.open_new_window(TSPApp, "Traveling Salesman Problem")

    def open_new_window(self, app_class, title, **kwargs):
        self.root.withdraw()  # Hide the main window
        new_window = tk.Toplevel(self.root)
        new_window.title(title)
        new_window.config(bg='#3498db')
        new_window.state('zoomed')

        # Initialize the app class with the new window and any additional parameters
        app_class(new_window, self)

# Run the main application
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
