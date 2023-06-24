import pygame

from Client.entities.game import Game
from Client.GUI.board import Board
from Client.game_manager.events_handler import GameEvents
from Client.GUI.ui_handler import UI
from Client.game_manager import config as Const
from Client.networking.client import Client


class TicTacToe(Game):
    """
    TicTacToe class: definition of TicTacToe game_manager
    """

    def __init__(self, client: Client) -> None:
        """
        Initializer for game_manager, here we init the Screen, Clock and Board
        """
        self.screen = pygame.display.set_mode(
            (Const.Game.SCREEN_WIDTH, Const.Game.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.board = Board(Const.Game.SCREEN_SIZE)
        self.client = client

    def start_game(self) -> None:
        """
        running when the game_manager first run
        """
        UI.init()

    def loop(self) -> str:
        """
        The game_manager loop: running in a loop when the game_manager is running
        """
        err = GameEvents.handle(self.board, self.client)

        if err == Const.Events.TERMINATE:
            return Const.Events.TERMINATE

        UI.update(self.screen, self.board)

        self.clock.tick(Const.Game.FPS)
