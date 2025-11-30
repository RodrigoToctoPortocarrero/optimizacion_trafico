import random
import math
from config import Config

class Vehicle:
    def __init__(self, vehicle_id, lane_start, lane_end, spawn_time):
        self.id = vehicle_id
        self.lane_start = lane_start
        self.lane_end = lane_end
        self.spawn_time = spawn_time
        
        # Posición inicial en el carril
        self.x, self.y = self._get_spawn_position(lane_start)
        self.target_x, self.target_y = self._get_target_position(lane_end)
        
        # Velocidad y estado
        self.speed = random.uniform(Config.VEHICLE_SPEED_MIN, Config.VEHICLE_SPEED_MAX)
        self.base_speed = self.speed
        self.waiting = False
        self.wait_time = 0
        self.total_travel_time = 0
        self.completed = False
        
        # Dirección de movimiento
        self.direction = self._calculate_direction()
        
    def _get_spawn_position(self, lane):
        """Obtiene la posición inicial en el carril"""
        x1, y1, x2, y2, direction = Config.LANES[lane]
        
        if direction == "horizontal":
            # Spawn desde la izquierda o derecha
            if random.random() < 0.5:
                return (x1, y1)  # Desde izquierda
            else:
                return (x2, y1)  # Desde derecha
        else:  # vertical
            # Spawn desde arriba o abajo
            if random.random() < 0.5:
                return (x1, y1)  # Desde arriba
            else:
                return (x1, y2)  # Desde abajo
    
    def _get_target_position(self, lane):
        """Obtiene la posición objetivo en el carril"""
        x1, y1, x2, y2, direction = Config.LANES[lane]
        
        if direction == "horizontal":
            # Target es el extremo opuesto
            if self.x < Config.CANVAS_WIDTH / 2:
                return (x2, y1)  # Ir hacia la derecha
            else:
                return (x1, y1)  # Ir hacia la izquierda
        else:  # vertical
            # Target es el extremo opuesto
            if self.y < Config.CANVAS_HEIGHT / 2:
                return (x1, y2)  # Ir hacia abajo
            else:
                return (x1, y1)  # Ir hacia arriba
    
    def _calculate_direction(self):
        """Calcula la dirección normalizada del movimiento"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            return (dx / distance, dy / distance)
        return (0, 0)
    
    def check_intersection_ahead(self, intersections, distance=40):
        """Verifica si hay una intersección adelante"""
        for intersection in intersections:
            dist = math.sqrt((intersection['x'] - self.x)**2 + (intersection['y'] - self.y)**2)
            if dist < distance:
                # Verificar si el vehículo se está acercando
                to_intersection_x = intersection['x'] - self.x
                to_intersection_y = intersection['y'] - self.y
                
                # Producto punto para ver si va hacia la intersección
                dot_product = (to_intersection_x * self.direction[0] + 
                              to_intersection_y * self.direction[1])
                
                if dot_product > 0:  # Se está acercando
                    return intersection
        return None
    
    def update(self, traffic_lights, intersections, dt=1/60):
        """Actualiza la posición del vehículo"""
        if self.completed:
            return
        
        # Verificar si llegó al destino
        dist_to_target = math.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)
        if dist_to_target < 5:
            self.completed = True
            return
        
        # Verificar intersección adelante
        intersection_ahead = self.check_intersection_ahead(intersections)
        
        if intersection_ahead:
            light_state = traffic_lights.get(f"light_{intersection_ahead['id']}", "red")
            
            if light_state in ["red", "yellow"]:
                self.waiting = True
                self.wait_time += dt
                self.speed = 0
                return
        
        # Continuar movimiento
        self.waiting = False
        self.speed = self.base_speed
        
        # Mover en la dirección calculada
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        
        self.total_travel_time += dt
    
    def draw(self, canvas):
        """Dibuja el vehículo en el canvas"""
        color = Config.VEHICLE_COLOR_WAITING if self.waiting else Config.VEHICLE_COLOR_MOVING
        
        canvas.create_oval(
            self.x - Config.VEHICLE_SIZE,
            self.y - Config.VEHICLE_SIZE,
            self.x + Config.VEHICLE_SIZE,
            self.y + Config.VEHICLE_SIZE,
            fill=color,
            outline="#ffffff",
            width=2
        )