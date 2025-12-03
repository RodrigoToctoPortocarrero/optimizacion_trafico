import tkinter as tk
from tkinter import ttk
from config import Config
#charts.py
class ChartWindow(tk.Toplevel):
    def __init__(self, parent, ga):
        super().__init__(parent)
        self.title("📊 Progreso del Algoritmo Genético")
        self.geometry("900x600")
        self.configure(bg=Config.COLOR_BG)
        
        self.ga = ga
        
        # Canvas para el gráfico
        self.canvas = tk.Canvas(
            self,
            width=850,
            height=500,
            bg="white",
            highlightthickness=2,
            highlightbackground=Config.COLOR_PRIMARY
        )
        self.canvas.pack(padx=20, pady=20)
        
        self.draw_chart()
        
    # En charts.py, actualizar el método draw_chart:

    def draw_chart(self):
        """Dibuja el gráfico de evolución del fitness con mejor presentación"""
        self.canvas.delete("all")
        
        generations, best, avg, min_fit = self.ga.get_history_data()
        
        if not generations or len(generations) < 2:
            self.canvas.create_text(
                425, 250,
                text="No hay suficientes datos para mostrar\n\n"
                    "Ejecuta la optimización completa primero",
                font=("Arial", 14),
                fill=Config.COLOR_TEXT_SECONDARY,
                justify=tk.CENTER
            )
            return
        
        # Configuración del gráfico
        padding = 80
        width = 850 - 2 * padding
        height = 500 - 2 * padding
        
        max_gen = max(generations)
        all_fitness = best + avg + min_fit
        max_fitness = max(all_fitness)
        min_fitness_val = min(all_fitness)
        
        # Asegurar rango visible
        if max_fitness - min_fitness_val < 10:
            max_fitness = min_fitness_val + 20
        
        # Escalar datos
        def scale_x(gen):
            return padding + (gen / max_gen) * width
        
        def scale_y(fitness):
            range_fit = max_fitness - min_fitness_val
            if range_fit == 0:
                return padding + height / 2
            # Invertir Y: menor fitness más arriba
            normalized = (fitness - min_fitness_val) / range_fit
            return padding + height - (normalized * height)
        
        # Dibujar fondo del gráfico
        self.canvas.create_rectangle(
            padding, padding,
            padding + width, padding + height,
            fill="#1a1a2e", outline=Config.COLOR_PRIMARY, width=2
        )
        
        # Dibujar ejes
        self.canvas.create_line(
            padding, padding + height,
            padding + width, padding + height,
            width=3, fill="white"
        )
        self.canvas.create_line(
            padding, padding,
            padding, padding + height,
            width=3, fill="white"
        )
        
        # Título
        self.canvas.create_text(
            425, 30,
            text="📈 EVOLUCIÓN DEL FITNESS - ALGORITMO GENÉTICO",
            font=("Arial", 16, "bold"),
            fill=Config.COLOR_ACCENT
        )
        
        # Etiquetas de ejes
        self.canvas.create_text(
            padding + width / 2, padding + height + 45,
            text="Generación",
            font=("Arial", 12, "bold"),
            fill="white"
        )
        
        self.canvas.create_text(
            padding - 45, padding + height / 2,
            text="Fitness (menor = mejor)",
            font=("Arial", 12, "bold"),
            fill="white",
            angle=90
        )
        
        # Dibujar líneas de datos con suavizado
        colors = {
            'best': "#00ff88",  # Verde brillante
            'avg': "#ff9900",   # Naranja
            'min': "#ff4444"    # Rojo
        }
        
        # Mejor fitness (línea principal)
        points_best = []
        for i, gen in enumerate(generations):
            x = scale_x(gen)
            y = scale_y(best[i])
            points_best.append((x, y))
        
        # Dibujar línea suavizada para mejor fitness
        for i in range(len(points_best) - 1):
            x1, y1 = points_best[i]
            x2, y2 = points_best[i + 1]
            
            # Línea principal
            self.canvas.create_line(x1, y1, x2, y2, 
                                fill=colors['best'], width=3, 
                                smooth=True)
            
            # Efecto brillante
            self.canvas.create_line(x1, y1, x2, y2, 
                                fill="#ffffff", width=1, 
                                smooth=True)
        
        # Fitness promedio
        for i in range(len(generations) - 1):
            x1 = scale_x(generations[i])
            y1 = scale_y(avg[i])
            x2 = scale_x(generations[i + 1])
            y2 = scale_y(avg[i + 1])
            self.canvas.create_line(x1, y1, x2, y2, 
                                fill=colors['avg'], width=2, 
                                dash=(4, 2))
        
        # Fitness mínimo
        for i in range(len(generations) - 1):
            x1 = scale_x(generations[i])
            y1 = scale_y(min_fit[i])
            x2 = scale_x(generations[i + 1])
            y2 = scale_y(min_fit[i + 1])
            self.canvas.create_line(x1, y1, x2, y2, 
                                fill=colors['min'], width=1, 
                                dash=(2, 2))
        
        # Leyenda
        legend_x = padding + width - 180
        legend_y = padding + 25
        
        legends = [
            ("Mejor Fitness", colors['best']),
            ("Fitness Promedio", colors['avg']),
            ("Peor Fitness", colors['min'])
        ]
        
        for i, (label, color) in enumerate(legends):
            y = legend_y + i * 28
            self.canvas.create_line(
                legend_x, y, legend_x + 40, y,
                fill=color, width=3
            )
            self.canvas.create_text(
                legend_x + 50, y,
                text=label,
                anchor=tk.W,
                font=("Arial", 10, "bold"),
                fill="white"
            )
        
        # Marcadores en los ejes
        num_markers = min(10, max_gen)
        
        # Marcadores X (generaciones)
        for i in range(num_markers + 1):
            gen = int((max_gen / num_markers) * i)
            x = scale_x(gen)
            self.canvas.create_line(x, padding + height, x, padding + height + 8, 
                                width=2, fill="white")
            self.canvas.create_text(
                x, padding + height + 25,
                text=str(gen),
                font=("Arial", 9, "bold"),
                fill="white"
            )
        
        # Marcadores Y (fitness)
        for i in range(6):  # 6 marcadores en Y
            fitness_val = min_fitness_val + ((max_fitness - min_fitness_val) / 5) * i
            y = scale_y(fitness_val)
            self.canvas.create_line(padding - 8, y, padding, y, 
                                width=2, fill="white")
            self.canvas.create_text(
                padding - 15, y,
                text=f"{fitness_val:.1f}",
                font=("Arial", 9, "bold"),
                fill="white",
                anchor=tk.E
            )
        
        # Anotación de mejora
        if len(best) > 1:
            improvement = ((best[0] - best[-1]) / best[0]) * 100 if best[0] > 0 else 0
            
            if improvement > 0:
                mejora_text = f"MEJORA: {improvement:.1f}%"
                mejora_color = "#00ff88"
            else:
                mejora_text = f"CAMBIO: {improvement:.1f}%"
                mejora_color = "#ff9900"
            
            self.canvas.create_text(
                padding + 100, padding + 35,
                text=mejora_text,
                font=("Arial", 12, "bold"),
                fill=mejora_color,
                anchor=tk.W
            )