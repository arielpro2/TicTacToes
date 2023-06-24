import asyncio
import enum
import json
import logging
import socket
import threading
from threading import Thread
from typing import Callable

PACKET_SIZE = 512
CONNECTION_TRIES = 5


class GameEvent(enum.Enum):
    CONNECTION_LOST = 1
    GAME_ACTION = 2
    PLAYER_JOINED = 3
    GAME_ENDED = 4


class Status(enum.Enum):
    SUCCESS = 0
    INVALID_ARGUMENTS = 1
    ROOM_NOT_FOUND = 2
    PLAYER_NOT_FOUND = 3
    NOT_ADMIN = 4
    OUT_OF_BOUNDS = 5
    WRONG_TURN = 6
    GAME_ALREADY_STARTED = 7
    OCCUPIED_POSITION = 8


class TCPGameClient:
    def __init__(self, ip_address: str, port: int, worker_count: int = 1):
        self.players = None
        self.player_id = None
        self.room_id = None
        self.player_index = -1
        self._event_thread = None
        self._callbacks = {event: lambda _: NotImplemented for event in GameEvent}
        for i in range(CONNECTION_TRIES):
            try:
                self._server = socket.socket()
                self._server.connect((ip_address, port))
                self.player_id = self._fetch_player_id()
                break
            except Exception as e:
                print(e)
                logging.warning(f"Connection to {ip_address} failed, trying again....")

        if not self.player_id:
            logging.error(f"Connection to {ip_address} failed!")

        self._loop = asyncio.new_event_loop()
        self._event_queue = asyncio.Queue()
        self._worker_count = worker_count

    @staticmethod
    def _deserialize_data(data: bytes) -> dict:
        return json.loads(data[:data.index(b'\0')].decode())

    @staticmethod
    def _serialize_data(data: dict) -> bytes:
        return json.dumps(data).encode().ljust(PACKET_SIZE, b'\0')

    def _next_network_event(self) -> dict:
        response = self._server.recv(PACKET_SIZE)
        return self._deserialize_data(response)

    def _fetch_player_id(self):
        pid_data = self._next_network_event()
        return pid_data['player_id']

    async def _event_worker(self, queue: asyncio.Queue):
        while True:
            event_type, event_data = await queue.get()
            self._callbacks[event_type](event_data)
            queue.task_done()

    async def _network_worker(self, queue: asyncio.Queue):
        while True:
            network_event_data = None
            try:
                network_event_data = self._next_network_event()
            except socket.error:
                queue.put_nowait((GameEvent.CONNECTION_LOST, {}))
            if network_event_data:
                if 'winner' in network_event_data:
                    queue.put_nowait((GameEvent.GAME_ENDED, network_event_data))
                    self._loop.close()
                elif 'players' in network_event_data:
                    self.players = network_event_data['players']
                    queue.put_nowait((GameEvent.PLAYER_JOINED, network_event_data))
                else:
                    queue.put_nowait((GameEvent.GAME_ACTION, network_event_data))

    def _start_workers(self):
        for _ in range(self._worker_count):
            asyncio.run_coroutine_threadsafe(self._event_worker(self._event_queue), self._loop)
            asyncio.run_coroutine_threadsafe(self._network_worker(self._event_queue), self._loop)

    @staticmethod
    def _initialize_event_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def set_connection_lost_callback(self, callback: Callable):
        """
        Set the callback for connection lost event.
        callback will be called in a separate thread.

        must be called before create_room or join_room
        """
        self._callbacks[GameEvent.CONNECTION_LOST] = callback

    def set_game_action_callback(self, callback: Callable):
        """
        Set the callback for any game action event.
        callback will be called in a separate thread.

        must be called before create_room or join_room
        """
        self._callbacks[GameEvent.GAME_ACTION] = callback

    def set_game_ended_callback(self, callback: Callable):
        """
        Set the callback for game ended event.
        callback will be called in a separate thread.

        must be called before create_room or join_room
        """
        self._callbacks[GameEvent.GAME_ENDED] = callback

    def set_player_joined_callback(self, callback: Callable):
        """
        Set the callback for new player joined event.
        callback will be called in a separate thread.

        must be called before create_room or join_room
        """
        self._callbacks[GameEvent.PLAYER_JOINED] = callback

    def create_room(self) -> bool:
        """
        Attempts to create a new room.
        returns True if successful else False.
        """
        self._server.send(self._serialize_data({'action': 'create_room',
                                                'player_id': self.player_id}))
        response = self._next_network_event()
        print(response)
        if 'status' in response and response['status'] == Status.SUCCESS.value:
            self.room_id = response['room_id']
            self._event_thread = Thread(target=self._initialize_event_loop, args=(self._loop,))
            self._event_thread.start()
            self._start_workers()
            return True

        return False

    def join_room(self, room_id: str) -> bool:
        """
        Attempts to join a room.
        returns True if successful else False.
        """
        self._server.send(self._serialize_data({'action': 'join_room',
                                                'player_id': self.player_id,
                                                'room_id': room_id}))
        response = self._next_network_event()
        if 'status' in response and response['status'] == Status.SUCCESS.value:
            self.room_id = response['room_id']
            self.player_index = response['player_index']
            self.players = response['players']
            self._event_thread = Thread(target=self._initialize_event_loop, args=(self._loop,))
            self._event_thread.start()
            self._start_workers()
            return True

        return False

    def start_game(self) -> bool:
        """
        Attempts to play a move.
        returns True if successful else False.
        """
        self._server.send(
            self._serialize_data({'action': 'start_game',
                                  'player_id': self.player_id,
                                  'room_id': self.room_id}))
        response = self._next_network_event()
        if 'status' in response and response['status'] == Status.SUCCESS.value:
            return True

        return False

    def play_move(self, x: int, y: int) -> bool:
        """
        Attempts to play a move.
        returns True if successful else False.
        """
        self._server.send(
            self._serialize_data({'action': 'play_move',
                                  'player_id': self.player_id,
                                  'room_id': self.room_id,
                                  'pos_x': x,
                                  'pos_y': y}))
        response = self._next_network_event()
        if 'status' in response and response['status'] == Status.SUCCESS.value:
            return True

        return False


# Example usage
if __name__ == "__main__":
    game_client = TCPGameClient('45.76.87.120', 9999)
    print(game_client.player_id)
    if game_client.player_id:
        game_client.set_connection_lost_callback(lambda data: print("Connection lost"))
        game_client.set_game_ended_callback(lambda data: print("Game ended"))
        game_client.set_game_action_callback(lambda data: print(f"Game action {data}"))
        game_client.set_player_joined_callback(lambda data: print(f"Player joined {data}"))
        print(game_client.create_room())
        print(f"room id: {game_client.room_id}")