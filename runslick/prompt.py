import tkinter
from tkinter import simpledialog
import logging as log


def _get_user_input(prompt, title):
    root = tkinter.Tk()
    root.focus_force()
    root.lower()
    result = simpledialog.askstring(title, prompt, parent=root)
    root.destroy()
    return result


class PromptManager(object):
    def __init__(self):
        self.actions = {}
        log.debug("PromptManager initialized")

    def register_action(self, magic_word, action):
        self.actions[magic_word] = action

    def run_prompt(self, prompt, title="runslick"):
        cmd = _get_user_input(prompt, title)
        if cmd in self.actions:
            self.actions[cmd]()
        elif cmd is not None:
            log.error("Unrecognized magic word: %s", cmd)

    def param_prompt(self, prompt, title="runslick"):
        return _get_user_input(prompt, title)
