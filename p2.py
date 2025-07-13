from src.maxflow_base import MaxFlowInteractiveBase
from src.timer_overlay import TimerOverlay
import networkx as nx
import matplotlib.pyplot as plt

class MaxFlowInteractive(MaxFlowInteractiveBase):
    def __init__(self, edge_name_dy=0.12, edge_flow_dy=-0.12, fig=None, ax=None):
        super().__init__(edge_name_dy=edge_name_dy, edge_flow_dy=edge_flow_dy, fig=fig, ax=ax)

        
    def build_graph(self):
        G = nx.DiGraph()
        # same to p1        
        G.add_edge('S', 'A', capacity=9)
        G.add_edge('S', 'B', capacity=6)
        G.add_edge('S', 'C', capacity=5)
        G.add_edge('A', 'D', capacity=5)
        G.add_edge('B', 'D', capacity=3)
        G.add_edge('B', 'E', capacity=4) # new
        G.add_edge('C', 'E', capacity=6) # new
        G.add_edge('C', 'F', capacity=8)
        G.add_edge('D', 'T', capacity=7)
        G.add_edge('E', 'T', capacity=8) # new
        G.add_edge('F', 'T', capacity=10)

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
    fig, axs = plt.subplots(1, 2, figsize=(18, 8))

    mfi1 = MaxFlowInteractive(edge_name_dy=0.12, edge_flow_dy=-0.15, fig=fig, ax=axs[0])
    mfi2 = MaxFlowInteractive(edge_name_dy=0.12, edge_flow_dy=-0.15, fig=fig, ax=axs[1])

    timer = TimerOverlay(fig, duration=120)

    plt.show()

