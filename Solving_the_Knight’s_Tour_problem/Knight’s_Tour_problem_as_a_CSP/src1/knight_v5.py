def knight_moves(position, size=8):
    """Generate all valid knight moves from a given position."""
    x, y = position
    deltas = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    return [(x + dx, y + dy) for dx, dy in deltas if 0 <= x + dx < size and 0 <= y + dy < size]

def successor_fct(current, visited, size=8):
    """Get positions that respect the three constraints: knight move, boundaries, not visited."""
    return [p for p in knight_moves(current, size) if p not in visited]

def count_onward_moves(x, y, visited, size=8):
    """Compte le nombre de mouvements possibles depuis (x,y) avec visited mis à jour."""
    temp_visited = visited | {(x, y)}
    return len(successor_fct((x, y), temp_visited, size))

def apply_heuristics(successors, visited, size=8):
        #Appliquer les heuristiques MRV et LCV
        #Calculer le score MRV (moins de déplacements vers l'avant)
        #Calculer le score LCV (flexibilité maximale pour les voisins)
        #Trier d'abord par MRV, puis par LCV
        # Le MRV est prépondérant ; le LCV est utile lorsque les valeurs de MRV sont égales.
        
        if not successors:
            return []
        
        scores = []
        
        for pos in successors:
            x, y = pos
            # MRV : Compte les coups suivants à partir de cette position
            #Compte le nombre de coups légaux possibles À PARTIR DE la position (x, y). Un score plus bas signifie une plus grande contrainte et donc une priorité plus élevée pour explorer en premier.
            mrv_score = count_onward_moves(x, y, visited,size)
            
            # LCV : Calcul de la flexibilité totale des voisins
            #Après avoir visité (x, y), le programme trouve tous les déplacements possibles suivants (voisins).
            #Pour chaque voisin, il compte le nombre de déplacements possibles.
            #La somme de ces comptes donne la flexibilité totale restante après ce déplacement.
            #Un score plus élevé signifie un avenir plus flexible et donc moins de contraintes (meilleur choix).
            temp_visited = visited | {pos}
            lcv_score = 0
            
            neighbors = successor_fct(pos, temp_visited, size)
            for nx, ny in neighbors:
                lcv_score += count_onward_moves(nx, ny, temp_visited,size)
            
            # Stockage : (score_mrv, score_lcv négatif pour le tri, x, y)
            # LCV négatif pour placer les valeurs LCV les plus élevées en premier
            # La négation inverse le sens du tri afin que les valeurs LCV les plus élevées apparaissent en premier sans avoir besoin de reverse=True.
            scores.append((mrv_score, -lcv_score, pos))
        
        # Trier par MRV (ordre croissant), puis par LCV (ordre décroissant par valeurs négatives)
        scores.sort(key=lambda x: (x[0], x[1]))
        
        # Retourner les positions triées
        return [pos for _, _, pos in scores]

def backtracking(assignment, heuristic=None, size=8):
    """Backtracking function with optional heuristic."""
    if len(assignment) == size * size:
        return assignment
    
    current = assignment[-1]
    visited = set(assignment)
    successors = successor_fct(current, visited, size)
    
    successors = apply_heuristics(successors, visited,size)

    
    for next_pos in successors:
        assignment.append(next_pos)
        result = backtracking(assignment, size)
        if result is not None:
            return result
        assignment.pop()
    
    return None
