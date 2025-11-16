import pygame
from ui.button import Button
from model.load_map import load_map_level

class SelectLevelPopup:
    def __init__(self, app, parent_screen):
        self.app = app
        self.parent = parent_screen
        self.message = "Choose level"
        self.font = pygame.font.SysFont("impact", 22)
        self.label_font = pygame.font.SysFont("Arial", 20, bold=True)

        self.buttons = []
        self.labels = []

        # Name and color of label
        label_texts = ["EASY", "MEDIUM", "HARD"]
        label_colors = [(0, 200, 0), (255, 140, 0), (200, 0, 0)]  #green, orange, red

        for row in range(3):
            # Nhãn bên trái (vd: EASY)
            label = {
                "text": label_texts[row],
                "pos": (160, 295 + row * 60 + 10), 
                "color": label_colors[row]
            }
            self.labels.append(label)

            for col in range(5):
                level_num = row * 5 + col + 1
                x = 250 + col * 60  
                y = 295 + row * 60

                def make_callback(level):
                    return lambda: self.select_level(level)

                # Màu nút theo mức độ
                if level_num <= 5:
                    bg_color = (0, 200, 0)       # EASY - green
                elif level_num <= 10:
                    bg_color = (255, 140, 0)     # MEDIUM - orange
                else:
                    bg_color = (200, 0, 0)       # HARD - red

                self.buttons.append(
                    Button(x, y, 50, 40, str(level_num), make_callback(level_num), self.app,
                           bg_color=bg_color, text_color=(255, 255, 255))
                )

        # Back
        self.btn_back = Button(295, 470, 120, 40, "Back", self.on_back, self.app,
                               bg_color=(100, 149, 237), text_color=(255, 255, 255))

        print("[DEBUG] SelectLevelPopup created")

    def draw(self, screen):
        # Popup frame
        pygame.draw.rect(screen, (220, 240, 250), (150, 240, 420, 290), border_radius=10)

        # Title
        text = self.font.render(self.message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(360, 260))
        screen.blit(text, text_rect)

        # EASY / MEDIUM / HARD
        for label in self.labels:
            label_surface = self.label_font.render(label["text"], True, label["color"])
            screen.blit(label_surface, label["pos"])

        # Level button
        for btn in self.buttons:
            btn.draw(screen)

        # Back
        self.btn_back.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.buttons:
                if btn.is_clicked(event.pos):
                    btn.on_click()
            if self.btn_back.is_clicked(event.pos):
                self.btn_back.on_click()

    def select_level(self, level):
        print(f"[DEBUG] select_level called with level = {level}")
        from screens.preview_screen import PreviewLevelScreen
        node = load_map_level(level)
        level_name = f"Level {level}"
        self.app.switch_screen(PreviewLevelScreen(self.app, node, self, level_name))

    def on_back(self):
        self.parent.popups.remove(self)
