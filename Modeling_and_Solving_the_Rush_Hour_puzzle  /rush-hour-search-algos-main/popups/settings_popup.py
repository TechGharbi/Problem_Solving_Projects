import pygame
from ui.button import Button
from ui.icon_button import IconButton
from screens.menu_screen import MenuScreen
from ui.icon_toggle import IconToggleButton

class SettingsPopup:
    def __init__(self, app, parent_screen):
        self.app = app
        self.parent = parent_screen
        self.font = pygame.font.SysFont("Arial", 22)

        self.btn_close = Button(300, 430, 120, 40, "Close", self.on_close, self.app)
        
        # Icon toggles
        self.sound_toggle = IconToggleButton(
            x= 290, y = 290,
            icon_on_path="assets/volume.png",
            icon_off_path="assets/mute.png",
            initial_state=True,
            on_toggle=self.toggle_sound
        )

        self.music_toggle = IconToggleButton(
            x= 490, y=290,
            icon_on_path="assets/music-player.png",
            icon_off_path="assets/music-off.png",
            initial_state=True,
            on_toggle=self.toggle_music
        )

        self.sound_enabled = True
        self.music_enabled = True

    def draw(self, screen):
        # Background container
        # Main popup box
        box_x, box_y = 200, 180
        box_width, box_height = 400, 320
        pygame.draw.rect(screen, (240, 240, 240), (box_x, box_y, box_width, box_height), border_radius=12)

        # Shorter title bar
        title_bar_width = 200
        title_bar_height = 40
        title_bar_x = box_x + (box_width - title_bar_width) // 2
        title_bar_y = box_y + 10  # slightly overlap the top of popup
        pygame.draw.rect(screen, (150, 130, 110), (title_bar_x, title_bar_y, title_bar_width, title_bar_height), border_radius=12)

        # Title centered in shorter bar
        title_text = self.font.render("Settings", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(title_bar_x + title_bar_width // 2, title_bar_y + title_bar_height // 2))
        screen.blit(title_text, title_rect)


        # Labels for Sound and Music (below title)
        label_y = box_y + title_bar_height + 20
        sound_label = self.font.render("Sound", True, (0, 0, 0))
        music_label = self.font.render("Music", True, (0, 0, 0))

        screen.blit(sound_label, (box_x + 80, label_y))
        screen.blit(music_label, (box_x + 280, label_y))

        # Sound/Music icons (centered below labels)
        self.sound_toggle.draw(screen)
        self.music_toggle.draw(screen)

        # Close button
        self.btn_close.rect.centerx = box_x + box_width // 2
        self.btn_close.rect.y = box_y + box_height - 60
        self.btn_close.draw(screen)



    def handle_input(self, event):
        self.sound_toggle.handle_event(event)
        self.music_toggle.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            for btn in [self.btn_close]:
                if btn.is_clicked(event.pos):
                    btn.on_click()
    
    def toggle_sound(self, enabled):
        self.app.sound.toggle_sound()

    def toggle_music(self, enabled):
        self.app.sound.toggle_music()

    def on_close(self):
        if hasattr(self.parent, "popups") and self in self.parent.popups:
            self.parent.popups.remove(self)
