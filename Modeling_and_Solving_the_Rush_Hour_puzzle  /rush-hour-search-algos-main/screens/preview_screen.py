import random
import pygame
from screens.screen import Screen
from ui.button import Button
from screens.solver_screen import SolverScreen
from screens.menu_screen import MenuScreen
from ui.sprites import CarSprite

CELL_SIZE = 80
DESERT_SAND = (210, 180, 140)

class PreviewLevelScreen(Screen):
    def __init__(self, app, node, parent_screen, level_name="Preview"):
        super().__init__(app)
        self.node = node
        self.level_name = level_name
        self.parent = parent_screen
        self.font = pygame.font.SysFont("Papyrus", 26, bold=True)
        self.sub_font = pygame.font.SysFont("Arial", 18)
        self.button_start = Button(220, 570, 100, 40, "Start", self.on_start, self.app)
        self.button_back = Button(420, 570, 100, 40, "Back", self.on_back, self.app)
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

        self.add_sand_grains()


    def render(self):
        self.app.screen.fill(DESERT_SAND)
        self.add_sand_grains()
        self.app.screen.blit(self.sand_surface, (0, 0))
        # Draw title
        title_text = self.font.render(f"Preview: {self.level_name}", True, (0, 0, 0))
        self.app.screen.blit(title_text, (self.app.screen.get_width() // 2 - title_text.get_width() // 2, 20))

        # Draw preview board (reuse from SolverScreen)
        from screens.solver_screen import SolverScreen
        SolverScreen.draw_board(self, self.node)

        # Buttons
        self.button_start.draw(self.app.screen)
        self.button_back.draw(self.app.screen)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_start.is_clicked(event.pos):
                    self.on_start()
                elif self.button_back.is_clicked(event.pos):
                    self.on_back()

    def on_start(self):
        self.app.switch_screen(SolverScreen(self.app, self.node, self.level_name))

    def on_back(self):
        self.app.switch_screen(MenuScreen(self.app))
        
    

    
