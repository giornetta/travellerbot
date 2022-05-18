from typing import Callable, List, Optional, Dict, Tuple
import re


class CommandParser:
    callbacks: Dict[str, Callable] = {}

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
                    return False, 'use /shop {[... type]|close}'
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
            else:
                return self.callbacks[cmd[0]](cmd[1:], referee_id)
        else:
            return False, 'Invalid command format.'

    def set_info_callback(self, callback: Callable[[str], Tuple[bool, str]]):
        self.callbacks['info'] = callback

    def set_set_callback(self, callback: Callable[[str, List[str], int], Tuple[bool, str]]):
        self.callbacks['set'] = callback

    def set_shop_callback(self, callback: Callable[[List[str]], Tuple[bool, str]]):
        self.callbacks['shop'] = callback

    def set_rest_callback(self, callback: Callable[[str], Tuple[bool, str]]):
        self.callbacks['rest'] = callback

    def set_combat_callback(self, callback: Callable[[str, Optional[str]], Tuple[bool, str]]):
        self.callbacks['combat'] = callback

    def set_travel_callback(self, callback: Callable[[str], Tuple[bool, str]]):
        self.callbacks['travel'] = callback

    def set_age_callback(self, callback: Callable[[List[str], List[str]], Tuple[bool, str]]):
        self.callbacks['age'] = callback

    def set_scene_callback(self, callback: Callable[[str, str], Tuple[bool, str]]):
        self.callbacks['scene'] = callback

    def set_exit_callback(self, callback: Callable[[], Tuple[bool, str]]):
        self.callbacks['exit'] = callback

    def __setitem__(self, key: str, callback: Callable):
        options = {
            "info": self.set_info_callback,
            "set": self.set_set_callback,
            "shop": self.set_shop_callback,
            "rest": self.set_rest_callback,
            "combat": self.set_combat_callback,
            "travel": self.set_travel_callback,
            "age": self.set_age_callback,
            "scene": self.set_scene_callback,
            "exit": self.set_exit_callback
        }
        func: Callable = options.get(key)
        if func is not None:
            func(callback)
        else:
            self.callbacks[key] = callback
