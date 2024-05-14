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
import client.midi.midi_listener as midi_listener


class Battle_play(Menu):
    def __init__(self, p):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = []
        self.is_game_started = 0
        self.listener = midi_listener.MidiListener(5)
        self.asset_man.load_sound("halt", "assets/multiplayer_game/halt.mp3")
        self.asset_man.load_sound("game_halted", "assets/game_halted.mp3")
        self.asset_man.load_sound("your_score_is", "assets/pitch/your_score_is.mp3")
        self.asset_man.load_sound("oppo_score_is", "assets/pitch/oppo_score_is.mp3")
        self.player_id = p
        self.asset_man.load_sound(
            "play_round_started", "assets/battle/play_round_started.mp3"
        )
        self.game_type = "battle_act_mult_game"
        self.score = 0
        self.halt_flag = 0

    def start_game(self):
        if self.is_game_started == 0:
            self.play_sound("play_round_started")
            time.sleep(1)
            self.is_game_started = 1
            self.listener.start()
            print("listener started")
            # self.flag = 1   # To be checked

    def update(self):
        pass

    def load_score(self, score):
        str_form = str(score)
        for digit in str_form:
            time.sleep(0.3)
            path_sd = "assets/numbers/" + digit + ".mp3"
            time.sleep(0.3)
            self.asset_man.load_sound(digit, path_sd)
            self.play_sound(digit)

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.halt_flag = 1
        return True

    def render(self, window):
        window.fill(BLACK)
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(
            "Playing round for Player - " + str(self.player_id), True, WHITE
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
