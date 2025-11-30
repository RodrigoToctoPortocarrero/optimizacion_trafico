import random
import time
from models.vehicle import Vehicle
from models.traffic_light import TrafficLight
from config import Config

class TrafficSimulation:
    def __init__(self, spawn_rate=3):
        self.spawn_rate = spawn_rate
        self.vehicles = []
        self.traffic_lights = []
        self.vehicle_id_counter = 0
        self.current_time = 0
        self.next_spawn_time = 0
        self.is_running = False
        self.is_optimized = False
        
        # Crear semáforos en las intersecciones
        self._create_traffic_lights()
        
        # Estadísticas
        self.total_spawned = 0
        self.total_completed = 0
        
    def _create_traffic_lights(self):
        """Crea los semáforos en las intersecciones"""
        self.traffic_lights = []
        for intersection in Config.INTERSECTIONS:
            # Configuración inicial desorganizada
            green_time = random.randint(20, 50)
            offset = random.randint(0, 60)
            
            light = TrafficLight(
                intersection['id'],
                intersection['x'],
                intersection['y'],
                green_time=green_time,
                offset=offset
            )
            self.traffic_lights.append(light)
    
    def start(self):
        """Inicia la simulación"""
        self.is_running = True
        self.current_time = 0
        self.next_spawn_time = 0
    
    def stop(self):
        """Detiene la simulación"""
        self.is_running = False
    
    def reset(self):
        """Reinicia la simulación"""
        self.vehicles = []
        self.vehicle_id_counter = 0
        self.current_time = 0
        self.next_spawn_time = 0
        self.total_spawned = 0
        self.total_completed = 0
        self.is_optimized = False
        self._create_traffic_lights()
    
    def apply_optimization(self, solution):
        """Aplica la solución del algoritmo genético"""
        for i, light in enumerate(self.traffic_lights):
            if i < len(solution):
                light.green_time = solution[i][0]
                light.offset = solution[i][2]
        
        self.is_optimized = True
    
    def spawn_vehicle(self):
        """Genera un nuevo vehículo en un carril aleatorio"""
        # Seleccionar carril de inicio y fin diferentes
        lane_start = random.randint(0, len(Config.LANES) - 1)
        lane_end = random.randint(0, len(Config.LANES) - 1)
        
        while lane_end == lane_start:
            lane_end = random.randint(0, len(Config.LANES) - 1)
        
        vehicle = Vehicle(
            self.vehicle_id_counter,
            lane_start,
            lane_end,
            self.current_time
        )
        
        self.vehicles.append(vehicle)
        self.vehicle_id_counter += 1
        self.total_spawned += 1
    
    def update(self, dt):
        """Actualiza la simulación"""
        if not self.is_running:
            return
        
        self.current_time += dt
        
        # Generar nuevos vehículos
        if self.current_time >= self.next_spawn_time:
            self.spawn_vehicle()
            self.next_spawn_time = self.current_time + (1.0 / self.spawn_rate)
        
        # Actualizar estados de semáforos
        traffic_light_states = {}
        for light in self.traffic_lights:
            state = light.update_state(self.current_time)
            traffic_light_states[f"light_{light.id}"] = state
        
        # Actualizar vehículos
        for vehicle in self.vehicles[:]:
            vehicle.update(traffic_light_states, Config.INTERSECTIONS, dt)
            
            if vehicle.completed:
                self.vehicles.remove(vehicle)
                self.total_completed += 1
    
    def get_statistics(self):
        """Obtiene estadísticas de la simulación"""
        waiting_vehicles = sum(1 for v in self.vehicles if v.waiting)
        
        avg_wait_time = 0
        if self.vehicles:
            avg_wait_time = sum(v.wait_time for v in self.vehicles) / len(self.vehicles)
        
        return {
            "total_vehicles": len(self.vehicles),
            "total_spawned": self.total_spawned,
            "completed": self.total_completed,
            "waiting": waiting_vehicles,
            "avg_wait_time": round(avg_wait_time, 2),
            "time": round(self.current_time, 1)
        }
    
    def draw(self, canvas):
        """Dibuja la simulación completa"""
        # Limpiar canvas
        canvas.delete("all")
        
        # Dibujar carreteras
        self._draw_roads(canvas)
        
        # Dibujar semáforos
        for light in self.traffic_lights:
            light.draw(canvas)
        
        # Dibujar vehículos
        for vehicle in self.vehicles:
            vehicle.draw(canvas)
    
    def _draw_roads(self, canvas):
        """Dibuja las carreteras y carriles"""
        # Dibujar carreteras horizontales
        for y in [200, 450]:
            canvas.create_rectangle(
                0, y - Config.ROAD_WIDTH/2,
                Config.CANVAS_WIDTH, y + Config.ROAD_WIDTH/2,
                fill=Config.ROAD_COLOR,
                outline=""
            )
        
        # Dibujar carreteras verticales
        for x in [250, 550, 850]:
            canvas.create_rectangle(
                x - Config.ROAD_WIDTH/2, 0,
                x + Config.ROAD_WIDTH/2, Config.CANVAS_HEIGHT,
                fill=Config.ROAD_COLOR,
                outline=""
            )
        
        # Dibujar líneas centrales (amarillas punteadas)
        # Horizontales
        for y in [200, 450]:
            for x in range(0, Config.CANVAS_WIDTH, 30):
                canvas.create_line(
                    x, y, x + 15, y,
                    fill=Config.ROAD_LINE_COLOR,
                    width=3
                )
        
        # Verticales
        for x in [250, 550, 850]:
            for y in range(0, Config.CANVAS_HEIGHT, 30):
                canvas.create_line(
                    x, y, x, y + 15,
                    fill=Config.ROAD_LINE_COLOR,
                    width=3
                )