from maxflow_base import MaxFlowInteractiveBase
import networkx as nx
import matplotlib.pyplot as plt

class MaxFlowInteractive(MaxFlowInteractiveBase):
    def __init__(self, edge_name_dy=0.12, edge_flow_dy=-0.12, fig=None, ax=None):
        super().__init__(edge_name_dy=edge_name_dy, edge_flow_dy=edge_flow_dy, fig=fig, ax=ax)
        
    def build_graph(self):
        G = nx.DiGraph()
        G.add_edge('S', 'A', capacity=10)
        G.add_edge('S', 'B', capacity=10)
        G.add_edge('S', 'C', capacity=10)
        G.add_edge('A', 'D', capacity=10)
        G.add_edge('B', 'D', capacity=10)
        G.add_edge('C', 'D', capacity=10)
        G.add_edge('D', 'E', capacity=20) # bottleneck
        G.add_edge('E', 'F', capacity=10)
        G.add_edge('E', 'G', capacity=10)
        G.add_edge('E', 'H', capacity=10)
        G.add_edge('F', 'T', capacity=10)
        G.add_edge('G', 'T', capacity=10)
        G.add_edge('H', 'T', capacity=10)
        return G

    def fixed_positions(self):
        return {
            'S': (0, 2),
            'A': (1, 3),
            'B': (1, 2),
            'C': (1, 1),
            'D': (2, 2),
            'E': (3, 2),
            'F': (4, 3),
            'G': (4, 2),
            'H': (4, 1),
            'T': (5, 2),
        }

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(18, 8))
    example = MaxFlowInteractive(fig=fig, ax=ax)

    plt.tight_layout()
    plt.show()
