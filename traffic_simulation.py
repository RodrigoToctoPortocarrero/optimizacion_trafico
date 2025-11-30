# traffic_simulation.py
import random
import math
from models.vehicle import Vehicle
from models.traffic_light import TrafficLight
from config import Config

class TrafficSimulation:
    def __init__(self, total_vehicles=20):
        self.total_vehicles_initial = total_vehicles
        self.spawn_rate_infinite = 0.5
        self.vehicles = []
        self.traffic_lights = []
        self.vehicle_id_counter = 0
        self.current_time = 0.0
        self.next_spawn_time = 0.0
        self.spawn_interval = 0.6
        self.is_running = False
        self.is_optimized = False
        self.total_spawned = 0
        self.total_completed = 0
        self._create_traffic_lights()

    def _create_traffic_lights(self):
        self.traffic_lights = []
        for inter in Config.INTERSECTIONS:
            iid = inter['id']
            is_north_south = iid in [0, 1, 2]  # S0-S2: vertical, S3-S5: horizontal
            green_time = random.randint(25, 45)
            offset = random.randint(0, 60)
            light = TrafficLight(iid, inter['x'], inter['y'], green_time, offset, is_north_south)
            self.traffic_lights.append(light)

    def start(self):
        self.is_running = True
        self.current_time = 0.0
        self.next_spawn_time = 1.5

    def stop(self):
        self.is_running = False

    def reset(self):
        self.vehicles.clear()
        self.vehicle_id_counter = 0
        self.current_time = 0.0
        self.next_spawn_time = 0.0
        self.total_spawned = 0
        self.total_completed = 0
        self.is_optimized = False
        self._create_traffic_lights()

    def apply_optimization(self, solution):
        """APLICA LA SOLUCIÓN CORRECTAMENTE"""
        for i, light in enumerate(self.traffic_lights):
            if i < len(solution):
                light.green_time = max(20, min(55, int(solution[i][0])))
                light.offset = int(solution[i][1]) % 60
        self.is_optimized = True

    def spawn_vehicle(self):
        lane_idx = random.randint(0, len(Config.LANES) - 1)
        vehicle = Vehicle(self.vehicle_id_counter, lane_idx, lane_idx, self.current_time, self)
        self.vehicles.append(vehicle)
        self.vehicle_id_counter += 1
        self.total_spawned += 1

    def update(self, dt):
        if not self.is_running:
            return
        self.current_time += dt

        # Spawn vehículos
        if self.total_spawned < self.total_vehicles_initial:
            if self.current_time >= self.next_spawn_time:
                self.spawn_vehicle()
                self.next_spawn_time = self.current_time + self.spawn_interval
        else:
            if self.current_time >= self.next_spawn_time:
                if random.random() < self.spawn_rate_infinite:
                    self.spawn_vehicle()
                self.next_spawn_time = self.current_time + random.uniform(1.7, 2.9)

        # Actualizar vehículos
        for vehicle in self.vehicles[:]:
            vehicle.update(dt)
            if vehicle.completed:
                self.vehicles.remove(vehicle)
                self.total_completed += 1

    def get_real_traffic_data(self):
        """DATOS REALES para el AG"""
        data = {}
        for light in self.traffic_lights:
            x, y = light.x, light.y
            queue = flow = 0
            for v in self.vehicles:
                dist = math.hypot(v.x - x, v.y - y)
                if dist < 80:
                    if v.waiting:
                        queue += 1
                    elif dist < 40:
                        flow += 1
            data[f"queue_{light.id}"] = queue
            data[f"flow_{light.id}"] = max(flow, 1)
        return data

    def get_statistics(self):
        waiting = sum(1 for v in self.vehicles if v.waiting)
        avg_wait = sum(v.wait_time for v in self.vehicles) / len(self.vehicles) if self.vehicles else 0
        return {
            "total_vehicles": len(self.vehicles),
            "total_spawned": self.total_spawned,
            "completed": self.total_completed,
            "waiting": waiting,
            "avg_wait_time": round(avg_wait, 2),
            "time": round(self.current_time, 1),
            "optimized": "Sí" if self.is_optimized else "No"
        }

    def draw(self, canvas):
        canvas.delete("all")
        self._draw_roads(canvas)
        for light in self.traffic_lights:
            light.draw(canvas, self.current_time)
        for vehicle in self.vehicles:
            vehicle.draw(canvas)

    def _draw_roads(self, canvas):
        for y in [200, 450]:
            canvas.create_rectangle(0, y-35, Config.CANVAS_WIDTH, y+35, fill="#2c3e50")
        for x in [250, 550, 850]:
            canvas.create_rectangle(x-35, 0, x+35, Config.CANVAS_HEIGHT, fill="#2c3e50")
        for y in [200, 450]:
            for i in range(0, Config.CANVAS_WIDTH, 40):
                canvas.create_line(i, y, i+20, y, fill="#ffeb3b", width=4)
        for x in [250, 550, 850]:
            for i in range(0, Config.CANVAS_HEIGHT, 40):
                canvas.create_line(x, i, x, i+20, fill="#ffeb3b", width=4)