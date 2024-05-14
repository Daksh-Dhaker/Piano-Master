import pygame
from client.utils.asset_manager import AssetManager
from client.utils.constants import BLACK


class Screen:
    def __init__(self, bg_music):
        self.switch_screen = False
        self.new_screen = None
        self.asset_man = AssetManager()
        self.asset_man.load_bg_music(bg_music)
        self.game_type = None

    def update(self) -> None:
        pass

    def render(self, window):
        window.fill(BLACK)

    def handle_events(self, events) -> bool:
        print("here!")
        for event in events:
            if event.type == pygame.QUIT:
                return False
        return True
