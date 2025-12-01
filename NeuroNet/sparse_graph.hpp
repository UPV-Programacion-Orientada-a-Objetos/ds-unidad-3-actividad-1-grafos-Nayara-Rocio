#ifndef SPARSE_GRAPH_HPP
#define SPARSE_GRAPH_HPP

#include "graph_base.hpp"
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <queue>
#include <unordered_set>
#include <memory>

class SparseGraph : public GraphBase {
private:
    std::vector<int> row_ptr;
    std::vector<int> col_indices;
    std::vector<double> values;
    
    int num_nodes;
    int num_edges;
    bool directed;
    
    std::vector<std::pair<int, int>> edge_list;
    
public:
    SparseGraph(bool is_directed = true);
    virtual ~SparseGraph() = default;
    
    bool loadData(const std::string& filename) override;
    std::vector<int> BFS(int start_node, int max_depth) override;
    int getNodeDegree(int node_id) override;
    std::vector<int> getNeighbors(int node_id) override;
    int getNodeWithMaxDegree() override;
    int getNumNodes() const override { return num_nodes; }
    int getNumEdges() const override { return num_edges; }
    size_t getMemoryUsage() const override;
    void printGraphInfo() const override;
    
private:
    void buildCSRFromEdgeList();
    int findMaxNodeId() const;
};

#endif