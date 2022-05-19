import socket
from _thread import *
import pickle
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


def threaded_client(conn, playerId, gameId):
    global idCount
    # sending id to player
    conn.send(str.encode(str(playerId)))
    # sending game settings
    conn.send((pickle.dumps(games[gameId].maze.shape)))
    # sending start position
    conn.send((pickle.dumps(games[gameId].ratsPos[playerId])))
    while True:
        try:
            data = pickle.loads(conn.recv(2048*2))
            response = "N"
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
                            print("here1")
                            games[gameId].move(playerId, data)
                            print("here2")
                            response = data
                        # if rat tries to move inside wall
                        # O - occupied
                        elif tile == 1:
                            response = "O"
                        # elif tile == 2:
                        #     response = "W"
                        #     games[gameId].
                        elif tile == -1:
                            print("Wrong code")
                        games[gameId].pWent[playerId] = True
                else:
                    response = "W"
                conn.send((pickle.dumps(response)))
            else:
                break
        except:
            break
        if all(games[gameId].pWent):
            games[gameId].reset_turn()

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



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

    start_new_thread(threaded_client, (conn, playerId, gameId))