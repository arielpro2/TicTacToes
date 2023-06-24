from Client.game import config as Const

import pygame


class UI:
    @staticmethod
    def update(screen, board) -> None:
        screen.fill(Const.Colors.BACKGROUND_COLOR)
        board.draw_grid(screen)
        pygame.display.update()

    @staticmethod
    def init() -> None:
        pygame.init()

    @staticmethod
    def stop() -> None:
        pygame.quit()

    @staticmethod
    def pil_image_to_surface(pil_image) -> pygame.image:
        return pygame.image.fromstring(
            pil_image.tobytes(), pil_image.size, pil_image.mode
        ).convert()
