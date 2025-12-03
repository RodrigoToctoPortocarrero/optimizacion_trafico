# gui/main_window.py - VERSIÓN CORREGIDA
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
        self.optimization_history = []

        self._create_layout()
        self._create_menu()

    def _create_layout(self):
        # === CABECERA ===
        header = tk.Frame(self.root, bg=Config.COLOR_PRIMARY, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(header, text="🚦 Sistema de Optimización de Tráfico", 
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

        self.control_panel = ControlPanel(left_panel, self)

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
        filemenu.add_command(label="📊 Ver Gráfico de Fitness", command=self.show_fitness_graph)
        filemenu.add_separator()
        filemenu.add_command(label="❌ Salir", command=self.root.quit)
        
        menubar.add_cascade(label="Archivo", menu=filemenu)
        self.root.config(menu=menubar)

    def show_fitness_graph(self):
        """Muestra el gráfico del algoritmo genético"""
        if self.ga and hasattr(self.ga, 'history') and self.ga.history:
            self.ga.show_graph()
        else:
            messagebox.showinfo(
                "Gráfico de Fitness", 
                "⚠️ No hay datos de optimización.\n\n"
                "Primero debes:\n"
                "1. Iniciar la simulación\n"
                "2. Hacer clic en 'Optimizar con AG'\n"
                "3. Esperar a que termine la optimización"
            )

    def start_simulation(self):
        """Inicia la simulación con semáforos DESORGANIZADOS"""
        if self.simulation and self.simulation.is_running:
            return
        
        vehicles = self.control_panel.get_vehicle_count()
        self.simulation = TrafficSimulation(total_vehicles=vehicles)
        self.simulation.start()
        self.control_panel.update_button_state(running=True)
        self.stats_panel.update_optimized(False)
        
        messagebox.showinfo(
            "Simulación Iniciada",
            f"✅ Simulación iniciada con {vehicles} vehículos iniciales\n\n"
            "⚠️ Los semáforos están DESORGANIZADOS\n"
            "💡 Usa 'Optimizar con AG' para mejorar el flujo"
        )
        
        self.animate()

    def stop_simulation(self):
        """Detiene la simulación"""
        if self.simulation:
            self.simulation.stop()
            self.control_panel.update_button_state(running=False)

    def reset_simulation(self):
        """Reinicia completamente la simulación"""
        self.stop_simulation()
        
        if self.simulation:
            self.simulation.reset()
        
        self.traffic_canvas.clear()
        self.stats_panel.clear()
        self.stats_panel.update_optimized(False)
        self.ga = None
        
        messagebox.showinfo("Reinicio Completo", "🔄 Sistema reiniciado completamente")

    def optimize_traffic(self):
        """Optimiza el tráfico con el Algoritmo Genético"""
        print("🔧 DEBUG: Botón Optimizar presionado")
        if not self.simulation or not self.simulation.is_running:
            messagebox.showwarning(
                "Advertencia", 
                "⚠️ Debes iniciar la simulación primero\n\n"
                "Haz clic en 'Iniciar Simulación'"
            )
            return

        generations = self.control_panel.get_generations()
        
        # Mostrar barra de progreso
        self.progress_bar.pack(pady=8)
        self.progress_label.pack(pady=2)
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = generations
        self.control_panel.btn_optimize.config(state=tk.DISABLED)
        self.progress_label.config(text="🧬 Iniciando optimización...")

        def progress_callback(gen, total, fitness):
            """Actualiza la barra de progreso"""
            self.progress_bar['value'] = gen + 1
            self.progress_label.config(
                text=f"🧬 Generación {gen+1}/{total} → Fitness: {fitness:.1f}"
            )
            self.root.update_idletasks()

        def run_optimization():
            """Ejecuta el AG en un thread separado"""
            # Obtener datos REALES del tráfico actual
            traffic_data = self.simulation.get_real_traffic_data()
            
            # Crear y ejecutar el algoritmo genético
            self.ga = GeneticAlgorithm(num_intersections=6)
            self.ga.generations = generations
            result = self.ga.optimize(traffic_data, callback=progress_callback)
            
            # Aplicar la solución (esto reinicia la simulación visualmente)
            self.simulation.apply_optimization(result['best_solution'])
            
            # Actualizar UI en el thread principal
            self.root.after(0, lambda: self._optimization_complete(result))

        # Iniciar optimización en thread
        threading.Thread(target=run_optimization, daemon=True).start()

    # En main_window.py, reemplazar SOLO el método _optimization_complete:

    # En main_window.py, busca y reemplaza SOLO el método _optimization_complete:

    def _optimization_complete(self, result):
        """Callback cuando termina la optimización"""
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()
        self.control_panel.btn_optimize.config(state=tk.NORMAL)
        
        # Calcular mejora real
        if result['history'] and len(result['history']) > 1:
            initial_fitness = result['history'][0]
            final_fitness = result['history'][-1]
            
            if initial_fitness > 0:
                improvement = ((initial_fitness - final_fitness) / initial_fitness) * 100
                if improvement > 0:
                    improvement_text = f"\n📈 MEJORA REAL: {improvement:.1f}%"
                    improvement_color = "#2ecc71"
                elif improvement < 0:
                    improvement_text = f"\n⚠️ Empeoró: {abs(improvement):.1f}%"
                    improvement_color = "#e74c3c"
                else:
                    improvement_text = "\n➡️ Sin cambios"
                    improvement_color = "#f39c12"
            else:
                improvement_text = "\n📈 Mejora significativa"
                improvement_color = "#2ecc71"
        else:
            improvement_text = "\n⚠️ No hay datos suficientes"
            improvement_color = "#f39c12"
        
        # Mostrar mensaje
        messagebox.showinfo(
            "✅ OPTIMIZACIÓN COMPLETADA",
            f"Fitness Inicial: {result['history'][0]:.2f}\n"
            f"Fitness Final: {result['best_fitness']:.2f}"
            f"{improvement_text}\n\n"
            "🎯 Los semáforos han sido REORGANIZADOS\n"
            "🚗 La simulación se ha REINICIADO\n"
            "📊 Observa la reducción en tiempos de espera\n\n"
            "💡 Usa 'Archivo > Ver Gráfico' para ver la evolución"
        )
        
        self.stats_panel.update_optimized(True)
        
        # ⚠️ ⚠️ ⚠️ COMENTA O ELIMINA ESTA LÍNEA PARA NO MOSTRAR GRÁFICO AUTOMÁTICO ⚠️ ⚠️ ⚠️
        # self.root.after(800, self.show_fitness_graph)  # <-- COMENTA ESTA LÍNEA
        
        # En su lugar, puedes dejar un pequeño delay para actualizar la UI
        self.root.after(500, lambda: None)  # Solo un pequeño delay

    def animate(self):
        """Loop de animación principal"""
        if self.simulation and self.simulation.is_running:
            dt = Config.UPDATE_INTERVAL / 1000.0
            self.simulation.update(dt)
            self.traffic_canvas.draw(self.simulation)
            self.stats_panel.update(self.simulation.get_statistics())
            self.root.after(Config.UPDATE_INTERVAL, self.animate)