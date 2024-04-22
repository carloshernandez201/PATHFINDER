import random
import sys
import pygame
import time
import copy
from queue import PriorityQueue

WIDTH = 1728
HEIGHT = 972
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Create a window with specified dimensions
pygame.display.set_caption("Dijkstra and A* Path Finding Algorithms")

# Define colors used in the program
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DEEP_SKY_BLUE = (0, 191, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Water colors
DARK_GREEN = (0, 100, 0)
DARK_RED = (139, 0, 0)
DARK_PURPLE = (75, 0, 130)

# Global time variables to be used in popupwindowcode.py
time_dijkstra = 0
time_astar = 0

class Spot:
    default_color = WHITE

    def __init__(self, row, col, x_position, width, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = x_position  # Accept x position value to accommodate for multiple side-by-side grids
        self.y = row * width  # Calculate y position based on row, assuming square cells for simplicity
        self.color = self.default_color  # Default color is white
        self.neighbors = []  # List to keep track of neighboring spots
        self.width = width  # Size of each spot
        self.total_rows = total_rows  # Total rows in the grid
        self.total_cols = total_cols  # Total columns in the grid
        self.weight = 1  # Default weight is 1
        self.g_score = float("inf")
        self.f_score = float("inf")
        self.tiebreaker = -1
        self.came_from = None

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
        return self.color == BLUE

    def reset(self):
        self.color = self.default_color

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = BLUE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        row_change = [1, -1, 0, 0]
        col_change = [0, 0, 1, -1]
        # Check neighbors in the grid (down, up, left, right)
        for i in range(4):
            neighbor_row = self.row + row_change[i]
            neighbor_col = self.col + col_change[i]
            if self.is_valid_spot(neighbor_row, neighbor_col) and not grid[neighbor_row][neighbor_col].is_barrier():
                self.neighbors.append(grid[neighbor_row][neighbor_col])

    def is_valid_spot(self, row, col):
        return 0 <= row < self.total_rows and 0 <= col < self.total_cols

    def get_weight(self):
        return self.weight

    def __lt__(self, other):
        if self.f_score == other.f_score:
            return self.tiebreaker < other.tiebreaker
        return self.f_score < other.f_score


class WaterSpot(Spot):
    default_color = DEEP_SKY_BLUE

    def __init__(self, row, col, x_position, width, total_rows, total_cols):
        super().__init__(row, col, x_position, width, total_rows, total_cols)
        self.color = self.default_color
        self.weight = 5

    def make_closed(self):
        self.color = DARK_RED

    def make_open(self):
        self.color = DARK_GREEN

    def make_path(self):
        self.color = DARK_PURPLE


def make_grid(rows, cols, width, height, water_enabled):
    rand_max = 0
    if water_enabled:
        rand_max = 1
    grid = []
    gap = min(width // cols, height // rows)
    for i in range(rows):
        grid.append([])
        for j in range(cols):  # Use cols for the inner loop
            x_position = j * gap
            if random.randint(0, rand_max) == 1:
                spot = WaterSpot(i, j, x_position, gap, rows, cols)
            else:
                spot = Spot(i, j, x_position, gap, rows, cols)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, cols, partial_width, height, x_offset):
    gap = min(partial_width // cols, height // rows)
    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (x_offset, i * gap), (x_offset + partial_width, i * gap))
    for j in range(cols + 1):
        pygame.draw.line(win, GREY, (x_offset + j * gap, 0), (x_offset + j * gap, height))


def draw(win, grid_list, rows, cols, partial_width, height):
    win.fill(WHITE)
    for grid_index, grid in enumerate(grid_list):
        x_offset = grid_index * partial_width
        for row in grid:
            for spot in row:
                # Draw each spot with the correct x_offset
                spot.draw(win)
        draw_grid(win, rows, cols, partial_width, height, x_offset)  # This might need to be adapted if grids overlap
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
    return abs(a1 - a2) + abs(b1 - b2)


def astar(draw, start, end):
    # Note that A* and Dijkstra are mostly the same except the priority queue ranks based on f score, not weight cost
    # from start
    return pathfind(draw, start, end, dist)


def dijkstra(draw, start, end):
    return pathfind(draw, start, end, lambda spot1, spot2: 0)


def pathfind(draw, start, end, heuristic):
    count = 0  # When the f scores are equal, the priority queue will utilize this count variable for comparisons
    open_set = PriorityQueue()
    open_set.put(start)  # The less than comparison for two spots is based on f score
    start.g_score = 0  # g score refers to weight cost from start tile
    start.f_score = heuristic(start, end)
    start.tiebreaker = count

    visited = set()  # Set to track visited nodes

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Reset to the initial start screen when backspace is pressed
                    return False

        # Take the minimum f score tile from the current priority queue
        current = open_set.get()
        visited.add(current)

        if current == end:
            print(current.g_score)
            reconstruct_path(current, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                # Water tiles that are the destination have a greater weight cost to travel to
                temp_g_score = current.g_score + neighbor.get_weight()

                if temp_g_score < neighbor.g_score:
                    neighbor.came_from = current
                    neighbor.g_score = temp_g_score
                    neighbor.f_score = neighbor.g_score + heuristic(neighbor, end)
                    neighbor.tiebreaker = count
                    count += 1
                    open_set.put(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def reconstruct_path(current, draw):
    current = current.came_from
    while current is not None:
        current.make_path()
        draw()
        current = current.came_from


def set_neighbors(grid):
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)


def update_grid_x_positions(grid, offset):
    for row in grid:
        for spot in row:
            spot.x += offset


def run_ye(win, width, height, ROWS, COLS, barriers, water, num_grids):
    grid_list = []
    partial_width = width // num_grids
    min_rand_int = min(ROWS, COLS) // 3
    starts = []
    ends = []

    end_tile_row = random.randint(min_rand_int, ROWS - 1)
    end_tile_col = random.randint(min_rand_int, COLS - 1)

    # Create the original grid
    core_grid = make_grid(ROWS, COLS, partial_width, height, water)

    # Use deepcopy to create independent copies of the grid for each board
    for i in range(num_grids):
        x_offset = i * partial_width
        copied_grid = copy.deepcopy(core_grid)
        grid_list.append(copied_grid)
        update_grid_x_positions(grid_list[i], x_offset)

        start = grid_list[i][0][0]  # Top-left corner
        start.make_start()
        end = grid_list[i][end_tile_row][end_tile_col]
        end.make_end()

        starts.append(start)
        ends.append(end)

    if barriers:
        for i in range(0, ROWS):
            for j in range(0, COLS):
                if random.randint(0, 3) == 1 and not grid_list[0][i][j].is_end() and (i != j or i != 0):
                    for grid in grid_list:
                        grid[i][j].make_barrier()

    run = True
    while run:
        draw(win, grid_list, ROWS, COLS, partial_width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, COLS, width, height)
                print(str(get_clicked_pos(pos, ROWS, COLS, WIDTH, HEIGHT)))
                if not (row >= ROWS or col >= COLS or row < 0 or col < 0):
                    print("A")
                    spot = grid_list[0][row][col]
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
                print(str(get_clicked_pos(pos, ROWS, COLS, WIDTH, HEIGHT)))
                if not (row >= ROWS or col >= COLS or row < 0 or col < 0):
                    spot = grid_list[0][row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and start and end:
                    if num_grids == 1:
                        set_neighbors(grid_list[0])
                        astar(lambda: draw(win, grid_list, ROWS, COLS, partial_width, height), starts[0], ends[0])
                    else:  # Time it if there are 2 grids
                        global time_astar
                        start_time = time.perf_counter()
                        set_neighbors(grid_list[0])
                        astar(lambda: draw(win, grid_list, ROWS, COLS, partial_width, height), starts[0], ends[0])
                        end_time = time.perf_counter()
                        time_astar = end_time - start_time
                if event.key == pygame.K_2 and start and end:
                    if num_grids == 1:
                        set_neighbors(grid_list[0])
                        dijkstra(lambda: draw(win, grid_list, ROWS, COLS, partial_width, height), starts[0], ends[0])
                    else:
                        global time_dijkstra
                        start_time = time.perf_counter()
                        set_neighbors(grid_list[1])
                        dijkstra(lambda: draw(win, grid_list, ROWS, COLS, partial_width, height), starts[1], ends[1])
                        end_time = time.perf_counter()
                        time_dijkstra = end_time - start_time
                if event.key == pygame.K_BACKSPACE:
                    # Reset to the initial start screen when backspace is pressed
                    run = False
