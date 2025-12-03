# genetic_algorithm.py - VERSIÓN CORREGIDA DEFINITIVA
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from config import Config

class GeneticAlgorithm:
    def __init__(self, num_intersections=6):
        self.num_intersections = num_intersections
        self.population_size = Config.GA_POPULATION_SIZE
        self.generations = Config.GA_GENERATIONS
        self.mutation_rate = Config.GA_MUTATION_RATE
        self.crossover_rate = Config.GA_CROSSOVER_RATE
        self.history = []
        self.avg_history = []
        self.min_history = []

    def _create_individual(self):
        """Crea un individuo: [green_time, offset]"""
        return [[random.randint(25, 50), random.randint(0, 59)] 
                for _ in range(self.num_intersections)]

    def _fitness(self, individual, traffic_data):
        """
        FUNCIÓN DE FITNESS ROBUSTA
        Retorna un valor donde MENOR es MEJOR
        """
        score = 100.0  # Base inicial
        
        # ============ 1. PENALIZAR COLAS ============
        total_queue_penalty = 0
        for i in range(self.num_intersections):
            queue = traffic_data.get(f"queue_{i}", 2)
            flow = max(traffic_data.get(f"flow_{i}", 3), 1)
            
            # Penalización cuadrática por colas
            total_queue_penalty += (queue ** 2) * 20
            
            # Bonificación por flujo
            score -= flow * 5
        
        score += total_queue_penalty
        
        # ============ 2. EVALUAR TIEMPOS DE VERDE ============
        green_times = [ind[0] for ind in individual]
        
        for green in green_times:
            # Penalizar tiempos muy cortos o muy largos
            if green < 28:
                score += (28 - green) ** 2 * 3
            elif green > 47:
                score += (green - 47) ** 2 * 3
            else:
                # Bonificación por estar en rango óptimo (28-47)
                score -= 15
        
        # Penalizar si hay poca variación (todos iguales)
        green_range = max(green_times) - min(green_times)
        if green_range < 5:
            score += 150  # Muy malo
        elif green_range < 10:
            score += 80
        elif green_range > 20:
            score -= 50  # Buena diversidad
        
        # ============ 3. SINCRONIZACIÓN HORIZONTAL (OLA VERDE) ============
        # Pares horizontales (calles Este-Oeste)
        h_pairs = [(0,1), (1,2), (3,4), (4,5)]
        
        for i, j in h_pairs:
            offset_i = individual[i][1]
            offset_j = individual[j][1]
            
            # Calcular diferencia circular
            diff = abs(offset_j - offset_i)
            if diff > 30:
                diff = 60 - diff
            
            # Ideal: 12-18 segundos (tiempo de viaje entre intersecciones)
            if 12 <= diff <= 18:
                score -= 100  # EXCELENTE sincronización
            elif 8 <= diff <= 22:
                score -= 50   # Buena sincronización
            elif diff < 5 or diff > 35:
                score += 80   # Mala sincronización
            else:
                score += 30   # Regular
        
        # ============ 4. SINCRONIZACIÓN VERTICAL ============
        v_pairs = [(0,3), (1,4), (2,5)]
        
        for i, j in v_pairs:
            offset_i = individual[i][1]
            offset_j = individual[j][1]
            
            diff = abs(offset_j - offset_i)
            if diff > 30:
                diff = 60 - diff
            
            # Ideal: 20-30 segundos
            if 20 <= diff <= 30:
                score -= 80
            elif 15 <= diff <= 35:
                score -= 40
            elif diff < 8 or diff > 45:
                score += 70
            else:
                score += 25
        
        # ============ 5. DIVERSIDAD EN OFFSETS ============
        offsets = [ind[1] for ind in individual]
        unique_offsets = len(set(offsets))
        
        if unique_offsets <= 3:
            score += 200  # Muy mala diversidad
        elif unique_offsets == 4:
            score += 100
        elif unique_offsets >= 5:
            score -= 80  # Buena diversidad
        
        # ============ 6. BALANCEO ENTRE INTERSECCIONES ============
        # Penalizar si hay mucha diferencia entre tiempos de verde
        avg_green = sum(green_times) / len(green_times)
        variance = sum((g - avg_green)**2 for g in green_times) / len(green_times)
        
        if variance > 80:
            score += variance * 2  # Alta varianza = malo
        elif variance < 20:
            score += 100  # Muy poca varianza = todos iguales = malo
        
        # ============ 7. RUIDO PARA EVITAR CONVERGENCIA ============
        # Agregar pequeño ruido aleatorio para mantener exploración
        noise = random.uniform(-8, 8)
        score += noise
        
        # ============ 8. RETORNO FINAL ============
        # NO usar max() con límite mínimo - dejar que sea negativo si es muy bueno
        return round(score, 2)

    def optimize(self, traffic_data, callback=None):
        """Ejecuta el algoritmo genético"""
        print("\n" + "="*70)
        print("🧬 INICIANDO OPTIMIZACIÓN")
        print(f"📊 Población: {self.population_size} | Generaciones: {self.generations}")
        print("="*70 + "\n")
        
        self.history = []
        self.avg_history = []
        self.min_history = []
        
        # Población inicial ULTRA DIVERSA
        population = []
        for _ in range(self.population_size):
            population.append(self._create_individual())
        
        best_individual = None
        best_fitness = float('inf')
        no_improvement_count = 0
        
        for gen in range(self.generations):
            # Calcular fitness
            fitnesses = [self._fitness(ind, traffic_data) for ind in population]
            
            # Estadísticas
            current_best = min(fitnesses)
            current_avg = sum(fitnesses) / len(fitnesses)
            current_worst = max(fitnesses)
            
            # Actualizar mejor
            if current_best < best_fitness:
                improvement = best_fitness - current_best
                best_fitness = current_best
                best_idx = fitnesses.index(current_best)
                best_individual = [g[:] for g in population[best_idx]]
                no_improvement_count = 0
                
                if gen % 5 == 0 or gen == 0:
                    print(f"✨ Gen {gen+1}: Nuevo MEJOR → {best_fitness:.2f} (↓{improvement:.2f})")
            else:
                no_improvement_count += 1
            
            # Mostrar progreso
            if gen % 15 == 0:
                print(f"📈 Gen {gen+1:3d} | Mejor: {current_best:7.2f} | "
                      f"Prom: {current_avg:7.2f} | Peor: {current_worst:7.2f}")
            
            # Guardar historial
            self.history.append(current_best)
            self.avg_history.append(current_avg)
            self.min_history.append(current_worst)
            
            # Callback
            if callback:
                callback(gen, self.generations, best_fitness)
            
            # ============ SELECCIÓN POR TORNEO ============
            tournament_size = 5
            parents = []
            
            for _ in range(self.population_size):
                # Seleccionar candidatos al azar
                candidates = random.sample(list(zip(population, fitnesses)), tournament_size)
                # El mejor (menor fitness) gana
                winner = min(candidates, key=lambda x: x[1])[0]
                parents.append(winner)
            
            # ============ NUEVA GENERACIÓN ============
            new_population = []
            
            # Elitismo: mantener los 8 mejores
            sorted_pop = sorted(zip(population, fitnesses), key=lambda x: x[1])
            for i in range(8):
                new_population.append([g[:] for g in sorted_pop[i][0]])
            
            # Generar resto
            while len(new_population) < self.population_size:
                p1 = random.choice(parents)
                p2 = random.choice(parents)
                
                # Cruce de dos puntos
                if random.random() < self.crossover_rate:
                    p1 = random.randint(1, self.num_intersections - 2)
                    p2 = random.randint(p1 + 1, self.num_intersections - 1)
                    
                    child = (parents[0][:p1] + 
                            parents[1][p1:p2] + 
                            parents[0][p2:])
                else:
                    child = [g[:] for g in p1]
                
                # Mutación adaptativa
                base_mut_rate = self.mutation_rate
                if no_improvement_count > 15:
                    base_mut_rate *= 2.5  # Aumentar mutación si hay estancamiento
                
                for i in range(self.num_intersections):
                    if random.random() < base_mut_rate:
                        # Mutación en tiempo verde
                        if random.random() < 0.5:
                            child[i][0] = random.randint(25, 50)
                        # Mutación en offset
                        else:
                            child[i][1] = random.randint(0, 59)
                
                new_population.append(child)
            
            population = new_population[:self.population_size]
        
        # Resultados
        if len(self.history) > 1 and self.history[0] != 0:
            improvement = ((self.history[0] - best_fitness) / abs(self.history[0])) * 100
        else:
            improvement = 0
        
        print("\n" + "="*70)
        print("✅ OPTIMIZACIÓN COMPLETADA")
        print(f"🎯 Fitness Inicial: {self.history[0]:.2f}")
        print(f"🎯 Fitness Final: {best_fitness:.2f}")
        print(f"📈 MEJORA: {improvement:.1f}%")
        print("="*70 + "\n")
        
        return {
            'best_solution': best_individual,
            'best_fitness': best_fitness,
            'history': self.history,
            'avg_history': self.avg_history,
            'min_history': self.min_history
        }

    def get_history_data(self):
        """Retorna datos para gráficos"""
        if not self.history:
            return [], [], [], []
        
        generations = list(range(1, len(self.history) + 1))
        return generations, self.history, self.avg_history, self.min_history

    def show_graph(self):
        """Muestra gráfico"""
        if not self.history or len(self.history) < 2:
            print("⚠️ Datos insuficientes")
            return
        
        gens, best, avg, worst = self.get_history_data()
        
        plt.figure(figsize=(15, 9))
        plt.style.use('dark_background')
        ax = plt.gca()
        ax.set_facecolor('#0f1620')
        
        # Graficar
        plt.plot(gens, best, color='#00ff88', linewidth=4, 
                marker='o', markersize=7, markevery=max(1, len(gens)//15),
                label='Mejor Fitness', zorder=3)
        
        plt.plot(gens, avg, color='#ff9900', linewidth=2.5, 
                linestyle='--', alpha=0.85, label='Fitness Promedio', zorder=2)
        
        plt.plot(gens, worst, color='#ff4444', linewidth=1.5,
                linestyle=':', alpha=0.7, label='Peor Fitness', zorder=1)
        
        plt.fill_between(gens, best, worst, color='#2c3e50', alpha=0.2)
        
        plt.title("EVOLUCIÓN DEL FITNESS - ALGORITMO GENÉTICO", 
                 fontsize=24, fontweight='bold', color='#00ff88', pad=20)
        plt.xlabel("Generación", fontsize=18, color='white', labelpad=15)
        plt.ylabel("Fitness (menor = mejor)", fontsize=18, color='white', labelpad=15)
        plt.grid(True, alpha=0.25, color='#666', linestyle='--', linewidth=0.8)
        plt.legend(fontsize=14, loc='upper right', framealpha=0.9)
        
        # Info
        if len(best) > 1 and best[0] != 0:
            mejora = ((best[0] - best[-1]) / abs(best[0])) * 100
            
            info_text = (f"Mejora: {mejora:.1f}%\n"
                        f"Fitness Inicial: {best[0]:.2f}\n"
                        f"Fitness Final: {best[-1]:.2f}\n"
                        f"Generaciones: {len(gens)}")
            
            plt.text(0.02, 0.98, info_text,
                    transform=ax.transAxes, fontsize=13, fontweight='bold',
                    verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.8', facecolor='#1e2a38', 
                            alpha=0.95, edgecolor='#00ff88', linewidth=3),
                    color='white')
        
        plt.xlim(0, max(gens) + 2)
        plt.tight_layout()
        plt.show()