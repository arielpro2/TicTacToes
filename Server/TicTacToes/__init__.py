import types

import TicTacToes.game_api as game_api

GAME_CALLBACKS = {name: func for name, func in game_api.__dict__.items() if
                  isinstance(func, types.FunctionType) and name.startswith('__')}
