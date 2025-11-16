import yaml
import pygame
from population import Population
from animation import run_animation
import random
from knight_v1 import Knight  # <--- AJOUTE CETTE LIGNE

# Charger la config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

population_size = config["population_size"]
max_generations = config["max_generations"]
fitness_target = config["fitness_target"]


def run_genetic_algorithm():
    population = Population(population_size=population_size)
    generation = 1

    while generation <= max_generations:
        print(f"\n{'='*60}")
        print(f" GÉNÉRATION {generation} ")
        print(f"{'='*60}")

        # 1. Vérifier tous les knights
        population.check_population()

        # 2. Évaluer la population
        best_knight, fitness = population.evaluate()
        print(f"\nMeilleur Knight - Fitness: {fitness}/64")
        print(f"Path actuel ({len(best_knight.path)} cases): {best_knight.path}")

        # Condition de victoire
        if fitness == fitness_target:
            print(f"\n{'!'*60}")
            print(f" SOLUTION COMPLÈTE TROUVÉE EN GÉNÉRATION {generation} ! ")
            print(f"{'!'*60}")
            print(f"Chemin complet ({len(best_knight.path)} cases) :")
            for i, pos in enumerate(best_knight.path):
                print(f"{i+1:2d}: {pos}", end=" ")
                if (i + 1) % 8 == 0: print()
            print()
            return best_knight.path

        # 3. Créer nouvelle génération avec logs détaillés
        print(f"\n--- Création nouvelle génération ---")
        new_generation = []
        example_shown = False  # Montrer un seul exemple de crossover/mutation

        while len(new_generation) < population_size:
            # Sélection par tournoi
            parent1 = population.tournament_selection()
            parent2 = population.tournament_selection()

            if not example_shown:
                print(f"\nExemple de sélection :")
                print(f"Parent 1 - Fitness: {parent1.fitness}, Gènes[:10]: {parent1.chromosome.genes[:10]}...")
                print(f"Parent 2 - Fitness: {parent2.fitness}, Gènes[:10]: {parent2.chromosome.genes[:10]}...")

            # Crossover
            offspring1 = parent1.chromosome.crossover(parent2.chromosome)
            offspring2 = parent2.chromosome.crossover(parent1.chromosome)

            if not example_shown:
                crossover_point = len(parent1.chromosome.genes) - len(offspring1.genes[len(parent1.chromosome.genes):])
                print(f"Point de crossover: {crossover_point}")
                print(f"Offspring 1 (après crossover)[:10]: {offspring1.genes[:10]}...")
                print(f"Offspring 2 (après crossover)[:10]: {offspring2.genes[:10]}...")

            # Mutation
            old1 = offspring1.genes.copy()
            old2 = offspring2.genes.copy()
            offspring1.mutation()
            offspring2.mutation()

            if not example_shown:
                diff1 = [i for i in range(len(old1)) if old1[i] != offspring1.genes[i]]
                diff2 = [i for i in range(len(old2)) if old2[i] != offspring2.genes[i]]
                print(f"Mutation Offspring 1 -> {len(diff1)} gène(s) muté(s) à indices: {diff1[:5]}...")
                print(f"Mutation Offspring 2 -> {len(diff2)} gène(s) muté(s) à indices: {diff2[:5]}...")
                example_shown = True  # Afficher qu'une fois

            # Créer nouveaux knights
            knight1 = Knight(offspring1)
            knight2 = Knight(offspring2)
            new_generation.append(knight1)
            if len(new_generation) < population_size:
                new_generation.append(knight2)

        # Mettre à jour population
        population.knights = new_generation[:population_size]
        population.generation += 1
        generation += 1

        # Réinitialiser position et path
        for knight in population.knights:
            knight.position = (0, 0)
            knight.path = [knight.position]

        generation += 1

    print("\nGénérations max atteintes sans solution complète.")
    return best_knight.path


# if __name__ == "__main__":
#     random.seed(42)
#     print("Démarrage de l'algorithme génétique...")

#     while True:
#         path = run_genetic_algorithm()
#         print(f"\nSolution trouvée : {len(path)} cases")

#         from animation import run_animation
#         result = run_animation(path)  # Retourne (x,y) ou "restart"

#         if result == "restart":
#             print("Redémarrage...")
#             continue
#         else:
#             chosen_start = result
#             print(f"Animation lancée depuis : {chosen_start}")
#             break

#     pygame.quit()
#     print("Programme terminé.")

if __name__ == "__main__":
    random.seed(42)
    print("Démarrage de l'algorithme génétique...")

    while True:
        path = run_genetic_algorithm()
        print(f"\nSolution trouvée : {len(path)} cases")

        from animation import run_animation
        result = run_animation(path)

        if result == "restart":
            print("Redémarrage...")
            continue
        else:
            chosen_start = result
            if chosen_start != (0, 0):
                print(f"Position de départ choisie: {chosen_start}")
                print("Recalcul du chemin avec la nouvelle position de départ...")
                
                # Recréer un Knight avec la nouvelle position de départ
                from knight_v1 import Knight
                from chromosome import Chromosome
                
                # Trouver le chromosome du meilleur chemin
                best_knight = None
                max_fitness = 0
                population = Population(population_size=population_size)
                population.check_population()
                for knight in population.knights:
                    if knight.fitness > max_fitness:
                        max_fitness = knight.fitness
                        best_knight = knight
                
                if best_knight:
                    # Créer un nouveau knight avec la position choisie
                    new_knight = Knight(
                        chromosome=best_knight.chromosome, 
                        start_pos=chosen_start
                    )
                    new_knight.check_moves()
                    new_path = new_knight.path
                    
                    print(f"Nouveau chemin ({len(new_path)} cases) depuis {chosen_start}")
                    
                    # Relancer l'animation avec le nouveau chemin
                    result = run_animation(new_path)
                    if result == "restart":
                        continue
            
            break

    pygame.quit()
    print("Programme terminé.")