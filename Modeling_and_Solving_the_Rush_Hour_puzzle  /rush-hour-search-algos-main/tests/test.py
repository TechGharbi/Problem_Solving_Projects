import sys
import os
import time
import csv
import psutil
from collections import defaultdict

# Ajouter le dossier parent au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from solution import AStar, UCS, BFS, IDS
from model import Car, Node
from model.rush_hour_puzzle import RushHourPuzzle


def process_memory():
    """Retourne la mémoire utilisée en octets."""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def read_map(path):
    """Lit la carte Rush Hour à partir d'un fichier CSV."""
    vehicles = []
    board_height = 6
    board_width = 6
    walls = []

    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        lines = list(reader)

        # Première ligne : dimensions
        if len(lines) > 0 and len(lines[0]) >= 2:
            board_height, board_width = map(int, lines[0])

        # Lignes suivantes : véhicules ou murs
        for row in lines[1:]:
            if len(row) == 0:
                continue
            if row[0] == '#':
                walls.append((int(row[1]), int(row[2])))
            else:
                vid, x, y, orient, length = row
                car = Car(
                    id=vid.strip(),
                    row=int(x),
                    col=int(y),
                    dir=orient.strip().lower(),
                    size=int(length)
                )
                vehicles.append(car)

    return vehicles, board_height, board_width, walls


def calculate_used_resources(solution):
    """Mesure le temps et la mémoire utilisés par l'algorithme."""
    start_time = time.perf_counter()
    start_mem = process_memory()

    goal_node = solution.solve()

    end_mem = process_memory()
    end_time = time.perf_counter()

    search_time = end_time - start_time
    memory_usage = (end_mem - start_mem) / (1024 * 1024)  # Convertir en MB

    return goal_node, search_time, memory_usage


def print_path(path):
    """Affiche le chemin vers l’état final (sécurisé)."""
    try:
        for i, node in enumerate(path):
            print(f"\n----- Étape {i} -----")
            if i == 0:
                print("État initial")
            elif hasattr(node, "action") and node.action:
                print(f"Action : {node.action}")
            print(node)
        print("\n✅ État final atteint")
    except Exception as e:
        print(f"\n⚠️ Erreur pendant l’affichage du chemin : {e}")


def main():
    # Lecture du fichier CSV
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "test_map.csv")
    vehicles, board_height, board_width, walls = read_map(csv_path)

    # Création du puzzle
    initial_state = RushHourPuzzle(
        vehicles=vehicles,
        board_height=board_height,
        board_width=board_width,
        walls=walls
    )

    print("📌 État initial :")
    print(initial_state)

    # Création du nœud initial
    initial_node = Node(cars=vehicles)

    # Choix de l’algorithme (ici BFS)
    solution = BFS(initial_node)

    # Résolution + mesure des ressources
    goal_node, search_time, memory_usage = calculate_used_resources(solution)

    if goal_node is None:
        print("\n❌ Aucun chemin vers l’état final n’a été trouvé.")
        return

    # Trouver le chemin
    path = solution.find_path(goal_node)

    # Afficher les infos
    print(f"\n📊 Nombre de nœuds explorés : {solution.number_expanded_nodes}")
    print(f"⏱️ Temps de recherche : {search_time:.2f} secondes")
    print(f"🧠 Mémoire utilisée : {memory_usage:.2f} MB")
    print(f"💰 Coût total : {goal_node.cost}")
    #print(f"🪜 Nombre d’étapes : {len(path) - 1}")

    # Afficher le chemin complet
    print_path(path)


if __name__ == "__main__":
    main()
