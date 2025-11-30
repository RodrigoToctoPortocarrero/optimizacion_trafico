# gui/traffic_canvas.py
import tkinter as tk
from config import Config

class TrafficCanvas:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, width=Config.CANVAS_WIDTH, height=Config.CANVAS_HEIGHT,
                                bg=Config.CANVAS_BG, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def draw(self, simulation):
        simulation.draw(self.canvas)

    def clear(self):
        self.canvas.delete("all")