from client.menu.menu import Menu
import client.games.base_game as base_game
import pygame
import client.menu.pitch_results as pitch_results
import time
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)
import client.menu.parameter_learn_pitch as parameter_learn_pitch


class LearnPitch(Menu):
    def __init__(self, narrate_name, narrate_pitch, note_length):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = ["Back", "Halt"]
        self.is_game_started = 0

        self.asset_man.load_sound("back", "assets/back.mp3")

        self.game_screen = base_game.MidiGame(
            "assets/midi/learn_pitch.mid", note_length, narrate_pitch, narrate_name
        )
        self.asset_man.load_sound("your_score_is", "assets/pitch/your_score_is.mp3")

        self.asset_man.load_sound("3", "assets/numbers/3.mp3")
        self.asset_man.load_sound("2", "assets/numbers/2.mp3")
        self.asset_man.load_sound("1", "assets/numbers/1.mp3")
        self.asset_man.load_sound("halt", "assets/multiplayer_game/halt.mp3")
        self.asset_man.load_sound(
            "the_game_starts_in", "assets/numbers/the_game_starts_in.mp3"
        )
        self.game_type = "pitch"
        self.halt_flag = 0
        self.narrate_name = narrate_name
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
            self.game_screen.start()

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.game_screen.stop()
            self.switch_screen = True
            self.new_screen = parameter_learn_pitch.Parameters(
                self.narrate_name, self.narrate_pitch, self.note_length, -1
            )
            pygame.mixer.music.pause()
        elif selected_option == 1:
            score = self.game_screen.stop()
            self.switch_screen = True
            self.new_screen = pitch_results.PitchResultMenu(
                score, self.narrate_name, self.narrate_pitch, self.note_length
            )

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
