import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class TimerOverlay:
    def __init__(self, fig, duration=120, position=(0.5, 0.90), fontsize=40):
        self.fig = fig
        self.duration = duration
        self.remaining = duration
        self.paused = True
        self.expired = False
        self.started_once = False
        self.awaiting_reset = False  
        self.start_time = None

        self.text_obj = fig.text(
            position[0], position[1], "",
            ha='center', va='center', fontsize=fontsize, weight='bold',
            color='orange',  
            bbox=dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3')  
        )


        self.ani = animation.FuncAnimation(fig, self._update, interval=1000)

    def _update(self, frame):
        
        if self.awaiting_reset:
            return

        if not self.paused and not self.expired:
            elapsed = int(time.time() - self.start_time)
            self.remaining = max(0, self.duration - elapsed)

        if self.remaining == 0 and not self.expired:
            self.expired = True
            self.paused = True
            self.awaiting_reset = True  
            self.text_obj.set_text("Time's up!\n(reset)")
        elif not self.started_once:
            mins = self.remaining // 60
            secs = self.remaining % 60
            self.text_obj.set_text(f"{mins:02}:{secs:02}\n(start)")
        else:
            mins = self.remaining // 60
            secs = self.remaining % 60
            self.text_obj.set_text(f"{mins:02}:{secs:02}")

        self.fig.canvas.draw_idle()

    def toggle(self):
        if self.awaiting_reset:
            self.reset()
            return

        if self.expired:
            return  

        if self.paused:
            self.started_once = True
            self.start_time = time.time() - (self.duration - self.remaining)
        else:
            self.remaining = max(0, self.remaining - int(time.time() - self.start_time))

        self.paused = not self.paused

    def reset(self):
        self.paused = True
        self.expired = False
        self.started_once = False
        self.awaiting_reset = False  
        self.remaining = self.duration
        mins = self.remaining // 60
        secs = self.remaining % 60
        self.text_obj.set_text(f"{mins:02}:{secs:02}\n(start)")

    def is_running(self):
        return not self.paused and not self.expired
