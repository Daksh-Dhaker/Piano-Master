from client.menu.screen import Screen
import pygame
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)


class Menu(Screen):
    def __init__(self, background):
        super().__init__(background)
        self.OPTIONS = []
        self.selected_option = -1
        self.asset_man.load_sound("click", "assets/click.mp3")
        self.font = pygame.font.Font(None, 36)

    def update(self):
        pass

    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                prev_selected_option = self.selected_option

                if event.key == pygame.K_UP:
                    self.selected_option = max(0, self.selected_option - 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = min(
                        len(self.OPTIONS) - 1, self.selected_option + 1
                    )
                elif event.key == pygame.K_RETURN:
                    if not self.handle_selection(self.selected_option):
                        return False

                if self.selected_option != prev_selected_option:
                    self.play_sound("click")
                    self.play_sound(
                        self.OPTIONS[self.selected_option].lower().replace(" ", "_")
                    )

        return True

    def handle_selection(self, selected_option):
        # Implement this method in the child classes
        raise NotImplementedError

    def play_sound(self, sound_name):
        self.asset_man.sounds[sound_name].play()

    def render(self, window):
        window.fill(BLACK)

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
