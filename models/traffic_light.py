from config import Config

class TrafficLight:
    def __init__(self, intersection_id, x, y, green_time=30, offset=0):
        self.id = intersection_id
        self.x = x
        self.y = y
        self.green_time = green_time
        self.yellow_time = 3
        self.offset = offset
        self.cycle_time = Config.GA_CYCLE_TIME
        
        self.current_state = "red"
        
    def update_state(self, current_time):
        """Actualiza el estado del semáforo según el tiempo"""
        adjusted_time = (current_time + self.offset) % self.cycle_time
        
        if adjusted_time < self.green_time:
            self.current_state = "green"
        elif adjusted_time < self.green_time + self.yellow_time:
            self.current_state = "yellow"
        else:
            self.current_state = "red"
        
        return self.current_state
    
    def draw(self, canvas):
        """Dibuja el semáforo en el canvas"""
        size = Config.LIGHT_SIZE
        
        # Posición ajustada (esquina superior derecha de la intersección)
        light_x = self.x + 30
        light_y = self.y - 30
        
        # Fondo del semáforo
        canvas.create_rectangle(
            light_x - size/2,
            light_y - size/2,
            light_x + size/2,
            light_y + size/2,
            fill=Config.LIGHT_BG,
            outline="#2c3e50",
            width=3
        )
        
        # Determinar color de la luz activa
        if self.current_state == "green":
            light_color = Config.LIGHT_GREEN
        elif self.current_state == "red":
            light_color = Config.LIGHT_RED
        elif self.current_state == "yellow":
            light_color = Config.LIGHT_YELLOW
        else:
            light_color = Config.LIGHT_OFF
        
        # Dibujar luz con brillo
        canvas.create_oval(
            light_x - 12,
            light_y - 12,
            light_x + 12,
            light_y + 12,
            fill=light_color,
            outline="#ffffff",
            width=2
        )
        
        # Agregar efecto de brillo con círculo más pequeño
        canvas.create_oval(
            light_x - 6,
            light_y - 6,
            light_x + 6,
            light_y + 6,
            fill="#ffffff",
            outline=""
        )
        
        # Etiqueta del semáforo
        canvas.create_text(
            light_x,
            light_y + size/2 + 12,
            text=f"S{self.id}",
            fill="#ffffff",
            font=("Arial", 10, "bold")
        )