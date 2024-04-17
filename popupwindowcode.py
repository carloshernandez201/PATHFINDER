import pygame
import sys

pygame.init()


WIDTH = 1500
HEIGHT = 860
FONT_BIG = pygame.font.Font(None, 40)  #BIG IS FOR HEADING, SMALL IS FOR THE BUTTON
FONT_SMALL = pygame.font.Font(None, 32)
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


def main():
    running = True
    medium_button = Button(BUTTON_COLOR, 450, 300, 250, 100, 'Small (55x75)')
    large_button = Button(BUTTON_COLOR, 800, 300, 250, 100, 'Large (110x150)')

    while running:
        WIN.fill(GRAY)
        draw_text('Select Grid Size', FONT_BIG, BLACK, WIN, WIDTH // 2, 50)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if medium_button.is_hovered(pos):
                    grid_size = (50, 50)
                    running = False
                elif large_button.is_hovered(pos):
                    grid_size = (100, 100)
                    running = False

        medium_button.draw(WIN)
        large_button.draw(WIN)

        pygame.display.update()


    WIN.fill(GRAY)
    draw_text(f"Grid of {grid_size[0]} rows and {grid_size[1]} columns is set.", FONT_BIG, BLACK, WIN, WIDTH // 2,
              HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(3000)


if __name__ == "__main__":
    main()
