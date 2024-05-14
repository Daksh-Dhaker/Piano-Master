from client.menu.menu import Menu
import client.menu.main_menu as main_menu
import pygame


class Home(Menu):
    def __init__(self):
        super().__init__("assets/menu/background.mp3")
        self.OPTIONS = ["Play", "Exit"]
        self.asset_man.load_sound("play", "assets/home/play.mp3")
        self.asset_man.load_sound("exit", "assets/menu/exit.mp3")
        self.asset_man.load_sound("info", "assets/home/info.mp3")
        self.play_sound("info")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.switch_screen = True
            self.new_screen = main_menu.MainMenu()
        elif selected_option == 1:
            return False

        return True

    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.asset_man.sounds["info"].stop()

        return super().handle_events(events)
