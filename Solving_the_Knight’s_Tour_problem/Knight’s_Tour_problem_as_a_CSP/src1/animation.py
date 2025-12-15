# animation.py
import pygame
import sys

# Initialisation
pygame.init()

# === CONFIGURATION ===
board_size = 8
square_size = 80
width = board_size * square_size
height = board_size * square_size + 100
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Knight's Tour - Algorithme Génétique")
clock = pygame.time.Clock()

# === COULEURS ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BROWN = (161, 122, 67)
DARK_BROWN = (76, 42, 33)
HOVER_BROWN = (210, 165, 125)
GOLD = (255, 215, 0)
DARK_GOLD = (184, 134, 11)

# === POLICES ===

    # Essayer de charger la police Algerian
title_font = pygame.font.SysFont('Algerian', 48, bold=True)
font = pygame.font.SysFont('Algerian', 20, bold=False)
small_font = pygame.font.SysFont('Algerian', 15)

# === IMAGE DE FOND ===
try:
    background_image = pygame.image.load("tournament.jpg")
    background_image = pygame.transform.scale(background_image, (width, height))
except pygame.error:
    print("Image 'tournament.jpg' non trouvée !")
    background_image = None

# === IMAGE DU CAVALIER ===
try:
    knight_image = pygame.image.load("knight.png")
    image_size = square_size - 20
    aspect_ratio = knight_image.get_width() / knight_image.get_height()
    new_width = image_size if aspect_ratio > 1 else int(image_size * aspect_ratio)
    new_height = int(image_size / aspect_ratio) if aspect_ratio > 1 else image_size
    knight_image = pygame.transform.scale(knight_image, (new_width, new_height))
except pygame.error:
    print("Image 'knight.png' non trouvée !")
    pygame.quit()
    sys.exit(1)

# === ÉTAT ===
path = None
passed_positions = []
path_index = 0
is_playing = False
is_running = True
animation_speed = 2
show_start_popup = False
start_pos = (0, 0)

