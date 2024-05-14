import pygame
from client.menu.home import Home
from client.utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH
import time
import client.menu.pitch_results as pitch_results
from client.utils.network import Network
import client.menu.multiplayer_game_result as multiplayer_game_result
import client.games.multi_game as multi_game
import client.menu.multiplayer_game_result as multiplayer_game_result
import client.games.practice_results as practice_results
import client.menu.songs_results as songs_results
import client.games.battle_game_play as battle_play
import client.menu.battle_game_results as battle_game_results
import client.games.battle_game_listen as battle_listen
import client.menu.versus as versus
import client.menu.battle_mode as battle
import pickle

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Piano Master")

running = True
cur_screen = Home()

n = 0
player = 0
halt = 0
round = 0
is_network_initialised = 0
score_keeper = (0, 0)


def versus_initialise_network():
    global n, is_network_initialised
    n = Network()
    print(n)
    n.send("0")
    is_network_initialised = 1


def versus_server_down():
    global cur_screen
    if cur_screen.game_type == "versus_waiting":
        cur_screen.asset_man.sounds["waiting"].stop()
    cur_screen.play_sound("server_is_down")
    time.sleep(2)
    cur_screen.new_screen = versus.Versus("Server is Down")
    cur_screen = cur_screen.new_screen


def versus_waiting_exit():
    global cur_screen, n, is_network_initialised
    if cur_screen.game_type == "versus_waiting":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n.send("DISCONNECTED")
                n.send("DISCONNECTED")
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    cur_screen.asset_man.sounds["waiting"].stop()
                    cur_screen.new_screen = versus.Versus()
                    n.send("DISCONNECTED")
                    n.send("DISCONNECTED")
                    is_network_initialised = 0
                    cur_screen = cur_screen.new_screen
                    cur_screen.play_sound("exit_waiting")
                    time.sleep(1)


def game_none():
    global game, cur_screen, is_network_initialised, player
    if game == None:
        cur_screen.game_screen.stop()
        cur_screen.play_sound("game_halted")
        print("A")
        cur_screen.new_screen = multiplayer_game_result.MultiGameResults(
            str(0), str(0), player
        )
        cur_screen = cur_screen.new_screen
        is_network_initialised = 0


def is_versus_game_halted():
    global halt, cur_screen, is_network_initialised, player
    if halt == 1:
        cur_screen.play_sound("game_halted")
        print("B")
        cur_screen.new_screen = multiplayer_game_result.MultiGameResults(
            str(0), str(0), player
        )
        cur_screen = cur_screen.new_screen
        is_network_initialised = 0
        halt = 0


def versus_game_halt_check():
    global cur_screen, n, halt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cur_screen.game_screen.stop()
            n.send("DISCONNECTED")
            pygame.quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            cur_screen.game_screen.stop()
            halt = 1
            n.send("DISCONNECTED")


def versus_connected():
    global cur_screen, game, n, player
    if cur_screen.game_type == "versus_waiting":
        if game.connected():
            if game.conn1 == n.client_number:
                player = 0
            else:
                player = 1

            print("player: ", player)
            print("both connected to server successfully")
            cur_screen.asset_man.sounds["waiting"].stop()
            cur_screen.play_sound("connected")
            time.sleep(2)
            cur_screen.new_screen = multi_game.MultiGame(int(player), game.song_number)
            cur_screen = cur_screen.new_screen
            pygame.mixer.music.pause()


def versus_bothwent():
    global game, cur_screen, player, is_network_initialised
    print("BothWent")
    move1 = game.get_player_move(0)
    move2 = game.get_player_move(1)
    print("C")
    cur_screen.new_screen = multiplayer_game_result.MultiGameResults(
        move1, move2, player
    )
    pygame.mixer.music.pause()
    cur_screen = cur_screen.new_screen
    pygame.display.flip()
    is_network_initialised = 0


