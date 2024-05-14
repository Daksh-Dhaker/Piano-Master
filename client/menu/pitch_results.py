from client.menu.menu import Menu
import client.menu.single_player as single_player
import pygame
import client.games.learn_pitch as learn_pitch
import time
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)
import client.menu.parameter_learn_pitch as parameter_learn_pitch


class PitchResultMenu(Menu):
    def __init__(self, score, narrate_name, narrate_pitch, note_length):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = ["Info", "Play Again", "Back"]
        pygame.mixer.music.pause()
        self.asset_man.load_sound("your_score_is", "assets/pitch/your_score_is.mp3")
        self.asset_man.load_sound("info", "assets/info.mp3")
        self.asset_man.load_sound("info_results", "assets/parameters/info_results.mp3")
        self.asset_man.load_sound("play_again", "assets/pitch/play_again.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.score = score
        self.narrate_name = narrate_name
        self.narrate_pitch = narrate_pitch
        self.note_length = note_length
        self.info_sound_playing = False
        time.sleep(1)
        self.play_sound("your_score_is")
        time.sleep(2)
        self.load_score(score)

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.play_info_sound()
        elif selected_option == 1:
            self.switch_screen = True
            self.new_screen = learn_pitch.LearnPitch(
                self.narrate_name, self.narrate_pitch, self.note_length
            )
            pygame.mixer.music.pause()
        elif selected_option == 2:
            self.switch_screen = True
            self.new_screen = parameter_learn_pitch.Parameters(
                self.narrate_name, self.narrate_pitch, self.note_length, -1
            )
            pygame.mixer.music.pause()

        return True

    def play_info_sound(self):
        self.play_sound("info_results")
        self.info_sound_playing = True

    def stop_info_sound(self):
        self.asset_man.sounds["info_results"].stop()
        self.info_sound_playing = False

    def load_score(self, score):
        pygame.mixer.music.pause()
        str_form = str(score)

        for digit in str_form:
            time.sleep(0.3)
            path_sd = "assets/numbers/" + digit + ".mp3"
            time.sleep(0.3)
            self.asset_man.load_sound(digit, path_sd)
            self.play_sound(digit)

    def render(self, window):
        window.fill(BLACK)

        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render("Your score is " + str(self.score), True, WHITE)
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

    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.info_sound_playing:
                    self.stop_info_sound()

        return super().handle_events(events)
