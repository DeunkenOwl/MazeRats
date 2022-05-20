import pygame
import numpy as np


class Maze:
    def __init__(self, layout=np.zeros((10, 10), dtype=int), screenSize=(500,500)):
        self.layout = layout
        self.shape = self.layout.shape
        self.grid = np.ndarray(self.shape, dtype=pygame.Rect)
        self.set_grid(screenSize)
        self.colors = np.array(((0, 0, 0), (255, 255, 0), (0, 255, 0), (255, 0, 0)))
        self.winners = np.array((False, False))

    def set_grid(self, screenSize):
        rectWidth = screenSize[0] / self.shape[0]
        rectHeight = screenSize[1] / self.shape[1]
        x = 0
        y = 0
        for i in range(self.shape[0]):
            x = 0
            for j in range(self.shape[1]):
                self.grid[i][j] = pygame.Rect((x, y, rectWidth, rectHeight))
                x += rectWidth
            y += rectHeight

    def draw(self, screen):
        # pygame.draw.rect(win, (255,0,0),(0, 0, 50, 50))
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                pygame.draw.rect(screen, self.colors[self.layout[i][j]], self.grid[i][j])


class Game:
    def __init__(self, gameId, screenSize=(500,500)):
        self.id = gameId
        self.connected = np.ndarray(2, dtype=object)
        self.playerId = np.array((0, 1))
        self.pWent = np.array((False, False))
        self.allWent = False
        self.ratsPos = np.array(((1, 2), (7, 8)))
        self.ready = False
        # 0 - free space
        # 1 - wall
        # 2 - exit
        self.maze = Maze(np.array(((1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                                   (1, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                                   (1, 0, 0, 1, 1, 0, 1, 1, 0, 1),
                                   (1, 0, 0, 2, 1, 0, 2, 1, 0, 1),
                                   (1, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                                   (1, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                                   (1, 0, 1, 0, 0, 0, 0, 1, 0, 1),
                                   (1, 0, 0, 1, 1, 1, 1, 0, 0, 1),
                                   (1, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                                   (1, 1, 1, 1, 1, 1, 1, 1, 1, 1),)))
        self.maze.set_grid(screenSize)
        self.winners = np.array((False, False))

    def reset_turn(self):
        self.pWent[0] = False
        self.pWent[1] = False

    def move(self, playerId, flag):
        # print(playerId, " starts moving ", flag)
        if flag == "U":
            self.ratsPos[playerId][0] -= 1
        elif flag == "D":
            self.ratsPos[playerId][0] += 1
        elif flag == "R":
            self.ratsPos[playerId][1] += 1
        elif flag == "L":
            self.ratsPos[playerId][1] -= 1

# width = 700
# height = 700
# win = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Client")
# win.fill((0, 0, 0))
#
# game = Game(1, (width, height))
# # game.maze.set_grid(win.get_size())
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#             pygame.quit()
#     win.fill((0, 0, 0))
#     game.maze.draw(win)
#     pygame.display.update()