def versus_send_score():
    global game, cur_screen, player, n
    if cur_screen.game_type == "versus_act_mult_game":

        if cur_screen.is_game_started == 0:
            cur_screen.start_game()
        if cur_screen.game_screen.is_running():
            cur_screen.game_screen.handle_events()

        if player == 0:
            if not game.p1Went:
                if not cur_screen.game_screen.is_running():
                    score = cur_screen.game_screen.stop()
                    n.send(str(score))
                    print("Score sent :", score)
        else:
            if not game.p2Went:
                if not cur_screen.game_screen.is_running():
                    score = cur_screen.game_screen.stop()
                    n.send(str(score))
                    print("Score sent :", score)


def versus_game():
    global game, cur_screen
    versus_waiting_exit()
    if cur_screen.game_type == "versus_act_mult_game":
        versus_game_halt_check()
        game_none()
        is_versus_game_halted()
        pygame.display.flip()

    versus_connected()

    if (cur_screen.game_type != None) and (cur_screen.game_type[:6] == "versus"):
        if game.bothWent():
            versus_bothwent()
        else:
            versus_send_score()


def pitch_game_check():
    global cur_screen
    if cur_screen.game_type == "pitch":

        if cur_screen.is_game_started == 0:
            cur_screen.start_game()

        cur_screen.game_screen.handle_events()
        if not cur_screen.game_screen.is_running():
            score = cur_screen.game_screen.stop()
            cur_screen.new_screen = pitch_results.PitchResultMenu(
                score,
                cur_screen.narrate_name,
                cur_screen.narrate_pitch,
                cur_screen.note_length,
            )
            cur_screen = cur_screen.new_screen
            pygame.mixer.music.unpause()


def practice_game_check():
    global cur_screen
    if cur_screen.game_type == "practice":
        if cur_screen.is_game_started == 0:
            cur_screen.start_game()

        cur_screen.game_screen.handle_events()
        if not cur_screen.game_screen.is_running():
            score = cur_screen.game_screen.stop()
            cur_screen.new_screen = practice_results.PracticeResults(
                score,
                cur_screen.narrate_pitch,
                cur_screen.note_length,
            )
            cur_screen = cur_screen.new_screen
            pygame.mixer.music.unpause()


def songs_game_check():
    global cur_screen
    if cur_screen.game_type == "songs":
        if cur_screen.is_game_started == 0:
            cur_screen.start_game()

        cur_screen.game_screen.handle_events()
        if not cur_screen.game_screen.is_running():
            score = cur_screen.game_screen.stop()
            cur_screen.new_screen = songs_results.SongsResults(
                cur_screen.song,
                score,
                cur_screen.narrate_name,
                cur_screen.narrate_pitch,
                cur_screen.note_length,
            )
            cur_screen = cur_screen.new_screen
            pygame.mixer.music.unpause()


def battle_initialise_newtork():
    global n, is_network_initialised, round
    n = Network()
    n.send("1")
    is_network_initialised = 1
    round = 0


def battle_server_down():
    global cur_screen
    if cur_screen.game_type == "battle_waiting":
        cur_screen.asset_man.sounds["waiting"].stop()
    cur_screen.play_sound("server_is_down")
    time.sleep(2)
    cur_screen.new_screen = battle.Battle("Server is down")
    cur_screen = cur_screen.new_screen


def battle_waiting_check():
    global cur_screen, n, is_network_initialised
    if cur_screen.game_type == "battle_waiting":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n.send("DISCONNECTED")
                n.send("DISCONNECTED")
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    cur_screen.asset_man.sounds["waiting"].stop()
                    cur_screen.new_screen = battle.Battle()
                    print("game stopped")
                    n.send("DISCONNECTED")
                    n.send("DISCONNECTED")
                    is_network_initialised = 0
                    cur_screen = cur_screen.new_screen
                    cur_screen.play_sound("exit_waiting")
                    time.sleep(1)


