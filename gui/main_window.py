import tkinter as tk
from tkinter import messagebox, ttk
import threading
from config import Config
from traffic_simulation import TrafficSimulation
from genetic_algorithm import GeneticAlgorithm
from gui.traffic_canvas import TrafficCanvas
from gui.control_panel import ControlPanel
from gui.charts import ChartWindow

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.configure(bg=Config.COLOR_BG)
        self.root.resizable(False, False)
        
        # Simulación y AG
        self.simulation = None
        self.ga = None
        self.animation_running = False
        
        self._create_layout()
        self._setup_menu()
        
    def _create_layout(self):
        """Crea el layout principal"""
        # Header
        header = tk.Frame(self.root, bg=Config.COLOR_PRIMARY, height=80)
        header.pack(fill=tk.X)
        
        title_label = tk.Label(
            header,
            text="🚦 Sistema de Optimización de Tráfico",
            font=("Arial", 24, "bold"),
            bg=Config.COLOR_PRIMARY,
            fg="white"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header,
            text="Simulación con Algoritmo Genético",
            font=("Arial", 12),
            bg=Config.COLOR_PRIMARY,
            fg="white"
        )
        subtitle_label.pack()
        
        # Contenedor principal
        main_container = tk.Frame(self.root, bg=Config.COLOR_BG)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Panel de control (izquierda)
        self.control_panel = ControlPanel(
            main_container,
            callbacks={
                'start': self.start_simulation,
                'stop': self.stop_simulation,
                'optimize': self.optimize_traffic,
                'reset': self.reset_system
            }
        )
        
        # Canvas de simulación (derecha)
        canvas_frame = tk.Frame(main_container, bg=Config.COLOR_BG)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.traffic_canvas = TrafficCanvas(canvas_frame)
        
        # Barra de progreso (para optimización)
        self.progress_frame = tk.Frame(canvas_frame, bg=Config.COLOR_BG)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT,
            font=("Arial", 10)
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=Config.CANVAS_WIDTH - 40
        )
        
    def _setup_menu(self):
        """Configura el menú de la aplicación"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Reiniciar", command=self.reset_system)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Herramientas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Ver Gráficos AG", command=self.show_charts)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Instrucciones", command=self.show_instructions)
        help_menu.add_command(label="Acerca de", command=self.show_about)
    
    def start_simulation(self):
        """Inicia la simulación"""
        spawn_rate = self.control_panel.get_spawn_rate()
        
        self.simulation = TrafficSimulation(spawn_rate=spawn_rate)
        self.simulation.start()
        
        self.control_panel.update_state(True, False)
        
        # Iniciar animación
        self.animation_running = True
        self.animate()
        
        messagebox.showinfo(
            "Simulación Iniciada",
            f"Simulación iniciada con {spawn_rate} vehículos/segundo.\nLos semáforos están desorganizados."
        )
    
    def stop_simulation(self):
        """Detiene la simulación"""
        if self.simulation:
            self.simulation.stop()
        
        self.animation_running = False
        self.control_panel.update_state(False, self.simulation.is_optimized if self.simulation else False)
        
        messagebox.showinfo("Simulación Detenida", "La simulación ha sido detenida.")
    
    def optimize_traffic(self):
        """Optimiza el tráfico con el algoritmo genético"""
        if not self.simulation or not self.simulation.is_running:
            messagebox.showwarning("Advertencia", "Debe iniciar la simulación primero.")
            return
        
        generations = self.control_panel.get_generations()
        
        # Mostrar barra de progreso
        self.progress_bar.pack(pady=5)
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = generations
        
        # Deshabilitar botón
        self.control_panel.btn_optimize.config(state=tk.DISABLED)
        
        def progress_callback(gen, total, fitness):
            """Callback para actualizar progreso"""
            self.progress_bar['value'] = gen + 1
            self.progress_label.config(
                text=f"Optimizando... Generación {gen + 1}/{total} | Fitness: {fitness:.2f}"
            )
            self.root.update_idletasks()
        
        def run_optimization():
            """Ejecuta la optimización en un thread separado"""
            # Datos de tráfico simulados
            traffic_data = {
                f"queue_{i}": 5 for i in range(6)
            }
            traffic_data.update({
                f"flow_{i}": 10 for i in range(6)
            })
            
            # Ejecutar AG
            self.ga = GeneticAlgorithm(num_intersections=6)
            self.ga.generations = generations
            result = self.ga.optimize(traffic_data, callback=progress_callback)
            
            # Aplicar solución
            self.simulation.apply_optimization(result['best_solution'])
            
            # Actualizar UI
            self.root.after(100, lambda: self._optimization_complete(result))
        
        # Iniciar optimización en thread
        thread = threading.Thread(target=run_optimization)
        thread.daemon = True
        thread.start()
    
    def _optimization_complete(self, result):
        """Callback cuando termina la optimización"""
        self.progress_bar.pack_forget()
        self.progress_label.config(text="")
        
        self.control_panel.update_state(True, True)
        
        messagebox.showinfo(
            "Optimización Completada",
            f"¡Optimización exitosa!\n\nFitness Final: {result['best_fitness']:.2f}\n\n"
            f"Los semáforos han sido reorganizados para mejorar el flujo."
        )
        
        # Mostrar gráficos automáticamente
        self.show_charts()
    
    def reset_system(self):
        """Reinicia todo el sistema"""
        self.animation_running = False
        
        if self.simulation:
            self.simulation.reset()
        
        self.ga = None
        self.traffic_canvas.clear()
        
        self.control_panel.update_state(False, False)
        self.control_panel.update_stats({
            'total_vehicles': 0,
            'total_spawned': 0,
            'completed': 0,
            'waiting': 0,
            'avg_wait_time': 0,
            'time': 0
        })
        
        messagebox.showinfo("Sistema Reiniciado", "El sistema ha sido reiniciado completamente.")
    
    def show_charts(self):
        """Muestra la ventana de gráficos"""
        if not self.ga or not self.ga.history:
            messagebox.showwarning(
                "Sin Datos",
                "No hay datos de optimización para mostrar.\nEjecute la optimización primero."
            )
            return
        
        ChartWindow(self.root, self.ga)
    
    def show_instructions(self):
        """Muestra las instrucciones"""
        instructions = """
