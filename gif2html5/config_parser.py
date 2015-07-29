import os
import functools
from configparser import ConfigParser
from io import StringIO


def parse_config(raw):
    config = ConfigParser(defaults={
        'GIF2HTML5_API_KEY': None,
    })
    if raw.strip().startswith('['):
        config.readfp(StringIO(raw))
    else:
        config.readfp(StringIO('\n[environment]\n' + raw))
        config.get = functools.partial(config.get, 'environment')
    return config


def get_config():
    if os.path.isfile('.env'):
        raw_config = open('.env').read()
        config = parse_config(raw_config)
    else:
        config = os.environ

    return config