# === CLASSE BOUTON ===
class Button:
    def __init__(self, text, x, y, w, h, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=20)
        pygame.draw.rect(surface, GOLD, self.rect, 4, border_radius=20)
        text_surf = font.render(self.text, True, BLACK if color != DARK_GOLD else WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and event.button == 1 and self.action:
                return self.action()
        return None

# === FONCTIONS ===
def select_x(val):
    global start_pos
    start_pos = (val, start_pos[1])
    highlight_buttons()

def select_y(val):
    global start_pos
    start_pos = (start_pos[0], val)
    highlight_buttons()

def highlight_buttons():
    for i, btn in enumerate(x_buttons):
        btn.color = GOLD if i == start_pos[0] else LIGHT_BROWN
        btn.hover_color = GOLD if i == start_pos[0] else HOVER_BROWN
    for i, btn in enumerate(y_buttons):
        btn.color = GOLD if i == start_pos[1] else LIGHT_BROWN
        btn.hover_color = GOLD if i == start_pos[1] else HOVER_BROWN

def toggle_pause():
    global is_playing
    is_playing = not is_playing
    pause_button.text = "Play" if not is_playing else "Pause"

def go_back():
    global path_index, passed_positions
    if path_index > 0:
        path_index -= 1
        passed_positions = path[:path_index]

def reset_animation():
    global path_index, passed_positions
    path_index = 0
    passed_positions = []

# === BOUTONS PRINCIPAUX ===
start_button = Button("START", width//2 - 100, 500, 200, 80, DARK_GOLD, GOLD, action=lambda: "start")

pause_button   = Button("Pause",   50, 660, 100, 60, LIGHT_BROWN, HOVER_BROWN, action=lambda: toggle_pause())
back_button    = Button("Back",   170, 660, 100, 60, LIGHT_BROWN, HOVER_BROWN, action=lambda: go_back())
again_button   = Button("Again",  290, 660, 100, 60, LIGHT_BROWN, HOVER_BROWN, action=lambda: reset_animation())
restart_button = Button("Restart",410, 660, 120, 60, LIGHT_BROWN, HOVER_BROWN, action=lambda: "restart")

# === POPUP : BOUTONS 0–7 (AMÉLIORÉ) ===
popup_width = 500
popup_height = 350
popup_x = (width - popup_width) // 2
popup_y = (height - popup_height) // 2

# Positionnement des boutons X (colonnes)
x_button_start_x = popup_x + 120
x_button_y = popup_y + 100

# Positionnement des boutons Y (lignes)
y_button_start_x = x_button_start_x
y_button_y = popup_y + 160

x_buttons = [
    Button(str(i), x_button_start_x + i * 45, x_button_y, 40, 40, LIGHT_BROWN, HOVER_BROWN, action=lambda i=i: select_x(i))
    for i in range(8)
]
y_buttons = [
    Button(str(i), y_button_start_x + i * 45, y_button_y, 40, 40, LIGHT_BROWN, HOVER_BROWN, action=lambda i=i: select_y(i))
    for i in range(8)
]

# Boutons de confirmation/annulation
confirm_button = Button("Play", popup_x + 120, popup_y + 220, 120, 50, (0, 150, 0), (0, 200, 0), action=lambda: "confirm")
cancel_button  = Button("Cancel",  popup_x + 260, popup_y + 220, 120, 50, (150, 0, 0), (200, 0, 0), action=lambda: "cancel")

# === DESSIN ===
def draw_board():
    for row in range(board_size):
        for col in range(board_size):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))
            pos = (col, row)
            if pos in passed_positions:
                idx = passed_positions.index(pos)
                pygame.draw.rect(screen, GREEN, (col * square_size + 5, row * square_size + 5, square_size - 10, square_size - 10), 3)
                num_text = small_font.render(str(idx + 1), True, WHITE)
                num_rect = num_text.get_rect(center=(col * square_size + square_size//2, row * square_size + square_size//2))
                screen.blit(num_text, num_rect)

def draw_knight(pos):
    x, y = pos
    knight_rect = knight_image.get_rect(center=(x * square_size + square_size//2, y * square_size + square_size//2))
    screen.blit(knight_image, knight_rect)

# === ÉCRANS ===
def waiting_screen():
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((245, 245, 245))

    title = title_font.render("KNIGHT'S TOUR", True, BLACK)
    subtitle = font.render("Algorithme Génétique", True, WHITE)
    screen.blit(title, (width//2 - title.get_width()//2, 380))
    screen.blit(subtitle, (width//2 - subtitle.get_width()//2, 420))

    start_button.draw(screen)
    if show_start_popup:
        draw_popup()

def draw_popup():
    # Fond semi-transparent
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Boîte de dialogue
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(screen, (240, 220, 180), popup_rect, border_radius=20)
    pygame.draw.rect(screen, GOLD, popup_rect, 5, border_radius=20)

    # Titre
    title = font.render("Position de départ", True, BLACK)
    screen.blit(title, (popup_x + popup_width//2 - title.get_width()//2, popup_y + 30))

    # Labels
    label_x = small_font.render("Colonne(X):", True, BLACK)
    label_y = small_font.render("Ligne(Y):", True, BLACK)
    screen.blit(label_x, (popup_x + 30, x_button_y + 15))
    screen.blit(label_y, (popup_x + 30, y_button_y + 15))

    # Boutons 0–7
    for btn in x_buttons + y_buttons:
        btn.draw(screen)

    # Boutons action
    confirm_button.draw(screen)
    cancel_button.draw(screen)

    # Affichage position sélectionnée
    pos_text = small_font.render(f"Position sélectionnée: ({start_pos[0]}, {start_pos[1]})", True, (0, 100, 0))
    screen.blit(pos_text, (popup_x + popup_width//2 - pos_text.get_width()//2, popup_y + 280))

def animation_screen():
    global path_index, passed_positions, path
    screen.fill((240, 240, 240))
    draw_board()

    if is_playing and path_index < len(path):
        pos = path[path_index]
        if pos not in passed_positions:
            passed_positions.append(pos)
        draw_knight(pos)
        path_index += 1
    elif path_index > 0:
        draw_knight(path[path_index - 1])

    for btn in [pause_button, back_button, again_button, restart_button]:
        btn.draw(screen)

    info = small_font.render(f"Etape: {len(passed_positions)}/64 | Vitesse: {animation_speed} FPS", True, BLACK)
    screen.blit(info, (20, 640))

# === BOUCLE PRINCIPALE ===
# === BOUCLE PRINCIPALE ===# === BOUCLE PRINCIPALE ===
def run_animation(final_path):
    global path, is_running, is_playing, show_start_popup, start_pos, passed_positions, path_index
    path = final_path  # Ce chemin commence à (0,0)
    state = "waiting"
    show_start_popup = False
    start_pos = (0, 0)
    passed_positions = []
    path_index = 0
    is_playing = False

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                return None

            # === ÉTAT : ATTENTE ===
            if state == "waiting":
                result = start_button.handle_event(event)
                if result == "start":
                    show_start_popup = True
                    start_pos = (0, 0)
                    highlight_buttons()

            # === ÉTAT : POPUP ===
            if show_start_popup:
                for btn in x_buttons + y_buttons + [confirm_button, cancel_button]:
                    res = btn.handle_event(event)
                    if res == "confirm":
                        show_start_popup = False
                        state = "animating"
                        reset_animation()
                        is_playing = True
                        pause_button.text = "Pause"
                        
                        # AJOUT: Ajuster le chemin selon la position de départ choisie
                        if start_pos != (0, 0):
                            adjust_path_to_start_position(start_pos)
                        
                    elif res == "cancel":
                        show_start_popup = False
                        start_pos = (0, 0)
                        highlight_buttons()

            # === ÉTAT : ANIMATION ===
            elif state == "animating":
                for btn in [pause_button, back_button, again_button, restart_button]:
                    result = btn.handle_event(event)
                    if result == "restart":
                        return "restart"

        # Affichage
        if state == "waiting" or show_start_popup:
            waiting_screen()
        elif state == "animating":
            animation_screen()
            
            # Vérifier si l'animation est terminée
            if path_index >= len(path) and is_playing:
                is_playing = False
                pause_button.text = "Play"

        pygame.display.flip()
        clock.tick(animation_speed)

    pygame.quit()
    return start_pos

# AJOUT: Fonction pour ajuster le chemin selon la position de départ
def adjust_path_to_start_position(new_start):
    global path
    if not path or len(path) < 2:
        return
    
    # Calculer le décalage entre (0,0) et la nouvelle position
    dx = new_start[0] - path[0][0]
    dy = new_start[1] - path[0][1]
    
    # Appliquer le décalage à tout le chemin
    adjusted_path = []
    for pos in path:
        new_x = (pos[0] + dx) % 8
        new_y = (pos[1] + dy) % 8
        adjusted_path.append((new_x, new_y))
    
    path = adjusted_path