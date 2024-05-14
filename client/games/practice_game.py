from client.menu.menu import Menu
import client.games.pitch_game as pitch_game
import client.games.pitch_game as pitch_game
import pygame
import client.games.practice_results as practice_results
import client.menu.practice_para as parameter_practice_pitch
import time
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)
import client.menu.parameter_learn_pitch as parameter_learn_pitch


class Practice_game(Menu):
    def __init__(self, narrate_pitch, note_length):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = ["Back", "Halt"]
        self.is_game_started = 0

        self.asset_man.load_sound("back", "assets/back.mp3")

        self.game_screen = pitch_game.PitchGame(note_length, narrate_pitch)
        self.asset_man.load_sound("your_score_is", "assets/pitch/your_score_is.mp3")

        self.asset_man.load_sound("3", "assets/numbers/3.mp3")
        self.asset_man.load_sound("2", "assets/numbers/2.mp3")
        self.asset_man.load_sound("1", "assets/numbers/1.mp3")
        self.asset_man.load_sound("halt", "assets/multiplayer_game/halt.mp3")
        self.asset_man.load_sound(
            "the_game_starts_in", "assets/numbers/the_game_starts_in.mp3"
        )
        self.game_type = "practice"
        self.halt_flag = 0
        self.narrate_pitch = narrate_pitch
        self.note_length = note_length

    def start_game(self):
        if self.is_game_started == 0:
            self.play_sound("the_game_starts_in")
            time.sleep(1)
            self.play_sound("3")
            time.sleep(1)
            self.play_sound("2")
            time.sleep(1)
            self.play_sound("1")
            time.sleep(1)
            self.is_game_started = 1
            print("Practice started")
            self.game_screen.start()
            print("Practice ended")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            print("entered stop function")
            self.game_screen.stop()
            print("game stopped")
            self.switch_screen = True
            self.new_screen = parameter_practice_pitch.Parameters_practice(
                self.narrate_pitch, self.note_length, -1
            )
            print("screen set")
        elif selected_option == 1:
            print("entered stop function")
            score = self.game_screen.stop()
            print("game stopped")
            self.switch_screen = True
            self.new_screen = practice_results.PracticeResults(
                score, self.narrate_pitch, self.note_length
            )
            print("screen set")

        return True

    def render(self, window):
        window.fill(BLACK)
        score_font = pygame.font.Font(None, 48)
        if self.game_screen.is_running():
            score_text = score_font.render("The game has started...", True, WHITE)
        else:
            score_text = score_font.render("The game has been finished...", True, WHITE)

        score_text_rect = score_text.get_rect()
        score_text_rect.midtop = (WINDOW_WIDTH // 2, 50)
        window.blit(score_text, score_text_rect)

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
