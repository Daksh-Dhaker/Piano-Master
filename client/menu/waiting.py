from client.menu.menu import Menu
import client.menu.main_menu as main_menu
import client.menu.versus as versus
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)
import pygame


class Waiting(Menu):
    def __init__(self):
        self.helper()
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = []
        self.asset_man.load_sound("server_is_down", "assets/server_is_down.mp3")
        self.asset_man.load_sound("waiting", "assets/versus/waiting.mp3")
        self.asset_man.load_sound("connected", "assets/versus/connected.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.game_type = "versus_waiting"
        self.play_sound("waiting")
        print(self.game_type)

    def update(self):
        pass

    def helper(self):

        self.game_type = "versus_waiting"

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.switch_screen = True
            self.new_screen = versus.Versus()

        return True

    def render(self, window):
        window.fill(BLACK)
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render("Waiting for a player...", True, WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.midtop = (WINDOW_WIDTH // 2, 50)
        window.blit(score_text, score_text_rect)
        text = self.font.render(
            "Press 'Downward arrow key' to exit waiting", True, WHITE
        )
        text_rect = text.get_rect()
        text_rect.midtop = (
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 1 * 36 // 2 + 0 * 36,
        )
        window.blit(text, text_rect)
