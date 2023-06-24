

class Client:
    def __init__(self) -> None:
        client_id: str = self.connect_to_server()
        room_id: str = ""

    def send_place_cell(self, position: (int, int)) -> None:
        x, y = position
        # TODO: implement
        pass

    def connect_to_server(self) -> str:
        # TODO: implement
        pass

    def enter_room(self) -> None:
        # TODO: implement
        pass

    def create_room(self) -> str:
        # TODO: implement
        pass
