import os
#from main import utils
#from utils import read_map, store_car
from model.node import Node
#import numpy as np
from model.car import Car
import pygame
from ui.button import Button
from screens.map_editor_screen import MapEditorScreen
from popups.select_level_popup import SelectLevelPopup
from screens.solver_screen import SolverScreen
from popups.select_level_popup import SelectLevelPopup

class SelectMapPopup:
    def __init__(self, app, parent_screen):
        self.app = app
        self.parent = parent_screen
        self.message = "Select a map"
        self.font = pygame.font.SysFont("impact", 22)

        self.btn_custom = Button(250, 300, 200, 50, "Custom", self.on_custom, self.app)
        self.btn_default = Button(250, 370, 200, 50, "Default", self.on_default, self.app)

    def draw(self, screen):
        pygame.draw.rect(screen, (220, 240, 250), (200, 250, 320, 200), border_radius=10)
        # Title
        text = self.font.render(self.message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(360, 260))
        screen.blit(text, text_rect)
        
        self.btn_custom.draw(screen)
        self.btn_default.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_custom.is_clicked(event.pos):
                self.on_custom()
            elif self.btn_default.is_clicked(event.pos):
                self.on_default()

    def on_custom(self):
        self.app.switch_screen(MapEditorScreen(self.app))


    def on_default(self):
        if self in self.parent.popups:
            self.parent.popups.remove(self)
            
        self.parent.popups.append(SelectLevelPopup(self.app, self.parent))

        
        # map_path = "Map/11.txt"
        # map = read_map(map_path)
        # level_number = os.path.basename(map_path).split('.')[0]  # '11'
        # level_name = f"Level {level_number}"
        # # all_cars: list of obstacle vehicles (include: id, direction, x, y, length)
        # all_cars = store_car(map)
        
        # A = Node(cars=all_cars)
        # initial_node = A  # build from selected map
        # self.app.switch_screen(SolverScreen(self.app, initial_node, level_name))
        