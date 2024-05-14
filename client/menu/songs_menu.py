from client.menu.menu import Menu
import client.menu.single_player as single_player
import client.menu.songs_parameter as songs_parameter
import pygame
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)


class SongsMenu(Menu):
    def __init__(self):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = ["Happy Birthday", "Twinkle", "Back"]

        self.asset_man.load_sound(
            "happy_birthday", "assets/songs_menu/happy_birthday.mp3"
        )
        self.asset_man.load_sound("twinkle", "assets/songs_menu/twinkle.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == len(self.OPTIONS) - 1:
            self.switch_screen = True
            self.new_screen = single_player.SinglePlayer()
        else:
            self.switch_screen = True
            self.new_screen = songs_parameter.SongsParameters(
                self.OPTIONS[selected_option], True, True, 3, -1
            )
            pygame.mixer.music.pause()

        return True

    def render(self, window):
        window.fill(BLACK)
        txt_font = pygame.font.Font(None, 48)
        txt_text = txt_font.render("Songs Menu", True, WHITE)
        txt_text_rect = txt_text.get_rect()
        txt_text_rect.midtop = (WINDOW_WIDTH // 2, 50)
        window.blit(txt_text, txt_text_rect)

        for i, option in enumerate(self.OPTIONS):
            if i == self.selected_option:
                color = SELECTED_COLOR
            else:
                color = WHITE

            text = self.font.render(option, True, color)
            text_rect = text.get_rect()
            text_rect.midtop = (
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2 - len(self.OPTIONS) * 36 // 2 + i * 36,
            )
            window.blit(text, text_rect)
