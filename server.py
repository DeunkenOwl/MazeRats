import socket
from _thread import *
import pickle

import numpy as np

from game import Game

server = "10.0.33.189"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_server(gameId, playerCount):
    global idCount
    # sending id to player
    # conn.send(str.encode(str(playerId)))
    # sending game settings
    # conn.send((pickle.dumps(games[gameId].maze.shape)))
    # sending start position
    # conn.send((pickle.dumps(games[gameId].ratsPos[playerId])))
    run = True
    action = np.array(("", ""))
    while run:
        for playerId in games[gameId].playerId:
            conn = games[gameId].connected[playerId]
            response = "N"
            try:
                data = pickle.loads(conn.recv(2048*2))
            except:
                print("Can't get action from client!")
                run = False
                break
            if gameId in games:
                # checks if player already went
                if not games[gameId].pWent[playerId]:
                    if data != "W":
                        ratPos = games[gameId].ratsPos[playerId]
                        tile = -1
                        if data == "U":
                            tile = games[gameId].maze.layout[ratPos[0] - 1, ratPos[1]]
                        elif data == "D":
                            tile = games[gameId].maze.layout[ratPos[0] + 1, ratPos[1]]
                        elif data == "R":
                            tile = games[gameId].maze.layout[ratPos[0], ratPos[1] + 1]
                        elif data == "L":
                            tile = games[gameId].maze.layout[ratPos[0], ratPos[1] - 1]
                        # if rat tries to move to empty space
                        if tile == 0:
                            # print("here1")
                            games[gameId].move(playerId, data)
                            # print("here2")
                            action[playerId] = data
                        # if rat tries to move inside wall
                        # O - occupied
                        elif tile == 1:
                            action[playerId] = "O"
                        elif tile == 2:
                            action[playerId] = "E"
                            games[gameId].winners[playerId] = True
                        else:
                            print("ERROR in maze")
                            run = False
                            break
                        games[gameId].pWent[playerId] = True
                else:
                    response = "W"
                conn.send((pickle.dumps(response)))
            else:
                print("Game vanished!")
                run = False
                break

        if all(games[gameId].pWent):
            games[gameId].reset_turn()
            if not any(games[gameId].winners):
                try:
                    for playerId in games[gameId].playerId:
                        conn = games[gameId].connected[playerId]
                        pickle.loads(conn.recv(2048 * 2))
                        conn.send((pickle.dumps(action[playerId])))
                except:
                    print("Failed to send turn action")
                    run = False
                    break
            else:
                # if anybody wins
                run = False
                try:
                    for playerId in games[gameId].playerId:
                        conn = games[gameId].connected[playerId]
                        pickle.loads(conn.recv(2048 * 2))
                        if games[gameId].winners[playerId]:
                            conn.send((pickle.dumps("E")))
                        else:
                            conn.send((pickle.dumps("GG")))
                        conn.sendall((pickle.dumps(games[gameId].winners)))
                        pickle.loads(conn.recv(2048 * 2))
                        # print(games[gameId].maze.layout)
                        conn.sendall((pickle.dumps(games[gameId].maze.layout)))

                except:
                    print("Failed to send final action")
                    run = False
                    break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 2
    conn.close()




def send_base_info(playerId, gameId):
    conn = games[gameId].connected[playerId]
    conn.send(str.encode(str(playerId)))
    conn.send((pickle.dumps(games[gameId].maze.shape)))
    conn.send((pickle.dumps(games[gameId].ratsPos[playerId])))

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    playerId = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        playerId = 1

    games[gameId].connected[playerId] = conn
    send_base_info(playerId, gameId)
    if games[gameId].ready:
        start_new_thread(threaded_server, (gameId, 2))