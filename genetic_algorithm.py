import random
from config import Config

class GeneticAlgorithm:
    def __init__(self, num_intersections=6):
        self.num_intersections = num_intersections
        self.population_size = Config.GA_POPULATION_SIZE
        self.generations = Config.GA_GENERATIONS
        self.mutation_rate = Config.GA_MUTATION_RATE
        self.crossover_rate = Config.GA_CROSSOVER_RATE
        
        self.min_green = Config.GA_MIN_GREEN_TIME
        self.max_green = Config.GA_MAX_GREEN_TIME
        self.cycle_time = Config.GA_CYCLE_TIME
        
        self.history = []
        
    def create_individual(self):
        """Crea un individuo (configuración de semáforos)"""
        individual = []
        for _ in range(self.num_intersections):
            green_time = random.randint(self.min_green, self.max_green)
            yellow_time = 3
            offset = random.randint(0, self.cycle_time - 1)
            individual.append([green_time, yellow_time, offset])
        return individual
    
    def create_population(self):
        """Crea la población inicial"""
        return [self.create_individual() for _ in range(self.population_size)]
    
    def fitness(self, individual, traffic_data):
        """
        Función de fitness mejorada
        Maximiza: throughput, sincronización
        Minimiza: tiempo de espera, colas
        """
        total_wait = 0
        total_throughput = 0
        sync_penalty = 0
        
        # Evaluar cada intersección
        for i, genes in enumerate(individual):
            green_time, yellow_time, offset = genes
            
            # Simular tráfico
            queue = traffic_data.get(f"queue_{i}", 5)
            flow = traffic_data.get(f"flow_{i}", 10)
            
            red_time = self.cycle_time - green_time - yellow_time
            
            # Tiempo de espera estimado
            wait_time = (queue * red_time) / max(flow, 1)
            total_wait += wait_time
            
            # Throughput (vehículos que pasan)
            throughput = (green_time / self.cycle_time) * flow
            total_throughput += throughput
            
            # Penalizar ciclos extremos
            if green_time < 20 or green_time > 55:
                sync_penalty += 30
        
        # Evaluar sincronización entre intersecciones adyacentes
        adjacency = [
            (0, 1), (1, 2), (3, 4), (4, 5),  # Horizontales
            (0, 3), (1, 4), (2, 5)            # Verticales
        ]
        
        for i, j in adjacency:
            if i < len(individual) and j < len(individual):
                offset_diff = abs(individual[i][2] - individual[j][2])
                # Ideal: offset entre 15-45 segundos
                if offset_diff < 15 or offset_diff > 45:
                    sync_penalty += 15
        
        # Fitness total
        fitness_value = (total_throughput * 100) - (total_wait * 3) - sync_penalty
        return max(fitness_value, 1)
    
    def selection(self, population, fitness_scores):
        """Selección por torneo"""
        selected = []
        tournament_size = 3
        
        for _ in range(len(population)):
            tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
            winner = max(tournament, key=lambda x: x[1])[0]
            selected.append(winner)
        
        return selected
    
    def crossover(self, parent1, parent2):
        """Crossover de un punto"""
        if random.random() > self.crossover_rate:
            return parent1[:], parent2[:]
        
        point = random.randint(1, self.num_intersections - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        
        return child1, child2
    
    def mutate(self, individual):
        """Mutación con ajustes graduales"""
        mutated = [genes[:] for genes in individual]
        
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                # Mutar tiempo verde
                if random.random() < 0.6:
                    change = random.randint(-8, 8)
                    mutated[i][0] = max(self.min_green, 
                                       min(self.max_green, 
                                           mutated[i][0] + change))
                
                # Mutar offset
                else:
                    change = random.randint(-12, 12)
                    mutated[i][2] = (mutated[i][2] + change) % self.cycle_time
        
        return mutated
    
    def optimize(self, traffic_data, callback=None):
        """
        Ejecuta el algoritmo genético
        callback: función para actualizar progreso (opcional)
        """
        self.history = []
        population = self.create_population()
        
        best_individual = None
        best_fitness = 0
        
        for generation in range(self.generations):
            # Evaluar fitness
            fitness_scores = [self.fitness(ind, traffic_data) for ind in population]
            
            # Actualizar mejor
            max_idx = fitness_scores.index(max(fitness_scores))
            if fitness_scores[max_idx] > best_fitness:
                best_fitness = fitness_scores[max_idx]
                best_individual = population[max_idx][:]
            
            # Guardar historial
            avg_fitness = sum(fitness_scores) / len(fitness_scores)
            min_fitness = min(fitness_scores)
            
            self.history.append({
                "generation": generation,
                "best_fitness": best_fitness,
                "avg_fitness": avg_fitness,
                "min_fitness": min_fitness
            })
            
            # Callback para actualizar UI
            if callback:
                callback(generation, self.generations, best_fitness)
            
            # Crear nueva generación
            selected = self.selection(population, fitness_scores)
            new_population = [best_individual]  # Elitismo
            
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(selected, 2)
                child1, child2 = self.crossover(parent1, parent2)
                
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                
                new_population.extend([child1, child2])
            
            population = new_population[:self.population_size]
        
        return {
            "best_solution": best_individual,
            "best_fitness": best_fitness,
            "history": self.history
        }
    
    def get_history_data(self):
        """Retorna datos para graficar"""
        if not self.history:
            return [], [], [], []
        
        generations = [h["generation"] for h in self.history]
        best = [h["best_fitness"] for h in self.history]
        avg = [h["avg_fitness"] for h in self.history]
        min_fit = [h["min_fitness"] for h in self.history]
        
        return generations, best, avg, min_fit