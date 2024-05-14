import pygame
from client.games.base_game import MidiGame

pygame.init()
game = MidiGame("assets/midi/happy_birthday.mid", 10, narrate_pitch=True)

game.start()
running = True
while running:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False
    game.handle_events()
    if not game.is_running():
        print(game.stop())
        running = False
