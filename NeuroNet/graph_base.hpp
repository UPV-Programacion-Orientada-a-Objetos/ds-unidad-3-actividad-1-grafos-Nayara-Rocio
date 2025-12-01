#ifndef GRAPH_BASE_HPP
#define GRAPH_BASE_HPP

#include <vector>
#include <string>
#include <memory>

class GraphBase {
public:
    virtual ~GraphBase() = default;
    
    virtual bool loadData(const std::string& filename) = 0;
    virtual std::vector<int> BFS(int start_node, int max_depth) = 0;
    virtual int getNodeDegree(int node_id) = 0;
    virtual std::vector<int> getNeighbors(int node_id) = 0;
    virtual int getNodeWithMaxDegree() = 0;
    virtual int getNumNodes() const = 0;
    virtual int getNumEdges() const = 0;
    virtual size_t getMemoryUsage() const = 0;
    
    virtual void printGraphInfo() const = 0;
};

#endif