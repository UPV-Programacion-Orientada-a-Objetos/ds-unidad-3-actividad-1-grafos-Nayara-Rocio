# distutils: language = c++
# distutils: sources = sparse_graph.cpp

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp cimport bool as cbool
from libc.stdint cimport intptr_t

cdef extern from "graph_base.hpp":
    cdef cppclass GraphBase:
        cbool loadData(string filename)
        vector[int] BFS(int start_node, int max_depth)
        int getNodeDegree(int node_id)
        vector[int] getNeighbors(int node_id)
        int getNodeWithMaxDegree()
        int getNumNodes()
        int getNumEdges()
        size_t getMemoryUsage()
        void printGraphInfo()

cdef extern from "sparse_graph.hpp":
    cdef cppclass SparseGraph(GraphBase):
        SparseGraph(cbool is_directed) except +

cdef class PyGraph:
    cdef GraphBase* _this_ptr
    cdef cbool _is_directed
    
    def __cinit__(self, directed=True):
        self._is_directed = directed
        self._this_ptr = new SparseGraph(directed)
        if self._this_ptr == NULL:
            raise MemoryError("No se pudo asignar memoria para el grafo")
    
    def __dealloc__(self):
        if self._this_ptr != NULL:
            del self._this_ptr
    
    def load_data(self, filename):
        """Carga un dataset desde archivo"""
        cdef string cpp_filename = filename.encode('utf-8')
        return self._this_ptr.loadData(cpp_filename)
    
    def bfs(self, start_node, max_depth):
        """Ejecuta BFS desde un nodo con profundidad máxima"""
        cdef vector[int] result = self._this_ptr.BFS(start_node, max_depth)
        return [node for node in result]
    
    def get_node_degree(self, node_id):
        """Obtiene el grado de un nodo"""
        return self._this_ptr.getNodeDegree(node_id)
    
    def get_neighbors(self, node_id):
        """Obtiene los vecinos de un nodo"""
        cdef vector[int] result = self._this_ptr.getNeighbors(node_id)
        return [node for node in result]
    
    def get_node_with_max_degree(self):
        """Encuentra el nodo con mayor grado"""
        return self._this_ptr.getNodeWithMaxDegree()
    
    def get_num_nodes(self):
        """Obtiene el número total de nodos"""
        return self._this_ptr.getNumNodes()
    
    def get_num_edges(self):
        """Obtiene el número total de aristas"""
        return self._this_ptr.getNumEdges()
    
    def get_memory_usage(self):
        """Obtiene el uso de memoria en MB"""
        return self._this_ptr.getMemoryUsage()
    
    def print_graph_info(self):
        """Imprime información del grafo"""
        self._this_ptr.printGraphInfo()
    
    def get_subgraph_edges(self, nodes):
        """Obtiene las aristas del subgrafo inducido por los nodos dados"""
        cdef set node_set = set(nodes)
        cdef list edges = []
        cdef int node, neighbor
        cdef vector[int] neighbors
        
        for node in nodes:
            if 0 <= node < self.get_num_nodes():
                neighbors = self._this_ptr.getNeighbors(node)
                for i in range(neighbors.size()):
                    neighbor = neighbors[i]
                    if neighbor in node_set:
                        edges.append((node, neighbor))
        
        return edges