import pygame

from Client.entities.game import Game
from Client.game.board import Board
from Client.game.events_handler import GameEvents
from Client.game.ui_handler import UI
from Client.game import config as Const
from Client.networking.client import Client


class TicTacToe(Game):
    """
    TicTacToe class: definition of TicTacToe game
    """

    def __init__(self, client: Client) -> None:
        """
        Initializer for game, here we init the Screen, Clock and Board
        """
        self.screen = pygame.display.set_mode(
            (Const.Game.SCREEN_WIDTH, Const.Game.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.board = Board(10)
        self.client = client

    def start_game(self) -> None:
        """
        running when the game first run
        """
        # Initializing Game UI
        UI.init()

    def loop(self) -> str:
        """
        The game loop: running in a loop when the game is running
        """
        # Handle Events
        err = GameEvents.handle(self.board, self.client)

        # if returned err is TERMINATE event
        if err == Const.Events.TERMINATE:
            return Const.Events.TERMINATE

        # Draw screen
        UI.update(self.screen, self.board)

        # Update clock
        self.clock.tick(Const.Game.FPS)
