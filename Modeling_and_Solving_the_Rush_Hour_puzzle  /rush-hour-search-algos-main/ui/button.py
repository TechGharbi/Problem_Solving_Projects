import pygame
from ui.sound import SoundManager

class Button:
    def __init__(self, x, y, width, height, label, on_click, app=None,
                 bg_color=(150, 130, 110), text_color=(255, 255, 255), hover_color=(170, 150, 130)):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.on_click = on_click
        self.font = pygame.font.SysFont("Papyrus", 24, bold=True)  # Use a carved-stone feel font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.app = app
        self.hovered = False

    def draw(self, screen):
        # Determine if hovered
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        # Apply hover color
        color = self.hover_color if self.hovered else self.bg_color

        # Shadowed border effect
        pygame.draw.rect(screen, (50, 40, 30), self.rect.inflate(6, 6), border_radius=12)  # Shadow border
        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        # Text carved effect
        text = self.font.render(self.label, True, self.text_color)
        text_shadow = self.font.render(self.label, True, (60, 60, 60))

        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))  # Shadow offset
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_clicked(event.pos):
            self.on_click()

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.play_click_sound()
            return True
        return False

    def play_click_sound(self):
        if self.app and hasattr(self.app, 'sound'):
            self.app.sound.play_click()
