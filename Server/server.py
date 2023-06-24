import json
import socket
import socketserver
import uuid
from json import JSONDecodeError
from typing import Dict

import coloredlogs
import logging

from TicTacToes import GAME_CALLBACKS

coloredlogs.install()

PACKET_LENGTH_SIZE = 4
CLIENTS = {}


class TCPGameServer(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def __init__(self, request, client_address, server):
        logging.info(f"client {request.getpeername()[0]} connected")
        self.player_id = str(uuid.uuid4())
        self._send_packet({'player_id': self.player_id}, request)
        CLIENTS[self.player_id] = request

        super().__init__(request, client_address, server)

    @staticmethod
    def _send_packet(data: dict, client: socket.socket):
        data = json.dumps(data).encode()
        client.send(len(data).to_bytes(PACKET_LENGTH_SIZE, byteorder='little'))
        client.send(data)

    @staticmethod
    def _recv_packet(client: socket.socket) -> dict:
        packet_length = client.recv(PACKET_LENGTH_SIZE)
        if not packet_length:
            return {}
        data = client.recv(int.from_bytes(packet_length, byteorder='little'))
        if not data:
            return {}
        return json.loads(data.decode().strip())

    def handle(self):
        while True:
            parsed_data = self._recv_packet(self.request)
            self._process_request(parsed_data)

    def _process_request(self, data: Dict):
        action = data.pop('action', None)
        clients_to_send = []
        if f"__{action}" in GAME_CALLBACKS and 'player_id' in data and data['player_id'] in CLIENTS:
            response, clients_to_send = GAME_CALLBACKS[f"__{action}"](**data)
            response['action'] = action
        else:
            data['action'] = action
            response = data
            response['status'] = 'invalid_request'

        self._send_packet(response, self.request)
        for client in clients_to_send:
            if client in CLIENTS:
                self._send_packet(response, CLIENTS[client])


if __name__ == "__main__":
    HOST, PORT = input("Enter ip address:"), int(input("Enter port:"))

    # Create the server, binding to host and port
    with socketserver.ThreadingTCPServer((HOST, PORT), TCPGameServer) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
