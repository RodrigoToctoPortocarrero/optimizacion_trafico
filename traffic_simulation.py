# traffic_simulation.py - VERSIÓN CON DEPURACIÓN
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
        """Crea semáforos DESORGANIZADOS al inicio"""
        self.traffic_lights = []
        for inter in Config.INTERSECTIONS:
            iid = inter['id']
            is_north_south = iid in [0, 1, 2]  # S0-S2: vertical, S3-S5: horizontal
            
            # VALORES ALEATORIOS DESORGANIZADOS
            green_time = random.randint(20, 50)
            offset = random.randint(0, 59)
            
            light = TrafficLight(iid, inter['x'], inter['y'], green_time, offset, is_north_south)
            self.traffic_lights.append(light)
        
        print(f"🚦 Semáforos creados: {len(self.traffic_lights)} con configuraciones aleatorias")

    def start(self):
        self.is_running = True
        self.current_time = 0.0
        self.next_spawn_time = 1.5
        print("▶️ Simulación iniciada")

    def stop(self):
        self.is_running = False
        print("⏹️ Simulación detenida")

    def reset(self):
        """Reinicia completamente la simulación"""
        self.vehicles.clear()
        self.vehicle_id_counter = 0
        self.current_time = 0.0
        self.next_spawn_time = 0.0
        self.total_spawned = 0
        self.total_completed = 0
        self.is_optimized = False
        self._create_traffic_lights()
        print("🔄 Simulación reiniciada completamente")

    def apply_optimization(self, solution):
        """
        APLICA LA SOLUCIÓN DEL AG Y REINICIA LA SIMULACIÓN VISUALMENTE
        """
        print("🎯 Aplicando optimización del algoritmo genético...")
        
        # 1. Aplicar nueva configuración a los semáforos
        for i, light in enumerate(self.traffic_lights):
            if i < len(solution):
                new_green = max(20, min(55, int(solution[i][0])))
                new_offset = int(solution[i][1]) % 60
                
                print(f"   Semáforo S{i}: {light.green_time}s→{new_green}s, "
                      f"offset {light.offset}→{new_offset}")
                
                light.green_time = new_green
                light.offset = new_offset
        
        # 2. REINICIAR SIMULACIÓN VISUAL
        self.vehicles.clear()
        self.vehicle_id_counter = 0
        self.current_time = 0.0
        self.next_spawn_time = 0.5
        self.total_spawned = 0
        self.total_completed = 0
        self.is_optimized = True
        
        print("✅ Optimización aplicada - Simulación reiniciada")

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

        # Spawn inicial de vehículos
        if self.total_spawned < self.total_vehicles_initial:
            if self.current_time >= self.next_spawn_time:
                self.spawn_vehicle()
                self.next_spawn_time = self.current_time + self.spawn_interval
        else:
            # Spawn continuo después del inicial
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
        """Obtiene datos REALES del tráfico actual para el AG"""
        print(f"\n📊 OBTENIENDO DATOS DE TRÁFICO PARA AG")
        print(f"   Vehículos en simulación: {len(self.vehicles)}")
        
        data = {}
        total_waiting = 0
        total_moving = 0
        
        for light in self.traffic_lights:
            x, y = light.x, light.y
            queue = 0
            flow = 0
            
            for v in self.vehicles:
                dist = math.hypot(v.x - x, v.y - y)
                if dist < 80:  # Radio de detección
                    if v.waiting:
                        queue += 1
                        total_waiting += 1
                    elif dist < 40:
                        flow += 1
                        total_moving += 1
            
            # Valores mínimos garantizados
            queue = max(queue, 1)
            flow = max(flow, 1)
            
            data[f"queue_{light.id}"] = queue
            data[f"flow_{light.id}"] = flow
            
            print(f"   S{light.id}: {queue} en cola, {flow} en movimiento")
        
        # Métricas globales
        data["total_waiting"] = total_waiting
        data["total_moving"] = total_moving
        data["total_vehicles"] = len(self.vehicles)
        
        print(f"   Total: {total_waiting} esperando, {total_moving} en movimiento")
        print(f"📦 Datos enviados al AG: {len(data)} valores\n")
        
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
            "optimized": "✅ Sí" if self.is_optimized else "❌ No"
        }

    def draw(self, canvas):
        """Dibuja todo en el canvas"""
        canvas.delete("all")
        self._draw_roads(canvas)
        
        # Dibujar semáforos
        for light in self.traffic_lights:
            light.draw(canvas, self.current_time)
        
        # Dibujar vehículos
        for vehicle in self.vehicles:
            vehicle.draw(canvas)

    def _draw_roads(self, canvas):
        """Dibuja las carreteras con líneas amarillas"""
        # Carreteras horizontales
        for y in [200, 450]:
            canvas.create_rectangle(0, y-35, Config.CANVAS_WIDTH, y+35, fill="#2c3e50")
        
        # Carreteras verticales
        for x in [250, 550, 850]:
            canvas.create_rectangle(x-35, 0, x+35, Config.CANVAS_HEIGHT, fill="#2c3e50")
        
        # Líneas amarillas horizontales
        for y in [200, 450]:
            for i in range(0, Config.CANVAS_WIDTH, 40):
                canvas.create_line(i, y, i+20, y, fill="#ffeb3b", width=4)
        
        # Líneas amarillas verticales
        for x in [250, 550, 850]:
            for i in range(0, Config.CANVAS_HEIGHT, 40):
                canvas.create_line(x, i, x, i+20, fill="#ffeb3b", width=4)