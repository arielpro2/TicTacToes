class Request:
    CREATE_ROOM = 0
    JOIN_ROOM = 1

class UserOptions:
    JOIN_ROOM = 'J'
    CREATE_ROOM = 'C'

class Game:
    FPS = 60
    SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900

    BLOCK_SIZE = SCREEN_WIDTH // self.n  # Set the size of the grid block (in pixels)


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    CELL_BORDER_COLOR = WHITE
    BACKGROUND_COLOR = BLACK
