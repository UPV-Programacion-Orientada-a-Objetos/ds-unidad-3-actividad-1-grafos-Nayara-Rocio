import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import time
import threading
from neuronet import PyGraph

class NeuroNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet - Análisis de Redes Masivas")
        self.root.geometry("1200x800")
        
        self.graph = PyGraph(directed=True)
        self.loaded_file = None
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        control_frame = ttk.LabelFrame(main_frame, text="Control", padding="5")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        file_frame = ttk.Frame(control_frame)
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(file_frame, text="Cargar Dataset", 
                  command=self.load_dataset).pack(side=tk.LEFT, padx=(0, 5))
        self.file_label = ttk.Label(file_frame, text="No se ha cargado ningún archivo")
        self.file_label.pack(side=tk.LEFT)
        
        metrics_frame = ttk.Frame(control_frame)
        metrics_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(metrics_frame, text="Calcular Métricas",
                  command=self.calculate_metrics).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(metrics_frame, text="Nodo con Mayor Grado",
                  command=self.find_max_degree).pack(side=tk.LEFT, padx=(0, 5))
        
        search_frame = ttk.Frame(control_frame)
        search_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(search_frame, text="BFS - Nodo Inicio:").pack(side=tk.LEFT)
        self.bfs_start_entry = ttk.Entry(search_frame, width=10)
        self.bfs_start_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(search_frame, text="Profundidad Máx:").pack(side=tk.LEFT)
        self.bfs_depth_entry = ttk.Entry(search_frame, width=10)
        self.bfs_depth_entry.insert(0, "2")
        self.bfs_depth_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(search_frame, text="Ejecutar BFS",
                  command=self.run_bfs).pack(side=tk.LEFT)
        
        info_frame = ttk.LabelFrame(main_frame, text="Información del Grafo", padding="5")
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.info_text = tk.Text(info_frame, height=8, width=50)
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        viz_frame = ttk.LabelFrame(main_frame, text="Visualización", padding="5")
        viz_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(0, weight=1)
        
        log_frame = ttk.LabelFrame(main_frame, text="Logs de Ejecución", padding="5")
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = tk.Text(log_frame, height=10, width=50)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log("Sistema NeuroNet inicializado. Cargue un dataset para comenzar.")
    
    def log(self, message):
        """Añade un mensaje al log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def load_dataset(self):
        """Carga un dataset de grafo"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de grafo",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            self.file_label.config(text=filename.split('/')[-1])
            self.loaded_file = filename
            
            thread = threading.Thread(target=self._load_dataset_thread, args=(filename,))
            thread.daemon = True
            thread.start()
    
    def _load_dataset_thread(self, filename):
        """Hilo para cargar el dataset"""
        self.log(f"Cargando dataset: {filename}")
        
        try:
            start_time = time.time()
            success = self.graph.load_data(filename)
            load_time = time.time() - start_time
            
            if success:
                self.log(f"Dataset cargado exitosamente en {load_time:.2f}s")
                self.update_graph_info()
            else:
                self.log("Error al cargar el dataset")
                messagebox.showerror("Error", "No se pudo cargar el dataset")
                
        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar dataset: {str(e)}")
    
    def update_graph_info(self):
        """Actualiza la información del grafo en la UI"""
        info = f"Archivo: {self.loaded_file}\n"
        info += f"Nodos: {self.graph.get_num_nodes():,}\n"
        info += f"Aristas: {self.graph.get_num_edges():,}\n"
        info += f"Memoria usada: {self.graph.get_memory_usage()} MB\n"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
    
    def calculate_metrics(self):
        """Calcula métricas básicas del grafo"""
        if self.graph.get_num_nodes() == 0:
            messagebox.showwarning("Advertencia", "Primero cargue un dataset")
            return
        
        self.log("Calculando métricas del grafo...")
        self.update_graph_info()
        self.log("Métricas calculadas")
    
    def find_max_degree(self):
        """Encuentra el nodo con mayor grado"""
        if self.graph.get_num_nodes() == 0:
            messagebox.showwarning("Advertencia", "Primero cargue un dataset")
            return
        
        self.log("Buscando nodo con mayor grado...")
        
        try:
            max_degree_node = self.graph.get_node_with_max_degree()
            degree = self.graph.get_node_degree(max_degree_node)
            
            self.log(f"Nodo con mayor grado: {max_degree_node} (Grado: {degree})")
            
            info = self.info_text.get(1.0, tk.END)
            info += f"\nNodo con mayor grado: {max_degree_node} (Grado: {degree})"
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info)
            
        except Exception as e:
            self.log(f"Error al calcular grado máximo: {str(e)}")
    
    def run_bfs(self):
        """Ejecuta BFS y visualiza resultados"""
        if self.graph.get_num_nodes() == 0:
            messagebox.showwarning("Advertencia", "Primero cargue un dataset")
            return
        
        try:
            start_node = int(self.bfs_start_entry.get())
            max_depth = int(self.bfs_depth_entry.get())
            
            if start_node < 0 or start_node >= self.graph.get_num_nodes():
                messagebox.showerror("Error", f"Nodo inicial debe estar entre 0 y {self.graph.get_num_nodes()-1}")
                return
            
            self.log(f"Ejecutando BFS desde nodo {start_node} con profundidad {max_depth}")
            
            thread = threading.Thread(target=self._run_bfs_thread, args=(start_node, max_depth))
            thread.daemon = True
            thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def _run_bfs_thread(self, start_node, max_depth):
        """Hilo para ejecutar BFS"""
        try:
            visited_nodes = self.graph.bfs(start_node, max_depth)
            
            edges = self.graph.get_subgraph_edges(visited_nodes)
            
            self.log(f"BFS completado. Nodos visitados: {len(visited_nodes)}, Aristas: {len(edges)}")
            
            self.root.after(0, self._visualize_subgraph, visited_nodes, edges, start_node)
            
        except Exception as e:
            self.log(f"Error en BFS: {str(e)}")
    
    def _visualize_subgraph(self, nodes, edges, start_node):
        """Visualiza el subgrafo resultante del BFS"""
        try:
            self.ax.clear()
            
            if not nodes:
                self.ax.text(0.5, 0.5, "No hay nodos para visualizar", 
                           ha='center', va='center', transform=self.ax.transAxes)
                self.canvas.draw()
                return
            
            G = nx.Graph()
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)
            
            pos = nx.spring_layout(G, k=1, iterations=50)
            
            node_colors = ['red' if node == start_node else 'skyblue' for node in G.nodes()]
            node_sizes = [300 if node == start_node else 100 for node in G.nodes()]
            
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                 node_size=node_sizes, alpha=0.9, ax=self.ax)
            nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color='gray', ax=self.ax)
            
            important_nodes = {start_node: str(start_node)}
            for node in G.nodes():
                if G.degree(node) > 2:
                    important_nodes[node] = str(node)
            
            nx.draw_networkx_labels(G, pos, labels=important_nodes, 
                                  font_size=8, ax=self.ax)
            
            self.ax.set_title(f"Subgrafo BFS - Nodo {start_node}\n"
                            f"{len(nodes)} nodos, {len(edges)} aristas")
            self.ax.axis('off')
            
            self.canvas.draw()
            self.log("Visualización actualizada")
            
        except Exception as e:
            self.log(f"Error en visualización: {str(e)}")

def main():
    root = tk.Tk()
    app = NeuroNetGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()