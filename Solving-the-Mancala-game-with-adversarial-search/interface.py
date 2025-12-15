import pygame
import sys
import math
import copy

class BallAnimation:
    """Classe pour contrôler l'animation des billes"""
    def __init__(self, start_pos, end_pos, speed=4, ball_size=15):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.speed = speed
        self.ball_size = ball_size
        self.current_pos = list(start_pos)
        self.active = True
        self.progress = 0.0
        
        # Calculer la distance et la direction
        self.dx = end_pos[0] - start_pos[0]
        self.dy = end_pos[1] - start_pos[1]
        self.distance = ((self.dx ** 2) + (self.dy ** 2)) ** 0.5
        
        if self.distance > 0:
            self.dx /= self.distance
            self.dy /= self.distance
    
    def update(self):
        """Mettre à jour la position de la bille"""
        if not self.active:
            return True
        
        self.progress += self.speed / self.distance
        if self.progress >= 1.0:
            self.current_pos = list(self.end_pos)
            self.active = False
            return True  # Animation terminée
        else:
            self.current_pos[0] = self.start_pos[0] + self.dx * self.distance * self.progress
            self.current_pos[1] = self.start_pos[1] + self.dy * self.distance * self.progress
        
        return False  # Animation en cours
    
    def draw(self, screen):
        """Dessiner la bille animée"""
        if self.active:
            # Dessiner l'ombre
            shadow_color = (50, 50, 50, 150)
            pygame.draw.circle(screen, shadow_color, 
                             (int(self.current_pos[0]) + 2, int(self.current_pos[1]) + 2), 
                             self.ball_size // 2)
            
            # Dessiner la bille
            ball_scaled = pygame.transform.scale(ball_img, (self.ball_size, self.ball_size))
            screen.blit(ball_scaled, 
                       (int(self.current_pos[0]) - self.ball_size // 2, 
                        int(self.current_pos[1]) - self.ball_size // 2))

try:
    from Game import Game
except ImportError:
    print("⚠️ Fichier Game.py non trouvé")
    sys.exit()

MAX = 1    # Ordinateur (Joueur 2)
MIN = -1   # Joueur humain (Joueur 1)

try:
    from Minimax import MinimaxAlphaBetaPruning
except ImportError:
    print("⚠️ Fichier Minimax.py non trouvé, utilisation d'un AI simple")
    def MinimaxAlphaBetaPruning(game, player, depth, alpha, beta, player_type="computer_vs_human"):
        """AI alternatif simple"""
        import random
        if player == MAX:
            current_player = 2  # Ordinateur
        else:
            current_player = 1  # Humain
        
        moves = game.state.possibleMoves(current_player)
        if moves:
            return 0, random.choice(moves)
        return 0, None

pygame.init()

# Taille de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Création de la fenêtre principale
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Mancala 3D")

# États du jeu
STATE_LOADING = 0
STATE_MENU = 1
STATE_LEVELS = 2
STATE_TUTORIAL = 3
STATE_GAME = 4
STATE_GAME_OVER = 5

current_state = STATE_LOADING

game_ai = None
ai_depth = 4
player_turn = 1  # 1: Joueur 1, 2: Joueur 2
game_mode = "human_vs_ai"  # "human_vs_ai", "ai_vs_ai"
ai1_depth = 4  
ai2_depth = 2  

player1_pits = [4, 4, 4, 4, 4, 4]  # A B C D E F
player2_pits = [4, 4, 4, 4, 4, 4]  # G H I J K L
player1_store = 0
player2_store = 0

# Noms des fosses
pit_names_player1 = ["A", "B", "C", "D", "E", "F"]
pit_names_player2 = ["G", "H", "I", "J", "K", "L"]

active_animations = []

ai_delay_timer = 0


try:
    # Images des écrans
    loading_img = pygame.image.load("assets/loading.png").convert_alpha()
    menu_img = pygame.image.load("assets/menu.png").convert_alpha()
    levels_img = pygame.image.load("assets/levels.png").convert_alpha()
    
    # Images du jeu
    background_img = pygame.image.load("assets/background.png").convert_alpha()
    board_img = pygame.image.load("assets/board.png").convert_alpha()
    player1_img = pygame.image.load("assets/player1.png").convert_alpha()
    player2_img = pygame.image.load("assets/player2.png").convert_alpha()
    box_img = pygame.image.load("assets/box.png").convert_alpha()
    
    notification_window_img = pygame.image.load("assets/notification.png").convert_alpha()
    
    try:
        ball_img = pygame.image.load("assets/ball.png").convert_alpha()
    except:
        ball_img = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(ball_img, (255, 100, 100), (10, 10), 9)
        pygame.draw.circle(ball_img, (255, 200, 200), (5, 5), 4)
    
    # 🎯 Images notifications 
    turn_p1_img = pygame.image.load("assets/tourPlayer1.png").convert_alpha()
    turn_p2_img = pygame.image.load("assets/tourPlayer2.png").convert_alpha()
    get_it_img = pygame.image.load("assets/get_it.png").convert_alpha()
    play_again_img = pygame.image.load("assets/play_again.png").convert_alpha()
    
    winner_p1_img = pygame.image.load("assets/winner_player1.png").convert_alpha()
    winner_p2_img = pygame.image.load("assets/winner_player2.png").convert_alpha()

    # Redimensionner
    notification_window_img = pygame.transform.scale(notification_window_img, (600, 100))
    
    # Redimensionner les images principales
    loading_img = pygame.transform.scale(loading_img, WINDOW_SIZE)
    menu_img = pygame.transform.scale(menu_img, WINDOW_SIZE)
    levels_img = pygame.transform.scale(levels_img, WINDOW_SIZE)
    background_img = pygame.transform.scale(background_img, WINDOW_SIZE)
    
    # Redimensionner les images du jeu
    board_img = pygame.transform.scale(board_img, (700, 200))
    player1_img = pygame.transform.scale(player1_img, (200, 80))
    player2_img = pygame.transform.scale(player2_img, (200, 80))
    box_img = pygame.transform.scale(box_img, (100, 50))
    ball_img = pygame.transform.scale(ball_img, (15, 15))
    
    # Création d'une image de tutoriel
    tutorial_img = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    tutorial_img.fill((50, 50, 100))
    font = pygame.font.Font(None, 48)
    text = font.render("TUTORIAL MANCALA 3D", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 100))
    tutorial_img.blit(text, text_rect)
    
    font_small = pygame.font.Font(None, 32)
    instructions = [
        "Règles du Mancala:",
        "1. Chaque joueur a 6 fosses et un magasin.",
        "2. Chaque fosse contient 4 billes au début.",
        "3. Choisissez une fosse pour prendre toutes ses billes.",
        "4. Distribuez les billes une par une.",
        "5. Si votre dernière bille tombe dans votre magasin, rejouez.",
        "6. Si votre dernière bille tombe dans une fosse vide, capturez.",
        "7. Le jeu se termine quand un joueur n'a plus de billes.",
        "8. Le joueur avec le plus de billes dans son magasin gagne."
    ]
    
    for i, line in enumerate(instructions):
        line_text = font_small.render(line, True, (255, 255, 255))
        line_rect = line_text.get_rect(topleft=(50, 150 + i*40))
        tutorial_img.blit(line_text, line_rect)
    
    back_text = font_small.render("CLIQUEZ N'IMPORTE OU POUR RETOURNER", True, (255, 255, 255))
    back_rect = back_text.get_rect(center=(WINDOW_WIDTH//2, 500))
    tutorial_img.blit(back_text, back_rect)
    
except pygame.error as e:
    print(f"Erreur lors du chargement des images: {e}")
    print("Assurez-vous que toutes les images sont dans le dossier assets/")
    sys.exit()

# ============================================================
# 🎯 مناطق النقر - الأزرار
# ============================================================

menu_buttons = {
    "against_ai": pygame.Rect(330, 260, 140, 50),
    "two_players": pygame.Rect(330, 340, 140, 50),
    "tutorial": pygame.Rect(330, 420, 140, 50)
}

level_buttons = {
    "easy": pygame.Rect(330, 250, 145, 50),
    "normal": pygame.Rect(330, 330, 145, 50),
    "hard": pygame.Rect(330, 410, 145, 50),
    "back": pygame.Rect(720, 20, 60, 60)
}

game_over_buttons = {
    "play_again": pygame.Rect(250, 450, 150, 50),
    "main_menu": pygame.Rect(420, 450, 150, 50)
}

# ============================================================
# 🎯 إحداثيات الحفر والمخازن
# ============================================================

pit_positions = {
    # Player 1 (bas) - A à F
    "A": (180, 380),
    "B": (270, 380),
    "C": (355, 380),
    "D": (440, 380),
    "E": (530, 380),
    "F": (620, 380),
    
    # Player 2 (haut) - G à L
    "G": (200, 290),
    "H": (280, 290),
    "I": (360, 290),
    "J": (440, 290),
    "K": (520, 290),
    "L": (600, 290),
    
    # STORES
    "S1": (685, 340),  
    "S2": (115, 340)   
}

# Rayon des cercles (pits)
pit_radius = 30

# Magasins (stores) - ovale
store_width = 70
store_height = 180
store2_rect = pygame.Rect(70, 250, store_width, store_height)  
store1_rect = pygame.Rect(650, 250, store_width, store_height)  

# ============================================================
# 🎮 نظام الإشعارات الجديد
# ============================================================

notification_text = ""
notification_start = 0
NOTIF_DURATION = 3000  # 3 ثواني

# ============================================================
# ⏱️ مؤقتات التحميل
# ============================================================

loading_time = 2000
loading_start = pygame.time.get_ticks()

# Niveau de difficulté
current_difficulty = "normal"

# Police pour le texte
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 28)
font_notification = pygame.font.Font(None, 32)

# ============================================================
# 🎮 الدوال المساعدة
# ============================================================

def check_button_click(mouse_pos, buttons):
    """Vérifier le clic sur un bouton"""
    for button_name, button_rect in buttons.items():
        if button_rect.collidepoint(mouse_pos):
            return button_name
    return None

def show_notification(text):
    """Afficher une notification textuelle"""
    global notification_text, notification_start
    notification_text = text
    notification_start = pygame.time.get_ticks()

def sync_board_with_game():
    """Synchroniser les données du plateau avec l'objet Game"""
    global player1_pits, player2_pits, player1_store, player2_store
    
    if game_ai is None:
        return
    
    # Mettre à jour les fosses
    for i, pit_name in enumerate(pit_names_player1):
        if pit_name in game_ai.state.board:
            player1_pits[i] = game_ai.state.board[pit_name]
    
    for i, pit_name in enumerate(pit_names_player2):
        if pit_name in game_ai.state.board:
            player2_pits[i] = game_ai.state.board[pit_name]
    
    # Mettre à jour les magasins
    player1_store = game_ai.state.board['S1']
    player2_store = game_ai.state.board['S2']
    
    return True

def draw_notification():
    """🎯 Dessiner la notification dans la fenêtre dédiée"""
    global notification_text
    
    if notification_text:
        now = pygame.time.get_ticks()
        if now - notification_start < NOTIF_DURATION:
            notification_rect = notification_window_img.get_rect(center=(WINDOW_WIDTH//2, 540))
            screen.blit(notification_window_img, notification_rect)
            
            text_surface = font_notification.render(notification_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, 545))
            screen.blit(text_surface, text_rect)
        else:
            notification_text = ""  # Supprimer la notification après expiration

def draw_ball_with_effect(x, y, size=15):
    """🎯 Dessiner une bille avec effet d'ombre"""
    # Dessiner l'ombre
    shadow_color = (50, 50, 50, 150)
    pygame.draw.circle(screen, shadow_color, (x+2, y+2), size//2)
    
    # Dessiner la bille
    ball_scaled = pygame.transform.scale(ball_img, (size, size))
    screen.blit(ball_scaled, (x - size//2, y - size//2))
    
    # Effet de brillance
    highlight = pygame.Surface((size//3, size//3), pygame.SRCALPHA)
    highlight.fill((255, 255, 255, 100))
    screen.blit(highlight, (x - size//4, y - size//4))

def draw_store_balls(store_rect, ball_count, player_num):
    """🎯 Dessiner les billes dans le magasin"""
    center_x = store_rect.centerx
    center_y = store_rect.centery
    
    if ball_count == 0:
        return
    
    # Arranger les billes en rangées
    max_per_row = 4
    ball_size = 18
    spacing = 22
    
    # Calculer le nombre de rangées
    rows = (ball_count + max_per_row - 1) // max_per_row
    
    # Commencer à dessiner depuis le haut
    start_y = center_y - (rows * spacing) // 2
    
    ball_index = 0
    for row in range(rows):
        # Nombre de billes dans cette rangée
        balls_in_row = min(max_per_row, ball_count - ball_index)
        start_x = center_x - ((balls_in_row - 1) * spacing) // 2
        
        for col in range(balls_in_row):
            x = start_x + col * spacing
            y = start_y + row * spacing
            
            # ضبط الموضع لمخزن اللاعب 1
            if player_num == 1:
                x = store_rect.centerx - 35 + col * 18
                y = store_rect.top + 40 + row * 25
            else:  
                x = store_rect.centerx - 35 + col * 18
                y = store_rect.top + 40 + row * 25
            
            draw_ball_with_effect(x, y, ball_size)
            ball_index += 1

def draw_pit_with_balls(pit_name, center_x, center_y, ball_count):
    """🎯 Dessiner une fosse avec ses billes"""
    # Dessiner les billes avec effet 3D
    if ball_count > 0:
        radius = min(20, 10 + ball_count)
        for i in range(ball_count):
            angle = (2 * math.pi * i) / max(ball_count, 1)
            offset_x = radius * math.cos(angle)
            offset_y = radius * math.sin(angle)
            draw_ball_with_effect(center_x + offset_x, center_y + offset_y)

def get_next_pit_for_player(current_pit, player):
    """🎯 الحصول على الحفرة التالية حسب اللاعب"""
    if player == 1:
        sequence_1 = ['A', 'B', 'C', 'D', 'E', 'F', 'S1', 'L', 'K', 'J', 'I', 'H', 'G', 'A']
        if current_pit not in sequence_1:
            return 'A'
        
        idx = sequence_1.index(current_pit)
        next_idx = (idx + 1) % len(sequence_1)
        next_pit = sequence_1[next_idx]
        
        if next_pit == 'S2':
            next_idx = (next_idx + 1) % len(sequence_1)
            next_pit = sequence_1[next_idx]
            
        return next_pit
    
    else:  # player == 2
        sequence_2 = ['L', 'K', 'J', 'I', 'H', 'G', 'S2', 'A', 'B', 'C', 'D', 'E', 'F', 'L']
        if current_pit not in sequence_2:
            return 'L'
        
        idx = sequence_2.index(current_pit)
        next_idx = (idx + 1) % len(sequence_2)
        next_pit = sequence_2[next_idx]
        
        if next_pit == 'S1':
            next_idx = (next_idx + 1) % len(sequence_2)
            next_pit = sequence_2[next_idx]
            
        return next_pit

def simulate_move_with_animation(player, pit_name, num_balls=None):
    """🎯 محاكاة الحركة مع الرسوم المتحركة"""
    if not game_ai or pit_name not in game_ai.state.board:
        return
    
    if num_balls is None:
        num_balls = game_ai.state.board[pit_name]
    
    if num_balls == 0:
        return
    
    current_pit = pit_name
    path = []
    
    for i in range(num_balls):
        next_pit = get_next_pit_for_player(current_pit, player)
        path.append((current_pit, next_pit))
        current_pit = next_pit
    
    for start_pit, end_pit in path:
        animate_move(start_pit, end_pit)

def animate_move(start_pit, end_pit):
    """Ajouter une animation de mouvement"""
    if start_pit in pit_positions and end_pit in pit_positions:
        animation = BallAnimation(pit_positions[start_pit], pit_positions[end_pit], speed=4)
        active_animations.append(animation)

def update_animations():
    """Mettre à jour toutes les animations"""
    animations_to_remove = []
    
    for i, animation in enumerate(active_animations):
        finished = animation.update()
        if finished:
            animations_to_remove.append(i)
    
    # Supprimer les animations terminées
    for i in reversed(animations_to_remove):
        active_animations.pop(i)

def draw_animations():
    """Dessiner les animations"""
    for animation in active_animations:
        animation.draw(screen)

def show_loading():
    """Afficher l'écran de chargement"""
    screen.blit(loading_img, (0, 0))

def show_menu():
    """Afficher le menu principal"""
    screen.blit(menu_img, (0, 0))

def show_levels():
    """Afficher l'écran de sélection du niveau"""
    screen.blit(levels_img, (0, 0))

def show_tutorial():
    """Afficher les instructions"""
    screen.blit(tutorial_img, (0, 0))

def show_game_over():
    """🎮 Afficher l'écran de fin de jeu"""
    global game_ai, player1_store, player2_store
    
    if not game_ai:
        return
    
    winner = game_ai.findWinner()
    
    overlay = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) 
    screen.blit(overlay, (0, 0))
    
    # 🏆 Affichage de le gagnant
    if winner == 1:
        winner_img = winner_p1_img
        winner_title = "PLAYER 1 WINS!"
        winner_color = (0, 200, 0)
    elif winner == 2:
        winner_img = winner_p2_img
        winner_title = "PLAYER 2 WINS!"
        winner_color = (200, 0, 0)
    else:
        winner_img = None
        winner_title = "MATCH DRAW!"
        winner_color = (200, 200, 0)
    
    if winner_img:
        img_width = min(winner_img.get_width(), 600)
        img_height = min(winner_img.get_height(), 500)
        
        img_rect = winner_img.get_rect(center=(WINDOW_WIDTH//2, 320))
        screen.blit(winner_img, img_rect)
    else:
        font_large = pygame.font.Font(None, 60)
        title_surface = font_large.render(winner_title, True, winner_color)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH//2, 150))
        screen.blit(title_surface, title_rect)

def show_game():
    """🎮 Afficher l'écran de jeu principal"""
    global notification_text
    
    # Afficher l'arrière-plan
    screen.blit(background_img, (0, 0))
    
    # Afficher le plateau au centre
    board_x = (WINDOW_WIDTH - 700) // 2
    board_y = (WINDOW_HEIGHT - 100) // 2
    screen.blit(board_img, (board_x, board_y))
    
    # Afficher les joueurs en haut
    screen.blit(player1_img, (30, 30))
    screen.blit(player2_img, (WINDOW_WIDTH - 230, 30))
    
    # Afficher la boîte de score
    box_x = (WINDOW_WIDTH - 100) // 2
    screen.blit(box_img, (box_x, 50))
    
    # Afficher les scores
    score_text = font_medium.render(f"{player1_store}   {player2_store}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, 78))
    screen.blit(score_text, score_rect)
    
    # ============================================================
    # 🎯 Dessiner les billes dans les fosses
    # ============================================================
    
    # Dessiner les fosses du Joueur 1 (A-F)
    for i, pit_name in enumerate(pit_names_player1):
        center_x, center_y = pit_positions[pit_name]
        ball_count = player1_pits[i]
        draw_pit_with_balls(pit_name, center_x, center_y, ball_count)
    
    # Dessiner les fosses du Joueur 2 (G-L)
    for i, pit_name in enumerate(pit_names_player2):
        center_x, center_y = pit_positions[pit_name]
        ball_count = player2_pits[i]
        draw_pit_with_balls(pit_name, center_x, center_y, ball_count)
    
    # ============================================================
    # 🎯 Dessiner les billes dans les magasins
    # ============================================================
    draw_store_balls(store1_rect, player1_store, 1)
    draw_store_balls(store2_rect, player2_store, 2)
    
    # ============================================================
    # 🎯 Dessiner les animations
    # ============================================================
    draw_animations()
    
    # ============================================================
    # 🎯 Afficher les notifications في النافذة المخصصة
    # ============================================================
    draw_notification()

    # ============================================================
    # 🎯 Informations supplémentaires
    # ============================================================
    
    # Afficher les noms des joueurs
    player1_label = font_medium.render("JOUEUR 1 (A-F)", True, (255, 255, 255))
    player1_label_rect = player1_label.get_rect(center=(WINDOW_WIDTH//2, 460))
    screen.blit(player1_label, player1_label_rect)
    
    player2_label = font_medium.render("JOUEUR 2 (G-L)", True, (255, 255, 255))
    player2_label_rect = player2_label.get_rect(center=(WINDOW_WIDTH//2, 240))
    screen.blit(player2_label, player2_label_rect)
    
    # Afficher le tour actuel
    turn_text = font_medium.render(f"TOUR: JOUEUR {player_turn}", True, (255, 255, 255))
    turn_rect = turn_text.get_rect(center=(WINDOW_WIDTH//2, 140))
    screen.blit(turn_text, turn_rect)
    
    # Afficher وضع اللعبة
    if game_mode == "human_vs_ai":
        mode_text = "MODE: HUMAIN vs IA"
    else:
        mode_text = "MODE: IA vs IA"
    
    mode_label = font_small.render(mode_text, True, (255, 255, 255))
    mode_rect = mode_label.get_rect(center=(WINDOW_WIDTH//2, 170))
    screen.blit(mode_label, mode_rect)
    
    # Afficher la difficulté (في وضع human_vs_ai فقط)
    if game_mode == "human_vs_ai":
        diff_text = font_small.render(f"DIFFICULTÉ: {current_difficulty.upper()}", True, (255, 255, 255))
        diff_rect = diff_text.get_rect(center=(WINDOW_WIDTH//2, 190))
        screen.blit(diff_text, diff_rect)
    else:
        # في وضع ai_vs_ai، عرض ذكاء الكمبيوترات
        comp_text = font_small.render(f"IA1: Niveau {ai1_depth} | IA2: Niveau {ai2_depth}", True, (255, 255, 255))
        comp_rect = comp_text.get_rect(center=(WINDOW_WIDTH//2, 190))
        screen.blit(comp_text, comp_rect)
    
    # Bouton retour
    pygame.draw.rect(screen, (205, 0, 0, 180), pygame.Rect(755, 9, 40, 40), border_radius=70)
    back_text = font_medium.render("X", True, (255, 255, 255))
    back_text_rect = back_text.get_rect(center=(775, 30))
    screen.blit(back_text, back_text_rect)
    
def reset_game():
    """Réinitialiser le jeu"""
    global game_ai, player_turn, player1_pits, player2_pits, player1_store, player2_store, notification_text, active_animations, ai_delay_timer
    
    # Créer un nouveau jeu
    game_ai = Game()
    
    # Réinitialiser les variables
    player_turn = 1
    player1_pits = [4, 4, 4, 4, 4, 4]
    player2_pits = [4, 4, 4, 4, 4, 4]
    player1_store = 0
    player2_store = 0
    notification_text = ""
    active_animations.clear()
    ai_delay_timer = 0
    
    # Synchroniser le plateau
    sync_board_with_game()
    
    if game_mode == "human_vs_ai":
        show_notification("Player 1's Turn")
    elif game_mode == "ai_vs_ai":
        show_notification("Player 1's Turn")
    
    return True

def execute_player_move(player, pit_name):
    """Exécuter UN SEUL mouvement pour un joueur"""
    if not game_ai or pit_name not in game_ai.state.board:
        return False
    
    # Vérifier si la fosse contient des billes
    if game_ai.state.board[pit_name] == 0:
        return False
    
    # 🎯 Simuler le mouvement avec animation
    simulate_move_with_animation(player, pit_name, game_ai.state.board[pit_name])
    
    # 🎯 Exécuter le mouvement dans le jeu (un seul mouvement)
    result = game_ai.state.doMove(player, pit_name)
    
    # 🎯 Synchroniser le plateau
    sync_board_with_game()
    
    # Traiter les résultats
    if result == "play_again":
        show_notification("Play Again!")
        return "play_again"
    elif result:  # S'il y a capture
        show_notification("You get the other player's stones!")
        return True
    else:
        return True

def play_computer_turn():
    """🎯 Jouer UN SEUL tour d'un ordinateur"""
    global player_turn, ai_delay_timer, current_state
    
    if not game_ai or game_ai.gameOver():
        current_state = STATE_GAME_OVER
        return "game_over"
    
    if player_turn == 1:
        current_depth = ai1_depth
        ai_player = "computer_vs_computer"  
    else:
        current_depth = ai2_depth
        ai_player = "computer_vs_human"  
    
    if player_turn == 1:
        player_for_ai = MIN  # Computer 1 
    else:
        player_for_ai = MAX  # Computer 2 
    
    best_value, best_pit = MinimaxAlphaBetaPruning(
        game_ai, player_for_ai, current_depth, -9999, 9999, ai_player
    )
    
    if best_pit:
        result = execute_player_move(player_turn, best_pit)
        
        if result == "play_again":
            # الكمبيوتر يعيد اللعب
            player_turn = player_turn
            if player_turn == 1:
                show_notification("Player 1's Turn - Play Again!")
            else:
                show_notification("Player 2's Turn - Play Again!")
            ai_delay_timer = pygame.time.get_ticks() + 1500
        elif result:
            player_turn = 1 if player_turn == 2 else 2
            
            # عرض إشعار الدور الجديد
            if player_turn == 1:
                show_notification("Player 1's Turn")
            else:
                show_notification("Player 2's Turn")
            
            if game_ai.gameOver():
                current_state = STATE_GAME_OVER
                return "game_over"
            
            if game_mode == "ai_vs_ai":
                ai_delay_timer = pygame.time.get_ticks() + 1500
        else:
            player_turn = 1 if player_turn == 2 else 2
            if player_turn == 1:
                show_notification("Player 1's Turn")
            else:
                show_notification("Player 2's Turn")
    
    else:
        player_turn = 1 if player_turn == 2 else 2
        if player_turn == 1:
            show_notification("Player 1's Turn")
        else:
            show_notification("Player 2's Turn")
    
    return None

def play_human_vs_ai_turn():
    """🎯 Jouer UN SEUL tour de l'IA contre l'humain"""
    global player_turn, ai_delay_timer, current_state
    
    if not game_ai or player_turn != 2 or game_ai.gameOver():
        if game_ai and game_ai.gameOver():
            current_state = STATE_GAME_OVER
        return
    
    # Obtenir le meilleur mouvement avec Minimax
    best_value, best_pit = MinimaxAlphaBetaPruning(
        game_ai, MAX, ai_depth, -9999, 9999, "computer_vs_human"
    )
    
    if best_pit:
        # 🎯 Exécuter un seul mouvement
        result = execute_player_move(2, best_pit)
        
        # Traiter les résultats
        if result == "play_again":
            # L'IA rejoue
            player_turn = 2
            show_notification("Player 2's Turn - Play Again!")
            # Délai pour le prochain tour
            ai_delay_timer = pygame.time.get_ticks() + 1500
        elif result:
            # Mouvement réussi, passer au Joueur 1
            player_turn = 1
            show_notification("Player 1's Turn")
            
            # Vérifier la fin du jeu
            if game_ai.gameOver():
                current_state = STATE_GAME_OVER
                return "game_over"
        else:
            # Erreur dans le mouvement
            player_turn = 1
            show_notification("Player 1's Turn")
    
    else:
        player_turn = 1
        show_notification("Player 1's Turn")
    
    return None

# ============================================================
# 🎮 الحلقة الرئيسية للعبة
# ============================================================

clock = pygame.time.Clock()
running = True

# Notification de début
show_notification("Player 1's Turn")

while running:
    # 🎯 Mettre à jour les animations
    update_animations()
    
    current_time = pygame.time.get_ticks()
    if ai_delay_timer > 0 and current_time >= ai_delay_timer:
        ai_delay_timer = 0
        if current_state == STATE_GAME:
            if game_mode == "human_vs_ai" and player_turn == 2:
                play_human_vs_ai_turn()
            elif game_mode == "ai_vs_ai":
                play_computer_turn()
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if current_state == STATE_MENU:
                clicked_button = check_button_click(mouse_pos, menu_buttons)
                
                if clicked_button == "against_ai":
                    game_mode = "human_vs_ai"
                    current_state = STATE_LEVELS
                elif clicked_button == "tutorial":
                    current_state = STATE_TUTORIAL
                elif clicked_button == "two_players":
                    game_mode = "ai_vs_ai"
                    current_difficulty = "normal"
                    ai1_depth = 4 
                    ai2_depth = 2  
                    
                    reset_game()
                    current_state = STATE_GAME
                    
            elif current_state == STATE_LEVELS:
                clicked_button = check_button_click(mouse_pos, level_buttons)
                
                if clicked_button == "back":
                    current_state = STATE_MENU
                elif clicked_button in ["easy", "normal", "hard"]:
                    current_difficulty = clicked_button
                    
                    if current_difficulty == "easy":
                        ai_depth = 2
                    elif current_difficulty == "normal":
                        ai_depth = 4
                    else:  # hard
                        ai_depth = 6
                    
                    reset_game()
                    current_state = STATE_GAME
                    
            elif current_state == STATE_TUTORIAL:
                current_state = STATE_MENU
                
            elif current_state == STATE_GAME:
                if pygame.Rect(720, 20, 60, 60).collidepoint(mouse_pos):
                    current_state = STATE_MENU
                
                elif player_turn == 1 and not game_ai.gameOver() and game_mode == "human_vs_ai":
                    for pit_name, (center_x, center_y) in pit_positions.items():
                        if pit_name in pit_names_player1:
                            distance = ((mouse_pos[0] - center_x)**2 + 
                                      (mouse_pos[1] - center_y)**2)**0.5
                            
                            if distance <= pit_radius:
                                index = pit_names_player1.index(pit_name)
                                if player1_pits[index] > 0:
                                    result = execute_player_move(1, pit_name)
                                    
                                    if result == "play_again":
                                        show_notification("Play Again!")
                                        player_turn = 1
                                    elif result:
                                        player_turn = 2
                                        show_notification("Player 2's Turn")
                                        ai_delay_timer = pygame.time.get_ticks() + 1500
                                    
                                    if game_ai.gameOver():
                                        current_state = STATE_GAME_OVER
                                
                                break
             
            elif current_state == STATE_GAME_OVER:
                clicked_button = check_button_click(mouse_pos, game_over_buttons)
                
                if clicked_button == "play_again":
                    reset_game()
                    current_state = STATE_GAME
                elif clicked_button == "main_menu":
                    current_state = STATE_MENU
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_state == STATE_GAME_OVER:
                    current_state = STATE_MENU
                else:
                    current_state = STATE_MENU
            elif event.key == pygame.K_r:
                reset_game()
    
    if current_state == STATE_LOADING:
        current_time = pygame.time.get_ticks()
        if current_time - loading_start >= loading_time:
            current_state = STATE_MENU
    
    if current_state == STATE_LOADING:
        show_loading()
    elif current_state == STATE_MENU:
        show_menu()
    elif current_state == STATE_LEVELS:
        show_levels()
    elif current_state == STATE_TUTORIAL:
        show_tutorial()
    elif current_state == STATE_GAME:
        show_game()
        
        if player_turn == 2 and ai_delay_timer == 0 and game_mode == "human_vs_ai":
            play_human_vs_ai_turn()
        elif game_mode == "ai_vs_ai" and ai_delay_timer == 0 and not game_ai.gameOver():
            play_computer_turn()
            
    elif current_state == STATE_GAME_OVER:
        show_game()  
        show_game_over()  
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()