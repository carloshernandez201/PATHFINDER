import random

import pygame
import math
from queue import PriorityQueue
from pygame.examples import grid
WIDTH = 1728
HEIGHT = 972
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Create a window with specified dimensions
pygame.display.set_caption("A* Path Finding Algorithm")

# Define colors used in the program
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = col * width  # Calculate x position based on column
        self.y = row * width  # Calculate y position based on row, assuming square cells for simplicity
        self.color = WHITE  # Default color is white
        self.neighbors = []  # List to keep track of neighboring spots
        self.width = width  # Size of each spot
        self.total_rows = total_rows  # Total rows in the grid
        self.total_cols = total_cols  # Total columns in the grid

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        rowChange = [1, -1, 0, 0]
        colChange = [0, 0, 1, -1]
        # Check neighbors in the grid (down, up, left, right)
        for i in range(4):
            neighborRow = self.row + rowChange[i]
            neighborCol = self.col + colChange[i]
            if self.is_valid_spot(neighborRow, neighborCol) and not grid[neighborRow][neighborCol].is_barrier():
                self.neighbors.append(grid[neighborRow][neighborCol])

    def is_valid_spot(self, row, col):
        return 0 <= row < self.total_rows and 0 <= col < self.total_cols

    def __lt__(self, other):
        pass

def make_grid(rows, cols, width, height):
    grid = []
    gap = min(width // cols, height // rows)
    for i in range(rows):
        grid.append([])
        for j in range(cols):  # Use cols for the inner loop
            spot = Spot(i, j, gap, rows, cols)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, cols, width, height):
    gap = min(width // cols, height // rows)
    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))  # Draw horizontal lines
    for j in range(cols + 1):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, height))  # Draw vertical lines

def draw(win, grid, rows, cols, width, height):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, cols, width, height)
    pygame.display.update()

def get_clicked_pos(pos, rows, cols, width, height):
    gap = min(width // cols, height // rows)
    y, x = pos
    row = y // gap
    col = x // gap
    return col, row

def dist(spot1, spot2):
    a1, b1 = spot1.x, spot1.y
    a2, b2 = spot2.x, spot2.y
    return abs(a1 - a2) + abs(b1-b2)

def astar(draw, grid, start, end):
    # Note that A* and Dijkstra are mostly the same except the priority queue ranks based on f score, not dist from start
    return pathfind(draw, grid, start, end, dist)

def dijkstra(draw, grid, start, end):
    return pathfind(draw, grid, start, end, lambda spot1, spot2: 0)

def pathfind(draw, grid, start, end, heuristic):
    tiebreaker = 0  # When the first element of the tuple are equal, the priority queue will check second element
    open_set = PriorityQueue()
    open_set.put((0, tiebreaker, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}  # g score refers to distance
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}  # f = g + h
    f_score[start] = heuristic(start, end)

    visited = set()  # Set to track visited nodes

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Take the minimum distance tile from the current priority queue
        current = open_set.get()[2]
        visited.add(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                temp_g_score = g_score[current] + 1  # Assume all edges have weight 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                    tiebreaker += 1
                    open_set.put((f_score[neighbor], tiebreaker, neighbor))
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def main(win, width, height, ROWS, COLS, barriers):
    grid = make_grid(ROWS, COLS, width, height)

    start = grid[0][0]  # Top-left corner
    start.make_start()
    end = grid[random.randint(30, ROWS - 1)][random.randint(30, COLS - 1)]
    end.make_end()

    if barriers:
        for i in range(1, ROWS - 1):
            for j in range(1, COLS - 1):
                if random.randint(0, 2) == 1 and not grid[i][j].is_end():
                    grid[i][j].make_barrier()



    run = True
    while run:
        draw(win, grid, ROWS, COLS, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, COLS, width, height)
                print(str(get_clicked_pos(pos, ROWS, COLS, WIDTH, HEIGHT)))
                if not (row >= ROWS or col >= COLS or row < 0 or col < 0):
                    print("A")
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, COLS, width, height)
                print(str(get_clicked_pos(pos,ROWS,COLS,WIDTH, HEIGHT)))
                if not (row >= ROWS or col >= COLS or row < 0 or col < 0):
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    dijkstra(lambda: draw(win, grid, ROWS, COLS, width, height), grid, start, end)
                if event.key == pygame.K_1 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    astar(lambda: draw(win, grid, ROWS, COLS, width, height), grid, start, end)
                '''if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)'''

    pygame.quit()