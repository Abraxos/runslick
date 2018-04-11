import logging as log
import shlex
from typing import Union

# local package imports
from runslick.prompt import PromptManager
from runslick.validation import INCANTATION_SCHEMA

class Incantation(object):
    def __init__(self, name, config: Union[str, dict]):
        INCANTATION_SCHEMA(config)
        self.name = name
        if isinstance(config, str):
            self.cmd = config
            self.format_str = config
            self.params = {}
        elif isinstance(config, dict):
            self.format_str = config['format']
            self.cmd = None
            self.params = {k: v for k, v in config.items() if k != 'format'}

    def concretize(self, prompt_manager: PromptManager = None):
        if self.cmd is not None:
            return self.cmd
        elif prompt_manager is not None:
            # prompt the user for input to build the command
            kwargs = {}
            for param, param_type in self.params.items():
                argument = prompt_manager.param_prompt(param, title=self.name)
                if param_type == "url":
                    argument = argument.replace(' ', '%20')
                    kwargs[param] = argument
            return self.format_str.format(**kwargs)
        log.error("No PromptManager provided, cannot fill parameters for: %s", self.format_str)
        return None

    def __repr__(self):
        if self.cmd:
            return ' '.join(self.cmd)
        return "Incantation: {} ({})".format(self.format_str, self.params)

    def __str__(self):
        return self.__repr__()
