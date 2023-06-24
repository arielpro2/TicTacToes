import sys

from Client.entities.game import Game
from Client.game.board import Board
from Client.networking.room_utils import connect_to_server, join_or_create_room_input, send_place_cell_request, \
    enter_room_request, create_room_request
from Client.game import config as Const


class TicTacToe(Game):
    """
    TicTacToe class: definition of TicTacToe game
    """
    def __init__(self) -> None:
        """
        Initializer for game, here we init the Screen, Clock and Board
        """
        self.screen = pygame.display.set_mode((Const.Game.SCREEN_WIDTH, Const.Game.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = Board(10)

    def start_game(self) -> None:
        """
        running when the game first run
        """
        player_id: str = connect_to_server()

        user_choice = join_or_create_room_input()

        if user_choice == Const.UserOptions.JOIN_ROOM:
            room_id = input("Enter room id:\n")
            enter_room_request(room_id)

        elif user_choice == Const.UserOptions.CREATE_ROOM:
            room_id = create_room_request()
            input("Press Enter to Start the game!")

        pygame.init()

    def loop(self) -> None:
        """
        The game loop: running in a loop when the game is running
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x_index_on_board = mouse_x // self.board.block_size
                y_index_on_board = mouse_y // self.board.block_size

                send_place_cell_request((x_index_on_board, y_index_on_board))
        # Update.

        # Draw.
        self.screen.fill(Const.Colors.BACKGROUND_COLOR)
        self.board.draw_grid(self.screen)

        pygame.display.update()
        self.clock.tick(Const.Game.FPS)
