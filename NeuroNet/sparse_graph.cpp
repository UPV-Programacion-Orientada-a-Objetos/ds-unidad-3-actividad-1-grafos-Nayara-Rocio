#include "sparse_graph.hpp"
#include <iostream>
#include <chrono>

SparseGraph::SparseGraph(bool is_directed) 
    : num_nodes(0), num_edges(0), directed(is_directed) {}

bool SparseGraph::loadData(const std::string& filename) {
    std::cout << "[C++ Core] Cargando dataset '" << filename << "'..." << std::endl;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "[C++ Core] Error: No se pudo abrir el archivo " << filename << std::endl;
        return false;
    }
    
    edge_list.clear();
    std::string line;
    int max_node = 0;
    
    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#' || line[0] == '%') {
            continue;
        }
        
        std::istringstream iss(line);
        int src, dst;
        
        if (iss >> src >> dst) {
            edge_list.emplace_back(src, dst);
            max_node = std::max(max_node, std::max(src, dst));
            
            if (!directed) {
                edge_list.emplace_back(dst, src);
            }
        }
    }
    
    file.close();
    
    std::sort(edge_list.begin(), edge_list.end());
    
    auto last = std::unique(edge_list.begin(), edge_list.end());
    edge_list.erase(last, edge_list.end());
    
    num_edges = edge_list.size();
    num_nodes = max_node + 1;
    
    buildCSRFromEdgeList();
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    
    std::cout << "[C++ Core] Carga completa. Nodos: " << num_nodes 
              << " | Aristas: " << num_edges << std::endl;
    std::cout << "[C++ Core] Tiempo de carga: " << duration.count() << "ms" << std::endl;
    std::cout << "[C++ Core] Memoria estimada: " << getMemoryUsage() << " MB" << std::endl;
    
    return true;
}

void SparseGraph::buildCSRFromEdgeList() {
    row_ptr.clear();
    col_indices.clear();
    values.clear();
    
    row_ptr.resize(num_nodes + 1, 0);
    
    for (const auto& edge : edge_list) {
        row_ptr[edge.first + 1]++;
    }
    
    for (int i = 1; i <= num_nodes; i++) {
        row_ptr[i] += row_ptr[i - 1];
    }
    
    col_indices.resize(num_edges);
    values.resize(num_edges, 1.0);
    
    std::vector<int> next_pos(row_ptr.begin(), row_ptr.begin() + num_nodes);
    
    for (const auto& edge : edge_list) {
        int pos = next_pos[edge.first]++;
        col_indices[pos] = edge.second;
    }
    
    std::vector<std::pair<int, int>>().swap(edge_list);
}

std::vector<int> SparseGraph::BFS(int start_node, int max_depth) {
    std::cout << "[C++ Core] Ejecutando BFS desde Nodo " << start_node 
              << ", Profundidad " << max_depth << std::endl;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    if (start_node < 0 || start_node >= num_nodes) {
        std::cerr << "[C++ Core] Error: Nodo inicial inválido" << std::endl;
        return {};
    }
    
    std::vector<int> visited_nodes;
    std::vector<bool> visited(num_nodes, false);
    std::queue<std::pair<int, int>> q;
    
    q.push({start_node, 0});
    visited[start_node] = true;
    visited_nodes.push_back(start_node);
    
    while (!q.empty()) {
        auto [current_node, depth] = q.front();
        q.pop();
        
        if (depth >= max_depth) {
            continue;
        }
        
        int start_idx = row_ptr[current_node];
        int end_idx = row_ptr[current_node + 1];
        
        for (int i = start_idx; i < end_idx; i++) {
            int neighbor = col_indices[i];
            
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                visited_nodes.push_back(neighbor);
                q.push({neighbor, depth + 1});
            }
        }
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    
    std::cout << "[C++ Core] BFS completado. Nodos encontrados: " << visited_nodes.size()
              << ". Tiempo ejecución: " << duration.count() << "μs" << std::endl;
    
    return visited_nodes;
}

int SparseGraph::getNodeDegree(int node_id) {
    if (node_id < 0 || node_id >= num_nodes) {
        return -1;
    }
    return row_ptr[node_id + 1] - row_ptr[node_id];
}

std::vector<int> SparseGraph::getNeighbors(int node_id) {
    if (node_id < 0 || node_id >= num_nodes) {
        return {};
    }
    
    int start_idx = row_ptr[node_id];
    int end_idx = row_ptr[node_id + 1];
    
    return std::vector<int>(col_indices.begin() + start_idx, 
                           col_indices.begin() + end_idx);
}

int SparseGraph::getNodeWithMaxDegree() {
    int max_degree = -1;
    int max_node = -1;
    
    for (int i = 0; i < num_nodes; i++) {
        int degree = getNodeDegree(i);
        if (degree > max_degree) {
            max_degree = degree;
            max_node = i;
        }
    }
    
    std::cout << "[C++ Core] Nodo con mayor grado: " << max_node 
              << " (Grado: " << max_degree << ")" << std::endl;
    
    return max_node;
}

size_t SparseGraph::getMemoryUsage() const {
    size_t memory = 0;
    memory += row_ptr.size() * sizeof(int);
    memory += col_indices.size() * sizeof(int);
    memory += values.size() * sizeof(double);
    
    return memory / (1024 * 1024);
}

void SparseGraph::printGraphInfo() const {
    std::cout << "=== INFORMACIÓN DEL GRAFO ===" << std::endl;
    std::cout << "Nodos: " << num_nodes << std::endl;
    std::cout << "Aristas: " << num_edges << std::endl;
    std::cout << "Dirigido: " << (directed ? "Sí" : "No") << std::endl;
    std::cout << "Memoria CSR: " << getMemoryUsage() << " MB" << std::endl;
    std::cout << "=============================" << std::endl;
}