def battle_results_none_check():
    global game, cur_screen, is_network_initialised, player
    if game != None and cur_screen.game_type == "battle_results":
        cur_screen.play_sound("game_halted")
        print("G")
        cur_screen.new_screen = battle_game_results.BattleResults(
            str(0), str(0), player
        )
        cur_screen = cur_screen.new_screen
        is_network_initialised = 0


def battle_halted_check():
    global game, cur_screen, is_network_initialised, player
    if (game == None) and cur_screen.game_type != "battle_results":
        if cur_screen.game_type == "battle_act_mult_game":
            cur_screen.listener.stop()
        if cur_screen.game_type == "battle_listen_mult_game":
            cur_screen.game_screen.stop()
        cur_screen.play_sound("game_halted")
        print("F")
        cur_screen.new_screen = battle_game_results.BattleResults(
            str(0), str(0), player
        )
        cur_screen = cur_screen.new_screen
        is_network_initialised = 0


def battle_listen_halted():
    global game, cur_screen, n, halt, player, is_network_initialised
    if game != None and cur_screen.game_type == "battle_listen_mult_game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n.send("DISCONNECTED")
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                halt = 1
                cur_screen.game_screen.stop()
                n.send("DISCONNECTED")

        if game == None:
            cur_screen.play_sound("game_halted")
            print("E")
            cur_screen.new_screen = battle_game_results.BattleResults(
                str(0), str(0), player
            )
            cur_screen = cur_screen.new_screen
            is_network_initialised = 0

        if halt == 1:
            cur_screen.play_sound("game_halted")
            print("D")
            cur_screen.new_screen = battle_game_results.BattleResults(
                str(0), str(0), player
            )
            cur_screen = cur_screen.new_screen
            is_network_initialised = 0
            halt = 0


def battle_playing_halted():
    global game, cur_screen, n, halt, is_network_initialised, player
    if game != None and cur_screen.game_type == "battle_act_mult_game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n.send("DISCONNECTED")
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                halt = 1
                cur_screen.listener.stop()
                n.send("DISCONNECTED")

        if game == None:
            cur_screen.play_sound("game_halted")
            print("C")
            cur_screen.new_screen = battle_game_results.BattleResults(
                str(0), str(0), player
            )
            cur_screen = cur_screen.new_screen
            is_network_initialised = 0

        if halt == 1:
            cur_screen.play_sound("game_halted")
            print("B")
            cur_screen.new_screen = battle_game_results.BattleResults(
                str(0), str(0), player
            )
            cur_screen = cur_screen.new_screen
            is_network_initialised = 0
            halt = 0


def battle_start_listener():
    global game, cur_screen
    if game != None and cur_screen.game_type == "battle_act_mult_game":
        pygame.display.flip()
        if cur_screen.is_game_started == 0:
            cur_screen.start_game()
        if cur_screen.listener.is_listening():
            cur_screen.listener.handle_events()


def battle_connected():
    global game, cur_screen, n, player
    if game != None and cur_screen.game_type == "battle_waiting":
        if game != None and game.connected():
            if game.conn1 == n.client_number:
                player = 0
            else:
                player = 1
            print("player: ", player)
            print("both connected to server successfully")
            cur_screen.asset_man.sounds["waiting"].stop()
            cur_screen.play_sound("connected")
            time.sleep(2)
            cur_screen.new_screen = battle_play.Battle_play(int(player))
            pygame.mixer.music.pause()
            cur_screen = cur_screen.new_screen
            print("both connected to server successfully and server is okay")


