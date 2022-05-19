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
            response = ""
            if gameId in games:
                # checks if player already went
                if not games[gameId].pWent[playerId]:
                    if data != "W":
                        ratPos = games[gameId].ratsPos[playerId]
                        if data == "U":
                            ratPos[1] += 1
                        elif data == "D":
                            ratPos[1] -= 1
                        elif data == "R":
                            ratPos[0] += 1
                        elif data == "L":
                            ratPos[0] -= 1
                        tile = games[gameId].maze.layout[ratPos[0], ratPos[1]]
                        # if rat tries to move to empty space
                        if tile == 0:
                            games[gameId].ratsPos[playerId] = ratPos
                            # E - empty
                            response = data
                        # if rat tries to move inside wall
                        # O - occupied
                        elif tile == 1:
                            response = "O"
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