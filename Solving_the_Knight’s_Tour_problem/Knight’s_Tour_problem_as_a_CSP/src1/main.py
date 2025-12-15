from knight_v5 import backtracking, successor_fct 
from knight_v5 import apply_heuristics 
from animation import run_animation
import time

def debug_backtracking(assignment, size=8, depth=0):
    indent = "  " * depth  

    if len(assignment) == size * size:
        print(f"{indent}Solution complète trouvée en {len(assignment)} coups !")
        return assignment.copy()

    current = assignment[-1]
    visited = set(assignment)

    print(f"\n{indent}=== Étape profondeur {depth} ===")
    print(f"{indent}Position actuelle : {current}")
    print(f"{indent}Cases visitées    : {len(visited)}")

    raw_succ = successor_fct(current, visited, size)
    if not raw_succ:
        print(f"{indent}Aucun mouvement possible → backtrack")
        return None

    print(f"{indent}Successeurs bruts : {raw_succ}")
    
    # Calcul du degré (onward moves) pour affichage
    onward_count = {}
    for pos in raw_succ:
        onward_count[pos] = len(successor_fct(pos, visited | {pos}, size))

    mrv_sorted = sorted(raw_succ, key=lambda p: onward_count[p])
    mrv_display = [f"{pos} ({onward_count[pos]})" for pos in mrv_sorted]
    print(f"{indent}Tri MRV          : [{' → '.join(mrv_display)}]")
  
    counts = list(onward_count.values())
    tie_exists = len(counts) > 1 and len(set(counts)) == 1 or len(set(counts)) < len(counts)
    print(f"{indent}Tie détecté ?     : {'Oui' if tie_exists else 'Non'}")

    if tie_exists:
        from knight_v5 import apply_heuristics
        lcv_sorted = apply_heuristics(raw_succ, visited, size)
        
        lcv_display = []
        for pos in lcv_sorted:
            mrv_val = onward_count[pos]
            temp_visited = visited | {pos}
            neighbors = successor_fct(pos, temp_visited, size)
            lcv_val = sum(len(successor_fct((nx,ny), temp_visited | {(nx,ny)}, size)) for nx,ny in neighbors)
            lcv_display.append(f"{pos} (MRV={mrv_val}, LCV={lcv_val})")
        
        print(f"{indent}Tri LCV appliqué : [{' → '.join(lcv_display)}]")
        successors = lcv_sorted
    else:
        successors = mrv_sorted

    for move in successors:
        count = onward_count[move]
        print(f"{indent}→ Essai : {move}  (onward moves = {count})")
        assignment.append(move)

        result = debug_backtracking(assignment, size, depth + 1)
        if result is not None:
            return result

        assignment.pop()
        print(f"{indent}← Échec {move} → backtrack")

    return None

def main():
    print("=" * 70)
    print("        KNIGHT'S TOUR 8×8 – Backtracking + MRV + LCV (Debug)")
    print("=" * 70)

    start_pos = (0, 0)
    assignment = [start_pos]

    start_time = time.time()
    solution = debug_backtracking(assignment, size=8, depth=0)
    end_time = time.time()

    print("\n" + "="*70)
    if solution:
        print("SOLUTION TROUVÉE !")
        print(f"Temps d'exécution : {end_time - start_time:.3f} secondes")
        print(f"Nombre de coups   : {len(solution)}")

        print("\nChemin complet de la tournée du cavalier :")
        for i, pos in enumerate(solution):
            print(f"{i+1:2d} → {pos}", end="  ")
            if (i + 1) % 8 == 0:    
                print()
        print("\n")

        print("\nLancement de l'animation...")
        run_animation(solution)
    else:
        print("Aucune solution trouvée depuis (0,0) avec ces heuristiques.")
        print("Essaie un autre point de départ ou désactive le debug pour plus de vitesse.")

if __name__ == "__main__":
    main()
