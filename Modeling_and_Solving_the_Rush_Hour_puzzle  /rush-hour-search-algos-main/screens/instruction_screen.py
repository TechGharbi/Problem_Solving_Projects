import random
import pygame
from screens.screen import Screen
from screens.solver_screen import SolverScreen 
from ui.button import Button


class InstructionScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.message = "Welcome to Rush Hour!\nGoal: Move the RED car to the exit.\nCars can move along their horizontal or vertical axes.\nChoose 1 of 4 algorithms for the machine to solve:\n- BFS: Breadth-First Search\n- IDS: Iterative Deepening Search\n- UCS: Uniform Cost Search\n- A*: A* search with heuristic\nDesign your own map with Custom mode!\nClick to place the car. Select length, direction, location.\nUse the Pause / Reset / Back buttons while playing."
        self.button_back = Button(280, 560, 160, 40, "Back", self.on_back, self.app)
        self.font = pygame.font.SysFont("Segoe UI", 20)
        
    def render(self):
        self.draw_background()
        screen_width = self.app.screen.get_width()
        
        # Draw title
        title_font = pygame.font.SysFont("Papyrus", 40, bold=True)
        title_text = title_font.render("Instructions", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, 40))
        self.app.screen.blit(title_text, title_rect)

        # White box background
        box_width, box_height = 500, 400
        box_x = (screen_width - box_width) // 2
        box_y = 90
        pygame.draw.rect(self.app.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), border_radius=16)
        
       
        # Draw multiline message with manual line breaks
        lines = self.message.split('\n')
        for i, line in enumerate(lines):
            rendered_line = self.font.render(line, True, (0, 0, 0))
            self.app.screen.blit(rendered_line, (box_x + 20, box_y + 20 + i * 30))


        self.button_back.draw(self.app.screen)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_back.is_clicked(event.pos):
                    self.on_back()

    def on_back(self):
        from screens.menu_screen import MenuScreen
        self.app.switch_screen(MenuScreen(self.app))

    

    
