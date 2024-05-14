from client.menu.menu import Menu
import client.menu.main_menu as main_menu
import client.menu.pitch_results as pitch_results
import client.games.learn_pitch as learn_pitch
import client.games.practice_results as practice_results
import client.menu.songs_menu as songs_menu
import pygame
import client.games.base_game as base_game
import client.menu.parameter_learn_pitch as parameter_learn_pitch
import client.menu.practice_para as parameter_practice_pitch
import time
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)


class SinglePlayer(Menu):
    def __init__(self):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = ["Info", "Pitch", "Songs", "Practice", "Back"]
        self.asset_man.load_sound("info", "assets/info.mp3")
        self.asset_man.load_sound("pitch", "assets/single/pitch.mp3")
        self.asset_man.load_sound("songs", "assets/single/songs.mp3")
        self.asset_man.load_sound("practice", "assets/single/practice.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.asset_man.load_sound(
            "info_single_player", "assets/single/info_single_player.mp3"
        )
        self.asset_man.load_sound("count_down", "assets/count_down.mp3")
        self.info_sound_playing = False
        self.score = 0

    def update(self):
        pass

    # TODO Pause background music (Done)
    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.play_info_sound()
        elif selected_option == 1:

            self.switch_screen = True
            self.new_screen = parameter_learn_pitch.Parameters(True, True, 3, -1)
            pygame.mixer.music.pause()
        elif selected_option == 2:
            self.switch_screen = True
            self.new_screen = songs_menu.SongsMenu()
            pygame.mixer.music.pause()
        elif selected_option == 3:

            self.switch_screen = True
            self.new_screen = parameter_practice_pitch.Parameters_practice(True, 3, -1)
            pygame.mixer.music.pause()
        else:
            self.switch_screen = True
            self.new_screen = main_menu.MainMenu()

        return True

    def play_info_sound(self):
        self.play_sound("info_single_player")
        self.info_sound_playing = True

    def stop_info_sound(self):
        self.asset_man.sounds["info_single_player"].stop()
        self.info_sound_playing = False

    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.info_sound_playing:
                    self.stop_info_sound()

        return super().handle_events(events)

    def render(self, window):
        window.fill(BLACK)

        txt_font = pygame.font.Font(None, 48)
        txt_text = txt_font.render("Single Player", True, WHITE)
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
