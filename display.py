import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

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

    def update_neighbots(self, grid):
        print()
    def __lt__(self, other):
        print()


    def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)


class Pathfinder:
    def __init__(self, rows):
        self.WIDTH = 800
        self.window = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("A* vs Dijkstra")
        self.rows = rows
        self.gap = self.WIDTH // rows
        # sum shi may be wack in regards to are nodes swuares or rects or wtf
        self.grid = []
        self.node_length = self.WIDTH // rows
        for i in range(rows):
            self.grid.append([])
            for j in range(rows):
                spot = Node(i, j, self.gap, rows)
                self.grid[i].append(spot)


        #INITIALIZE wiNDOW SHI
    def heuristic(self, spot1, target):
        #target and spot are spots
        #bro uses manhattan distance str line should i
        row_diff = target.get_pos()[0] - spot1.get_pos()[0]
        col_diff = target.get_pos()[0]  - spot1.get_pos()[0]
        return math.sqrt(row_diff*row_diff - col_diff*col_diff)
    def draw_grid(self):
        for i in range(self.rows):
            pygame.draw.line(self.window, GRAY, (0, i * self.gap), (self.WIDTH, i * self.gap))
            for j in range(self.rows):
                pygame.draw.line(self.window, GRAY, (j * self.gap, 0), (j * self.gap, self.WIDTH))

    def draw_all(self):
            self.window.fill(WHITE)
            for row in self.grid:
                for square in row:
                    square.draw(self.window)
            self.draw_grid()
            pygame.display.update()
    def convert_clicK_to_node_location(self, click_position_y, click_position_x):
            #returns what node coordinates were clicked in ro col terms
        row_coordinate  = click_position_y // self.node_length
        col_coordinate = click_position_x // self.node_length
        return int(row_coordinate), int(col_coordinate)
