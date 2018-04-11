# runslick

A python package for simulating the functionality of [slickrun](https://bayden.com/slickrun/) on Linux and Mac OS X. Effectively a tool for rapidly running pre-configured "magic words" which can open files, programs, and URLs with input parameters.

## Setup

Install Tkinter:

```
apt-get install python3-tk
```

Clone the repo:

```
git clone git@github.com:Abraxos/runslick.git
```

Install the python package:

```
pip3 install --user -e runslick/
```

## Running

As of right now, it can only be started from the commandline, like so:

```
runslick -c examples/config.json
```

However, the intention is to provide instructions for how to run this at startup soon, so that its automatically available and responding to shortcuts as soon as you log in.

## Configuration

There are several options for configuring slickrun, most of them demonstrated in `examples/config.json`:

```
{
    "service": {
        "log_level": "DEBUG",
        "hotkey": "Alt+Q",
        "terminal": "xterm -hold -e",
        "open": "xdg-open"
    },
    "magic_words": {
        "test": {
            "incantation": "echo 'Hello, world!'",
            "terminal": true,
            "hotkey": "Alt+W"
        },
        "google": {
            "incantation": {
                "format": "https://www.google.com/search?&q={search_query}",
                "search_query": "url"
            },
            "terminal": false,
            "hotkey": "Alt+G"
        },
        "syu": {
            "incantation": "sudo apt-get dist-upgrade",
            "terminal": true
        },
        "home": {
            "incantation": "/home/eugene"
        }
    }
}

```
