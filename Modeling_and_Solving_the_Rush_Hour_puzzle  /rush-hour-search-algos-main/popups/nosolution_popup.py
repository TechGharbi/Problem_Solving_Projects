import pygame
import time

class NoSolutionPopup:
    def __init__(self, app, solver_screen, parent_screen=None):
        self.app = app
        self.solver_screen = solver_screen
        self.parent_screen = parent_screen  
        self.visible = True
        self.width = 420
        self.height = 200
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(app.screen.get_width() // 2, app.screen.get_height() // 2))

        self.title_font = pygame.font.SysFont("Segoe UI", 36, bold=True)
        self.instruction_font = pygame.font.SysFont("Segoe UI", 20, italic=True)
        self.close_font = pygame.font.SysFont("Arial", 24, bold=True)

        self.close_button_rect = pygame.Rect(self.rect.right - 45, self.rect.top + 10, 30, 30)

        self.start_time = time.time()
        self.animation_duration = 1.0  # seconds

        self.bg_color = (255, 235, 180, 240)  # desert sand with alpha
        self.border_color = (160, 110, 60)    # stone-like outline
        self.text_color = (80, 40, 0)

    def draw(self):
        if not self.visible:
            return

        elapsed = time.time() - self.start_time
        alpha = min(255, int((elapsed / self.animation_duration) * 255))
        self.surface.set_alpha(alpha)

        # Background with border
        self.surface.fill(self.bg_color)
        pygame.draw.rect(self.surface, self.border_color, (0, 0, self.width, self.height), 6, border_radius=20)

        # Title
        title = self.title_font.render("Failure!", True, self.text_color)
        self.surface.blit(title, title.get_rect(center=(self.width // 2, 50)))

        # Instruction
        instruction = self.instruction_font.render("The puzzle has no solution! Click X to continue.", True, self.text_color)
        self.surface.blit(instruction, instruction.get_rect(center=(self.width // 2, 110)))

        # Close button (wooden style)
        rel_close_rect = self.close_button_rect.move(-self.rect.left, -self.rect.top)
        pygame.draw.rect(self.surface, (160, 80, 40), rel_close_rect, border_radius=8)
        close_text = self.close_font.render("X", True, (255, 255, 255))
        self.surface.blit(close_text, close_text.get_rect(center=rel_close_rect.center))

        # Draw popup on screen
        self.app.screen.blit(self.surface, self.rect.topleft)

    def handle_event(self, event):
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect.collidepoint(event.pos):
                self.visible = False
                if self in self.solver_screen.popups:
                    self.solver_screen.popups.remove(self)
