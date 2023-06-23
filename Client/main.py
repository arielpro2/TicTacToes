import sys
import pygame
import json
import constants as Const


class Board:
    def __init__(self, n):
        self.n = n
        self.board = [[Const.Game.EMPTY_CELL for _ in range(n)] for _ in range(n)]
        self.characters = []

        self.block_size = Const.Game.SCREEN_WIDTH // self.n  # Set the size of the grid block (in pixels)

    def draw_grid(self, screen):

        for x in range(1, Const.Game.SCREEN_WIDTH // self.block_size):
            pygame.draw.line(screen, Const.Colors.CELL_BORDER_COLOR, (x * self.block_size, 0),
                             (x * self.block_size, Const.Game.SCREEN_HEIGHT))

        for y in range(1, Const.Game.SCREEN_HEIGHT // self.block_size):
            pygame.draw.line(screen, Const.Colors.CELL_BORDER_COLOR, (0, y * self.block_size),
                             (Const.Game.SCREEN_WIDTH, y * self.block_size))

    def draw_cells(self):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == Const.Game.EMPTY_CELL:
                    continue
                self.draw_character(cell, y, x)

    def draw_character(self, cell, y, x):
        image = self.characters[cell]


def pil_image_to_surface(pil_image) -> pygame.image:
    return pygame.image.fromstring(
        pil_image.tobytes(),
        pil_image.size,
        pil_image.mode
    ).convert()


def update_board_thread():
    ...


def send_place_cell_request(position: (int, int)) -> None:
    x, y = position


def connect_to_server() -> str:
    pass


def enter_room_request(room_id):
    pass


def create_room_request() -> str:
    pass


def main():
    player_id: str = connect_to_server()

    user_choice = join_or_create_room_input()

    if user_choice == Const.UserOptions.JOIN_ROOM:
        room_id = input("Enter room id:\n")
        enter_room_request(room_id)

    elif user_choice == Const.UserOptions.CREATE_ROOM:
        room_id = create_room_request()
        input("Press Enter to Start the game!")

    pygame.init()
    screen = pygame.display.set_mode((Const.Game.SCREEN_WIDTH, Const.Game.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    board = Board(10)
    # Game loop.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x_index_on_board = mouse_x // board.block_size
                y_index_on_board = mouse_y // board.block_size

                send_place_cell_request((x_index_on_board, y_index_on_board))
        # Update.

        # Draw.
        screen.fill(Const.Colors.BACKGROUND_COLOR)
        board.draw_grid(screen)

        pygame.display.update()
        clock.tick(Const.Game.FPS)


def join_or_create_room_input():
    user_choice = input(
        f"Join room ({Const.UserOptions.JOIN_ROOM}) or Create room ({Const.UserOptions.CREATE_ROOM}):\n"
    ).upper()
    while user_choice not in Const.UserOptions.JOIN_ROOM + Const.UserOptions.CREATE_ROOM:
        print(
            f"Enter {Const.UserOptions.JOIN_ROOM} to join a room, or enter {Const.UserOptions.CREATE_ROOM} to create a room.")
        user_choice = input().upper()
    return user_choice


if __name__ == '__main__':
    main()
