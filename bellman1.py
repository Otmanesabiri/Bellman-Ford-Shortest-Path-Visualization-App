import networkx as nwx
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Nombre de sommets
        self.graph = []    # Liste pour stocker les arêtes

    def add_edge(self, u, v, w):
        """Ajouter une arête au graphe"""
        self.graph.append((u, v, w))

    def bellman_ford(self, src, dest=None):
        """Algorithme de Bellman-Ford pour trouver les plus courts chemins"""
        # Initialisation
        distances = [float('inf')] * self.V
        predecesseurs = [None] * self.V
        distances[src] = 0

        # Relaxation des arêtes
        for _ in range(self.V - 1):
            mise_a_jour = False
            for u, v, w in self.graph:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    predecesseurs[v] = u
                    mise_a_jour = True
            
            # Optimisation : arrêter si aucune mise à jour
            if not mise_a_jour:
                break

        # Vérification des cycles de poids négatif
        for u, v, w in self.graph:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                raise ValueError("Le graphe contient un cycle de poids négatif")

        # Reconstruction des chemins
        chemins = {}
        for sommet in range(self.V):
            if dest is not None and sommet != dest:
                continue
            
            chemin = []
            courant = sommet
            while courant is not None:
                chemin.append(courant)
                courant = predecesseurs[courant]
            
            chemins[sommet] = list(reversed(chemin))

        # Si une destination spécifique est donnée, retourner son chemin
        if dest is not None:
            return distances[dest], chemins[dest]
        
        return distances, chemins

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Bellman-Ford Shortest Path")
        
        self.graph = None
        self.vertices = 0
        self.edges = []

        # Interface utilisateur
        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Zone de configuration du graphe
        config_frame = tk.LabelFrame(frame, text="Configuration du Graphe")
        config_frame.pack(fill=tk.X, padx=5, pady=5)

        # Nombre de sommets
        tk.Label(config_frame, text="Nombre de sommets:").grid(row=0, column=0, padx=5, pady=5)
        self.vertices_entry = tk.Entry(config_frame, width=10)
        self.vertices_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Bouton de création de graphe
        tk.Button(config_frame, text="Créer Graphe", command=self.create_graph).grid(row=0, column=2, padx=5, pady=5)

        # Zone d'ajout d'arêtes
        edge_frame = tk.LabelFrame(frame, text="Ajouter des Arêtes")
        edge_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(edge_frame, text="De:").grid(row=0, column=0, padx=5, pady=5)
        self.from_entry = tk.Entry(edge_frame, width=5)
        self.from_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(edge_frame, text="À:").grid(row=0, column=2, padx=5, pady=5)
        self.to_entry = tk.Entry(edge_frame, width=5)
        self.to_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(edge_frame, text="Poids:").grid(row=0, column=4, padx=5, pady=5)
        self.weight_entry = tk.Entry(edge_frame, width=5)
        self.weight_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(edge_frame, text="Ajouter Arête", command=self.add_edge).grid(row=0, column=6, padx=5, pady=5)

        # Zone d'algorithme
        algo_frame = tk.LabelFrame(frame, text="Algorithme de Bellman-Ford")
        algo_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(algo_frame, text="Source:").grid(row=0, column=0, padx=5, pady=5)
        self.source_entry = tk.Entry(algo_frame, width=5)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(algo_frame, text="Destination (optionnel):").grid(row=0, column=2, padx=5, pady=5)
        self.dest_entry = tk.Entry(algo_frame, width=5)
        self.dest_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(algo_frame, text="Calculer Chemin", command=self.calculate_path).grid(row=0, column=4, padx=5, pady=5)

        # Zone de résultat
        self.result_text = tk.Text(frame, height=5, width=50)
        self.result_text.pack(fill=tk.X, padx=5, pady=5)

        # Zone de visualisation du graphe
        self.figure_frame = tk.Frame(frame)
        self.figure_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_graph(self):
        try:
            self.vertices = int(self.vertices_entry.get())
            self.graph = Graph(self.vertices)
            self.edges = []
            messagebox.showinfo("Succès", f"Graphe créé avec {self.vertices} sommets")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide de sommets")

    def add_edge(self):
        if self.graph is None:
            messagebox.showerror("Erreur", "Créez d'abord un graphe")
            return

        try:
            from_vertex = int(self.from_entry.get())
            to_vertex = int(self.to_entry.get())
            weight = int(self.weight_entry.get())

            if 0 <= from_vertex < self.vertices and 0 <= to_vertex < self.vertices:
                self.graph.add_edge(from_vertex, to_vertex, weight)
                self.edges.append((from_vertex, to_vertex, weight))
                
                # Effacer les entrées
                self.from_entry.delete(0, tk.END)
                self.to_entry.delete(0, tk.END)
                self.weight_entry.delete(0, tk.END)
                
                messagebox.showinfo("Succès", f"Arête ajoutée: {from_vertex} -> {to_vertex} (poids: {weight})")
                self.visualize_graph()
            else:
                messagebox.showerror("Erreur", "Sommets en dehors de la plage")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides")

    def calculate_path(self):
        if self.graph is None:
            messagebox.showerror("Erreur", "Créez d'abord un graphe")
            return

        try:
            source = int(self.source_entry.get())
            dest_str = self.dest_entry.get()

            # Vider le texte de résultat
            self.result_text.delete(1.0, tk.END)

            if dest_str:
                # Chemin d'un sommet source à un sommet destination
                destination = int(dest_str)
                distance, path = self.graph.bellman_ford(source, destination)
                
                self.result_text.insert(tk.END, f"Distance de {source} à {destination}: {distance}\n")
                self.result_text.insert(tk.END, f"Chemin: {' -> '.join(map(str, path))}")
                
                # Surligner le chemin dans la visualisation
                self.visualize_graph(path)
            else:
                # Calcul des distances pour tous les sommets
                distances, paths = self.graph.bellman_ford(source)
                
                for dest, distance in enumerate(distances):
                    if distance != float('inf'):
                        self.result_text.insert(tk.END, f"Distance de {source} à {dest}: {distance}\n")
                
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def visualize_graph(self, highlight_path=None):
        # Effacer l'ancien graphique s'il existe
        for widget in self.figure_frame.winfo_children():
            widget.destroy()

        # Créer un graphe NetworkX
        G = nwx.DiGraph()
        
        # Ajouter les arêtes
        for edge in self.edges:
            G.add_edge(edge[0], edge[1], weight=edge[2])

        # Créer la figure
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Position des nœuds
        pos = nwx.spring_layout(G, seed=42)
        
        # Dessiner les nœuds
        nwx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', node_size=500)
        
        # Dessiner les étiquettes de nœuds
        nwx.draw_networkx_labels(G, pos, ax=ax)
        
        # Dessiner les arêtes
        edge_colors = ['red' if highlight_path and 
                       (u, v) in list(zip(highlight_path, highlight_path[1:])) 
                       else 'gray' 
                       for (u, v, d) in G.edges(data=True)]
        
        nwx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, 
                                arrows=True, arrowsize=20)
        
        # Dessiner les poids des arêtes
        edge_labels = nwx.get_edge_attributes(G, 'weight')
        nwx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
        
        plt.title("Graphe")
        plt.axis('off')
        
        # Intégrer le graphique matplotlib dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.figure_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    root.geometry("800x900")
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()