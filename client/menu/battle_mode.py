from client.menu.menu import Menu
import client.menu.main_menu as main_menu
import client.menu.waiting_battle as waiting
import pygame
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)


class Battle(Menu):
    def __init__(self, message=None):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = ["Info", "Find Match", "Back"]
        self.message = message
        self.asset_man.load_sound("server_is_down", "assets/server_is_down.mp3")
        self.asset_man.load_sound("find_match", "assets/versus/find_match.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.asset_man.load_sound("exit_waiting", "assets/versus/exit_waiting.mp3")
        self.asset_man.load_sound(
            "info_find_match", "assets/battle/info_find_match.mp3"
        )
        self.asset_man.load_sound("info", "assets/info.mp3")
        self.info_sound_playing = False

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.play_info_sound()
        elif selected_option == 1:
            self.switch_screen = True
            self.new_screen = waiting.Waiting_Battle()
            pygame.mixer.music.pause()
        elif selected_option == 2:
            self.switch_screen = True
            self.new_screen = main_menu.MainMenu()
        return True

    def play_info_sound(self):
        self.play_sound("info_find_match")
        self.info_sound_playing = True

    def stop_info_sound(self):
        self.asset_man.sounds["info_find_match"].stop()
        self.info_sound_playing = False

    def render(self, window):
        window.fill(BLACK)

        txt_font = pygame.font.Font(None, 48)
        txt_text = txt_font.render("Battle Mode", True, WHITE)
        txt_text_rect = txt_text.get_rect()
        txt_text_rect.midtop = (WINDOW_WIDTH // 2, 50)
        window.blit(txt_text, txt_text_rect)
        if self.message:
            score_font = pygame.font.Font(None, 30)
            score_text = score_font.render(self.message, True, WHITE)
            score_text_rect = score_text.get_rect()
            score_text_rect.midtop = (WINDOW_WIDTH // 2, 100)
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
