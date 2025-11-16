import pygame

class SoundManager:
    def __init__(self):
        self.click_sound = pygame.mixer.Sound("assets/sound.mp3")
        self.music_path = "assets/music.mp3"
        self.music_playing = False
        self.sound_on = True
        self.music_on = True

    def play_click(self):
        if self.sound_on:
            self.click_sound.play()

    def play_music(self):
        if self.music_on and not self.music_playing:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # loop forever
            self.music_playing = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False

    def toggle_sound(self):
        self.sound_on = not self.sound_on

    def toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            self.play_music()
        else:
            self.stop_music()
