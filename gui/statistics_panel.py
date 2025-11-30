# gui/statistics_panel.py
import tkinter as tk
from config import Config

class StatisticsPanel:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=Config.COLOR_PANEL, relief=tk.SUNKEN, bd=2)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title = tk.Label(self.frame, text="Estadísticas", font=("Arial", 16, "bold"),
                         fg=Config.COLOR_TEXT, bg=Config.COLOR_PANEL)
        title.pack(pady=(10, 5))

        self.labels = {}
        stats = [
            "Vehículos Totales", "Generados", "Completados", "Esperando",
            "Tiempo Promedio Espera", "Tiempo Simulación", "Optimizado"
        ]
        for stat in stats:
            lbl = tk.Label(self.frame, text=f"{stat}: -", font=("Arial", 11),
                           fg=Config.COLOR_TEXT_DARK, bg=Config.COLOR_PANEL, anchor="w")
            lbl.pack(fill=tk.X, padx=20, pady=2)
            self.labels[stat] = lbl

        self.optimized_label = tk.Label(self.frame, text="No optimizado", font=("Arial", 12, "bold"),
                                        fg="orange", bg=Config.COLOR_PANEL)
        self.optimized_label.pack(pady=10)

    def update(self, stats):
        self.labels["Vehículos Totales"].config(text=f"Vehículos Totales : {stats['total_vehicles']}")
        self.labels["Generados"].config(text=f"Generados        : {stats['total_spawned']}")
        self.labels["Completados"].config(text=f"Completados      : {stats['completed']}")
        self.labels["Esperando"].config(text=f"Esperando        : {stats['waiting']}")
        self.labels["Tiempo Promedio Espera"].config(text=f"Tiempo Espera    : {stats['avg_wait_time']}s")
        self.labels["Tiempo Simulación"].config(text=f"Tiempo           : {stats['time']}s")
        self.labels["Optimizado"].config(text=f"Optimizado       : {stats['optimized']}")

    def update_optimized(self, optimized):
        if optimized:
            self.optimized_label.config(text="OPTIMIZADO!", fg="#2ecc71", font=("Arial", 14, "bold"))
        else:
            self.optimized_label.config(text="No optimizado", fg="orange")

    def clear(self):
        for lbl in self.labels.values():
            lbl.config(text=lbl.cget("text").split(":")[0] + ": -")
        self.optimized_label.config(text="No optimizado", fg="orange")