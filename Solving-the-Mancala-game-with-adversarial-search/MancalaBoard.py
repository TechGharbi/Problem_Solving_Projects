class MancalaBoard:
    def __init__(self):
        # Representation du plateau
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4,  # Joueur 1
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4,  # Joueur 2
            'S1': 0, 'S2': 0  # Magasins
        }
        
        # Definition des fosses pour chaque joueur
        self.player1_pits = ['A', 'B', 'C', 'D', 'E', 'F']
        self.player2_pits = ['G', 'H', 'I', 'J', 'K', 'L']
        
        # Fosses opposees pour la capture
        self.opposite_pits = {
            'A': 'L', 'B': 'K', 'C': 'J', 'D': 'I', 'E': 'H', 'F': 'G',
            'G': 'F', 'H': 'E', 'I': 'D', 'J': 'C', 'K': 'B', 'L': 'A'
        }
    
    def possibleMoves(self, player):
        """Retourner les mouvements possibles pour le joueur"""
        if player == 1:
            return [pit for pit in self.player1_pits if self.board[pit] > 0]
        else:  # player == 2
            return [pit for pit in self.player2_pits if self.board[pit] > 0]
    
    def get_next_pit(self, current_pit, player):
        if player == 1:
            # Chemin du Joueur 1: A→B→C→D→E→F→S1→L→K→J→I→H→G→A
            sequence = ['A', 'B', 'C', 'D', 'E', 'F', 'S1', 'L', 'K', 'J', 'I', 'H', 'G', 'A']
        else:
            # Chemin du Joueur 2: L→K→J→I→H→G→S2→A→B→C→D→E→F→L
            sequence = ['L', 'K', 'J', 'I', 'H', 'G', 'S2', 'A', 'B', 'C', 'D', 'E', 'F', 'L']
        
        if current_pit not in sequence:
            return sequence[0]
        
        idx = sequence.index(current_pit)
        next_idx = (idx + 1) % len(sequence)
        next_pit = sequence[next_idx]
        
        return next_pit
    
    def doMove(self, player, pit):
        if self.board[pit] == 0:
            return False
        
        seeds = self.board[pit]
        self.board[pit] = 0
         
        current_pit = pit
        last_pit = None
        captured = False
        play_again = False
        
        # Distribuer les graines une par une
        for i in range(seeds):
            # Obtenir la fosse suivante
            next_pit = self.get_next_pit(current_pit, player)
            
            # Verifier si c'est le magasin du joueur
            if (player == 1 and next_pit == 'S1') or (player == 2 and next_pit == 'S2'):
                # Ajouter une graine au magasin du joueur
                self.board[next_pit] += 1
                last_pit = next_pit
                
                # Si c'est la dernière graine, rejouer
                if i == seeds - 1:
                    play_again = True
            
            # Verifier si c'est le magasin de l'adversaire
            elif (player == 1 and next_pit == 'S2') or (player == 2 and next_pit == 'S1'):
                # Sauter le magasin de l'adversaire
                current_pit = next_pit
                # Obtenir la fosse suivante après le saut
                next_pit = self.get_next_pit(current_pit, player)
                self.board[next_pit] += 1
                last_pit = next_pit
            
            else:
                # Ajouter une graine à la fosse
                self.board[next_pit] += 1
                last_pit = next_pit
            
            current_pit = next_pit
        
        # 🎯 Règle de capture
        if last_pit and last_pit not in ['S1', 'S2']:
            if player == 1 and last_pit in self.player1_pits and self.board[last_pit] == 1:
                opposite = self.opposite_pits[last_pit]
                if self.board[opposite] > 0:
                    captured_seeds = self.board[opposite] + 1
                    self.board['S1'] += captured_seeds
                    self.board[last_pit] = 0
                    self.board[opposite] = 0
                    captured = True
            
            elif player == 2 and last_pit in self.player2_pits and self.board[last_pit] == 1:
                opposite = self.opposite_pits[last_pit]
                if self.board[opposite] > 0:
                    captured_seeds = self.board[opposite] + 1
                    self.board['S2'] += captured_seeds
                    self.board[last_pit] = 0
                    self.board[opposite] = 0
                    captured = True
        
        if play_again:
            return "play_again"
        elif captured:
            return True
        else:
            return False

    
    def get_board_state(self):
        """Retourner l'etat actuel du plateau pour l'interface"""
        return self.board.copy()