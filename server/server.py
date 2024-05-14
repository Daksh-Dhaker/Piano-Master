import socket
from _thread import *
import pickle
import threading
from game_status import GameStatus
import time
import struct

DISCONNECT_SIGNAL = "DISCONNECTED"


def send_one_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack("!I", length))
    sock.sendall(data)


def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    (length,) = struct.unpack("!I", lengthbuf)
    return recvall(sock, length)


def recvall(sock, count):
    buf = b""
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf


if __name__ == "__main__":
    flag = 0
    server = "0.0.0.0"
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((server, port))
    except socket.error as e:
        print(str(e))

    s.listen()
    print("Waiting for a connection, Server Started")

    connected = set()
    games = {}
    waiting = []
    idCount = 0

    def threaded_client(conn, p, gameId):
        global idCount
        while True:
            try:
                data = pickle.loads(recv_one_message(conn))
                if type(data) == list:
                    game.feed(p, list(data))
                    pass
                else:
                    if gameId in games:
                        game = games[gameId][0]

                        if not data:
                            break
                        else:
                            if data == "reset":
                                print("reset called")
                                game.resetWent()
                            elif data == "DISCONNECTED":
                                if games[gameId].dc:
                                    del games[gameId]
                                    # send_one_message(conn, pickle.dumps("ok"))
                                    idCount = idCount - 1
                                    conn.close()
                                else:
                                    games[gameId].dc = True
                            elif data == "round_finished":
                                game.round = game.round + 0.5
                            elif data != "get" and data != "game_mode":
                                game.play(p, data)
                    else:
                        break
                send_one_message(conn, pickle.dumps(game))
            except:
                break

        print("Lost Connection for player ", p)
        try:
            del games[gameId]
            print("Closing Game", gameId)
        except:
            pass

        idCount = idCount - 1
        conn.close()

    while True:
        conn, addr = s.accept()
        print("Connected to: ", int(addr[1]))
        idCount = idCount + 1
        flag = 0
        send_one_message(conn, pickle.dumps(int(addr[1])))
        game_mode = pickle.loads(recv_one_message(conn))
        if game_mode:
            send_one_message(conn, (pickle.dumps("ok")))
        print("game_mode: ", game_mode)

        for key, value in games.items():
            (a, b, c) = value
            if b == 1 and c == game_mode:

                flag = 1
                games[key] = (a, 2, game_mode)
                games[key][0].ready = True
                a.conn2 = int(addr[1])
                start_new_thread(threaded_client, (conn, 1, key))
                break

        if flag == 0:
            games[idCount] = (GameStatus(idCount), 1, game_mode)
            games[idCount][0].conn1 = int(addr[1])
            start_new_thread(threaded_client, (conn, 0, idCount))
