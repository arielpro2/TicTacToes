from abc import abstractmethod

from Client.game_manager import config as Const


class Game:
    """
    Game Class: defines how the game_manager behaves
    """

    def run_game(self) -> None:
        """
        Running the game_manager: *Blocking Function*
        """
        self.start_game()
        self._start_loop()

    @abstractmethod
    def start_game(self) -> None:
        """
        Main Thread of the game_manager, start running when the game_manager first run. please implement
        """
        pass

    def _start_loop(self) -> None:
        """
        Running the game_manager loop: *Blocking Function*
        """
        while True:
            res = self.loop()
            if res == Const.Events.TERMINATE:
                return

    @abstractmethod
    def loop(self) -> str:
        """
        Main game_manager loop, running in a loop after the game_manager first run. please implement
        """
        pass
