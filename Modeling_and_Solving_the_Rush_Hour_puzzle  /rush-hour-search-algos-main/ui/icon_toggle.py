import pygame

class IconToggleButton:
    def __init__(self, x, y, icon_on_path, icon_off_path, initial_state=True, on_toggle=None, size=36):
        self.icon_on = pygame.image.load(icon_on_path).convert_alpha()
        self.icon_off = pygame.image.load(icon_off_path).convert_alpha()

        self.icon_on = pygame.transform.scale(self.icon_on, (size, size))
        self.icon_off = pygame.transform.scale(self.icon_off, (size, size))

        self.rect = self.icon_on.get_rect(topleft=(x, y))
        self.state = initial_state
        self.on_toggle = on_toggle  # function to call on toggle

    def draw(self, screen):
        icon = self.icon_on if self.state else self.icon_off
        screen.blit(icon, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.state = not self.state
            if self.on_toggle:
                self.on_toggle(self.state)
