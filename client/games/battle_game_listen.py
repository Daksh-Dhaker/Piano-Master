from client.menu.menu import Menu
import client.games.base_game as base_game
import pygame
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)
import time


class Battle_listen(Menu):
    def __init__(self, p, song_arr):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = []
        self.is_game_started = 0
        self.asset_man.load_sound("play_to_listen", "assets/battle/play_to_listen.mp3")
        self.asset_man.load_sound("game_halted", "assets/game_halted.mp3")
        self.asset_man.load_sound("round_over", "assets/battle/round_over.mp3")
        self.asset_man.load_sound("your_score_is", "assets/pitch/your_score_is.mp3")
        self.asset_man.load_sound("oppo_score_is", "assets/pitch/oppo_score_is.mp3")
        self.game_type = "battle_listen"
        self.game_screen = base_game.MidiGame(
            song_arr, note_length=4, narrate_name=False, narrate_pitch=True
        )
        self.asset_man.load_sound("halt", "assets/multiplayer_game/halt.mp3")
        self.player_id = p
        self.game_type = "battle_listen_mult_game"
        self.score = 0
        self.halt_flag = 0

    def start_game(self):
        if self.is_game_started == 0:
            time.sleep(1)
            self.game_screen.start()
            self.is_game_started = 1

    def load_score(self, score):
        str_form = str(score)
        for digit in str_form:
            time.sleep(0.3)
            path_sd = "assets/numbers/" + digit + ".mp3"
            time.sleep(0.3)
            self.asset_man.load_sound(digit, path_sd)
            self.play_sound(digit)

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.halt_flag = 1
        return True

    def render(self, window):
        window.fill(BLACK)
        score_font = pygame.font.Font(None, 48)

        score_text = score_font.render(
            "Listening Mode For Player - " + str(self.player_id), True, WHITE
        )

        score_text_rect = score_text.get_rect()
        score_text_rect.midtop = (WINDOW_WIDTH // 2, 50)
        window.blit(score_text, score_text_rect)
        text = self.font.render("Press 'Enter' to end the game", True, WHITE)
        text_rect = text.get_rect()
        text_rect.midtop = (
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 1 * 36 // 2 + 0 * 36,
        )
        window.blit(text, text_rect)
