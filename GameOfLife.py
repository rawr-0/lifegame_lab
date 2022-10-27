import numpy
import pygame

import Buttoned


class GameOfLife:
    def __init__(self, width: int = 1024, height: int = 1024, cell_size: int = 4, speed: int = 5):
        self.width = width
        self.height = height
        self.buttonspace = width + 200
        self.cell_size = cell_size
        self.screen_size = self.buttonspace, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed
        self.grid = None
        self.but1 = Buttoned.Button(self.screen, self.width + 30, 50, 100, 50, "start", self.go)
        self.but2 = Buttoned.Button(self.screen, self.width + 30, 200, 100, 50, "pause", self.ret)

    def draw_lines(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def go(self):
        clock = pygame.time.Clock()
        clock.tick(self.speed)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
            arr = self.check()
            self.create_grid()
            for i in arr[0]:
                self.set_life((i[0], i[1]))
            for i in arr[1]:
                self.set_dead((i[0], i[1]))
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
            self.but2.process()
            if (self.but2.alreadyPressed == True):
                self.but2.alreadyPressed = False
                return

    def ret(self):
        return

    def run(self):
        pygame.init()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.create_grid()
        running = True
        while running:
            self.but1.process()
            self.but2.process()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.set_life(event.pos)
                        self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
        pygame.quit()

    def create_grid(self):
        self.grid = numpy.zeros((self.width, self.height), dtype=int)

    def draw_grid(self):
        for i in range(0, self.width, self.cell_size):
            for o in range(0, self.height, self.cell_size):
                if self.grid[i][o] == 1:
                    pygame.draw.rect(self.screen, pygame.Color("black"), (i, o, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color("white"), (i, o, self.cell_size, self.cell_size))

    def set_life(self, pos):
        if (pos[0] <= self.height):
            pos1 = 0
            pos2 = 0
            for i in range(0, self.height + 1, self.cell_size):
                if i > pos[0]:
                    pos1 = i - self.cell_size
                    break
            for i in range(0, self.width + 1, self.cell_size):
                if i > pos[1]:
                    pos2 = i - self.cell_size
                    break
            self.grid[pos1][pos2] = 1
            print(pos1, pos2)

    def set_dead(self, pos):
        if pos[0] <= self.height:
            pos1 = 0
            pos2 = 0
            for i in range(0, self.height + 1, self.cell_size):
                if i > pos[0]:
                    pos1 = i - self.cell_size
                    break
            for i in range(0, self.width + 1, self.cell_size):
                if i > pos[1]:
                    pos2 = i - self.cell_size
                    break
            self.grid[pos1][pos2] = 0

    def check(self):
        sum = 0
        alive = []
        dead = []
        m = self.cell_size
        for i in range(0, self.width - m + 1, self.cell_size):
            for o in range(0, self.height - m + 1, self.cell_size):
                if i == 0 and o != 0 and o != self.height - m:
                    sum = self.grid[i + m][o] + self.grid[i + m][o + m] + self.grid[i + m][o - m] + self.grid[i][o + m] \
                          + self.grid[i][o - m] + self.grid[self.width - m][o] + self.grid[self.width - m][o + m] + \
                          self.grid[self.width - m][o - m]
                if i == self.width - m and o != self.height - m and o != 0:
                    sum = self.grid[0][o] + self.grid[0][o + m] + self.grid[0][o - m] + self.grid[i][o + m] \
                          + self.grid[i][o - m] + self.grid[i - m][o] + self.grid[i - m][o + m] + \
                          self.grid[i - m][o - m]
                if i != self.width - m and i != 0 and o == self.height - m:
                    sum = self.grid[i + m][o] + self.grid[i + m][0] + self.grid[i + m][o - m] + self.grid[i][0] \
                          + self.grid[i][o - m] + self.grid[i - m][o] + self.grid[i - m][0] + \
                          self.grid[i - m][o - m]
                if i == 0 and o == self.height - m:
                    sum = self.grid[i + m][o] + self.grid[i + m][0] + self.grid[i + m][o - m] + self.grid[i][0] \
                          + self.grid[i][o - m] + self.grid[self.width - m][o] + self.grid[self.width - m][0] + \
                          self.grid[self.width - m][o - m]
                if i == self.width - m and o == 0:
                    sum = self.grid[0][o] + self.grid[0][o + m] + self.grid[0][self.height - m] + self.grid[i][o + m] \
                          + self.grid[i][self.height - m] + self.grid[i - m][o] + self.grid[i - m][o + m] + \
                          self.grid[i - m][self.height - m]
                if i == self.width - m and o == self.height - m:
                    sum = self.grid[0][o] + self.grid[0][0] + self.grid[0][o - m] + self.grid[i][0] \
                          + self.grid[i][o - m] + self.grid[i - m][o] + self.grid[i - m][0] + \
                          self.grid[i - m][o - m]
                if i != 0 and i != self.width - m and o == 0:
                    sum = self.grid[i + m][o + m] + self.grid[i][o + m] + self.grid[i - m][o + m] + self.grid[i + m][o] \
                          + self.grid[i - m][o] + self.grid[i][self.height - m] + self.grid[i + m][self.height - m] + \
                          self.grid[i - m][self.height - m]
                if i == 0 and o == 0:
                    sum = self.grid[i + m][o] + self.grid[i + m][o + m] + self.grid[i + m][self.height - m] + \
                          self.grid[i][o + m] \
                          + self.grid[i][self.height - m] + self.grid[self.width - m][o] + self.grid[self.width - m][
                              o + m] + \
                          self.grid[self.width - m][self.height - m]
                if i != 0 and o != 0 and i != self.width - m and o != self.height - m:
                    sum = self.grid[i + m][o] + self.grid[i + m][o + m] + self.grid[i + m][o - m] + self.grid[i][o + m] \
                          + self.grid[i][o - m] + self.grid[i - m][o] + self.grid[i - m][o + m] + \
                          self.grid[i - m][o - m]
                if sum == 3:
                    alive.append((i, o))
                else:
                    if sum == 2 and self.grid[i][o] == 1:
                        alive.append((i, o))
                    else:
                        dead.append((i, o))
        return alive, dead
