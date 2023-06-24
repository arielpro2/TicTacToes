"""
TicTacToes game entry point module: here we create a new TicTacToe Game and call it
"""
from Client.networking.client import Client
from Client.game.game_handler import TicTacToe
from Client.game.menu import Menu


def main() -> None:
    # Creating client
    client = Client()

    while True:
        # handle Menu for connecting to room
        Menu.handle(client)

        # Creating game
        game = TicTacToe(client)

        # Running game
        game.run_game()


if __name__ == "__main__":
    main()
