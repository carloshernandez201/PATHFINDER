import pygame
import sys
import ye
from tkinter import *
from tkinter import messagebox

pygame.init()


WIDTH = 1728
HEIGHT = 972
FONT_BIG = pygame.font.Font(None, 40)  #BIG IS FOR HEADING, SMALL IS FOR THE BUTTON
FONT_SMALL = pygame.font.Font(None, 32)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
BUTTON_COLOR = (30, 144, 255)
HOVER_COLOR = (65, 105, 225)


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Choose Grid Size")


def draw_text(text, font, color, surface, x, y, center=True):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        current_color = self.color
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            current_color = HOVER_COLOR

        pygame.draw.rect(win, current_color, (self.x, self.y, self.width, self.height), 0, border_radius=10)

        if outline:
            pygame.draw.rect(win, outline, (self.x, self.y, self.width, self.height), 2, border_radius=10)

        if self.text != '':
            text = FONT_SMALL.render(self.text, True, WHITE)
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_hovered(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height


class ToggleButton(Button):
    def __init__(self, color, x, y, width, height, text='', enabled=False):
        super().__init__(color, x, y, width, height, text)
        self.enabled = enabled

    def draw(self, win, outline=None):
        if self.enabled:
            current_color = GREEN  # Green indicates the option is enabled
        else:
            current_color = RED  # Red indicates the option is disabled

        super().draw(win, outline=current_color)  # Draw the button with updated color

    def toggle(self):
        self.enabled = not self.enabled


def switch_to_board(grid_rows, grid_cols, barriers, water):
    WIN.fill(GRAY)
    text = f"Grid of {grid_rows} rows and {grid_cols} columns is set."
    if barriers:
        text += " Random barriers are enabled."
    if water:
        text += " Water tiles are enabled."
    draw_text(text, FONT_BIG,
              BLACK, WIN,
              WIDTH // 2,
              HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(2000)
    ye.run_ye(WIN, WIDTH, HEIGHT, grid_rows, grid_cols, barriers, water)
    initialize_start_screen(WIN)


def initialize_start_screen(win):
    global about_button, random_button, small_button, large_button, barriers_button, water_button
    about_button = Button(BUTTON_COLOR, 600, 650, 300, 100, 'About Our Program')
    random_button = Button(BUTTON_COLOR, 600, 500, 300, 100, 'Random Barriers (54x96)')
    small_button = Button(BUTTON_COLOR, 450, 300, 250, 100, 'Small (54x96)')
    large_button = Button(BUTTON_COLOR, 800, 300, 250, 100, 'Large (108x192)')
    barriers_button = ToggleButton(BUTTON_COLOR, 100, 400, 250, 100, 'Toggle Barriers')
    water_button = ToggleButton(BUTTON_COLOR, 100, 540, 250, 100, 'Toggle Water')
    win.fill(GRAY)
    draw_text('Select Grid Size', FONT_BIG, BLACK, win, WIDTH // 2, 50)


def main():
    global WIN
    running = True

    initialize_start_screen(WIN)  # Initialize the start screen for the first time

    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if random_button.is_hovered(pos):
                    switch_to_board(54, 96, True, True)
                elif small_button.is_hovered(pos):
                    switch_to_board(54, 96, barriers_button.enabled, water_button.enabled)
                elif large_button.is_hovered(pos):
                    switch_to_board(108, 192, barriers_button.enabled, water_button.enabled)
                elif about_button.is_hovered(pos):
                    messagebox.showinfo('About', 'Dijkstra\'s algorithm and A* are both pathfinding '
                                                 'algorithms used in graph traversal. Dijkstra\'s guarantees the shortest'
                                                 ' path in weighted graphs by exploring all possible paths. A* enhances'
                                                 ' Dijkstra\'s by incorporating a heuristic to estimate the cost to reach'
                                                 ' the goal, prioritizing nodes that are likely on the shortest path. '
                                                 'A* is more efficient in finding the shortest'
                                                 ' path in terms of both time and space complexity, especially in scenarios'
                                                 ' with a clear goal. \nWhen in the program, press 1 for A*,'
                                                 ' press 2 for Dijkstra, and press Backspace to return to the menu screen')
                elif barriers_button.is_hovered(pos):
                    barriers_button.toggle()
                elif water_button.is_hovered(pos):
                    water_button.toggle()

        about_button.draw(WIN)
        random_button.draw(WIN)
        small_button.draw(WIN)
        large_button.draw(WIN)
        barriers_button.draw(WIN)
        water_button.draw(WIN)

        pygame.display.update()

if __name__ == "__main__":
    main()