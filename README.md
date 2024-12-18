# Bellman-Ford Shortest Path Visualization Application

## Description
This is a Python application that demonstrates the Bellman-Ford algorithm for finding shortest paths in a weighted directed graph. The application provides a graphical user interface (GUI) that allows users to:
- Create a graph with a specified number of vertices
- Add weighted edges to the graph
- Calculate shortest paths between vertices
- Visualize the graph and highlighted shortest paths

## Features
- Interactive graph creation
- Edge addition with custom weights
- Shortest path calculation using Bellman-Ford algorithm
- Real-time graph visualization
- Path highlighting
- Error handling for graph and path calculations

## Prerequisites
- Python 3.8+
- Required Libraries:
  - tkinter (usually comes pre-installed with Python)
  - networkx
  - matplotlib

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/bellman-ford-visualization.git
cd bellman-ford-visualization
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install networkx matplotlib
```

## How to Use

### Running the Application
```bash
python bellman_ford_app.py
```

### Using the Application

1. **Create Graph**
   - Enter the number of vertices
   - Click "Créer Graphe" (Create Graph)

2. **Add Edges**
   - Enter source vertex, destination vertex, and edge weight
   - Click "Ajouter Arête" (Add Edge)
   - Repeat for all desired edges

3. **Calculate Shortest Path**
   - Enter source vertex
   - Optionally enter destination vertex
   - Click "Calculer Chemin" (Calculate Path)
   - View results in the text area
   - Shortest path will be highlighted in red on the graph

## Example Workflow
1. Create a graph with 5 vertices
2. Add edges:
   - 0 -> 1 (weight 4)
   - 0 -> 2 (weight 2)
   - 1 -> 3 (weight 3)
   - 2 -> 1 (weight 1)
   - 2 -> 3 (weight 5)
3. Calculate path from vertex 0 to vertex 3

## Algorithm Details
The Bellman-Ford algorithm finds the shortest paths from a source vertex to all other vertices in a weighted graph. It can handle graphs with negative edge weights and detect negative weight cycles.

### Time Complexity
- O(VE), where V is the number of vertices and E is the number of edges

### Key Differences from Dijkstra's Algorithm
- Can handle negative edge weights
- Slower than Dijkstra's algorithm
- Detects negative weight cycles

## Potential Improvements
- Add more graph generation options
- Implement step-by-step algorithm visualization
- Support for loading graphs from files
- More detailed error handling

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

