# models/traffic_light.py
class TrafficLight:
    def __init__(self, intersection_id, x, y, green_time=30, offset=0, is_north_south=True):
        self.id = intersection_id
        self.x = x
        self.y = y
        self.green_time = green_time
        self.offset = offset
        self.cycle_time = 60
        self.is_north_south = is_north_south  # True = controla Norte-Sur

    def update_state(self, current_time):
        effective_time = (current_time + self.offset) % self.cycle_time
        if effective_time < self.green_time:
            return "green" if self.is_north_south else "red"
        else:
            return "red" if self.is_north_south else "green"

    def draw(self, canvas, current_time):
        state = self.update_state(current_time)
        
        # Estado real de cada dirección
        ns_green = (self.is_north_south and state == "green")
        ew_green = (not self.is_north_south and state == "green")

        size = 14
        offset = 38

        # Norte
        color = "#00ff00" if ns_green else "#ff0000"
        canvas.create_oval(self.x - size, self.y - offset - size, self.x + size, self.y - offset + size,
                          fill=color, outline="white", width=2)
        canvas.create_text(self.x, self.y - offset - 22, text="N", fill="white", font=("Arial", 9, "bold"))

        # Sur
        canvas.create_oval(self.x - size, self.y + offset - size, self.x + size, self.y + offset + size,
                          fill=color, outline="white", width=2)
        canvas.create_text(self.x, self.y + offset + 22, text="S", fill="white", font=("Arial", 9, "bold"))

        # Este
        color_ew = "#00ff00" if ew_green else "#ff0000"
        canvas.create_oval(self.x + offset - size, self.y - size, self.x + offset + size, self.y + size,
                          fill=color_ew, outline="white", width=2)
        canvas.create_text(self.x + offset + 22, self.y, text="E", fill="white", font=("Arial", 9, "bold"))

        # Oeste
        canvas.create_oval(self.x - offset - size, self.y - size, self.x - offset + size, self.y + size,
                          fill=color_ew, outline="white", width=2)
        canvas.create_text(self.x - offset - 22, self.y, text="O", fill="white", font=("Arial", 9, "bold"))

        # Etiqueta del cruce
        canvas.create_text(self.x, self.y - 65, text=f"S{self.id}", fill="#f1c40f", font=("Arial", 16, "bold"))