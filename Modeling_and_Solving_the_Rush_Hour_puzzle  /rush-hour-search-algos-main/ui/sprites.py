import pygame

class CarSprite:
    def __init__(self, image_path, size, direction, cell_size):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.direction = direction.upper()  # Ensure it's 'H' or 'V'
        self.size = size
        self.cell_size = cell_size

        # Scale image according to size and direction
        if self.direction == 'H':
            self.image = pygame.transform.scale(self.original_image, (self.cell_size * size, self.cell_size))
        elif self.direction == 'V':
            # Scale then rotate
            scaled = pygame.transform.scale(self.original_image, (self.cell_size * size, self.cell_size))
            self.image = pygame.transform.rotate(scaled, 90)

    def draw_car(self, screen, x, y):
        screen.blit(self.image, (x, y))