🚦 INSTRUCCIONES DEL SISTEMA

1. Ajuste los parámetros de simulación:
   - Vehículos/segundo: Controla cuántos carros aparecen
   - Generaciones: Iteraciones del algoritmo genético

2. Haga clic en "Iniciar Simulación"
   Los vehículos comenzarán a aparecer con semáforos desorganizados

3. Observe el tráfico:
   - Círculos azules: vehículos en movimiento
   - Círculos rojos: vehículos esperando
   - Semáforos brillan en verde (avanzar) o rojo (detener)

4. Cuando vea congestión, use "Optimizar con AG"
   El algoritmo genético encontrará la mejor configuración

5. Los semáforos se reorganizarán automáticamente
   El flujo mejorará y las esperas disminuirán

6. Use "Ver Gráficos AG" para analizar la evolución del fitness
"""
        messagebox.showinfo("Instrucciones", instructions)
    
    def show_about(self):
        """Muestra información sobre la aplicación"""
        about = """
🚦 Sistema de Optimización de Tráfico
Versión 2.0

Desarrollado con:
- Python 3.x
- Tkinter (Interfaz Gráfica)
- Algoritmo Genético

Características:
✓ Simulación de tráfico en tiempo real
✓ Optimización con algoritmo genético
✓ Visualización interactiva
✓ Gráficos de evolución
✓ Semáforos inteligentes

© 2024 - Sistema de IA para Gestión de Tráfico
"""
        messagebox.showinfo("Acerca de", about)
    
    def animate(self):
        """Loop de animación"""
        if not self.animation_running or not self.simulation:
            return
        
        # Actualizar simulación
        self.simulation.update(1/Config.FPS)
        
        # Dibujar en el canvas
        self.simulation.draw(self.traffic_canvas)
        
        # Actualizar estadísticas
        stats = self.simulation.get_statistics()
        self.control_panel.update_stats(stats)
        
        # Programar siguiente frame
        self.root.after(Config.UPDATE_INTERVAL, self.animate)
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()