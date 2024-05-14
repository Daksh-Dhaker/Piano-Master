import pygame


class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}

    def load_image(self, name, path):
        try:
            self.images[name] = pygame.image.load(path)
        except pygame.error:
            print(f"Unable to load {name}: {path}")

    def load_sound(self, name, path):
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
        except FileNotFoundError:
            print(f"Unable to load {name}: {path}")

    def load_bg_music(self, path):
        try:
            pygame.mixer.music.unload()
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

        except pygame.error:
            print(f"Unable to load music: {path}")
