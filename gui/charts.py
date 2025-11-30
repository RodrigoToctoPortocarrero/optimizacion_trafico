import tkinter as tk
from tkinter import ttk
from config import Config

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
        
    def draw_chart(self):
        """Dibuja el gráfico de evolución del fitness"""
        self.canvas.delete("all")
        
        generations, best, avg, min_fit = self.ga.get_history_data()
        
        if not generations:
            self.canvas.create_text(
                425, 250,
                text="No hay datos para mostrar",
                font=("Arial", 14),
                fill=Config.COLOR_TEXT_SECONDARY
            )
            return
        
        # Configuración del gráfico
        padding = 60
        width = 850 - 2 * padding
        height = 500 - 2 * padding
        
        max_gen = max(generations)
        max_fitness = max(best + avg)
        min_fitness_val = min(min_fit + avg)
        
        # Escalar datos
        def scale_x(gen):
            return padding + (gen / max_gen) * width
        
        def scale_y(fitness):
            range_fit = max_fitness - min_fitness_val
            if range_fit == 0:
                return padding + height / 2
            return padding + height - ((fitness - min_fitness_val) / range_fit) * height
        
        # Dibujar ejes
        self.canvas.create_line(
            padding, padding + height,
            padding + width, padding + height,
            width=2, fill="black"
        )
        self.canvas.create_line(
            padding, padding,
            padding, padding + height,
            width=2, fill="black"
        )
        
        # Etiquetas de ejes
        self.canvas.create_text(
            padding + width / 2, padding + height + 40,
            text="Generaciones",
            font=("Arial", 12, "bold")
        )
        
        self.canvas.create_text(
            padding - 40, padding + height / 2,
            text="Fitness",
            font=("Arial", 12, "bold"),
            angle=90
        )
        
        # Título
        self.canvas.create_text(
            padding + width / 2, 20,
            text="Evolución del Fitness del Algoritmo Genético",
            font=("Arial", 14, "bold"),
            fill=Config.COLOR_PRIMARY
        )
        
        # Dibujar líneas de datos
        colors = {
            'best': Config.COLOR_SUCCESS,
            'avg': Config.COLOR_WARNING,
            'min': Config.COLOR_DANGER
        }
        
        # Mejor fitness
        for i in range(len(generations) - 1):
            x1 = scale_x(generations[i])
            y1 = scale_y(best[i])
            x2 = scale_x(generations[i + 1])
            y2 = scale_y(best[i + 1])
            self.canvas.create_line(x1, y1, x2, y2, fill=colors['best'], width=2)
        
        # Fitness promedio
        for i in range(len(generations) - 1):
            x1 = scale_x(generations[i])
            y1 = scale_y(avg[i])
            x2 = scale_x(generations[i + 1])
            y2 = scale_y(avg[i + 1])
            self.canvas.create_line(x1, y1, x2, y2, fill=colors['avg'], width=2)
        
        # Fitness mínimo
        for i in range(len(generations) - 1):
            x1 = scale_x(generations[i])
            y1 = scale_y(min_fit[i])
            x2 = scale_x(generations[i + 1])
            y2 = scale_y(min_fit[i + 1])
            self.canvas.create_line(x1, y1, x2, y2, fill=colors['min'], width=2)
        
        # Leyenda
        legend_x = padding + width - 150
        legend_y = padding + 20
        
        legends = [
            ("Mejor Fitness", colors['best']),
            ("Fitness Promedio", colors['avg']),
            ("Fitness Mínimo", colors['min'])
        ]
        
        for i, (label, color) in enumerate(legends):
            y = legend_y + i * 25
            self.canvas.create_line(
                legend_x, y, legend_x + 30, y,
                fill=color, width=3
            )
            self.canvas.create_text(
                legend_x + 40, y,
                text=label,
                anchor=tk.W,
                font=("Arial", 10)
            )
        
        # Marcadores en los ejes
        num_markers = 5
        
        # Marcadores X (generaciones)
        for i in range(num_markers + 1):
            gen = int((max_gen / num_markers) * i)
            x = scale_x(gen)
            self.canvas.create_line(x, padding + height, x, padding + height + 5, width=1)
            self.canvas.create_text(
                x, padding + height + 20,
                text=str(gen),
                font=("Arial", 9)
            )
        
        # Marcadores Y (fitness)
        for i in range(num_markers + 1):
            fitness = min_fitness_val + ((max_fitness - min_fitness_val) / num_markers) * i
            y = scale_y(fitness)
            self.canvas.create_line(padding - 5, y, padding, y, width=1)
            self.canvas.create_text(
                padding - 20, y,
                text=f"{fitness:.1f}",
                font=("Arial", 9)
            )