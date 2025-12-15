from knight_v1 import Knight
import random
class Population:
    def __init__(self, population_size=50):
        self.population_size = population_size
        #self.knights = [Knight() for _ in range(population_size)]
        self.knights = [Knight(start_pos=(0, 0)) for _ in range(population_size)]
        self.generation = 1

    def check_population(self):
        for knight in self.knights:
            knight.check_moves()

    def evaluate(self):
        best_knight = max(self.knights, key=lambda knight: knight.evaluate_fitness())
        return best_knight, best_knight.fitness

    def tournament_selection(self, size=3):
        tournament = random.sample(self.knights, size)
        winner = max(tournament, key=lambda knight: knight.fitness)
        return winner

    def create_new_generation(self):
        new_generation = []
        while len(new_generation) < self.population_size:
            parent1 = self.tournament_selection()
            parent2 = self.tournament_selection()
            offspring1 = parent1.chromosome.crossover(parent2.chromosome)
            offspring2 = parent2.chromosome.crossover(parent1.chromosome)
            offspring1.mutation()
            offspring2.mutation()
            new_generation.append(Knight(offspring1))
            new_generation.append(Knight(offspring2))
        self.knights = new_generation[:self.population_size]
        self.generation += 1

        for knight in self.knights:
            knight.position = (0, 0)
            knight.path = [knight.position]
