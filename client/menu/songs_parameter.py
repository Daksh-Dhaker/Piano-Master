from client.menu.menu import Menu
import client.menu.main_menu as main_menu
import client.menu.pitch_results as pitch_results
import client.games.learn_pitch as learn_pitch
import client.games.practice_results as practice_results
import client.games.songs_game as songs_game
import pygame
import client.games.base_game as base_game
import client.menu.single_player as single_player
import client.menu.songs_menu as songs_menu
import time
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)


class SongsParameters(Menu):
    def __init__(self, song, narrate_name, narrate_pitch, note_length, selected_option):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = [
            "Info",
            "Narrate name",
            "Narrate pitch",
            "Note length",
            "Play",
            "Back",
        ]
        self.asset_man.load_sound("info", "assets/info.mp3")
        self.asset_man.load_sound("narrate_name", "assets/parameters/narrate_name.mp3")
        self.asset_man.load_sound(
            "narrate_pitch", "assets/parameters/narrate_pitch.mp3"
        )
        self.asset_man.load_sound("note_length", "assets/parameters/note_length.mp3")
        self.asset_man.load_sound("play", "assets/home/play.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.asset_man.load_sound("info_pitch", "assets/parameters/info_pitch.mp3")
        self.song = song
        self.asset_man.load_sound("count_down", "assets/count_down.mp3")
        self.info_sound_playing = False
        self.score = 0
        self.selected_option = selected_option

        self.narrate_name = narrate_name
        self.narrate_pitch = narrate_pitch
        self.note_length = note_length
        self.asset_man.load_sound("on", "assets/parameters/on.mp3")
        self.asset_man.load_sound("off", "assets/parameters/off.mp3")
        self.asset_man.load_sound("narrate_name", "assets/parameters/narrate_name.mp3")
        self.asset_man.load_sound(
            "narrate_pitch", "assets/parameters/narrate_pitch.mp3"
        )
        self.asset_man.load_sound("note_length", "assets/parameters/note_length.mp3")
        self.asset_man.load_sound("1", "assets/numbers/1.mp3")
        self.asset_man.load_sound("2", "assets/numbers/2.mp3")
        self.asset_man.load_sound("3", "assets/numbers/3.mp3")
        self.asset_man.load_sound("4", "assets/numbers/4.mp3")
        self.asset_man.load_sound("5", "assets/numbers/5.mp3")
        self.asset_man.load_sound("6", "assets/numbers/6.mp3")
        self.asset_man.load_sound("7", "assets/numbers/7.mp3")
        self.asset_man.load_sound("0", "assets/numbers/0.mp3")

    def update(self):
        pass

    # TODO Pause background music (Done)
    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.play_info_sound()
        elif selected_option == 1:
            self.narrate_name = not (self.narrate_name)
            self.switch_screen = True
            if self.narrate_name:
                self.play_sound("on")
            else:
                self.play_sound("off")
            self.new_screen = SongsParameters(
                self.song,
                self.narrate_name,
                self.narrate_pitch,
                self.note_length,
                selected_option,
            )
            pygame.mixer.music.pause()
        elif selected_option == 2:
            self.narrate_pitch = not (self.narrate_pitch)
            self.switch_screen = True
            if self.narrate_pitch:
                self.play_sound("on")
            else:
                self.play_sound("off")
            self.new_screen = SongsParameters(
                self.song,
                self.narrate_name,
                self.narrate_pitch,
                self.note_length,
                selected_option,
            )
            pygame.mixer.music.pause()
        elif selected_option == 3:
            self.note_length = self.note_length + 1
            self.switch_screen = True
            self.new_screen = SongsParameters(
                self.song,
                self.narrate_name,
                self.narrate_pitch,
                self.note_length,
                selected_option,
            )
            pygame.mixer.music.pause()
        elif selected_option == 4:
            self.switch_screen = True
            self.new_screen = songs_game.SongsGame(
                self.song, self.narrate_name, self.narrate_pitch, self.note_length
            )
            pygame.mixer.music.pause()
        else:
            self.switch_screen = True
            self.new_screen = songs_menu.SongsMenu()

        return True

    def play_info_sound(self):
        self.play_sound("info_pitch")
        self.info_sound_playing = True

    def stop_info_sound(self):
        self.asset_man.sounds["info_pitch"].stop()
        self.info_sound_playing = False

    def render(self, window):
        window.fill(BLACK)
        for i, option in enumerate(self.OPTIONS):
            if i == self.selected_option:
                color = SELECTED_COLOR
            else:
                color = WHITE

            if i == 1:
                value = "OFF"
                if self.narrate_name == True:
                    value = "ON"
                text = self.font.render(option + " - " + value, True, color)
            elif i == 2:
                value = "OFF"
                if self.narrate_pitch == True:
                    value = "ON"
                text = self.font.render(option + " - " + value, True, color)
            elif i == 3:
                value = str(self.note_length)
                text = self.font.render(option + " - " + value, True, color)
            else:
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
                prev_selected_option = self.selected_option

                if event.key == pygame.K_UP:
                    self.selected_option = max(0, self.selected_option - 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = min(
                        len(self.OPTIONS) - 1, self.selected_option + 1
                    )
                elif event.key == pygame.K_RETURN:
                    if self.selected_option != 3:
                        if not self.handle_selection(self.selected_option):
                            return False
                elif event.key == pygame.K_RIGHT:
                    if self.selected_option == 3:
                        self.note_length = min(7, self.note_length + 1)
                        self.switch_screen = True
                        self.new_screen = SongsParameters(
                            self.song,
                            self.narrate_name,
                            self.narrate_pitch,
                            self.note_length,
                            self.selected_option,
                        )
                        self.play_sound(str(self.note_length))
                        pygame.mixer.music.pause()
                        return True

                elif event.key == pygame.K_LEFT:
                    if self.selected_option == 3:
                        self.note_length = max(1, self.note_length - 1)
                        self.switch_screen = True
                        self.new_screen = SongsParameters(
                            self.song,
                            self.narrate_name,
                            self.narrate_pitch,
                            self.note_length,
                            self.selected_option,
                        )
                        self.play_sound(str(self.note_length))
                        pygame.mixer.music.pause()
                        return True

                if self.selected_option != prev_selected_option:
                    self.play_sound("click")
                    self.play_sound(
                        self.OPTIONS[self.selected_option].lower().replace(" ", "_")
                    )

        return True
