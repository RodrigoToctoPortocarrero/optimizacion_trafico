import tkinter as tk
from config import Config

class TrafficCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(
            parent,
            width=Config.CANVAS_WIDTH,
            height=Config.CANVAS_HEIGHT,
            bg=Config.CANVAS_BG,
            highlightthickness=2,
            highlightbackground=Config.COLOR_PRIMARY
        )
        
        self.pack(padx=10, pady=10)
        
    def clear(self):
        """Limpia el canvas"""
        self.delete("all")