def battle_score_sender():
    global game, cur_screen, player, n
    if (
        (game != None)
        and (cur_screen.game_type != None)
        and (cur_screen.game_type == "battle_listen_mult_game")
    ):
        pygame.display.flip()
        if cur_screen.is_game_started == 0:
            cur_screen.start_game()
        if cur_screen.game_screen.is_running():
            cur_screen.game_screen.handle_events()
        if player == 0:
            if not game.p1Went:
                if not cur_screen.game_screen.is_running():
                    score = cur_screen.game_screen.stop()
                    print("score sent by 1", score)
                    n.send(str(score))
        else:
            if not game.p2Went:
                if not cur_screen.game_screen.is_running():
                    score = cur_screen.game_screen.stop()
                    print("score sent by 2", score)
                    n.send(str(score))


def send_array_to_server():
    global game, cur_screen, player, n
    if game != None and cur_screen.game_type == "battle_act_mult_game":
        if player == 0:
            if not game.p1_ready_to_go_forward:
                if not cur_screen.listener.is_listening():
                    arr = cur_screen.listener.stop()
                    barr = pickle.dumps(arr)
                    n.send_bin(barr)
                    print(pickle.loads(barr))
        else:
            if not game.p2_ready_to_go_forward:
                if not cur_screen.listener.is_listening():
                    arr = cur_screen.listener.stop()
                    barr = pickle.dumps(arr)
                    n.send_bin(barr)
                    print(pickle.loads(barr))


def switch_play_to_listen():
    global game, cur_screen, player
    if game != None and cur_screen.game_type == "battle_act_mult_game":
        if game.p1_ready_to_go_forward and game.p2_ready_to_go_forward:
            song_1 = game.song_array[1]
            song_2 = game.song_array[0]
            if player == 0:
                cur_screen.new_screen = battle_listen.Battle_listen(int(player), song_1)
            else:
                cur_screen.new_screen = battle_listen.Battle_listen(int(player), song_2)
            pygame.mixer.music.pause()
            cur_screen = cur_screen.new_screen
            cur_screen.play_sound("play_to_listen")
            time.sleep(2)
            pygame.display.flip()


def battle_round_over():
    global game, cur_screen, n, round, player, is_network_initialised
    if (
        game != None
        and (cur_screen.game_type != None)
        and (cur_screen.game_type == "battle_listen_mult_game")
    ):
        if game.p1Went and game.p2Went:
            try:
                n.send("round_finished")
            except Exception as e:
                print(e)
            round += 1

            if round > 1:
                score1 = game.moves[0]
                score2 = game.moves[1]
                print("A")
                cur_screen.new_screen = battle_game_results.BattleResults(
                    str(score1), str(score2), player
                )
                cur_screen = cur_screen.new_screen
                is_network_initialised = 0
            else:
                cur_screen.play_sound("round_over")
                time.sleep(1.5)
                cur_screen.new_screen = battle_play.Battle_play(player)
                pygame.mixer.music.pause()
                cur_screen = cur_screen.new_screen
                n.send("reset")
                game = n.send("get")


def battle_game():
    battle_waiting_check()
    battle_results_none_check()
    battle_halted_check()
    battle_listen_halted()
    battle_playing_halted()
    battle_start_listener()
    battle_connected()
    battle_score_sender()
    send_array_to_server()
    switch_play_to_listen()
    battle_round_over()


while running:

    running = cur_screen.handle_events(pygame.event.get())
    cur_screen.update()
    cur_screen.render(window)

    if cur_screen.switch_screen:
        cur_screen = cur_screen.new_screen

    pitch_game_check()
    practice_game_check()
    songs_game_check()
    if (cur_screen.game_type != None) and (cur_screen.game_type[:6] == "versus"):
        try:
            if is_network_initialised == 0:
                versus_initialise_network()
            game = n.send("get")

        except Exception as e:
            versus_server_down()
            continue

        versus_game()

    if (cur_screen.game_type != None) and (cur_screen.game_type[:6] == "battle"):
        try:
            if is_network_initialised == 0:
                battle_initialise_newtork()
            try:
                game = n.send("get")
            except Exception as e:
                game = None
        except Exception as e:
            battle_server_down()
            continue

        battle_game()

    pygame.display.flip()

pygame.quit()
# B F A
