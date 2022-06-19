__author__ = "Amirreza Eskandarani"

from pygame import display, time, draw, QUIT, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame
from math import sqrt

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

cols = 12
rows = 12

width = 600
height = 600
wr = width/cols
hr = height/rows
direction = 1

screen = display.set_mode([width, height])
display.set_caption("Maze")
clock = time.Clock()

def make_blocks(grid):
    grid[1][2].blocks = True
    grid[2][3].blocks = True
    grid[2][4].blocks = True
    grid[3][3].blocks = True
    grid[3][4].blocks = True
    grid[3][6].blocks = True
    grid[3][8].blocks = True
    grid[4][4].blocks = True
    grid[4][6].blocks = True
    grid[4][9].blocks = True
    grid[5][7].blocks = True
    grid[5][9].blocks = True
    grid[5][10].blocks = True
    grid[5][11].blocks = True
    grid[6][3].blocks = True
    grid[6][6].blocks = True
    grid[6][9].blocks = True
    grid[6][11].blocks = True
    grid[7][2].blocks = True
    grid[7][5].blocks = True
    grid[7][7].blocks = True
    grid[7][10].blocks = True
    grid[8][3].blocks = True
    grid[8][6].blocks = True
    grid[8][7].blocks = True
    grid[8][8].blocks = True
    grid[8][11].blocks = True
    grid[9][2].blocks = True
    grid[9][4].blocks = True
    grid[9][7].blocks = True
    grid[9][8].blocks = True
    grid[9][11].blocks = True
    grid[10][2].blocks = True
    grid[10][5].blocks = True
    grid[10][2].blocks = True
    grid[10][8].blocks = True
    grid[11][4].blocks = True
    grid[11][5].blocks = True
    grid[11][1].blocks = True
    grid[11][8].blocks = True
    grid[11][10].blocks = True

# make blocks around the maze
    for i in range(0, rows):
        for j in range(0, cols):
            # if grid[i][j].camefrom != goal :
            if(i == 0 or i == rows - 1 or j == 0 or j == cols - 1)   :
                grid[i][j].blocks = True
    return grid
# print all directions of players go from start to the goal point 
def print_directions(status):
    for direction in status:
        match direction:
            case 0:
                print("down")
            case 1:
                print("right")
            case 2:
                print("up")
            case 3:
                print("left")
       
    
def Astar(goal, player):

    for s in player:
        s.camefrom = []
    openset = [player[-1]]
    closedset = []
    directions = []
    while 1:
        current = min(openset, key = lambda x: x.f)
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current]
        closedset.append(current)
        for neighbor in current.neighbors:
            if neighbor not in closedset and not neighbor.blocks and neighbor not in player:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                # use euclidean distance as heuristic
                neighbor.h = sqrt((neighbor.x - goal.x) ** 2 + (neighbor.y - goal.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.camefrom = current
        if current == goal:
            break
    while current.camefrom:
        if current.x == current.camefrom.x and current.y < current.camefrom.y:
            directions.append(2)
        elif current.x == current.camefrom.x and current.y > current.camefrom.y:
            directions.append(0)
        elif current.x < current.camefrom.x and current.y == current.camefrom.y:
            directions.append(3)
        elif current.x > current.camefrom.x and current.y == current.camefrom.y:
            directions.append(1)
        current = current.camefrom

    print_directions(directions)
    # print(directions1)
    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0

    return directions



class Maze():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = []
        self.blocks = False

        # # make number of blocks with probability
        # if randint(1, 101) < 12:
        #     self.blocks = True

    def show(self, color):
        draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

# create maze
grid = [[Maze(i, j) for j in range(cols)] for i in range(rows)]

for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

# position of player
player = [grid[1][1]]

# position of goal
goal = grid[-2][-2]

# last visited cell by player
current = player[-1]

grid = make_blocks(grid)

# find path from start to goal point
directions = Astar(goal, player)


while not done:
    clock.tick(1)

    # make all places of screen cells black
    screen.fill(BLACK)
    direction = directions.pop(-1)
    if direction == 0:    # down
        player.append(grid[current.x][current.y + 1])
    elif direction == 1:  # right
        player.append(grid[current.x + 1][current.y])
    elif direction == 2:  # up
        player.append(grid[current.x][current.y - 1])
    elif direction == 3:  # left
        player.append(grid[current.x - 1][current.y])
    current = player[-1]


    if current.x == goal.x and current.y == goal.y:
        done = True

    # make visited cells of player white
    # for Maze in player:
    #     Maze.show(WHITE)

    # make blocks' cells red    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j].blocks:
                grid[i][j].show(RED)

    # make the goal cell green
    goal.show(GREEN)
    # make the last visited cell blue
    player[-1].show(BLUE)

    # update the full display Surface to the screen
    display.flip()

    # use to close program
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True