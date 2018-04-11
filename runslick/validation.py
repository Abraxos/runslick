from voluptuous import Schema, Required, Any, Optional

INCANTATION_SCHEMA = Any(str, {Required("format"): str,
                               Optional(str): Any("url")})

CONFIG_SCHEMA = Schema({Required("service"): {Optional("log_level"): Any('CRITICAL',
                                                                         'ERROR',
                                                                         'WARNING',
                                                                         'INFO',
                                                                         'DEBUG'),
                                              Required("hotkey"): str,
                                              Required("terminal"): str,
                                              Required("open"): str},
                        Required("magic_words"): {str: {Required("incantation"): INCANTATION_SCHEMA,
                                                        Optional("terminal"): bool,
                                                        Optional("hotkey"): str}}})
