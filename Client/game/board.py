from Client.game import config as Const

import pygame


class Board:
    def __init__(self, n) -> None:
        self.n = n
        self.board = [[Const.Game.EMPTY_CELL for _ in range(n)] for _ in range(n)]
        self.characters = []

        self.block_size = (
            Const.Game.SCREEN_WIDTH // self.n
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

    def draw_character(self, cell, y, x) -> None:
        image = self.characters[cell]
        # TODO: implement
        pass
