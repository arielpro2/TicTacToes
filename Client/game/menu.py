from Client.game import config as Const
from Client.networking.client import Client


class Menu:
    @classmethod
    def handle(cls, client: Client) -> None:
        user_choice: str = cls._menu_choice()

        if user_choice == Const.UserOptions.JOIN_ROOM:
            client.room_id = input("Enter room id:\n")
            client.enter_room()

        elif user_choice == Const.UserOptions.CREATE_ROOM:
            client.room_id = client.create_room()
            input("Press Enter to Start the game!")

    @staticmethod
    def _menu_choice() -> str:
        user_choice = ""
        while user_choice not in [Const.UserOptions.JOIN_ROOM, Const.UserOptions.CREATE_ROOM]:
            user_choice = input(
                f"Join room ({Const.UserOptions.JOIN_ROOM}) or Create room ({Const.UserOptions.CREATE_ROOM}): "
            ).upper()
        return user_choice
