from maxflow_base import MaxFlowInteractiveBase
import networkx as nx

class MaxFlowInteractive(MaxFlowInteractiveBase):
    def __init__(self):
        super().__init__(edge_name_dy=0.12, edge_flow_dy=-0.12)

    def build_graph(self):
        G = nx.DiGraph()
        G.add_edge('S', 'A', capacity=5)     
        G.add_edge('S', 'B', capacity=6)
        G.add_edge('S', 'C', capacity=5)
        G.add_edge('A', 'D', capacity=9)
        G.add_edge('B', 'D', capacity=4)
        G.add_edge('B', 'E', capacity=4)
        G.add_edge('C', 'E', capacity=6)
        G.add_edge('C', 'F', capacity=6)
        G.add_edge('D', 'T', capacity=7)
        G.add_edge('E', 'T', capacity=8)
        G.add_edge('F', 'T', capacity=7)

        return G

    def fixed_positions(self):
        return {
            'S': (0, 2),
            'A': (1, 3),
            'B': (1, 2),
            'C': (1, 1),
            'D': (2, 3),
            'E': (2, 2),
            'F': (2, 1),
            'T': (3, 2),
        }

if __name__ == "__main__":
    MaxFlowInteractive()
