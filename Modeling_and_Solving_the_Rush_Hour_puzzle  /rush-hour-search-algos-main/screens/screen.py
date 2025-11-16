from abc import ABC, abstractmethod
import pygame
import random

class Screen(ABC):
    def __init__(self, app=None):
        self.app = app
        self.popups = []
        self.sand_surface = None

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def handle_input(self):
        pass

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


    
    def draw_background(self):
        DESERT_SAND = (210, 180, 140)
        self.app.screen.fill(DESERT_SAND)
        self.add_sand_grains()
        self.app.screen.blit(self.sand_surface, (0, 0))

        # Diagonal stripe pattern across the screen
        screen_width, screen_height = 720, 640
        spacing = 100  # spacing between lines
        item_spacing = 80  # spacing between items on each line

        diagonals = range(-screen_height, screen_width, spacing)  # diagonal start x-offsets

        for d, offset in enumerate(diagonals):
            x = offset
            y = 0
            i = 0
            while x < screen_width and y < screen_height:
                if i % 2 == 0:
                    self.draw_cactus(x, y)
                else:
                    self.draw_cone(x, y)
                x += item_spacing
                y += item_spacing
                i += 1

    
    def add_sand_grains(self):
        self.sand_surface = pygame.Surface((720, 640), pygame.SRCALPHA)

        num_grains = (720 * 640) // 100  # Adjust density here
        for _ in range(num_grains):
            x = random.randint(0, 719)
            y = random.randint(0, 639)

            DESERT_SAND = (210, 180, 140)

            # Pick a base color variation from DESERT_SAND (single color or list)
            base_color = DESERT_SAND if isinstance(DESERT_SAND, tuple) else random.choice(DESERT_SAND)
            variation = random.randint(-20, 20)
            grain_color = tuple(max(0, min(255, c + variation)) for c in base_color)

            size = random.randint(1, 2)
            pygame.draw.circle(self.sand_surface, grain_color, (x, y), size)
