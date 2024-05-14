from client.menu.menu import Menu
import client.menu.versus as versus
import client.menu.single_player as single_player
import client.menu.home as home
import pygame
import client.menu.battle_mode as battle


class MainMenu(Menu):
    def __init__(self):
        super().__init__("assets/menu/background.mp3")
        self.OPTIONS = ["Info", "Single Player", "Versus Mode", "Battle Mode", "Back"]

        self.asset_man.load_sound("info", "assets/info.mp3")
        self.asset_man.load_sound("single_player", "assets/menu/single_player.mp3")
        self.asset_man.load_sound("versus_mode", "assets/menu/versus_mode.mp3")
        self.asset_man.load_sound("battle_mode", "assets/menu/battle_mode.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.asset_man.load_sound("info_menu", "assets/menu/info_menu.mp3")
        self.info_sound_playing = False

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:

            self.play_info_sound()
        elif selected_option == 1:
            self.switch_screen = True
            self.new_screen = single_player.SinglePlayer()
        elif selected_option == 2:
            self.switch_screen = True
            self.new_screen = versus.Versus()
        elif selected_option == 3:
            self.switch_screen = True
            self.new_screen = battle.Battle()
        elif selected_option == 4:
            self.switch_screen = True
            self.new_screen = home.Home()

        return True

    def play_info_sound(self):
        self.play_sound("info_menu")
        self.info_sound_playing = True

    def stop_info_sound(self):
        self.asset_man.sounds["info_menu"].stop()
        self.info_sound_playing = False

    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.info_sound_playing:
                    self.stop_info_sound()

        return super().handle_events(events)
