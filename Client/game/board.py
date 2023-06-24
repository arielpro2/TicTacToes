from Client.game import config as Const

import pygame


class Board:
    def __init__(self, board_size: int) -> None:
        self.board_size = board_size
        self.board = [[Const.Game.EMPTY_CELL]*board_size]*board_size
        self.characters = []

        self.block_size = (
            Const.Game.SCREEN_WIDTH // self.board_size
        )  # Set the size of the grid block (in pixels)

    def draw_grid(self, screen) -> None:
        for x in range(1, Const.Game.SCREEN_WIDTH // self.block_size):
            pygame.draw.line(
                screen,
                Const.Colors.CELL_BORDER_COLOR,
                (x * self.block_size, 0),
                (x * self.block_size, Const.Game.SCREEN_HEIGHT),
            )

        for y in range(1, Const.Game.SCREEN_HEIGHT // self.block_size):
            pygame.draw.line(
                screen,
                Const.Colors.CELL_BORDER_COLOR,
                (0, y * self.block_size),
                (Const.Game.SCREEN_WIDTH, y * self.block_size),
            )

    def draw_cells(self) -> None:
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == Const.Game.EMPTY_CELL:
                    continue
                self.draw_character(cell, y, x)

    def draw_character(self, cell: int, y: int, x: int) -> None:
        image: list = self.characters[cell]
        # TODO: implement
        pass
