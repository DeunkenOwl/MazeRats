import numpy as np
import pygame
from network import Network
import pickle
from game import Maze
pygame.font.init()

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, maze, ratPos, text):
    # maze.draw(win)
    maze.draw_textured(win)
    win.blit(maze.scaled_textures[3], maze.grid[ratPos[0]][ratPos[1]])
    # pygame.draw.rect(win, maze.colors[3], maze.grid[ratPos[0]][ratPos[1]])
    # W - wait
    if text != "":
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(text, 1, (255, 255, 255))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network("10.0.33.189", 5555)
    playerId = int(n.getId())
    print("You are player", playerId)
    mazeShape = n.receive()
    print("Maze shape:", mazeShape)
    maze = Maze(np.zeros(mazeShape, dtype=int), (width, height))
    maze.set_scaled_textures()
    ratPos = n.receive()
    print("Starting position is in: ", ratPos)
    # redrawWindow(win, maze)
    text = None
    went = False
    connectionLost = False
    oldAction = ""
    while run:
        # print("run")
        action = "W"
        text = ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN and not went:
                if event.key == pygame.K_UP:
                    action = "U"
                    oldAction = "U"
                    went = True
                elif event.key == pygame.K_DOWN:
                    action = "D"
                    oldAction = "D"
                    went = True
                elif event.key == pygame.K_RIGHT:
                    action = "R"
                    oldAction = "R"
                    went = True
                elif event.key == pygame.K_LEFT:
                    action = "L"
                    oldAction = "L"
                    went = True
        try:
            # print("Sending: ", action)
            n.send(action)
        except:
            run = False
            connectionLost = True
            print("Couldn't send action")
            break
        try:
            response = n.receive()
            # print("Recieving: ", response)
        except:
            run = False
            connectionLost = True
            print("Couldn't get response")
            break
        if response == None:
            run = False
            connectionLost = True
            print("Couldn't get response")
            break
        # print(ratPos)
        # print(oldAction)
        if response != "N" and response != "W":
            # if move is successful(space was empty)
            if response == "U":
                ratPos[0] -= 1
            elif response == "D":
                ratPos[0] += 1
            elif response == "R":
                ratPos[1] += 1
            elif response == "L":
                ratPos[1] -= 1
            elif response == "O":
                # print(oldAction)
                if oldAction == "U":
                    maze.layout[ratPos[0] - 1][ratPos[1]] = 1
                elif oldAction == "D":
                    maze.layout[ratPos[0] + 1][ratPos[1]] = 1
                elif oldAction == "R":
                    maze.layout[ratPos[0]][ratPos[1] + 1] = 1
                elif oldAction == "L":
                    maze.layout[ratPos[0]][ratPos[1] - 1] = 1
                oldAction = ""
            elif response == "E":
                if oldAction == "U":
                    maze.layout[ratPos[0] - 1][ratPos[1]] = 2
                elif oldAction == "D":
                    maze.layout[ratPos[0] + 1][ratPos[1]] = 2
                elif oldAction == "R":
                    maze.layout[ratPos[0]][ratPos[1] + 1] = 2
                elif oldAction == "L":
                    maze.layout[ratPos[0]][ratPos[1] - 1] = 2
                text = "You escaped..."
                oldAction = "E"
                run = False
            elif response == "GG":
                text = "Someone escaped..."
                run = False
            went = False
        if response == "W":
            text = "Wait for opponent's turn..."
        redrawWindow(win, maze, ratPos, text)
        clock.tick(10)
    pygame.time.delay(1000)
    if connectionLost:
        redrawWindow(win, maze, ratPos, "Connection lost!")
        print("Connection lost!")
        pygame.time.delay(2000)
    else:
        winners = n.receive()
        n.send("OK")
        maze.layout = n.receive()
        # print(maze.layout)
        text = ""
        if all(winners):
            text = "It's a tie!"
        elif winners[playerId]:
            text = "Victory!"
        else:
            text = "You lose!"
        redrawWindow(win, maze, ratPos, text)
        pygame.time.delay(5000)
    n.close()
    pygame.quit()


main()
