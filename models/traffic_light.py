# models/traffic_light.py - LÓGICA REAL DE SEMÁFOROS
from config import Config

class TrafficLight:
    def __init__(self, intersection_id, x, y, green_time=30, offset=0, is_north_south=True):
        self.id = intersection_id
        self.x = x
        self.y = y
        self.green_time = green_time  # Tiempo que estará verde
        self.yellow_time = 3  # Tiempo de amarillo
        self.offset = offset  # Offset para sincronización
        self.cycle_time = 60  # Ciclo completo
        self.is_north_south = is_north_south  # True = controla Norte-Sur primero

    def get_states(self, current_time):
        """
        Devuelve el estado de AMBAS direcciones (NS y EW)
        REGLA: Si uno está verde, el otro DEBE estar rojo
        """
        effective_time = (current_time + self.offset) % self.cycle_time
        
        # Calcular tiempo de rojo (lo que queda del ciclo)
        red_time = self.cycle_time - self.green_time - self.yellow_time
        
        # Fases del ciclo:
        # 0 - green_time: NS verde
        # green_time - (green_time + yellow_time): NS amarillo
        # (green_time + yellow_time) - cycle_time: NS rojo (EW verde)
        
        if effective_time < self.green_time:
            # Norte-Sur VERDE, Este-Oeste ROJO
            ns_state = "green"
            ew_state = "red"
        elif effective_time < self.green_time + self.yellow_time:
            # Norte-Sur AMARILLO, Este-Oeste ROJO
            ns_state = "yellow"
            ew_state = "red"
        else:
            # Norte-Sur ROJO, Este-Oeste VERDE
            ns_state = "red"
            ew_state = "green"
        
        return ns_state, ew_state

    def update_state(self, current_time):
        """Devuelve el estado para compatibilidad (ya no se usa mucho)"""
        ns_state, ew_state = self.get_states(current_time)
        return ns_state if self.is_north_south else ew_state

    def draw(self, canvas, current_time):
        """Dibuja el semáforo con AMBAS direcciones"""
        ns_state, ew_state = self.get_states(current_time)
        
        size = 14
        offset = 38

        # NORTE-SUR (vertical)
        if ns_state == "green":
            ns_color = "#00ff00"
        elif ns_state == "yellow":
            ns_color = "#ffff00"
        else:
            ns_color = "#ff0000"

        # ESTE-OESTE (horizontal)
        if ew_state == "green":
            ew_color = "#00ff00"
        elif ew_state == "yellow":
            ew_color = "#ffff00"
        else:
            ew_color = "#ff0000"

        # Dibujar semáforos verticales (Norte y Sur)
        # Norte
        canvas.create_oval(
            self.x - size, self.y - offset - size,
            self.x + size, self.y - offset + size,
            fill=ns_color, outline="white", width=2
        )
        canvas.create_text(
            self.x, self.y - offset - 22,
            text="N", fill="white", font=("Arial", 9, "bold")
        )

        # Sur
        canvas.create_oval(
            self.x - size, self.y + offset - size,
            self.x + size, self.y + offset + size,
            fill=ns_color, outline="white", width=2
        )
        canvas.create_text(
            self.x, self.y + offset + 22,
            text="S", fill="white", font=("Arial", 9, "bold")
        )

        # Dibujar semáforos horizontales (Este y Oeste)
        # Este
        canvas.create_oval(
            self.x + offset - size, self.y - size,
            self.x + offset + size, self.y + size,
            fill=ew_color, outline="white", width=2
        )
        canvas.create_text(
            self.x + offset + 22, self.y,
            text="E", fill="white", font=("Arial", 9, "bold")
        )

        # Oeste
        canvas.create_oval(
            self.x - offset - size, self.y - size,
            self.x - offset + size, self.y + size,
            fill=ew_color, outline="white", width=2
        )
        canvas.create_text(
            self.x - offset - 22, self.y,
            text="O", fill="white", font=("Arial", 9, "bold")
        )

        # Etiqueta del semáforo
        canvas.create_text(
            self.x, self.y - 65,
            text=f"S{self.id}",
            fill="#f1c40f",
            font=("Arial", 16, "bold")
        )