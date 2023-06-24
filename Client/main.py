"""
TicTacToes game_manager entry point module: here we create a new TicTacToe Game and call it
"""
from Client.networking.client import Client
from Client.game_manager.game_handler import TicTacToe
from Client.menu.menu_handler import Menu


def main() -> None:
    # Creating client
    client = Client()

    while True:
        # handle Menu for connecting to room
        Menu.handle(client)

        # Creating game_manager
        game = TicTacToe(client)

        # Running game_manager
        game.run_game()


if __name__ == "__main__":
    main()
