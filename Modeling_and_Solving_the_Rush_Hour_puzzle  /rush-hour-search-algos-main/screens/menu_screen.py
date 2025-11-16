import pygame
from screens.screen import Screen
from ui.button import Button
from ui.icon_button import IconButton
# from ui.sprites import CarSprite

class MenuScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.buttons = [
            Button(260, 200, 200, 50, "Play", self.on_play, self.app),
            Button(260, 280, 200, 50, "Instructions", self.on_instructions, self.app),
            Button(260, 360, 200, 50, "Credits", self.on_credits, self.app),
            Button(260, 440, 200, 50, "Quit", self.on_quit, self.app),
            IconButton(650, 10, "assets/settings.png", self.on_settings, 64, self.app)
        ]
        self.background_img = pygame.image.load("assets/menu_bg.jpg").convert()
        self.title_font = pygame.font.SysFont("Papyrus", 80, bold=True)
        self.popups = []

    def render(self):
        # Draw background
        self.app.screen.blit(self.background_img, (0, 0))
        # self.sprite.draw_car(self.app.screen, 80, 80)
        title_surface = self.title_font.render("RUSH HOUR", True, (216, 40, 11))
        title_rect = title_surface.get_rect(center=(360, 120))
        self.app.screen.blit(title_surface, title_rect)
        
        for button in self.buttons:
            button.draw(self.app.screen)
        for popup in self.popups:
            popup.draw(self.app.screen)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Let popups handle input first
                if self.popups:
                    self.popups[-1].handle_input(event)
                else:
                    for button in self.buttons:
                        if button.is_clicked(event.pos):
                            button.on_click()

    def on_play(self):
        from popups.select_map_popup import SelectMapPopup
        self.popups.append(SelectMapPopup(self.app, self))

        #from popups.select_level_popup import SelectLevelPopup
        #self.popups.append(SelectLevelPopup(self.app, self))
       

    def on_settings(self):
        from popups.settings_popup import SettingsPopup
        self.popups.append(SettingsPopup(self.app, self))

    def on_instructions(self):
        from screens.instruction_screen import InstructionScreen
        self.app.switch_screen(InstructionScreen(self.app))

    def on_credits(self):
        from screens.credits_screen import CreditsScreen
        self.app.switch_screen(CreditsScreen(self.app))
        
    def on_quit(self):
        pygame.quit()
        exit()
