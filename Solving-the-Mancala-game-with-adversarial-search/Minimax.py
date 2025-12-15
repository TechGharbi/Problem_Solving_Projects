import copy

def MinimaxAlphaBetaPruning(game, player, depth, alpha, beta, player_type="computer_vs_human"):
    # Cas de base
    if depth == 0 or game.gameOver():
        # Utilisez la fonction d'evaluation appropriee
        if player_type == "computer_vs_computer":
           
            score = evaluate_computer_vs_computer(game, player)
        else:
            
            score = evaluate_computer_vs_human(game, player)
        
        return score, None
    
    # Determiner le joueur actuel
    current_player = 2 if player == 1 else 1  # MAX=2, MIN=1
    
    # Obtenir les mouvements possibles
    possible_moves = game.state.possibleMoves(current_player)
    
    if not possible_moves:
        score = evaluate_computer_vs_human(game, player)
        return score, None
    
    if player == 1:  # MAX 
        max_eval = -9999
        best_move = None
        
        for move in possible_moves:
            # Copier le jeu pour simuler
            game_copy = copy.deepcopy(game)
            
            # Jouer le mouvement
            game_copy.state.doMove(current_player, move)
            
            # Recursion
            eval_value, _ = MinimaxAlphaBetaPruning(game_copy, -player, depth-1, alpha, beta, player_type)
            
            if eval_value > max_eval:
                max_eval = eval_value
                best_move = move
            
            alpha = max(alpha, eval_value)
            if beta <= alpha:
                break  # elagage Beta
        
        return max_eval, best_move
    
    else:  # player == -1 
        min_eval = 9999
        best_move = None
        
        for move in possible_moves:
            # Copier le jeu pour simuler
            game_copy = copy.deepcopy(game)
            
            # Jouer le mouvement
            game_copy.state.doMove(current_player, move)
            
            # Recursion
            eval_value, _ = MinimaxAlphaBetaPruning(game_copy, -player, depth-1, alpha, beta, player_type)
            
            if eval_value < min_eval:
                min_eval = eval_value
                best_move = move
            
            beta = min(beta, eval_value)
            if beta <= alpha:
                break  # elagage Alpha
        
        return min_eval, best_move

def evaluate_computer_vs_human(game, player):
    """Une strategie simple pour les ordinateurs face aux humains"""
    # La difference entre le stockage informatique et le stockage humain
    if player == 1:  
        return game.state.board['S2'] - game.state.board['S1']
    else:  
        return game.state.board['S1'] - game.state.board['S2']

def evaluate_computer_vs_computer(game, player):
    """Une strategie astucieuse d'un ordinateur contre un autre ordinateur"""
    board = game.state.board
    
    if player == 1:  # 1 (MIN)
       # Calcul des points pour l'ordinateur 1
        store_diff = board['S1'] - board['S2']  
        
        # Nombre de boules dans la rangee de l'ordinateur : 1
        player1_total = sum(board[p] for p in ['A', 'B', 'C', 'D', 'E', 'F'])
        player2_total = sum(board[p] for p in ['G', 'H', 'I', 'J', 'K', 'L'])
        pit_diff = player1_total - player2_total
        
        # Possibilites de rediffusion
        replay_opportunities = 0
        for pit in ['A', 'B', 'C', 'D', 'E', 'F']:
            seeds = board[pit]
            if seeds > 0:
                
                final_pit = simulate_single_move(pit, 1, seeds, board)
                if final_pit == 'S1':
                    replay_opportunities += 1
        
        
        score = (store_diff * 5) + (pit_diff * 3) + (replay_opportunities * 10)
        
    else:  #  C2 (MAX)
        
        store_diff = board['S2'] - board['S1']  
        
        
        player2_total = sum(board[p] for p in ['G', 'H', 'I', 'J', 'K', 'L'])
        player1_total = sum(board[p] for p in ['A', 'B', 'C', 'D', 'E', 'F'])
        pit_diff = player2_total - player1_total
        
        replay_opportunities = 0
        for pit in ['G', 'H', 'I', 'J', 'K', 'L']:
            seeds = board[pit]
            if seeds > 0:
                
                final_pit = simulate_single_move(pit, 2, seeds, board)
                if final_pit == 'S2':
                    replay_opportunities += 1
        
        
        score = (store_diff * 5) + (pit_diff * 3) + (replay_opportunities * 10)
    
    return score

def simulate_single_move(start_pit, player, seeds, board):
    
    if player == 1:
        sequence = ['A', 'B', 'C', 'D', 'E', 'F', 'S1', 'L', 'K', 'J', 'I', 'H', 'G', 'A']
    else:
        sequence = ['L', 'K', 'J', 'I', 'H', 'G', 'S2', 'A', 'B', 'C', 'D', 'E', 'F', 'L']
    
    if start_pit not in sequence:
        return start_pit
    
    idx = sequence.index(start_pit)
    for _ in range(seeds):
        idx = (idx + 1) % len(sequence)
    
    return sequence[idx]