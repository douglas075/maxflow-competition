import networkx as nx
import matplotlib.pyplot as plt

class MaxFlowInteractiveBase:
    def __init__(self, edge_name_dy=0.2, edge_flow_dy=-0.2, fig=None, ax=None):
        self.edge_name_dy = edge_name_dy
        self.edge_flow_dy = edge_flow_dy
        self.G = self.build_graph()
        self.pos = self.fixed_positions()
        self.fig = fig or plt.figure(figsize=(14, 8))
        self.ax = ax or self.fig.add_subplot(111)
        self.cid = None
        self.flow_value = 0
        self.flow_dict = {}
        self.edge_labels_map = {
            (u, v): f"{i}" for i, (u, v) in enumerate(self.G.edges())
        }
        self.log = []  # 紀錄互動
        self.compute_max_flow() 
        self.draw_graph()
        self.connect_events()

    def build_graph(self):
        raise NotImplementedError

    def fixed_positions(self):
        raise NotImplementedError

    def compute_max_flow(self):
        self.flow_value, self.flow_dict = nx.maximum_flow(self.G, 'S', 'T')

    def draw_graph(self):
        self.ax.clear()
        # self.compute_max_flow()

        nx.draw(
            self.G, self.pos, ax=self.ax, with_labels=True,
            node_color='lightblue', node_size=3000, font_size=18,
            arrows=True, arrowstyle='->', arrowsize=15, width=4
        )

        edge_names = {
            (u, v): self.edge_labels_map[(u, v)]
            for u, v in self.G.edges()
        }

        edge_flows = {
            (u, v): f"{self.flow_dict[u][v]}/{d['capacity']}"
            for u, v, d in self.G.edges(data=True)
        }

        self.draw_offset_labels(edge_names, dy=self.edge_name_dy, fontsize=18, color='black')
        self.draw_offset_labels(edge_flows, dy=self.edge_flow_dy, fontsize=18, color='red')

        self.ax.set_title(f"Max Flow = {self.flow_value}", fontsize=20, pad=20)

        # 根據 ax 決定左上角或右上角顯示 log
        if self.ax.get_subplotspec().colspan.start == 0:
            # 左圖
            self.draw_log(x=0.02, y=0.98, halign='left', valign='top')
        else:
            # 右圖
            self.draw_log(x=0.98, y=0.98, halign='right', valign='top')

        self.ax.axis("off")
        self.fig.canvas.draw()

    def draw_offset_labels(self, labels, dy=0.2, fontsize=20, color='black'):
        new_pos = {}
        for (u, v), label in labels.items():
            x0, y0 = self.pos[u]
            x1, y1 = self.pos[v]
            new_pos[(u, v)] = ((x0 + x1) / 2, (y0 + y1) / 2 + dy)

        for (u, v), (x, y) in new_pos.items():
            self.ax.text(
                x, y, labels[(u, v)],
                fontsize=fontsize,
                color=color,
                ha='center',
                va='center'
            )

    def draw_log(self, x=0.02, y=0.98, halign='left', valign='top'):
        if not self.log:
            return
        log_text = "\n".join(self.log[-6:])
        self.ax.text(
            x, y, log_text,
            transform=self.ax.transAxes,
            fontsize=12,
            verticalalignment=valign,
            horizontalalignment=halign,
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='gray')
        )

    def connect_events(self):
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        if event.button not in (1, 3):
            return

        min_dist = float('inf')
        closest_edge = None

        for u, v in self.G.edges():
            x0, y0 = self.pos[u]
            x1, y1 = self.pos[v]
            px, py = event.xdata, event.ydata
            if px is None or py is None:
                continue
            dist = self.point_line_distance(px, py, x0, y0, x1, y1)
            if dist < min_dist:
                min_dist = dist
                closest_edge = (u, v)

        if closest_edge and min_dist < 0.3:
            u, v = closest_edge
            old_cap = self.G[u][v]['capacity']
            edge_idx = self.edge_labels_map[(u, v)]  # 尋找該邊的編號

            if event.button == 1:
                self.G[u][v]['capacity'] *= 2
                op = "*=2"
            elif event.button == 3:
                self.G[u][v]['capacity'] = max(1, int(old_cap // 2))
                op = "/=2"

            # 重新計算 flow，並紀錄 log
            self.compute_max_flow()
            self.log.append(f"e{edge_idx}{op} MF:{self.flow_value}")

            self.draw_graph()


    @staticmethod
    def point_line_distance(px, py, x0, y0, x1, y1):
        dx, dy = x1 - x0, y1 - y0
        if dx == dy == 0:
            return ((px - x0)**2 + (py - y0)**2) ** 0.5
        t = max(0, min(1, ((px - x0) * dx + (py - y0) * dy) / (dx*dx + dy*dy)))
        proj_x = x0 + t * dx
        proj_y = y0 + t * dy
        return ((px - proj_x)**2 + (py - proj_y)**2) ** 0.5
