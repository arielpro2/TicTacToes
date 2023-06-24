import re

from Client.game import config as Const
from Client.networking.client import Client


class Menu:
    _RE_IPV4 = re.compile(r"""^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$""")

    @classmethod
    def handle(cls, client: Client) -> None:
        cls._handle_server(client)
        cls._handle_room(client)

    @classmethod
    def _handle_room(cls, client: Client):
        user_choice: str = cls._room_menu_choice()

        if user_choice == Const.UserOptions.JOIN_ROOM:
            client.room_id = input("Enter room id:\n")
            client.enter_room()

        elif user_choice == Const.UserOptions.CREATE_ROOM:
            client.room_id = client.create_room()
            input("Press Enter to Start the game!")

    @classmethod
    def _handle_server(cls, client: Client):
        client.server_ip = cls._server_menu_choice()

    @classmethod
    def _server_menu_choice(cls) -> str:
        user_choice = ""
        while not cls._RE_IPV4.match(user_choice):
            user_choice = input(
                f"Enter Server IP. default - {Const.Request.DEFAULT_SERVER_IP}: "
            ).upper()
        return user_choice

    @staticmethod
    def _room_menu_choice() -> str:
        user_choice = ""
        while user_choice not in [
            Const.UserOptions.JOIN_ROOM,
            Const.UserOptions.CREATE_ROOM,
        ]:
            user_choice = input(
                f"Join room ({Const.UserOptions.JOIN_ROOM}) or Create room ({Const.UserOptions.CREATE_ROOM}): "
            ).upper()
        return user_choice
