from Client.game import config as Const


def send_place_cell_request(position: (int, int)) -> None:
    x, y = position


def connect_to_server() -> str:
    pass


def enter_room_request(room_id):
    pass


def create_room_request() -> str:
    pass


def join_or_create_room_input():
    user_choice = input(
        f"Join room ({Const.UserOptions.JOIN_ROOM}) or Create room ({Const.UserOptions.CREATE_ROOM}):\n"
    ).upper()
    while user_choice not in Const.UserOptions.JOIN_ROOM + Const.UserOptions.CREATE_ROOM:
        print(
            f"Enter {Const.UserOptions.JOIN_ROOM} to join a room, or enter {Const.UserOptions.CREATE_ROOM} to create a room.")
        user_choice = input().upper()
    return user_choice
