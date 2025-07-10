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
        G.add_edge('A', 'C', capacity=2)
        G.add_edge('A', 'D', capacity=6)
        G.add_edge('B', 'D', capacity=8)
        G.add_edge('B', 'E', capacity=3)
        G.add_edge('C', 'F', capacity=8)
        G.add_edge('D', 'F', capacity=2)
        G.add_edge('D', 'G', capacity=3)
        G.add_edge('E', 'G', capacity=6)
        G.add_edge('F', 'T', capacity=10)
        G.add_edge('G', 'T', capacity=10)
        return G

    def fixed_positions(self):
        return {
            'S': (0, 2),
            'A': (1, 3),
            'B': (1, 1),
            'C': (2, 4),
            'D': (2, 2),
            'E': (2, 0),
            'F': (3, 3),
            'G': (3, 1),
            'T': (4, 2),
        }
        
if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(16, 8))
    example = MaxFlowInteractive(edge_name_dy=0.2, edge_flow_dy=-0.2, fig=fig, ax=ax)

    plt.tight_layout()
    plt.show()
