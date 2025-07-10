from src.maxflow_base import MaxFlowInteractiveBase
from src.timer_overlay import TimerOverlay 
import networkx as nx
import matplotlib.pyplot as plt

class MaxFlowInteractive(MaxFlowInteractiveBase):
    def __init__(self, edge_name_dy=0.12, edge_flow_dy=-0.12, fig=None, ax=None):
        super().__init__(edge_name_dy=edge_name_dy, edge_flow_dy=edge_flow_dy, fig=fig, ax=ax)

    def build_graph(self):
        G = nx.DiGraph()
        G.add_edge('S', 'A', capacity=9)
        G.add_edge('S', 'B', capacity=6)
        G.add_edge('S', 'C', capacity=5)
        G.add_edge('A', 'D', capacity=5)
        G.add_edge('B', 'D', capacity=3)
        G.add_edge('C', 'E', capacity=8)
        G.add_edge('D', 'T', capacity=7)
        G.add_edge('E', 'T', capacity=10)
        return G

    def fixed_positions(self):
        return {
            'S': (0, 2),
            'A': (1, 3),
            'B': (1, 2),
            'C': (1, 1),
            'D': (2, 3),
            'E': (2, 1),
            'T': (3, 2),
        }


if __name__ == "__main__":
    fig, axs = plt.subplots(1, 2, figsize=(18, 8))

    mfi1 = MaxFlowInteractive(fig=fig, ax=axs[0])
    mfi2 = MaxFlowInteractive(fig=fig, ax=axs[1])

    timer = TimerOverlay(fig, duration=120)

    def on_click(event):
        if event.inaxes not in [axs[0], axs[1]]:
            return

        px, py = event.xdata, event.ydata
        for mfi in [mfi1, mfi2]:
            for u, v in mfi.G.edges():
                dist = mfi.point_line_distance(px, py, *mfi.pos[u], *mfi.pos[v])
                if dist < 0.3:
                    return  

        timer.toggle() 

    fig.canvas.mpl_connect("button_press_event", on_click)

    plt.tight_layout()
    plt.show()

'''
solution

for each edge, calculate how much maxflow will increase if it's doubled
in 1st, 2nd, 3rd round, for example:

e2: 3/3/3
e3: 0/4/0
e6: 1/1/1

if we choose (6 -> 3 -> 2), the final amount is
original * 3 + 1 * 3 + 4 * 2 + 3 * 1 = 3 * ori + 14

in the other hand (2 -> 6 -> 3) gives
original * 3 + 3 * 3 + 1 * 2 + 4 * 1 = 3 * ori + 15

'''