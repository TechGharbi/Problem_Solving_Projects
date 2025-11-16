import pygame

class IconButton:
    def __init__(self, x, y, icon_path, on_click, size=36, app=None):
        self.image = pygame.image.load(icon_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.on_click = on_click
        self.app = app

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_clicked(event.pos):
            self.on_click()
