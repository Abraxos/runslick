import logging as log
import json
import shlex
from typing import Union
from pathlib import Path
from functools import partial
from subprocess import Popen
from pynput import keyboard
import click
from voluptuous import MultipleInvalid

# Local module imports
from runslick.validation import CONFIG_SCHEMA
from runslick.hotkey import HotKeyManager
from runslick.prompt import PromptManager
from runslick.incantation import Incantation

# Global logging configuration
LOG_LEVEL = {'CRITICAL': log.CRITICAL, 'ERROR': log.ERROR, 'WARNING': log.WARNING, 'INFO': log.INFO,
             'DEBUG': log.DEBUG, 'NOTSET': log.NOTSET}
log.basicConfig(format='%(levelname)s - %(module)s.%(funcName)s - [%(asctime)s]: %(message)s')


def configure_logging(log_level: str):
    log.getLogger().setLevel(LOG_LEVEL[log_level])


def load_configuration(config_path: Path):
    log.info("Loading configuration: %s", str(config_path))
    config_data = json.load(config_path.open('r'))
    CONFIG_SCHEMA(config_data)
    log.info("Configuration loaded.")
    return config_data


def load_configuration_or_die(config_path: Path):
    """Loads configuration and validates it or exits the application."""
    try:
        return load_configuration(config_path)
    except MultipleInvalid as exc:
        log.critical("Configuration (%s) parsing error: %s", str(config_path), str(exc))
        exit(2)
    except json.JSONDecodeError as exc:
        log.critical("JSON parsing error when trying to read configuration: %s", str(config_path))
        exit(2)


def prompt(prompt_manager: PromptManager):
    log.debug("Main prompt invoked")
    result = prompt_manager.run_prompt("Run:")
    log.info("User prompt result: %s", result)


def execute(incantation: Incantation, exec_cmd, prompt_manager=None):
    log.info("Executing: %s", incantation)
    cmd = incantation.concretize(prompt_manager)
    if cmd:
        cmd = shlex.split(exec_cmd) + [cmd]
        log.info("Executing: %s", str(cmd))
        Popen(cmd)
    else:
        log.error("Could not concretize incantation: %s", incantation)


@click.command()
@click.option('--config-file', '-c', type=click.Path(exists=True, file_okay=True, dir_okay=False,
                                                     writable=False, readable=True,
                                                     resolve_path=True, allow_dash=True),
              default=str(Path.cwd() / 'config.json'), help="JSON-formatted configuration file, "
                                                            "defaults to config.json in the current"
                                                            " directory")
@click.option('--debug/--no-debug', default=False)
def main(config_file: Union[Path, str], debug: bool):
    '''A highly configurable hotkey launcher for programs based on slickrun but for Linux/Mac'''
    config_file = Path(config_file)
    if debug:
        configure_logging('DEBUG')
        log.debug("Logging level set to debug")
    config = load_configuration_or_die(config_file)
    terminal_cmd = config['service']['terminal']
    open_cmd = config['service']['open']

    log.debug("Initializing hotkey and prompt managers...")
    hkm = HotKeyManager()
    prompt_manager = PromptManager()
    # register primary hotkey to prompt for magic word
    hkm.register(config['service']['hotkey'], partial(prompt, prompt_manager))
    # register magic words as hotkeys and prompt-commands
    for magic_word, info in config["magic_words"].items():
        log.debug(magic_word, info)
        if 'terminal' in info and info['terminal'] is True:
            prompt_manager.register_action(magic_word, partial(execute,
                                                               Incantation(magic_word,
                                                                           info['incantation']),
                                                               terminal_cmd,
                                                               prompt_manager=prompt_manager))
            if 'hotkey' in info:
                hkm.register(info['hotkey'], partial(execute,
                                                     Incantation(magic_word,
                                                                 info['incantation']),
                                                     terminal_cmd,
                                                     prompt_manager=prompt_manager))
        else:
            prompt_manager.register_action(magic_word, partial(execute,
                                                               Incantation(magic_word,
                                                                           info['incantation']),
                                                               open_cmd,
                                                               prompt_manager=prompt_manager))
            if 'hotkey' in info:
                hkm.register(info['hotkey'], partial(execute,
                                                     Incantation(magic_word,
                                                                 info['incantation']),
                                                     open_cmd,
                                                     prompt_manager=prompt_manager))
    log.debug("Hotkey manager initialized, listening for shortcuts...")
    # Collect events until released
    with keyboard.Listener(on_press=hkm.on_press, on_release=hkm.on_release) as listener:
        listener.join()
