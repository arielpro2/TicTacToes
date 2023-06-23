import sys
import pygame


class Board:
    def __init__(self, n):
        self.n = n

        self.block_size = SCREEN_WIDTH // self.n  # Set the size of the grid block (in pixels)

    def draw(self, screen):

        for x in range(1, SCREEN_WIDTH // self.block_size):
            pygame.draw.line(screen, CELL_BORDER_COLOR, (x * self.block_size, 0), (x * self.block_size, SCREEN_HEIGHT))

        for y in range(1, SCREEN_HEIGHT // self.block_size):
            pygame.draw.line(screen, CELL_BORDER_COLOR, (0, y*self.block_size), (SCREEN_WIDTH, y * self.block_size))

# CONSTANTS
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900
# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CELL_BORDER_COLOR = WHITE
BACKGROUND_COLOR = BLACK



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    board = Board(3)
    # Game loop.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update.

        # Draw.
        screen.fill(BACKGROUND_COLOR)
        board.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
