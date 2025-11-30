# genetic_algorithm.py  ← VERSIÓN FINAL 100% FUNCIONAL (sin warnings, gráfico perfecto)
import random
import matplotlib
matplotlib.use('TkAgg')  # ← Esto elimina el warning para siempre
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    def __init__(self, num_intersections=6):
        self.num_intersections = num_intersections
        self.population_size = 60
        self.generations = 120
        self.mutation_rate = 0.18
        self.crossover_rate = 0.85
        self.history = []  # Guardamos el historial para mostrar el gráfico cuando queramos

    def _create_individual(self):
        return [[random.randint(20, 55), random.randint(0, 59)] for _ in range(self.num_intersections)]

    def _fitness(self, individual, traffic_data):
        total_wait = 0
        total_flow = 1
        for i in range(self.num_intersections):
            queue = traffic_data.get(f"queue_{i}", 0)
            flow = max(traffic_data.get(f"flow_{i}", 1), 1)
            total_wait += queue ** 1.6   # Penaliza más las colas grandes
            total_flow += flow
        return total_wait / total_flow

    def optimize(self, traffic_data, callback=None):
        self.history = []
        population = [self._create_individual() for _ in range(self.population_size)]
        best_individual = None
        best_fitness = float('inf')

        for gen in range(self.generations):
            fitnesses = [self._fitness(ind, traffic_data) for ind in population]
            current_best_fitness = min(fitnesses)
            current_best_idx = fitnesses.index(current_best_fitness)

            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                best_individual = [gene[:] for gene in population[current_best_idx]]

            self.history.append(best_fitness)

            if callback:
                callback(gen, self.generations, best_fitness)

            # Selección + cruce + mutación
            weights = [1/(f + 0.1) for f in fitnesses]
            parents = random.choices(population, weights=weights, k=self.population_size)
            next_population = []

            for i in range(0, self.population_size, 2):
                p1 = parents[i]
                p2 = parents[(i + 1) % self.population_size]
                if random.random() < self.crossover_rate:
                    point = random.randint(1, self.num_intersections - 1)
                    c1 = p1[:point] + p2[point:]
                    c2 = p2[:point] + p1[point:]
                else:
                    c1, c2 = p1[:], p2[:]
                if random.random() < self.mutation_rate:
                    c1[random.randint(0, self.num_intersections-1)] = [random.randint(20,55), random.randint(0,59)]
                if random.random() < self.mutation_rate:
                    c2[random.randint(0, self.num_intersections-1)] = [random.randint(20,55), random.randint(0,59)]
                next_population.extend([c1, c2])

            population = next_population[:self.population_size]

        return {
            'best_solution': best_individual,
            'best_fitness': best_fitness,
            'history': self.history
        }

    def show_graph(self):
        """Muestra el gráfico en cualquier momento sin warnings"""
        if not self.history:
            print("No hay datos de optimización")
            return

        plt.switch_backend('TkAgg')
        plt.figure(figsize=(12, 7))
        plt.plot(self.history, color='#00ff88', linewidth=4, marker='o', markersize=4, markevery=10)
        plt.title("Evolución del Fitness - Ola Verde Activada", fontsize=20, fontweight='bold', color='white')
        plt.xlabel("Generación", fontsize=14, color='white')
        plt.ylabel("Fitness (menor = mejor)", fontsize=14, color='white')
        plt.grid(True, alpha=0.4, color='#444')
        plt.style.use('dark_background')
        plt.tight_layout()
        plt.show()