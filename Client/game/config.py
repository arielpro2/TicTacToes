class Request:
    CREATE_ROOM: int = 0
    JOIN_ROOM: int = 1


class UserOptions:
    JOIN_ROOM: chr = 'J'
    CREATE_ROOM: chr = 'C'


class Game:
    FPS: int = 60
    SCREEN_WIDTH: int = 900
    SCREEN_HEIGHT: int = 900

    EMPTY_CELL: int = 0


class Colors:
    BLACK: tuple = (0, 0, 0)
    WHITE: tuple = (255, 255, 255)

    CELL_BORDER_COLOR: tuple = WHITE
    BACKGROUND_COLOR: tuple = BLACK
