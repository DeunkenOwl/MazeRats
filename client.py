import numpy as np
import pygame
from network import Network
import pickle
from game import Maze
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, maze, ratPos, text):
    maze.draw(win)
    pygame.draw.rect(win, maze.colors[3], maze.grid[ratPos[0]][ratPos[1]])
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
    ratPos = n.receive()
    print("Starting position is in: ", ratPos)
    # redrawWindow(win, maze)
    winners = None
    text = None
    while run:
        action = "W"
        text = ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    action = "U"
                elif event.key == pygame.K_DOWN:
                    action = "D"
                elif event.key == pygame.K_RIGHT:
                    action = "R"
                elif event.key == pygame.K_LEFT:
                    action = "L"
        try:
            # print("Sending: ", action)
            n.send(action)
        except:
            run = False
            print("Couldn't send action")
            break
        try:
            response = n.receive()
            # print("Recieving: ", response)
        except:
            run = False
            print("Couldn't get response")
            break
        # print(ratPos)
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
            if action == "U":
                maze.layout[ratPos[0] - 1][ratPos[1]] = 1
            elif action == "D":
                maze.layout[ratPos[0] + 1][ratPos[1]] = 1
            elif action == "R":
                maze.layout[ratPos[0]][ratPos[1] + 1] = 1
            elif action == "L":
                maze.layout[ratPos[0]][ratPos[1] - 1] = 1
        elif response == "E":
            redrawWindow(win, maze, ratPos, "You escaped...")
            pygame.time.delay(2000)
            run = False
        if response == "W":
            text = "Wait for opponent's turn..."
        redrawWindow(win, maze, ratPos, text)
        clock.tick(10)


# def menu_screen():
#     run = True
#     clock = pygame.time.Clock()
#
#     while run:
#         clock.tick(60)
#         win.fill((128, 128, 128))
#         font = pygame.font.SysFont("comicsans", 60)
#         text = font.render("Click to Play!", 1, (255,0,0))
#         win.blit(text, (100,200))
#         pygame.display.update()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 run = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 run = False
#
#     main()
#
# while True:
#     menu_screen()

main()
