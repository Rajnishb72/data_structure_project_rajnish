import tkinter as tk
from tkinter import messagebox, Menu, ttk


class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = Node(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.val:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node

        if key < node.val:
            node.left = self._delete(node.left, key)
        elif key > node.val:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            min_larger_node = self._get_min(node.right)
            node.val = min_larger_node.val
            node.right = self._delete(node.right, min_larger_node.val)

        return node

    def _get_min(self, node):
        while node.left:
            node = node.left
        return node

    def inorder_traversal(self):
        return self._traverse(self.root, order='inorder')

    def preorder_traversal(self):
        return self._traverse(self.root, order='preorder')

    def postorder_traversal(self):
        return self._traverse(self.root, order='postorder')

    def _traverse(self, node, order):
        res = []
        if node:
            if order == 'preorder':
                res.append(node.val)
            res.extend(self._traverse(node.left, order))
            if order == 'inorder':
                res.append(node.val)
            res.extend(self._traverse(node.right, order))
            if order == 'postorder':
                res.append(node.val)
        return res

    def reset(self):
        self.root = None


class BinaryTreeApp:
    def __init__(self, root, main_app):
        self.tree = BinaryTree()
        self.root = root
        self.main_app = main_app  # Store a reference to the main application
        self.root.title("Binary Tree GUI")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # Close protocol to handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

        # Create a menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        # Add options to the menu
        self.tree_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Tree Operations", menu=self.tree_menu)
        self.tree_menu.add_command(label="Insert Key", command=self.show_insert)
        self.tree_menu.add_command(label="Delete Key", command=self.show_delete)
        self.tree_menu.add_separator()
        self.tree_menu.add_command(label="Inorder Traversal", command=self.show_inorder)
        self.tree_menu.add_command(label="Preorder Traversal", command=self.show_preorder)
        self.tree_menu.add_command(label="Postorder Traversal", command=self.show_postorder)
        self.tree_menu.add_separator()
        self.tree_menu.add_command(label="Reset Tree", command=self.reset_tree)

        # Add an Exit option to the menu
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=self.exit_app)

        # Create a frame for display
        self.frame = tk.Frame(self.root, bg="#e0e0e0", padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg='#2980b9', fg='white')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.set_status("Ready")

    def exit_app(self):
        self.root.destroy()  # Close the current window
        self.main_app.root.deiconify()  # Show the main application window again

    def set_status(self, message):
        """Updates the status bar with a message."""
        self.status_var.set(message)

    def reset_tree(self):
        """Resets the binary tree to an empty state."""
        self.tree.reset()
        self.set_status("Binary tree has been reset.")

    def show_insert(self):
        self._show_input_dialog("Insert Key", self.insert)

    def show_delete(self):
        self._show_input_dialog("Delete Key", self.delete)

    def _show_input_dialog(self, title, callback):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)

        label = tk.Label(dialog, text="Enter Key:", bg="#e0e0e0")
        label.pack(pady=5)

        entry = tk.Entry(dialog, width=20)
        entry.pack(pady=5)

        button = ttk.Button(dialog, text="Submit", command=lambda: callback(entry.get(), dialog))
        button.pack(pady=5)

    def insert(self, key, dialog):
        try:
            key = int(key)
            self.tree.insert(key)
            messagebox.showinfo("Insert", f"Inserted {key} into the tree.")
            self.set_status(f"Inserted {key} into the tree.")
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer.")

    def delete(self, key, dialog):
        try:
            key = int(key)
            self.tree.delete(key)
            messagebox.showinfo("Delete", f"Deleted {key} from the tree.")
            self.set_status(f"Deleted {key} from the tree.")
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer.")

    def show_inorder(self):
        traversal = self.tree.inorder_traversal()
        messagebox.showinfo("Inorder Traversal", "Inorder Traversal: " + " -> ".join(map(str, traversal)))
        self.set_status("Displayed Inorder Traversal.")

    def show_preorder(self):
        traversal = self.tree.preorder_traversal()
        messagebox.showinfo("Preorder Traversal", "Preorder Traversal: " + " -> ".join(map(str, traversal)))
        self.set_status("Displayed Preorder Traversal.")

    def show_postorder(self):
        traversal = self.tree.postorder_traversal()
        messagebox.showinfo("Postorder Traversal", "Postorder Traversal: " + " -> ".join(map(str, traversal)))
        self.set_status("Displayed Postorder Traversal.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryTreeApp(root, None)  # Placeholder for main_app reference
    root.mainloop()
