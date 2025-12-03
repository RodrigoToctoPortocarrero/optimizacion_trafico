# gui/control_panel.py  ← VERSIÓN CORREGIDA Y FINAL
import tkinter as tk
from tkinter import ttk
from config import Config
#control_panel.py
class ControlPanel:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        
        # Creamos el frame principal y lo empaquetamos directamente
        self.frame = tk.Frame(parent, bg=Config.COLOR_PANEL)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # ← pack aquí

        # Título
        tk.Label(self.frame, text="Controles", font=("Arial", 16, "bold"),
                 fg=Config.COLOR_TEXT, bg=Config.COLOR_PANEL).pack(pady=(10, 20))

        # Número de vehículos
        tk.Label(self.frame, text="Número de vehículos:", fg=Config.COLOR_TEXT, bg=Config.COLOR_PANEL).pack(anchor="w", padx=20)
        self.veh_scale = tk.Scale(self.frame, from_=10, to=100, orient=tk.HORIZONTAL, 
                                   bg=Config.COLOR_PANEL, fg="white", highlightthickness=0)
        self.veh_scale.set(30)
        self.veh_scale.pack(fill=tk.X, padx=20, pady=5)

        # Generaciones
        tk.Label(self.frame, text="Generaciones:", fg=Config.COLOR_TEXT, bg=Config.COLOR_PANEL).pack(anchor="w", padx=20)
        self.gen_scale = tk.Scale(self.frame, from_=20, to=300, orient=tk.HORIZONTAL,
                                  bg=Config.COLOR_PANEL, fg="white", highlightthickness=0)
        self.gen_scale.set(100)
        self.gen_scale.pack(fill=tk.X, padx=20, pady=5)

        # Botones
        self.btn_start = tk.Button(self.frame, text="Iniciar Simulación", bg=Config.COLOR_SUCCESS, fg="white",
                                   font=("Arial", 12, "bold"), command=main_window.start_simulation, height=2)
        self.btn_start.pack(fill=tk.X, pady=8, padx=20)

        self.btn_stop = tk.Button(self.frame, text="Detener", bg=Config.COLOR_DANGER, fg="white",
                                  font=("Arial", 12, "bold"), command=main_window.stop_simulation, 
                                  state=tk.DISABLED, height=2)
        self.btn_stop.pack(fill=tk.X, pady=5, padx=20)

        self.btn_optimize = tk.Button(self.frame, text="Optimizar con AG", bg=Config.COLOR_INFO, fg="white",
                                      font=("Arial", 12, "bold"), command=main_window.optimize_traffic, height=2)
        self.btn_optimize.pack(fill=tk.X, pady=8, padx=20)

        tk.Button(self.frame, text="Reiniciar Todo", bg="#95a5a6", fg="white",
                  font=("Arial", 11), command=main_window.reset_simulation, height=2).pack(fill=tk.X, pady=5, padx=20)

    def get_vehicle_count(self):
        return self.veh_scale.get()

    def get_generations(self):
        return self.gen_scale.get()

    def update_button_state(self, running):
        if running:
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
        else:
            self.btn_start.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)