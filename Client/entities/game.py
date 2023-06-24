from abc import abstractmethod

from Client.game import config as Const


class Game:
    """
    Game Class: defines how the game behaves
    """

    def run_game(self) -> None:
        """
        Running the game: *Blocking Function*
        """
        self.start_game()
        self._start_loop()

    @abstractmethod
    def start_game(self) -> None:
        """
        Main Thread of the game, start running when the game first run. please implement
        """
        pass

    def _start_loop(self) -> None:
        """
        Running the game loop: *Blocking Function*
        """
        while True:
            res = self.loop()
            if res == Const.Events.TERMINATE:
                return

    @abstractmethod
    def loop(self) -> str:
        """
        Main game loop, running in a loop after the game first run. please implement
        """
        pass
