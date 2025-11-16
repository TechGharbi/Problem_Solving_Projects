import random
import time
import threading
import pygame
from screens.screen import Screen
from ui.button import Button
from solution import BFS, IDS, UCS, AStar
from popups.victory_popup import VictoryPopup
from popups.nosolution_popup import NoSolutionPopup
from ui.sprites import CarSprite

CELL_SIZE = 80
GRID_SIZE = 6
MARGIN = 60

# Colors
DESERT_SAND = (210, 180, 140)
GRID_BORDER = (70, 130, 180)
GRID_BACKGROUND = (176, 196, 222)
EXIT_ARROW = (255, 255, 255) 

class SolverScreen(Screen): 
    def __init__(self, app, initial_node, level_number="", car_colors=None):
        super().__init__(app)
        self.node = initial_node
        self.level_number = level_number
        self.step = 0
        self.solution_path = []
        self.solver = None
        self.state = 'idle'  # states: idle, loading, solving, paused, finished
        self.loading_start_time = None
        self.spinner_image = pygame.image.load("assets/spinner.png")  # Add your spinner image
        self.spinner_angle = 0
        self.solution_thread = None
        self.stats = None
        self.timer = 0
        self.step_delay = 0.7  # seconds between steps
        self.victory_popup_shown = False
        self.animation_done = False
        self.animate_goal = False
        self.goal_anim_step = 0
        self.goal_anim_timer = 0
        self.goal_anim_delay = 0.3  # s if car_colors is not None else {}econds between frames
        self.car_colors = car_colors if car_colors is not None else {}
        self.car_sprites = {
            ("G", "H", 2): CarSprite("assets/cars/car_0.png", 2, "H", CELL_SIZE),
            ("A","V",2): CarSprite("assets/cars/car_1.png", 2, "V", CELL_SIZE),
            ("A","H",2): CarSprite("assets/cars/car_1.png", 2, "H", CELL_SIZE),
            ("B","H",2): CarSprite("assets/cars/car_2.png", 2, "H", CELL_SIZE),
            ("B","V",2): CarSprite("assets/cars/car_2.png", 2, "V", CELL_SIZE),
            ("C","H",2): CarSprite("assets/cars/car_3.png", 2, "H", CELL_SIZE),
            ("C","V",2): CarSprite("assets/cars/car_3.png", 2, "V", CELL_SIZE),
            ("D","H",2): CarSprite("assets/cars/car_4.png", 2, "H", CELL_SIZE),
            ("D","V",2): CarSprite("assets/cars/car_4.png", 2, "V", CELL_SIZE),
            ("E","H",2): CarSprite("assets/cars/car_5.png", 2, "H", CELL_SIZE),
            ("E","V",2): CarSprite("assets/cars/car_5.png", 2, "V", CELL_SIZE),
            ("F","H",2): CarSprite("assets/cars/car_6.png", 2, "H", CELL_SIZE),
            ("F","V",2): CarSprite("assets/cars/car_6.png", 2, "V", CELL_SIZE),
            ("H","H",2): CarSprite("assets/cars/car_7.png", 2, "H", CELL_SIZE),
            ("H","V",2): CarSprite("assets/cars/car_7.png", 2, "V", CELL_SIZE),
            ("I","H",2): CarSprite("assets/cars/car_8.png", 2, "H", CELL_SIZE),
            ("J","V",2): CarSprite("assets/cars/car_9.png", 2, "V", CELL_SIZE),
            ("K","V",2): CarSprite("assets/cars/car_10.png", 2, "V", CELL_SIZE),
            ("O","V",2): CarSprite("assets/cars/car_17.png", 2, "V", CELL_SIZE),
            ("N","H",2): CarSprite("assets/cars/car_11.png", 2, "H", CELL_SIZE),
            ("N","V",2): CarSprite("assets/cars/car_11.png", 2, "V", CELL_SIZE),
            ("Q","H",2): CarSprite("assets/cars/car_12.png", 2, "H", CELL_SIZE),
            ("T","V",2): CarSprite("assets/cars/car_13.png", 2, "V", CELL_SIZE),
            ("U","V",2): CarSprite("assets/cars/car_14.png", 2, "V", CELL_SIZE),
            ("U","H",2): CarSprite("assets/cars/car_14.png", 2, "H", CELL_SIZE),
            ("Y","V",2): CarSprite("assets/cars/car_15.png", 2, "V", CELL_SIZE),
            ("Z","V",2): CarSprite("assets/cars/car_16.png", 2, "V", CELL_SIZE),
            ("A","V",3): CarSprite("assets/cars/truck_1.png", 3, "V", CELL_SIZE),
            ("B","V",3): CarSprite("assets/cars/truck_2.png", 3, "V", CELL_SIZE),
            ("B","H",3): CarSprite("assets/cars/truck_2.png", 3, "H", CELL_SIZE),
            ("C","H",3): CarSprite("assets/cars/truck_3.png", 3, "H", CELL_SIZE),
            ("C","V",3): CarSprite("assets/cars/truck_3.png", 3, "V", CELL_SIZE),
            ("D","V",3): CarSprite("assets/cars/truck_14.png", 3, "V", CELL_SIZE),
            ("E","H",3): CarSprite("assets/cars/truck_4.png", 3, "H", CELL_SIZE),
            ("F","H",3): CarSprite("assets/cars/truck_5.png", 3, "H", CELL_SIZE),
            ("F","V",3): CarSprite("assets/cars/truck_5.png", 3, "V", CELL_SIZE),
            ("H","V",3): CarSprite("assets/cars/truck_6.png", 3, "V", CELL_SIZE),
            ("I","H",3): CarSprite("assets/cars/truck_7.png", 3, "H", CELL_SIZE),
            ("O","H",3): CarSprite("assets/cars/truck_8.png", 3, "H", CELL_SIZE),
            ("O","V",3): CarSprite("assets/cars/truck_8.png", 3, "V", CELL_SIZE),
            ("N","V",3): CarSprite("assets/cars/truck_15.png", 3, "V", CELL_SIZE),
            ("R","H",3): CarSprite("assets/cars/truck_9.png", 3, "H", CELL_SIZE),
            ("T","H",3): CarSprite("assets/cars/truck_10.png", 3, "H", CELL_SIZE),
            ("U","H",3): CarSprite("assets/cars/truck_11.png", 3, "H", CELL_SIZE),
            ("V","H",3): CarSprite("assets/cars/truck_12.png", 3, "H", CELL_SIZE),
            ("Y","V",3): CarSprite("assets/cars/truck_13.png", 3, "V", CELL_SIZE),
        }

        self.btn_bfs = Button(40, 580, 100, 40, "BFS", lambda: self.solve(BFS), self.app)
        self.btn_ids = Button(170, 580, 100, 40, "IDS", lambda: self.solve(IDS), self.app)
        self.btn_ucs = Button(300, 580, 100, 40, "UCS", lambda: self.solve(UCS), self.app)
        self.btn_astar = Button(430, 580, 100, 40, "A*", lambda: self.solve(AStar), self.app)
        self.button_back = Button(580, 30, 100, 40, "Back", self.on_back, self.app)
        self.button_pause = Button(580, 80, 100, 40, "Pause", self.on_pause, self.app)
        self.button_reset = Button(580, 130, 100, 40, "Reset", self.on_reset, self.app)
        self.title = pygame.font.SysFont("Papyrus", 30, bold=True)
        self.font = pygame.font.SysFont("impact", 24)
        self.sand_surface = pygame.Surface((720, 640), pygame.SRCALPHA)
        self.add_sand_grains()
        if self.car_colors:
            self.load_custom_car_colors_and_sprites()


    def render(self):
        self.draw_background()
        self.draw_blue_striped_border()

        title_text = self.title.render(f"{self.level_number}", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.app.screen.get_width() // 2, 20))
        self.app.screen.blit(title_text, title_rect)

        if self.state == 'loading':
            if self.solution_thread.is_alive():
                self.draw_board(self.node)
                self.spinner_angle = (self.spinner_angle + 5) % 360
                rotated = pygame.transform.rotate(self.spinner_image, self.spinner_angle)
                rect = rotated.get_rect(center=(self.app.screen.get_width() // 2, 300))
                self.app.screen.blit(rotated, rect)

                loading_text = self.font.render("Solving...", True, (0, 0, 0))
                text_rect = loading_text.get_rect(center=(self.app.screen.get_width() // 2, 360))
                self.app.screen.blit(loading_text, text_rect)
                return
            else:
                # Transitioned out of loading, state is now solving or finished
                self.state = 'finished'
                self.stats = {"Message": "No solution found"}
                print("No solution.")
                # Hiển thị popup khi không có lời giải
                popup = NoSolutionPopup(self.app, self)
                self.popups.append(popup)


        # Animate step-by-step solving
        if self.state == 'solving' and self.solution_path:
            if time.time() - self.timer > self.step_delay:
                self.timer = time.time()
                if self.step < len(self.solution_path) - 1:
                    self.step += 1
                elif self.step == len(self.solution_path) - 1:
                    self.state = 'goal_animating'
                    self.goal_animation_start = time.time()
                    self.goal_animation_duration = 1  # 1 second
                    self.step = len(self.solution_path) - 1

        if self.state == 'goal_animating':
            current_node = self.solution_path[-1]
            self.draw_board_with_goal_animation(current_node)

            if time.time() - self.goal_animation_start >= self.goal_animation_duration:
                 self.state = 'finished'
                 self.animation_done = True

        else:
            current_node = self.solution_path[self.step] if self.solution_path else self.node
            self.draw_board(current_node)
       

        # Step count and Total cost
        self.draw_step_info(current_node)


        # Draw control buttons
        for btn in [self.btn_bfs, self.btn_ids, self.btn_ucs, self.btn_astar, self.button_back, self.button_pause, self.button_reset]:
            btn.draw(self.app.screen)

        # Draw final stats 
        if self.state == 'finished' and self.stats:
            # self.draw_stats()
            if self.state == 'finished' and self.stats:

                # Chỉ hiện popup nếu animation_done là True
                if self.animation_done and not self.victory_popup_shown:
                    popup = VictoryPopup(self.app, self)
                    self.popups.append(popup)
                    self.victory_popup_shown = True

        # Luôn vẽ các popup
        for popup in self.popups:
            if popup.visible:
                popup.draw()
    

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.pos)
                # Nếu có popup đang mở thì chỉ xử lý popup, không xử lý nút
                if any(popup.visible for popup in self.popups):
                    for popup in self.popups:
                        if popup.visible:
                            popup.handle_event(event)
                    return  # Ngăn không cho xử lý nút bên dưới

                # Nếu không có popup nào đang mở, xử lý nút như bình thường
                for btn in [self.btn_bfs, self.btn_ids, self.btn_ucs, self.btn_astar, self.button_back, self.button_pause, self.button_reset]:
                    if btn.is_clicked(event.pos):
                        btn.on_click()
            for popup in self.popups:
                if popup.visible:
                    popup.handle_event(event)

    def load_custom_car_colors_and_sprites(self):
        """
        This function updates car colors and their associated sprites
        for a custom map passed from the map editor.
        """
        self.car_sprites = {}
        color_to_sprite = {
            (100, 150, 250): ("car_8.png", "truck_7.png"),   # blue
            (0, 200, 100):   ("car_7.png", "truck_6.png"),   # green
            (255, 200, 0):   ("car_5.png", "truck_8.png"),   # yellow
            (138, 43, 226):  ("car_4.png", "truck_1.png"),   # purple
            (255, 105, 180): ("car_12.png", "truck_12.png"), # pink
            (255, 100, 100): ("car_0.png", "car_0.png")      # red goal car
        }

        for car in self.node.cars:
            color = self.car_colors.get(car.id, (100, 150, 250))
            sprite_names = color_to_sprite.get(color, ("car_9.png", "truck_9.png"))
            sprite_file = sprite_names[0] if car.size == 2 else sprite_names[1]
            sprite_path = f"assets/cars/{sprite_file}"
            self.car_sprites[(car.id, car.dir.upper(), car.size)] = CarSprite(sprite_path, car.size, car.dir.upper(), CELL_SIZE)


    def draw_board(self, node):
        # Draw empty grid
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                rect = pygame.Rect(
                    MARGIN + j * CELL_SIZE,
                    MARGIN + i * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(self.app.screen, (220, 220, 220), rect, 1)

        for car in node.cars:
            x_px = MARGIN + (car.col - 2) * CELL_SIZE
            y_px = MARGIN + (car.row - 2) * CELL_SIZE
            key = (car.id, car.dir.upper(), car.size)
            sprite = self.car_sprites.get(key)

            if sprite:
                sprite.draw_car(self.app.screen, x_px, y_px)
            else:
                # fallback rectangle if sprite missing
                width = CELL_SIZE * (car.size if car.dir == 'h' else 1)
                height = CELL_SIZE * (car.size if car.dir == 'v' else 1)
                fallback_color = (255, 0, 0) if car.id == 'G' else (100, 100, 200)
                # pygame.draw.rect(self.app.screen, fallback_color, (x_px, y_px, width, height), border_radius=10)


    def draw_board_with_goal_animation(self, node):
        board = node.state
        red_car_offset = int((time.time() - self.goal_animation_start) * CELL_SIZE)  # animate rightward

        # Draw empty grid
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                rect = pygame.Rect(
                    MARGIN + j * CELL_SIZE,
                    MARGIN + i * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(self.app.screen, (220, 220, 220), rect, 1)

        for car in node.cars:
            x_px = MARGIN + (car.col - 2) * CELL_SIZE
            y_px = MARGIN + (car.row - 2) * CELL_SIZE

            key = (car.id, car.dir.upper(), car.size)

            # Animate red car ('G') moving right
            if car.id == 'G':
                x_px += red_car_offset

            if key in self.car_sprites:
                self.car_sprites[key].draw_car(self.app.screen, x_px, y_px)
            else:
                # fallback rectangle if no sprite
                width = CELL_SIZE * (car.size if car.dir.lower() == 'h' else 1)
                height = CELL_SIZE * (car.size if car.dir.lower() == 'v' else 1)
                color = (255, 100, 100) if car.id == 'G' else (100, 150, 250)
                # pygame.draw.rect(self.app.screen, color, (x_px, y_px, width, height), border_radius=8)




    def draw_background(self):
        # Desert background with decorative elements
        self.app.screen.fill(DESERT_SAND)
        self.app.screen.blit(self.sand_surface, (0, 0))
        # Road to the right
        pygame.draw.rect(self.app.screen, (230, 230, 230), (MARGIN + GRID_SIZE * CELL_SIZE, MARGIN + 2 * CELL_SIZE, 100, CELL_SIZE))

        # Cactus Positions (corners and side gaps)
        cactus_positions = [
            (611, 374),
            (672, 550),
            (2, 49),
            (2, 285), 
            (481, 587),
            (3, 472)
        ]

        for x, y in cactus_positions:
            self.draw_cactus(x, y)

        # Traffic Cones near entrance/exit and bottom
        cone_positions = [
            (135, 20),
            (15, 164),
            (422, 594),
            (688, 486),
            (642, 324),
            (695, 213),
            (78, 603)
        ]

        for x, y in cone_positions:
            self.draw_cone(x, y)

        # self.add_sand_grains()
        exit_x = MARGIN + GRID_SIZE * CELL_SIZE + 90
        exit_y = MARGIN + 2 * CELL_SIZE + 10
        self.draw_road_sign(exit_x, exit_y)


    def add_sand_grains(self):
        # Create a surface once if it doesn't exist
        if not hasattr(self, 'sand_surface'):
            self.sand_surface = pygame.Surface((720, 640), pygame.SRCALPHA)

        num_grains = (720 * 640) // 100  # Adjust density here
        for _ in range(num_grains):
            x = random.randint(0, 719)
            y = random.randint(0, 639)

            # Pick a base color variation from DESERT_SAND (single color or list)
            base_color = DESERT_SAND if isinstance(DESERT_SAND, tuple) else random.choice(DESERT_SAND)
            variation = random.randint(-20, 20)
            grain_color = tuple(max(0, min(255, c + variation)) for c in base_color)

            size = random.randint(1, 2)
            pygame.draw.circle(self.sand_surface, grain_color, (x, y), size)

    

    def draw_blue_striped_border(self):
        stripe_size = CELL_SIZE // 4
        grid_left = MARGIN
        grid_top = MARGIN
        grid_right = grid_left + GRID_SIZE * CELL_SIZE
        grid_bottom = grid_top + GRID_SIZE * CELL_SIZE
        exit_row = 2  # red car is always on row 2
        exit_y = grid_top + exit_row * CELL_SIZE
        stripe_colors = [(80, 180, 255), (255, 255, 255)]

        # ─ Top border
        for i in range(-stripe_size, GRID_SIZE * CELL_SIZE + stripe_size, stripe_size):
            color = stripe_colors[(i // stripe_size) % 2]
            pygame.draw.rect(self.app.screen, color, (grid_left + i, grid_top - stripe_size, stripe_size, stripe_size))

        # ─ Bottom border
        for i in range(-stripe_size, GRID_SIZE * CELL_SIZE + stripe_size, stripe_size):
            color = stripe_colors[(i // stripe_size) % 2]
            pygame.draw.rect(self.app.screen, color, (grid_left + i, grid_bottom, stripe_size, stripe_size))

        # │ Left border
        for i in range(-stripe_size, GRID_SIZE * CELL_SIZE + stripe_size, stripe_size):
            color = stripe_colors[(i // stripe_size) % 2]
            pygame.draw.rect(self.app.screen, color, (grid_left - stripe_size, grid_top + i, stripe_size, stripe_size))

        # │ Right border — skip exit row
        for row in range(GRID_SIZE):
            if row == exit_row:
                continue
            y_start = grid_top + row * CELL_SIZE
            for i in range(0, CELL_SIZE, stripe_size):
                color = stripe_colors[(i // stripe_size) % 2]
                pygame.draw.rect(self.app.screen, color, (grid_right, y_start + i, stripe_size, stripe_size))

        # ➤ Exit tunnel side walls (top and bottom only — aligned to grid)
        tunnel_length = CELL_SIZE
        for i in range(0, tunnel_length, stripe_size):
            color = stripe_colors[(i // stripe_size) % 2]
            # Top edge of exit tunnel
            pygame.draw.rect(self.app.screen, color, (grid_right + i, exit_y - 20, stripe_size, stripe_size))
            # Bottom edge of exit tunnel
            pygame.draw.rect(self.app.screen, color, (grid_right + i, exit_y + CELL_SIZE - stripe_size + 20, stripe_size, stripe_size))


    def draw_step_info(self, current_node):
        step_text = f"Step: {self.step}/{len(self.solution_path)-1 if self.solution_path else 0}"
        cost_text = f"Total Cost: {current_node.cost}"

        # Desert color palette
        desert_colors = {
            'text': (101, 67, 33),        # Dark brown (burnt sienna)
            'text_shadow': (160, 120, 80), # Light brown shadow
            'bg_main': (218, 165, 32),     # Goldenrod
            'bg_secondary': (184, 134, 11), # Darker gold
            'border': (139, 69, 19),       # Saddle brown
            'accent': (205, 133, 63),      # Peru/terracotta
        }
        
        # Render text with shadow effect for "carved" look
        step_surface = self.font.render(step_text, True, desert_colors['text'])
        cost_surface = self.font.render(cost_text, True, desert_colors['text'])
        
        # Create shadow surfaces
        step_shadow = self.font.render(step_text, True, desert_colors['text_shadow'])
        cost_shadow = self.font.render(cost_text, True, desert_colors['text_shadow'])

        # Calculate background dimensions
        max_width = max(step_surface.get_width(), cost_surface.get_width())
        total_height = step_surface.get_height() + cost_surface.get_height() + 12
        
        # Add padding
        padding = 10
        rect_width = max_width + (padding)
        rect_height = total_height + (padding * 2)
        
        # Position
        x_pos = 570
        y_pos = 370
        
        # Create textured background using gradients and patterns
        background_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        
        # Main gradient background (sandstone effect)
        for i in range(rect_height):
            # Create gradient from light to dark
            ratio = i / rect_height
            r = int(desert_colors['bg_main'][0] - (desert_colors['bg_main'][0] - desert_colors['bg_secondary'][0]) * ratio)
            g = int(desert_colors['bg_main'][1] - (desert_colors['bg_main'][1] - desert_colors['bg_secondary'][1]) * ratio)
            b = int(desert_colors['bg_main'][2] - (desert_colors['bg_main'][2] - desert_colors['bg_secondary'][2]) * ratio)
            
            pygame.draw.line(background_surface, (r, g, b), (0, i), (rect_width, i))
        
        # Add sand texture noise
        for _ in range(rect_width * rect_height // 50):
            noise_x = pygame.math.Vector2(
                random.randint(0, rect_width - 1),
                random.randint(0, rect_height - 1)
            )
            noise_color = (
                desert_colors['bg_main'][0] + random.randint(-20, 20),
                desert_colors['bg_main'][1] + random.randint(-20, 20),
                desert_colors['bg_main'][2] + random.randint(-20, 20)
            )
            # Clamp color values
            noise_color = tuple(max(0, min(255, c)) for c in noise_color)
            pygame.draw.circle(background_surface, noise_color, (int(noise_x.x), int(noise_x.y)), 1)
        
        # Add weathered edge effect
        edge_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        
        # Top highlight (sun-bleached effect)
        for i in range(5):
            alpha = 30 - i * 5
            highlight_color = (*desert_colors['accent'], alpha)
            pygame.draw.rect(edge_surface, highlight_color, (i, i, rect_width - 2*i, 3))
        
        # Bottom shadow (depth effect)
        for i in range(5):
            alpha = 40 - i * 7
            shadow_color = (*desert_colors['border'], alpha)
            pygame.draw.rect(edge_surface, shadow_color, (i, rect_height - 3 - i, rect_width - 2*i, 3))
        
        # Combine background elements
        background_surface.blit(edge_surface, (0, 0))
        
        # Draw main background
        self.app.screen.blit(background_surface, (x_pos, y_pos))
        
        # Draw decorative border (carved stone effect)
        border_thickness = 3
        
        # Outer border (dark)
        pygame.draw.rect(self.app.screen, desert_colors['border'], 
                        (x_pos - border_thickness, y_pos - border_thickness, 
                        rect_width + 2*border_thickness, rect_height + 2*border_thickness), 
                        border_thickness)
        
        # Inner accent border (lighter)
        pygame.draw.rect(self.app.screen, desert_colors['accent'], 
                        (x_pos - 1, y_pos - 1, rect_width + 2, rect_height + 2), 1)
        
        # Add corner decorations (desert gem/stone accents)
        corner_size = 8
        corner_color = desert_colors['accent']
        
        # Top-left corner
        pygame.draw.polygon(self.app.screen, corner_color, [
            (x_pos - border_thickness, y_pos - border_thickness),
            (x_pos - border_thickness + corner_size, y_pos - border_thickness),
            (x_pos - border_thickness, y_pos - border_thickness + corner_size)
        ])
        
        # Top-right corner
        pygame.draw.polygon(self.app.screen, corner_color, [
            (x_pos + rect_width + border_thickness, y_pos - border_thickness),
            (x_pos + rect_width + border_thickness - corner_size, y_pos - border_thickness),
            (x_pos + rect_width + border_thickness, y_pos - border_thickness + corner_size)
        ])
        
        # Bottom-left corner
        pygame.draw.polygon(self.app.screen, corner_color, [
            (x_pos - border_thickness, y_pos + rect_height + border_thickness),
            (x_pos - border_thickness + corner_size, y_pos + rect_height + border_thickness),
            (x_pos - border_thickness, y_pos + rect_height + border_thickness - corner_size)
        ])
        
        # Bottom-right corner
        pygame.draw.polygon(self.app.screen, corner_color, [
            (x_pos + rect_width + border_thickness, y_pos + rect_height + border_thickness),
            (x_pos + rect_width + border_thickness - corner_size, y_pos + rect_height + border_thickness),
            (x_pos + rect_width + border_thickness, y_pos + rect_height + border_thickness - corner_size)
        ])
        
        # Draw text shadows first (offset for carved effect)
        shadow_offset = 2
        self.app.screen.blit(step_shadow, (x_pos + padding + shadow_offset, y_pos + padding + shadow_offset))
        self.app.screen.blit(cost_shadow, (x_pos + padding + shadow_offset, y_pos + padding + step_surface.get_height() + 12 + shadow_offset))
        
        # Draw main text on top
        self.app.screen.blit(step_surface, (x_pos + padding, y_pos + padding))
        self.app.screen.blit(cost_surface, (x_pos + padding, y_pos + padding + step_surface.get_height() + 12))


    def draw_cactus(self, x, y):
        # Main stem
        pygame.draw.rect(self.app.screen, (34, 139, 34), (x + 8, y, 14, 50), border_radius=4)

        # Left arm
        pygame.draw.rect(self.app.screen, (34, 139, 34), (x - 2, y + 15, 10, 20), border_radius=4)
        pygame.draw.rect(self.app.screen, (34, 139, 34), (x + 2, y + 25, 10, 10), border_radius=4)

        # Right arm
        pygame.draw.rect(self.app.screen, (34, 139, 34), (x + 20, y + 20, 10, 20), border_radius=4)
        pygame.draw.rect(self.app.screen, (34, 139, 34), (x + 18, y + 30, 10, 10), border_radius=4)

        # Cactus base shadow
        pygame.draw.ellipse(self.app.screen, (0, 100, 0), (x + 4, y + 48, 20, 6))


    def draw_cone(self, x, y):
        # Cone base
        pygame.draw.rect(self.app.screen, (255, 140, 0), (x, y + 20, 14, 6))  # base
        pygame.draw.polygon(self.app.screen, (255, 140, 0), [(x + 7, y), (x, y + 20), (x + 14, y + 20)])  # cone
        pygame.draw.rect(self.app.screen, (255, 255, 255), (x + 3, y + 10, 8, 4))  # stripe

    def draw_road_sign(self, x, y):
        # Sign post (vertical rectangle)
        post_color = (194, 115, 68)
        pygame.draw.rect(self.app.screen, post_color, (x + 18, y, 10, 90), border_radius=3)

        # Top sign panel (right-pointing)
        sign_color = (255, 230, 120)
        pygame.draw.rect(self.app.screen, sign_color, (x, y + 5, 60, 20), border_radius=6)
        pygame.draw.polygon(self.app.screen, sign_color, [(x + 60, y + 5), (x + 70, y + 15), (x + 60, y + 25)])

        # Bottom sign panel (left-pointing)
        pygame.draw.rect(self.app.screen, sign_color, (x + 10, y + 35, 60, 20), border_radius=6)
        pygame.draw.polygon(self.app.screen, sign_color, [(x + 10, y + 35), (x, y + 45), (x + 10, y + 55)])


    def solve(self, solver_class):
        self.victory_popup_shown = False
        self.spinner_angle = 0
        self.state = 'loading'

        def thread_solve():
            solver = solver_class(self.node)

            start = time.time()
            goal_node = solver.solve()
            end = time.time()

            if goal_node:
                self.solution_path = list(solver.find_path(goal_node))
                self.step = 0
                self.timer = time.time()
                self.state = 'solving'


                # Collect stats from the solver instance
                self.stats = {
                    "Steps": solver.step_count,
                    "Time": round(end - start, 3),
                    "Nodes": solver.number_expanded_nodes,
                    "Memory": solver.memory_usage,
                    "Cost": solver.total_cost
                }
                print("Found solution!")

            else:
                self.state = 'finished'
                self.stats = {"Message": "No solution found"}
                print("No solution.")
                
                # Hiển thị popup khi không có lời giải
                popup = NoSolutionPopup(self.app, self)
                self.popups.append(popup)
        
        self.solution_thread = threading.Thread(target=thread_solve)
        self.solution_thread.start()
        

    
    def on_back(self):
        from screens.menu_screen import MenuScreen
        self.app.switch_screen(MenuScreen(self.app))

    def on_pause(self):
        if self.state == 'solving':
            self.state = 'paused'
            self.button_pause.label = "Resume"
        elif self.state == 'paused':
            self.state = 'solving'
            self.timer = time.time()
            self.button_pause.label = "Pause"

    def on_reset(self):
        self.step = 0
        self.state = 'idle'
        self.solution_path = []
        self.stats = None
        self.button_pause.label = "Pause"
        self.popups.clear()
        self.victory_popup_shown = False
        self.animation_done = False  # reset lại trạng thái animation


    def draw_stats(self):
        font = pygame.font.SysFont("Arial", 18)
        y = 370

        for key, val in self.stats.items():
            text = font.render(f"{key}: {val}", True, (0, 0, 0))
            self.app.screen.blit(text, (600, y))
            y += 25
        