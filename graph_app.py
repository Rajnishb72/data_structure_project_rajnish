import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


class Graph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = {}
            return f"Vertex '{vertex}' added."
        else:
            return f"Vertex '{vertex}' already exists."

    def remove_vertex(self, vertex):
        if vertex in self.graph:
            del self.graph[vertex]
            for v in self.graph:
                if vertex in self.graph[v]:
                    del self.graph[v][vertex]
            return f"Vertex '{vertex}' removed."
        else:
            return f"Vertex '{vertex}' not found."

    def add_edge(self, vertex1, vertex2, direction, distance):
        if vertex1 in self.graph and vertex2 in self.graph:
            self.graph[vertex1][vertex2] = {'direction': direction, 'distance': distance}
            self.graph[vertex2][vertex1] = {'direction': self._reverse_direction(direction), 'distance': distance}
            return f"Edge from '{vertex1}' to '{vertex2}' with direction '{direction}' and distance {distance} added."
        else:
            return "One or both vertices not found."

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.graph and vertex2 in self.graph[vertex1]:
            del self.graph[vertex1][vertex2]
            del self.graph[vertex2][vertex1]
            return f"Edge between '{vertex1}' and '{vertex2}' removed."
        else:
            return f"Edge between '{vertex1}' and '{vertex2}' not found."

    def _reverse_direction(self, direction):
        direction_map = {'left': 'right', 'right': 'left', 'straight': 'straight'}
        return direction_map.get(direction, 'straight')

    def bfs(self, start_vertex):
        if start_vertex not in self.graph:
            return f"Vertex '{start_vertex}' not found."
        visited = set()
        queue = deque([start_vertex])
        bfs_order = []
        highlighted_edges = []

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                bfs_order.append(vertex)

                for neighbor in self.graph[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
                        highlighted_edges.append((vertex, neighbor))
        self.visualize(highlighted_edges=highlighted_edges, highlighted_nodes=bfs_order)
        return "-> ".join(bfs_order)

    def visualize(self, highlighted_edges=None, highlighted_nodes=None):
        G = nx.Graph()
        for vertex, edges in self.graph.items():
            for adjacent, attributes in edges.items():
                G.add_edge(vertex, adjacent, direction=attributes['direction'], weight=attributes['distance'])

        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 10))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
                node_size=3000, font_size=12, font_weight='bold')

        if highlighted_edges:
            nx.draw_networkx_edges(G, pos, edgelist=highlighted_edges, edge_color='red', width=2)

        if highlighted_nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=highlighted_nodes, node_color='orange',
                                   node_size=3000)

        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.4, font_size=10,
                                       font_color='blue')

        # Draw directions on edges
        for (u, v, data) in G.edges(data=True):
            direction = data['direction']
            mid_point = [(pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2]
            plt.text(mid_point[0], mid_point[1] + 0.03, direction, fontsize=10, ha='center', color='green')

        plt.title("Graph Visualization", fontsize=20)
        plt.show()


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Visualization with Directions")
        self.graph = Graph()

        # Set a normal window size with minimum size
        self.root.geometry('1200x800')
        self.root.minsize(800, 600)

        # Create a main frame with padding
        self.main_frame = tk.Frame(root, bg='#e4e4e4')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create a text widget with larger font size
        self.output_text = tk.Text(self.main_frame, height=15, width=100, font=('Arial', 12),
                                    wrap=tk.WORD)
        self.output_text.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        # Create a clear output button
        self.clear_button = tk.Button(self.main_frame, text="Clear Output", command=self.clear_output,
                                      bg="#FFC107", fg="black")
        self.clear_button.pack(pady=10)

        # Create a menu bar with a clean design
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        self.graph_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Graph", menu=self.graph_menu)
        self.graph_menu.add_command(label="Add Vertex", command=self.add_vertex)
        self.graph_menu.add_command(label="Remove Vertex", command=self.remove_vertex)
        self.graph_menu.add_command(label="Add Edge", command=self.add_edge)
        self.graph_menu.add_command(label="Remove Edge", command=self.remove_edge)
        self.graph_menu.add_separator()
        self.graph_menu.add_command(label="Display Graph", command=self.display_graph)
        self.graph_menu.add_command(label="Visualize Graph", command=self.visualize_graph)
        self.graph_menu.add_separator()
        self.graph_menu.add_command(label="BFS", command=self.perform_bfs)
        self.graph_menu.add_separator()
        self.graph_menu.add_command(label="Exit", command=root.quit)

    def add_vertex(self):
        vertex = simpledialog.askstring("Input", "Enter the vertex to add:")
        if vertex:
            result = self.graph.add_vertex(vertex)
            self.output_text.insert(tk.END, result + "\n")

    def remove_vertex(self):
        vertex = simpledialog.askstring("Input", "Enter the vertex to remove:")
        if vertex:
            result = self.graph.remove_vertex(vertex)
            self.output_text.insert(tk.END, result + "\n")

    def add_edge(self):
        vertex1 = simpledialog.askstring("Input", "Enter the first vertex:")
        vertex2 = simpledialog.askstring("Input", "Enter the second vertex:")
        direction = simpledialog.askstring("Input", "Enter the direction (left/right/straight):")
        distance = simpledialog.askstring("Input", "Enter the distance between the vertices:")
        if vertex1 and vertex2 and direction and distance:
            try:
                distance = float(distance)
                result = self.graph.add_edge(vertex1, vertex2, direction, distance)
                self.output_text.insert(tk.END, result + "\n")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for the distance.")

    def remove_edge(self):
        vertex1 = simpledialog.askstring("Input", "Enter the first vertex of the edge to remove:")
        vertex2 = simpledialog.askstring("Input", "Enter the second vertex of the edge to remove:")
        if vertex1 and vertex2:
            result = self.graph.remove_edge(vertex1, vertex2)
            self.output_text.insert(tk.END, result + "\n")

    def display_graph(self):
        result = "\n".join([f"{v}: {edges}" for v, edges in self.graph.graph.items()])
        self.output_text.insert(tk.END, "Graph:\n" + result + "\n")

    def visualize_graph(self):
        self.graph.visualize()

    def perform_bfs(self):
        start_vertex = simpledialog.askstring("Input", "Enter the start vertex for BFS:")
        if start_vertex:
            result = self.graph.bfs(start_vertex)
            self.output_text.insert(tk.END, "BFS Traversal:\n" + result + "\n")

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)  # Clears the text area


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
