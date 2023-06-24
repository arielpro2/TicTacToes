import enum
import inspect
import random
import time
from functools import wraps
from typing import Callable, List, Dict, Union
from dataclasses import dataclass, field

MIN_ROOM_ID = 0
MAX_ROOM_ID = 9999
GAME_NOT_STARTED = 0
GAME_STARTED = 1
GAME_ENDED = 2


class Status(enum.Enum):
    SUCCESS = 0
    INVALID_ARGUMENTS = 1
    ROOM_NOT_FOUND = 2
    PLAYER_NOT_FOUND = 3
    NOT_ADMIN = 4
    OUT_OF_BOUNDS = 5
    WRONG_TURN = 6
    GAME_ALREADY_STARTED = 7


@dataclass
class GameData:
    players: List[str] = field(default_factory=list)
    player_count: int = 0
    state: int = GAME_NOT_STARTED
    turn: int = 0
    game_board: List[List[int]] = field(default_factory=lambda: [[]])


GAMES: Dict[str, GameData] = {}


def generate_response(_room_id: str, _player_id: str, _status: Status, additional_args=None):
    if additional_args is None:
        additional_args = {}
    if _status == Status.SUCCESS:
        return {'status': _status.value} | additional_args, [p for p in GAMES[_room_id].players if p != _player_id]
    return {'status': _status.value} | additional_args, list()


def check_input(func: Callable):
    @wraps(func)
    def wrapper(**kwargs):
        if set(kwargs.keys()) != set(func.__code__.co_varnames[:func.__code__.co_argcount]):
            return generate_response(str(), str(), Status.INVALID_ARGUMENTS, kwargs)
        if 'room_id' in kwargs and kwargs['room_id'] not in GAMES:
            return generate_response(str(), str(), Status.ROOM_NOT_FOUND, kwargs)

        response, clients_to_send = func(**kwargs)

        return response | kwargs, clients_to_send

    return wrapper


@check_input
def __create_room(player_id: str):
    room_id = str(random.randint(MIN_ROOM_ID, MAX_ROOM_ID)).zfill(4)
    while room_id in GAMES:
        room_id = str(random.randint(MIN_ROOM_ID, MAX_ROOM_ID)).zfill(4)

    GAMES[room_id] = GameData(players=[player_id])

    return generate_response(room_id, player_id, Status.SUCCESS, {'room_id': room_id})


@check_input
def __join_room(player_id: str, room_id: str):
    if GAMES[room_id].state == GAME_STARTED:
        return generate_response(room_id, player_id, Status.GAME_ALREADY_STARTED)
    GAMES[room_id].players.append(player_id)
    return generate_response(room_id, player_id, Status.SUCCESS, {'players': GAMES[room_id].players})


@check_input
def __start_game(player_id: str, room_id: str):
    if player_id != GAMES[room_id].players[0]:
        return generate_response(room_id, player_id, Status.NOT_ADMIN)

    GAMES[room_id].state = GAME_STARTED
    GAMES[room_id].player_count = len(GAMES[room_id].players)
    GAMES[room_id].game_board = [[] for _ in range(GAMES[room_id].player_count + 1)]

    return generate_response(room_id, player_id, Status.SUCCESS, {'shape_seed': time.time()})


def check_winner(room_id: str) -> Union[bool, int]:
    game_board = GAMES[room_id].game_board


@check_input
def __play_move(player_id: str, room_id: str, pos_x: int, pos_y: int):
    player_count = GAMES[room_id].player_count
    if player_id not in GAMES[room_id].players:
        return generate_response(room_id, player_id, Status.PLAYER_NOT_FOUND)

    player_index = GAMES[room_id].turn % player_count
    if player_index != GAMES[room_id].players.index(player_id):
        return generate_response(room_id, player_id, Status.WRONG_TURN)

    if 0 > pos_x > player_count or 0 > pos_y > player_count:
        return generate_response(room_id, player_id, Status.OUT_OF_BOUNDS)

    GAMES[room_id].game_board[pos_x][pos_y] = player_index
    GAMES[room_id].turn += 1

    additional_args = {'player_index': player_index}

    winner = check_winner(room_id)
    if winner:
        additional_args['winner'] = winner

    return generate_response(room_id, player_id, Status.SUCCESS, additional_args)
