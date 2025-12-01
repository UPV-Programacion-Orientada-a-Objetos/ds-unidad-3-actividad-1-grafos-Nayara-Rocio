cdef extern from "graph_base.hpp":
    cdef cppclass GraphBase:
        bool loadData(string filename)
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
        SparseGraph(bool is_directed)

cdef class PyGraph:
    cdef GraphBase* _this_ptr
    cdef bool _is_directed