import tkinter as tk
from tkinter import messagebox
from itertools import permutations
import math

class TSP:
    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)

    def calculate_total_distance(self, route):
        """Calculate the total distance of a given route."""
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += self.distance_matrix[route[i]][route[i + 1]]
        # Add distance to return to the starting city
        total_distance += self.distance_matrix[route[-1]][route[0]]
        return total_distance

    def solve(self):
        """Solve the TSP using brute force."""
        min_distance = math.inf
        best_route = None
        # Generate all possible permutations of cities
        for perm in permutations(range(self.num_cities)):
            current_distance = self.calculate_total_distance(perm)
            if current_distance < min_distance:
                min_distance = current_distance
                best_route = perm
        return best_route, min_distance


class TSPApp:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.distance_matrix = []
        self.num_cities = 0

        self.root.title("Traveling Salesman Problem")
        self.root.geometry("500x400")
        self.root.config(bg='#3498db')

        # Input for number of cities
        self.label_cities = tk.Label(root, text="Enter number of cities:", font=("Arial", 14), bg='#3498db', fg='white')
        self.label_cities.pack(pady=10)

        self.entry_cities = tk.Entry(root, width=5, font=("Arial", 14))
        self.entry_cities.pack(pady=5)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_cities, font=("Arial", 12))
        self.submit_button.pack(pady=5)

        # Back Button
        self.back_button = tk.Button(root, text="Back", font=("Arial", 12), command=self.go_back)
        self.back_button.pack(pady=5)

    def submit_cities(self):
        try:
            self.num_cities = int(self.entry_cities.get())
            if self.num_cities < 2:
                raise ValueError
            self.show_distance_matrix_input()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of cities (at least 2).")

    def show_distance_matrix_input(self):
        self.entry_cities.config(state='disabled')
        self.submit_button.config(state='disabled')

        self.matrix_frame = tk.Frame(self.root, bg='#3498db')
        self.matrix_frame.pack(pady=10)

        self.labels = []
        self.entries = []

        for i in range(self.num_cities):
            row = []
            for j in range(self.num_cities):
                label = tk.Label(self.matrix_frame, text=f"Distance [{i}][{j}]", font=("Arial", 10), bg='#3498db', fg='white')
                label.grid(row=i, column=j * 2)
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j * 2 + 1)
                row.append(entry)
            self.entries.append(row)

        self.solve_button = tk.Button(self.root, text="Solve TSP", font=("Arial", 12), command=self.solve_tsp)
        self.solve_button.pack(pady=10)

    def solve_tsp(self):
        try:
            # Create the distance matrix from the user input
            self.distance_matrix = [
                [int(self.entries[i][j].get()) for j in range(self.num_cities)]
                for i in range(self.num_cities)
            ]
            tsp = TSP(self.distance_matrix)
            best_route, min_distance = tsp.solve()
            self.show_solution(best_route, min_distance)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid distances for all cities.")

    def show_solution(self, best_route, min_distance):
        result_window = tk.Toplevel(self.root)
        result_window.title("TSP Solution")
        result_window.geometry("400x300")
        result_window.config(bg='#2ecc71')

        route_str = " -> ".join(f"City {city}" for city in best_route)
        result_label = tk.Label(result_window, text=f"Optimal Route: {route_str}\nTotal Distance: {min_distance}",
                                font=("Arial", 14), bg='#2ecc71', fg='white')
        result_label.pack(pady=20)

        close_button = tk.Button(result_window, text="Close", command=result_window.destroy, font=("Arial", 12))
        close_button.pack(pady=10)

    def go_back(self):
        self.root.destroy()
        self.main_app.deiconify()
