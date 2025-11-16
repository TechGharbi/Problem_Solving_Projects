import pygame
import sys

# Initialisation
pygame.init()


# === CONFIGURATION ===
board_size = 8
square_size = 80
width = board_size * square_size
height = board_size * square_size + 100  # +100 pour les boutons
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Knight's Tour - Algorithme Génétique")
clock = pygame.time.Clock()

# === CHARGER L'IMAGE DE FOND ===
try:
    background_image = pygame.image.load("tournament.jpg")
    background_image = pygame.transform.scale(background_image, (width, height))
except pygame.error:
    print("Image 'tournament.jpg' non trouvée !")
    background_image = None

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BROWN = (161, 122, 67)
DARK_BROWN = (76, 42, 33)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
RED = (220, 20, 60)
HOVER_BROWN = (210, 165, 125)  # Marron clair au survol

# Police
font = pygame.font.SysFont('Arial', 28,bold=True)
small_font = pygame.font.SysFont('Arial', 20)

# Charger l'image du cavalier
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

# === ÉTAT DE L'ANIMATION ===
path = None
passed_positions = []
path_index = 0
is_playing = False
is_running = True

# === BOUTONS ===
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
        pygame.draw.rect(surface, (255, 215, 0), self.rect, 5, border_radius=20)  # Bord doré
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and event.button == 1:
                if self.action:
                    return self.action()
        return None

# === CONTRÔLE DE VITESSE ===
animation_speed = 2  # Vitesse par défaut (2 FPS)

def set_speed(fps):
    global animation_speed
    animation_speed = fps
# Boutons
# Bouton START
start_button = Button("START", 260, 660, 120, 60, LIGHT_BROWN, HOVER_BROWN, action=lambda: "start")

# Boutons d'animation
pause_button   = Button("Pause",   50, 660, 100, 60, LIGHT_BROWN, HOVER_BROWN, action=lambda: toggle_pause())
back_button    = Button("Back",   170, 660, 100, 60, LIGHT_BROWN, HOVER_BROWN, action=lambda: go_back())
again_button   = Button("Again",  290, 660, 100, 60, LIGHT_BROWN, HOVER_BROWN, action=lambda: reset_animation())
restart_button = Button("Restart",410, 660, 120, 60, LIGHT_BROWN, HOVER_BROWN, action=lambda: "restart")

# Boutons vitesse
slow_button    = Button("Slow",   540, 660,  80, 60, LIGHT_BROWN, HOVER_BROWN, action=lambda: set_speed(1))
fast_button    = Button("Fast",   630, 660,  80, 60, LIGHT_BROWN, HOVER_BROWN, action=lambda: set_speed(6))
# === FONCTIONS ===
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

# Bouton START - doré et plus grand
start_button = Button(
    "START", 
    width//2 - 100, 500, 200, 80, 
    (184, 134, 11), (255, 215, 0),  # Marron doré → Or au survol
    action=lambda: "start"
)

# === ÉCRAN D'ATTENTE ===
def waiting_screen():
    # Fond avec l'image du tournoi
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((245, 245, 245))

    # Titre (optionnel, si tu veux garder du texte)
    title = font.render("KNIGHT'S TOUR", True, (255, 215, 0))  # Or
    subtitle = small_font.render("Algorithme Génétique", True, WHITE)
    screen.blit(title, (width//2 - title.get_width()//2, 180))
    screen.blit(subtitle, (width//2 - subtitle.get_width()//2, 220))

    start_button.draw(screen)


# === ÉCRAN D'ANIMATION ===
def animation_screen():
    global path_index, is_playing

    # Fond
    screen.fill((240, 240, 240))
    draw_board()

    # Avancer si en lecture
    if is_playing and path_index < len(path):
        current_pos = path[path_index]
        if current_pos not in passed_positions:
            passed_positions.append(current_pos)
        draw_knight(current_pos)
        path_index += 1

    # Afficher le cavalier actuel
    if path_index > 0:
        draw_knight(path[path_index - 1])

    # Boutons
    pause_button.draw(screen)
    back_button.draw(screen)
    again_button.draw(screen)
    restart_button.draw(screen)

    # Info
    info = small_font.render(f"Étape: {len(passed_positions)}/64", True, BLACK)
    screen.blit(info, (20, 610))

# === MAIN LOOP ===
def run_animation(final_path):
    global path, passed_positions, path_index, is_playing, is_running
    path = final_path
    state = "waiting"  # "waiting" ou "animating"

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            # Gérer les boutons
            if state == "waiting":
                result = start_button.handle_event(event)
                if result == "start":
                    state = "animating"
                    reset_animation()
                    is_playing = True
                    pause_button.text = "Pause"
            else:
                for btn in [pause_button, back_button, again_button, restart_button]:
                    result = btn.handle_event(event)
                    if result == "restart":
                        return "restart"

        # Affichage
        if state == "waiting":
            waiting_screen()
        else:
            animation_screen()

        pygame.display.flip()
        clock.tick(2)

    pygame.quit()
    return None