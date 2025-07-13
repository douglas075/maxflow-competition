import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

class TimerOverlay:
    def __init__(self, fig, duration=60, position=(0.5, 0.90), fontsize=40):
        self.fig = fig
        self.duration = duration
        self.elapsed = 0.0
        self.running_since = None

        self.paused = True
        self.expired = False
        self.awaiting_reset = False

        self.text_obj = fig.text(
            position[0], position[1], "",
            ha='center', va='center', fontsize=fontsize, weight='bold',
            color='orange',
            bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.5')
        )

        # Buttons
        self.ax_reset = fig.add_axes([0.445, 0.76, 0.05, 0.06])
        self.ax_start = fig.add_axes([0.505, 0.76, 0.05, 0.06])

        self.btn_reset = Button(self.ax_reset, 'Reset', color='peru', hovercolor='darkorange')
        self.btn_start = Button(self.ax_start, 'Start', color='mediumseagreen', hovercolor='limegreen')

        self.btn_reset.label.set_fontsize(16)
        self.btn_start.label.set_fontsize(16)

        self.btn_reset.on_clicked(self._on_reset)
        self.btn_start.on_clicked(self._on_toggle)

        self.ani = animation.FuncAnimation(fig, self._update, interval=100, cache_frame_data=False)

    def _update(self, frame):
        if self.awaiting_reset:
            return

        now = time.time()
        if not self.paused and not self.expired and self.running_since is not None:
            self.elapsed += now - self.running_since
            self.running_since = now

        remaining = max(0, self.duration - self.elapsed)

        if remaining == 0 and not self.expired:
            self.expired = True
            self.paused = True
            self.awaiting_reset = True
            self.text_obj.set_text("Time's up!")
        else:
            rounded = int(round(remaining))
            mins = rounded // 60
            secs = rounded % 60
            self.text_obj.set_text(f"{mins}:{secs:02}")

        self.fig.canvas.draw_idle()


    def _rebuild_start_button(self, label, color, hovercolor):
        self.ax_start.remove()
        self.ax_start = self.fig.add_axes([0.505, 0.76, 0.05, 0.06])
        self.btn_start = Button(self.ax_start, label, color=color, hovercolor=hovercolor)
        self.btn_start.label.set_fontsize(16)
        self.btn_start.on_clicked(self._on_toggle)

    def _on_toggle(self, event):
        self.toggle()
        if not self.paused:
            self._rebuild_start_button("Stop", "firebrick", "indianred")
        else:
            self._rebuild_start_button("Start", "mediumseagreen", "limegreen")
        self.fig.canvas.draw_idle()

    def _on_reset(self, event):
        self.reset()
        self._rebuild_start_button("Start", "mediumseagreen", "limegreen")

    def toggle(self):
        if self.awaiting_reset or self.expired:
            return

        if self.paused:
            self.running_since = time.time()
        else:
            now = time.time()
            self.elapsed += now - self.running_since
            self.running_since = None

        self.paused = not self.paused

    def reset(self):
        self.paused = True
        self.expired = False
        self.awaiting_reset = False
        self.elapsed = 0.0
        self.running_since = None

        mins = self.duration // 60
        secs = self.duration % 60
        self.text_obj.set_text(f"{mins}:{secs:02}")
        self.fig.canvas.draw_idle()


# Example usage
if __name__ == "__main__":
    fig = plt.figure(figsize=(5, 5), facecolor='black')
    timer = TimerOverlay(fig, duration=60)
    plt.show()
