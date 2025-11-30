import tkinter as tk
from tkinter import ttk
from config import Config

class ControlPanel(tk.Frame):
    def __init__(self, parent, callbacks):
        super().__init__(parent, bg=Config.COLOR_PANEL)
        self.callbacks = callbacks
        
        self.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Crea los widgets del panel de control"""
        
        # Título
        title = tk.Label(
            self,
            text="🎮 Controles",
            font=("Arial", 16, "bold"),
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_PRIMARY
        )
        title.pack(pady=10)
        
        # Parámetros
        params_frame = tk.LabelFrame(
            self,
            text="⚙️ Parámetros",
            font=("Arial", 12, "bold"),
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_TEXT,
            bd=2
        )
        params_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Spawn Rate
        tk.Label(
            params_frame,
            text="🚗 Vehículos/seg:",
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_TEXT,
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.spawn_rate_var = tk.IntVar(value=3)
        spawn_scale = tk.Scale(
            params_frame,
            from_=1,
            to=8,
            orient=tk.HORIZONTAL,
            variable=self.spawn_rate_var,
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_TEXT,
            highlightthickness=0,
            length=150
        )
        spawn_scale.grid(row=0, column=1, padx=5, pady=5)
        
        # Generaciones
        tk.Label(
            params_frame,
            text="🧬 Generaciones:",
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_TEXT,
            font=("Arial", 10)
        ).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.generations_var = tk.IntVar(value=100)
        gen_scale = tk.Scale(
            params_frame,
            from_=20,
            to=200,
            orient=tk.HORIZONTAL,
            variable=self.generations_var,
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_TEXT,
            highlightthickness=0,
            length=150
        )
        gen_scale.grid(row=1, column=1, padx=5, pady=5)
        
        # Botones
        buttons_frame = tk.Frame(self, bg=Config.COLOR_PANEL)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.btn_start = tk.Button(
            buttons_frame,
            text="▶️ Iniciar Simulación",
            command=self.callbacks['start'],
            bg=Config.COLOR_SUCCESS,
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=3,
            cursor="hand2"
        )
        self.btn_start.pack(fill=tk.X, pady=5)
        
        self.btn_stop = tk.Button(
            buttons_frame,
            text="⏸️ Detener",
            command=self.callbacks['stop'],
            bg=Config.COLOR_DANGER,
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.btn_stop.pack(fill=tk.X, pady=5)
        
        self.btn_optimize = tk.Button(
            buttons_frame,
            text="🧬 Optimizar con AG",
            command=self.callbacks['optimize'],
            bg=Config.COLOR_PRIMARY,
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.btn_optimize.pack(fill=tk.X, pady=5)
        
        self.btn_reset = tk.Button(
            buttons_frame,
            text="🔄 Reiniciar Todo",
            command=self.callbacks['reset'],
            bg=Config.COLOR_TEXT_SECONDARY,
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=3,
            cursor="hand2"
        )
        self.btn_reset.pack(fill=tk.X, pady=5)
        
        # Estado
        state_frame = tk.LabelFrame(
            self,
            text="📊 Estado",
            font=("Arial", 12, "bold"),
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_TEXT,
            bd=2
        )
        state_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_label = tk.Label(
            state_frame,
            text="🔴 Detenido",
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_DANGER,
            font=("Arial", 11, "bold")
        )
        self.status_label.pack(pady=5)
        
        self.time_label = tk.Label(
            state_frame,
            text="Tiempo: 0.0s",
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_TEXT,
            font=("Arial", 10)
        )
        self.time_label.pack(pady=2)
        
        self.optimized_label = tk.Label(
            state_frame,
            text="Optimizado: ❌",
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_TEXT,
            font=("Arial", 10)
        )
        self.optimized_label.pack(pady=2)
        
        # Estadísticas
        stats_frame = tk.LabelFrame(
            self,
            text="📈 Estadísticas",
            font=("Arial", 12, "bold"),
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_TEXT,
            bd=2
        )
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.stats_text = tk.Text(
            stats_frame,
            height=8,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT,
            font=("Courier", 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Leyenda
        legend_frame = tk.LabelFrame(
            self,
            text="📋 Leyenda",
            font=("Arial", 12, "bold"),
            bg=Config.COLOR_PANEL,
            fg=Config.COLOR_TEXT,
            bd=2
        )
        legend_frame.pack(fill=tk.X, padx=10, pady=10)
        
        legends = [
            ("🔵", "Vehículo en movimiento"),
            ("🔴", "Vehículo esperando"),
            ("🟢", "Semáforo verde"),
            ("🔴", "Semáforo rojo"),
        ]
        
        for symbol, text in legends:
            frame = tk.Frame(legend_frame, bg=Config.COLOR_PANEL)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(
                frame,
                text=symbol,
                bg=Config.COLOR_PANEL,
                font=("Arial", 10)
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                frame,
                text=text,
                bg=Config.COLOR_PANEL,
                fg=Config.COLOR_TEXT,
                font=("Arial", 9)
            ).pack(side=tk.LEFT)
    
    def update_state(self, is_running, is_optimized):
        """Actualiza el estado de los botones"""
        if is_running:
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.btn_optimize.config(state=tk.NORMAL if not is_optimized else tk.DISABLED)
            self.status_label.config(text="🟢 Activo", fg=Config.COLOR_SUCCESS)
        else:
            self.btn_start.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
            self.btn_optimize.config(state=tk.DISABLED)
            self.status_label.config(text="🔴 Detenido", fg=Config.COLOR_DANGER)
        
        opt_text = "✅" if is_optimized else "❌"
        self.optimized_label.config(text=f"Optimizado: {opt_text}")
    
    def update_stats(self, stats):
        """Actualiza las estadísticas"""
        self.time_label.config(text=f"Tiempo: {stats['time']}s")
        
        stats_text = f"""
Vehículos Totales: {stats['total_vehicles']}
Generados: {stats['total_spawned']}
Completados: {stats['completed']}
Esperando: {stats['waiting']}
Tiempo Espera Prom: {stats['avg_wait_time']}s
"""
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
    
    def get_spawn_rate(self):
        return self.spawn_rate_var.get()
    
    def get_generations(self):
        return self.generations_var.get()