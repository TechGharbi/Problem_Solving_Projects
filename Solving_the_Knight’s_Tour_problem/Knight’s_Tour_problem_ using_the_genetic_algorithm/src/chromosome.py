import random

class Chromosome:
    def __init__(self, genes=None):
        self.genes = genes if genes else self.generate_random_genes()

    def generate_random_genes(self):
        return [random.randint(1, 8) for _ in range(63)]

    def crossover(self, partner):
        crossover_point = random.randint(1, 62)
        new_genes = self.genes[:crossover_point] + partner.genes[crossover_point:]
        return Chromosome(new_genes)

    def mutation(self, mutation_rate=0.1):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = random.randint(1, 8)
