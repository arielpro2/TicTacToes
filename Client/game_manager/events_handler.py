import pygame

from Client.GUI.board import Board
from Client.GUI.ui_handler import UI
from Client.networking.client import Client
from Client.game_manager import config as Const


class GameEvents:
    @staticmethod
    def handle(board: Board, client: Client) -> str:
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                UI.stop()
                return Const.Events.TERMINATE

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x_index_on_board = mouse_x // board.block_size
                y_index_on_board = mouse_y // board.block_size

                client.send_place_cell((x_index_on_board, y_index_on_board))
