import json
from TicTacToes import GAME_CALLBACKS
import uuid
import socketserver
import coloredlogs, logging
from json import JSONDecodeError
from typing import Dict

coloredlogs.install()

PACKET_SIZE = 512
CLIENTS = {}


class TCPGameServer(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def __init__(self, request, client_address, server):
        self.player_id = str(uuid.uuid4())
        request.send(self.serialize_data({'player_id': self.player_id}))
        CLIENTS[self.player_id] = request

        super().__init__(request, client_address, server)
        logging.info(f"client {request.getpeername()[0]} connected")

    @staticmethod
    def serialize_data(data) -> bytes:
        return json.dumps(data).encode().ljust(PACKET_SIZE, b'\0')

    def handle(self):
        while True:
            data = self.request.recv(PACKET_SIZE)
            if not data:
                return

            data = data[:data.index(b'\0')].decode().strip()

            try:
                parsed_data = json.loads(data)
            except JSONDecodeError:
                logging.warning("Client sent a bad packet")
                continue

            self.process_request(parsed_data)

    def process_request(self, data: Dict):
        action = data.pop('action', None)
        clients_to_send = []
        if action in GAME_CALLBACKS and 'player_id' in data and data['player_id'] in CLIENTS:
            response, clients_to_send = GAME_CALLBACKS[action](**data)
            response['action'] = action
        else:
            data['action'] = action
            response = data
            response['status'] = 'invalid_request'

        response_bytes = self.serialize_data(response)
        self.request.send(response_bytes)
        for client in clients_to_send:
            if client in CLIENTS:
                CLIENTS[client].send(response_bytes)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), TCPGameServer) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
