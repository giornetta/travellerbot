from typing import Callable, List, Optional, Dict, Tuple
import re


class CommandParser:
    callbacks: Dict[str, Callable]

    def __init__(self):
        self.callbacks = {}

    def execute(self, command: str, referee_id: int) -> (bool, str):
        if re.match(r'^/[\da-zA-Z+\- :]+$', command):
            cmd = list(filter(lambda s: s != '', command.split(' ')))
            cmd[0] = cmd[0][1:]  # remove the '/' character

            if cmd[0] not in self.callbacks:
                return False, 'Unrecognized command.'

            if cmd[0] == "info":
                if len(cmd) == 2:
                    return self.callbacks[cmd[0]](cmd[1], referee_id)
                else:
                    return False, 'use /info name {world|map|scene|adventure}'
            elif cmd[0] == "set":
                if len(cmd) >= 4:
                    name = cmd[1]
                    last = cmd[-1]
                    if re.match(r'^[+\-]?\d+$', last):
                        return self.callbacks[cmd[0]](name, cmd[2:-1], last, referee_id)
                    elif last.lower() in ['true', 'false']:
                        value = '1' if last.lower() == 'true' else '0'
                        return self.callbacks[cmd[0]](name, cmd[2:-1], value, referee_id)
                    elif last.lower() in ['standing', 'crouched', 'prone']:
                        return self.callbacks[cmd[0]](name, cmd[2:-1], last.lower(), referee_id)

                    return self.callbacks[cmd[0]](name, cmd[2:], '1', referee_id)
                else:
                    return False, 'use /set name ... fieldName [{+|-}][value]'
            elif cmd[0] == "shop":
                if len(cmd) >= 2:
                    return self.callbacks[cmd[0]](cmd[1:], referee_id)
                else:
                    return False, 'use /shop {[... type] technology level|close}'
            elif cmd[0] == "rest":
                if len(cmd) == 2:
                    return self.callbacks[cmd[0]](cmd[1], referee_id)
                else:
                    return False, 'use /rest {short|long}'
            elif cmd[0] == "combat":
                if len(cmd) == 2:
                    return self.callbacks[cmd[0]](cmd[1], None, referee_id)
                elif len(cmd) == 3 and cmd[2] == 'end':
                    return self.callbacks[cmd[0]](cmd[1], cmd[2], referee_id)
                else:
                    return False, 'use /combat sceneName [end]'
            elif cmd[0] == "travel":
                if len(cmd) == 2:
                    return self.callbacks[cmd[0]](cmd[1], referee_id)
                else:
                    return False, 'use /travel destination'
            elif cmd[0] == "age":
                try:
                    i = cmd.index('roll')
                    return self.callbacks[cmd[0]](cmd[1:i], cmd[i + 1:], referee_id)
                except ValueError:
                    return self.callbacks[cmd[0]]([], [], referee_id)
            elif cmd[0] == "scene":
                if len(cmd) == 2:
                    return self.callbacks[cmd[0]](cmd[1], None, referee_id)
                if len(cmd) == 3:
                    return self.callbacks[cmd[0]](cmd[1], cmd[2], referee_id)
                else:
                    return False, 'use /scene new name'
            elif cmd[0] == "exit":
                if len(cmd) == 1:
                    return self.callbacks[cmd[0]](referee_id)
                else:
                    return False, 'use /exit'
            elif cmd[0] == 'starship':
                return self.callbacks[cmd[0]](referee_id)
            else:
                return self.callbacks[cmd[0]](cmd[1:], referee_id)
        else:
            return False, 'Invalid command format.'