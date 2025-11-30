# gui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from gui.control_panel import ControlPanel
from gui.traffic_canvas import TrafficCanvas
from gui.statistics_panel import StatisticsPanel
from traffic_simulation import TrafficSimulation
from genetic_algorithm import GeneticAlgorithm
from config import Config

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.configure(bg=Config.COLOR_BG)

        self.simulation = None
        self.ga = None

        self._create_layout()
        self._create_menu()

    def _create_layout(self):
        # === CABECERA ===
        header = tk.Frame(self.root, bg=Config.COLOR_PRIMARY, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(header, text="Sistema de Optimización de Tráfico", 
                         font=("Arial", 24, "bold"), fg="white", bg=Config.COLOR_PRIMARY)
        title.pack(expand=True)
        
        subtitle = tk.Label(header, text="Simulación con Algoritmo Genético", 
                            font=("Arial", 14), fg="#bdc3c7", bg=Config.COLOR_PRIMARY)
        subtitle.pack()

        # === CONTENIDO PRINCIPAL ===
        main_frame = tk.Frame(self.root, bg=Config.COLOR_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel izquierdo - Controles
        left_panel = tk.Frame(main_frame, bg=Config.COLOR_SECONDARY, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)

        self.control_panel = ControlPanel(left_panel, self)  # ← pack ya se hace dentro del ControlPanel

        # Canvas central
        canvas_frame = tk.Frame(main_frame, bg=Config.CANVAS_BG)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.traffic_canvas = TrafficCanvas(canvas_frame)
        self.traffic_canvas.canvas.pack(fill=tk.BOTH, expand=True)

        # Panel derecho - Estadísticas
        right_panel = tk.Frame(main_frame, bg=Config.COLOR_SECONDARY, width=280)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_panel.pack_propagate(False)

        self.stats_panel = StatisticsPanel(right_panel)

        # Barra de progreso (oculta al inicio)
        self.progress_bar = ttk.Progressbar(self.root, mode='determinate', length=600)
        self.progress_label = tk.Label(self.root, text="", fg="#00ff00", bg=Config.COLOR_BG, 
                                       font=("Arial", 11, "bold"))

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Ver Gráfico de Optimización", command=self.show_fitness_graph)
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.root.quit)
        
        menubar.add_cascade(label="Archivo", menu=filemenu)
        self.root.config(menu=menubar)

    def show_fitness_graph(self):
        """Abre el gráfico desde el menú en cualquier momento"""
        if hasattr(self, 'ga') and self.ga and hasattr(self.ga, 'history') and self.ga.history:
            self.ga.show_graph()
        else:
            messagebox.showinfo("Gráfico de Fitness", "No hay datos de optimización aún.\nEjecuta 'Optimizar con AG' primero.")

    def start_simulation(self):
        if self.simulation and self.simulation.is_running:
            return
        vehicles = self.control_panel.get_vehicle_count()
        self.simulation = TrafficSimulation(total_vehicles=vehicles)
        self.simulation.start()
        self.control_panel.update_button_state(running=True)
        self.animate()

    def stop_simulation(self):
        if self.simulation:
            self.simulation.stop()
            self.control_panel.update_button_state(running=False)

    def reset_simulation(self):
        self.stop_simulation()
        if self.simulation:
            self.simulation.reset()
        self.traffic_canvas.clear()
        self.stats_panel.clear()
        self.stats_panel.update_optimized(False)

    def optimize_traffic(self):
        if not self.simulation or not self.simulation.is_running:
            messagebox.showwarning("Advertencia", "Primero inicia la simulación.")
            return

        generations = self.control_panel.get_generations()
        self.ga = GeneticAlgorithm(num_intersections=6)  # ← Guardamos la instancia
        self.progress_bar.pack(pady=8)
        self.progress_label.pack(pady=2)
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = generations
        self.control_panel.btn_optimize.config(state=tk.DISABLED)
        self.progress_label.config(text="Iniciando optimización...")

        def progress_callback(gen, total, fitness):
            self.progress_bar['value'] = gen + 1
            self.progress_label.config(text=f"Generación {gen+1}/{total} → Fitness: {fitness:.1f}")
            self.root.update_idletasks()

        def run_optimization():
            # DATOS REALES EN TIEMPO REAL
            traffic_data = self.simulation.get_real_traffic_data()
            self.ga = GeneticAlgorithm(num_intersections=6)
            self.ga.generations = generations
            result = self.ga.optimize(traffic_data, callback=progress_callback)

            # APLICAR SOLUCIÓN
            self.simulation.apply_optimization(result['best_solution'])

            self.root.after(0, lambda: self._optimization_complete(result))

        threading.Thread(target=run_optimization, daemon=True).start()

    def _optimization_complete(self, result):
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()
        self.control_panel.btn_optimize.config(state=tk.NORMAL)
        messagebox.showinfo("¡ÉXITO!", 
                            f"Optimización completada\nFitness final: {result['best_fitness']:.0f}\n"
                            "¡Ola verde activada!")
        self.stats_panel.update_optimized(True)

    def animate(self):
        if self.simulation and self.simulation.is_running:
            dt = Config.UPDATE_INTERVAL / 1000.0
            self.simulation.update(dt)
            self.traffic_canvas.draw(self.simulation)
            self.stats_panel.update(self.simulation.get_statistics())
            self.root.after(Config.UPDATE_INTERVAL, self.animate)