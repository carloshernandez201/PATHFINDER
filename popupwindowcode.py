import pygame
import sys

pygame.init()

# THIS IS STILL IN PROGRESS
WIDTH = 1500
HEIGHT = 860
FONT = pygame.font.Font(None, 32)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
BUTTON_COLOR = (0, 150, 150)

# Initialize window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Select Grid Size")


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
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
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.Font(None, 20)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False


def main():
    running = True
    small_button = Button(BUTTON_COLOR, 150, 200, 150, 50, 'Small (55x75)')
    medium_button = Button(BUTTON_COLOR, 325, 200, 150, 50, 'Medium (50x50)')
    large_button = Button(BUTTON_COLOR, 500, 200, 150, 50, 'Large (110x150)')

    while running:
        WIN.fill(GRAY)
        draw_text('Select Grid Size', FONT, BLACK, WIN, WIDTH // 2, 50)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if small_button.is_over(pos):
                    grid_size = (10, 10)
                    running = False
                elif medium_button.is_over(pos):
                    grid_size = (50, 50)
                    running = False
                elif large_button.is_over(pos):
                    grid_size = (100, 100)
                    running = False

        small_button.draw(WIN)
        medium_button.draw(WIN)
        large_button.draw(WIN)

        pygame.display.update()

    # Placeholder for further grid visualization or adjustments
    WIN.fill(GRAY)
    draw_text(f"Grid of {grid_size[0]} rows and {grid_size[1]} columns is set.", FONT, BLACK, WIN, WIDTH // 2,
              HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(3000)  # Display the setup result for a few seconds before exiting


if __name__ == "__main__":
    main()
