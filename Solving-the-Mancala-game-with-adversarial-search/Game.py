from MancalaBoard import MancalaBoard

class Game:
   
    def __init__(self):
        self.state = MancalaBoard()
        self.turn = 1  # 1: Joueur 1 (MIN), 2: Joueur 2 (MAX)
    
    def gameOver(self):
        """Verifier si le jeu est termine"""
        return len(self.state.possibleMoves(1)) == 0 or len(self.state.possibleMoves(2)) == 0
    
    def findWinner(self):
        """Determiner le gagnant"""
        if self.state.board['S1'] > self.state.board['S2']:
            return 1
        elif self.state.board['S2'] > self.state.board['S1']:
            return 2
        else:
            return 0  
    
    def can_capture(self, pit, player):
        seeds = self.state.board[pit]
        if seeds == 0:
            return False
        
        current_pit = pit
        for i in range(seeds):
            if player == 1:
                sequence = ['A', 'B', 'C', 'D', 'E', 'F', 'S1', 'L', 'K', 'J', 'I', 'H', 'G', 'A']
            else:
                sequence = ['L', 'K', 'J', 'I', 'H', 'G', 'S2', 'A', 'B', 'C', 'D', 'E', 'F', 'L']
            
            idx = sequence.index(current_pit) if current_pit in sequence else 0
            next_idx = (idx + 1) % len(sequence)
            current_pit = sequence[next_idx]
        
        if player == 1 and current_pit in self.state.player1_pits:
            return self.state.board[current_pit] == 0
        elif player == 2 and current_pit in self.state.player2_pits:
            return self.state.board[current_pit] == 0
        
        return False