"""
TicTacToes game entry point module: here we create a new TicTacToe Game and call it
"""

from Client.game.game_handler import TicTacToe


def main() -> None:
    game = TicTacToe()
    game.run_game()


if __name__ == '__main__':
    main()
