import types
import TicTacToes.game_api as game_api

GAME_CALLBACKS = {name: func for name, func in game_api.__dict__.items() if isinstance(func, types.FunctionType)}
GAME_CALLBACKS.pop('generate_response')
GAME_CALLBACKS.pop('check_input')
GAME_CALLBACKS.pop('wraps')
GAME_CALLBACKS.pop('dataclass')
GAME_CALLBACKS.pop('field')

