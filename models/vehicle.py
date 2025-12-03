# models/vehicle.py - VERSIÓN CORREGIDA
import random
import math
from config import Config

class Vehicle:
    def __init__(self, vehicle_id, lane_start, lane_end, spawn_time, simulation):
        self.id = vehicle_id
        self.lane_start = lane_start
        self.lane_end = lane_end
        self.spawn_time = spawn_time
        self.simulation = simulation
        
        # Posición inicial y final
        self.x, self.y = self._get_spawn_position()
        self.target_x, self.target_y = self._get_target_position()
        
        # Velocidad
        self.base_speed = random.uniform(Config.VEHICLE_SPEED_MIN, Config.VEHICLE_SPEED_MAX)
        self.speed = self.base_speed
        
        # Estado
        self.waiting = False
        self.wait_time = 0
        self.total_travel_time = 0
        self.completed = False
        
        # Dirección normalizada
        self.direction = self._calculate_direction()

    def _get_spawn_position(self):
        x1, y1, x2, y2, direction = Config.LANES[self.lane_start]
        if direction == "horizontal":
            return (random.choice([x1 - 40, x2 + 40]), y1 + random.uniform(-8, 8))
        else:
            return (x1 + random.uniform(-8, 8), random.choice([y1 - 40, y2 + 40]))

    def _get_target_position(self):
        x1, y1, x2, y2, direction = Config.LANES[self.lane_end]
        if direction == "horizontal":
            return (x2 + 100 if self.x < x1 else x1 - 100, y1)
        else:
            return (x1, y2 + 100 if self.y < y1 else y1 - 100)

    def _calculate_direction(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return (0, 0)
        return (dx / dist, dy / dist)

    def is_going_north_south(self):
        """True si va principalmente vertical (Norte o Sur)"""
        return abs(self.direction[1]) > abs(self.direction[0])

    def get_nearest_light(self):
        """Devuelve el semáforo más cercano en dirección de avance"""
        nearest = None
        min_dist = float('inf')
        
        for light in self.simulation.traffic_lights:
            dist = math.hypot(light.x - self.x, light.y - self.y)
            
            if dist < 80:  # Solo si está cerca
                # Proyección: solo si la intersección está adelante
                to_light_x = light.x - self.x
                to_light_y = light.y - self.y
                dot = to_light_x * self.direction[0] + to_light_y * self.direction[1]
                
                if dot > 0 and dist < min_dist:
                    min_dist = dist
                    nearest = light
        
        return nearest

    def update(self, dt):
        if self.completed:
            return

        # ¿Llegó al final?
        if math.hypot(self.target_x - self.x, self.target_y - self.y) < 15:
            self.completed = True
            return

        # Buscar semáforo adelante
        light = self.get_nearest_light()
        must_stop = False

        if light:
            # Obtener estados de AMBAS direcciones
            ns_state, ew_state = light.get_states(self.simulation.current_time)
            
            going_ns = self.is_going_north_south()
            distance_to_light = math.hypot(self.x - light.x, self.y - light.y)

            # Lógica CORRECTA:
            # - Si va N-S → verifica el estado NS
            # - Si va E-O → verifica el estado EW
            if going_ns:
                # Va vertical (Norte-Sur)
                if ns_state in ["red", "yellow"]:
                    must_stop = True
            else:
                # Va horizontal (Este-Oeste)
                if ew_state in ["red", "yellow"]:
                    must_stop = True

            # Detenerse si está cerca de la intersección
            if must_stop and distance_to_light < 35:
                self.waiting = True
                self.speed = 0
                self.wait_time += dt
                return

        # Si no hay que parar → avanzar
        self.waiting = False
        self.speed = self.base_speed
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        self.total_travel_time += dt

    def draw(self, canvas):
        color = Config.VEHICLE_COLOR_WAITING if self.waiting else Config.VEHICLE_COLOR_MOVING
        
        # Dibujar carro según dirección
        if abs(self.direction[0]) > abs(self.direction[1]):  # Horizontal
            canvas.create_rectangle(
                self.x - 15, self.y - 8,
                self.x + 15, self.y + 8,
                fill=color, outline="white", width=2
            )
            # Ventanas
            canvas.create_rectangle(
                self.x - 8, self.y - 6,
                self.x + 8, self.y + 6,
                fill="#2c3e50"
            )
        else:  # Vertical
            canvas.create_rectangle(
                self.x - 8, self.y - 15,
                self.x + 8, self.y + 15,
                fill=color, outline="white", width=2
            )
            canvas.create_rectangle(
                self.x - 6, self.y - 8,
                self.x + 6, self.y + 8,
                fill="#2c3e50"
            )