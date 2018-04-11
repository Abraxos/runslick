from collections import namedtuple
import logging as log
from pynput import keyboard

KEY_MAP = {'alt': keyboard.Key.alt,
           'ctrl': keyboard.Key.ctrl,
           'shift': keyboard.Key.shift,
           'left': keyboard.Key.left,
           'right': keyboard.Key.right,
           'down': keyboard.Key.down,
           'up': keyboard.Key.up,
           'caps': keyboard.Key.caps_lock,
           'enter': keyboard.Key.enter,
           'backspace': keyboard.Key.backspace,
           'insert': keyboard.Key.insert,
           'delete': keyboard.Key.delete,
           'pgup': keyboard.Key.page_down,
           'pgdown': keyboard.Key.page_up,
           'home': keyboard.Key.home,
           'end': keyboard.Key.end,
           'cmd': keyboard.Key.cmd}


HotkeyAction = namedtuple('HotkeyAction', ['keyset', 'callback'])


def string_to_key(key_str: str):
    if key_str.lower() in KEY_MAP:
        return KEY_MAP[key_str.lower()]
    return keyboard.KeyCode.from_char(char=key_str.lower())


def string_to_combo(hotkey_str: str):
    '''Converts a string of the form Alt+Shift+Q into a set of keys'''
    return set(string_to_key(k) for k in hotkey_str.split('+'))


class HotKeyManager(object):
    def __init__(self):
        self.currently_pressed = set()
        self.actions = []

    def register(self, hotkey_str: str, callback):
        action = HotkeyAction(string_to_combo(hotkey_str), callback)
        self.actions.append(action)
        log.debug("Registered callback for [%s] -> %s", action.keyset, action.callback)
        return self

    def on_press(self, key):
        self.currently_pressed.add(key)
        log.debug("Currently pressed: %s", self.currently_pressed)
        action = next((a for a in self.actions if a.keyset == self.currently_pressed), None)
        if action:
            log.debug("Executing action: %s", str(action.callback))
            action.callback()

    def on_release(self, key):
        if key in self.currently_pressed:
            self.currently_pressed.remove(key)
