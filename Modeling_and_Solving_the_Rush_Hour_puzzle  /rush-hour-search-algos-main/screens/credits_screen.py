import random
import pygame
from screens.screen import Screen
from ui.button import Button

DESERT_SAND = (210, 180, 140)

class CreditsScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.font_title = pygame.font.SysFont("Papyrus", 40, bold=True)
        self.font_body = pygame.font.SysFont("Segoe UI", 20)
        self.btn_back = Button(280, 560, 160, 40, "Back", self.on_back, self.app)

    def render(self):
        self.draw_background()
        screen_width = self.app.screen.get_width()
        
        # Draw title
        title_text = self.font_title.render("Credits", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, 40))
        self.app.screen.blit(title_text, title_rect)

        # White box background
        box_width, box_height = 500, 370
        box_x = (screen_width - box_width) // 2
        box_y = 90
        pygame.draw.rect(self.app.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), border_radius=16)

        # Draw game name
        name_font = self.font_body
        rush_hour_text = name_font.render("Rush Hour", True, (0, 0, 0))
        self.app.screen.blit(rush_hour_text, rush_hour_text.get_rect(center=(screen_width // 2, box_y + 30)))

        # Developer label
        dev_label = self.font_body.render("Developed by:", True, (0, 0, 0))
        self.app.screen.blit(dev_label, dev_label.get_rect(center=(screen_width // 2, box_y + 70)))

        # Developer names (centered inside the box)
        devs = [
            "23127102 - Lê Quang Phúc",
            "23127148 - Ân Tiến Nguyên An",
            "23127307 - Nguyễn Phạm Minh Thư",
            "23127442 - Trầm Hữu Nhân",
            "                        ",
            "CSC14003 - Introduction to Artificial Intelligence",
            "Special thanks to:",
            "  Prof. Nguyễn Ngọc Thảo",
            "  Prof. Nguyễn Thanh Tình"
        ]
        y = box_y + 110
        for dev in devs:
            dev_text = self.font_body.render(dev, True, (0, 0, 0))
            self.app.screen.blit(dev_text, dev_text.get_rect(center=(screen_width // 2, y)))
            y += 30
        self.btn_back.draw(self.app.screen)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_back.is_clicked(event.pos):
                    self.on_back()

    def on_back(self):
        from screens.menu_screen import MenuScreen
        self.app.switch_screen(MenuScreen(self.app))

    
    


