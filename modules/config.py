import configparser
import sys
import time
from dataclasses import dataclass

config = configparser.ConfigParser()


def save():
    with open('config.ini', 'w') as config_file:
        config.write(config_file)


def set_section(section, conf):
    if section in conf:
        return conf[section]
    else:
        conf[section] = {}
        save()
        return conf[section]


def set_option(option, section, attr, default):
    try:
        if option in section:
            return getattr(section, attr)(option)
        else:
            section[option] = default
            save()
            return getattr(section, attr)(option)
    except Exception as error:
        print(f'{option} - {error}')
        time.sleep(2)
        sys.exit()


@dataclass
class Config:
    config.read('config.ini')
    Overlay = set_section('Overlay', config)
    Layout = set_section('Layout', config)
    Colors = set_section('Colors', config)


@dataclass
class ConfigOverlay:
    show_small_monsters = set_option('show_small_monsters', Config.Overlay, 'getboolean', 'true')
    emu_window = set_option('emulator_window',  Config.Overlay, 'get', 'main')
    hotkey = set_option('hotkey',  Config.Overlay, 'get', '^!f')
    hp_update_time = set_option('hp_update_time',  Config.Overlay, 'getfloat', '1')
    font_family = set_option('font_family',  Config.Overlay, 'get', 'Consolas, monaco, monospace')
    font_weight = set_option('font_weight', Config.Overlay, 'get', 'bold')
    font_size = set_option('font_size',  Config.Overlay, 'getint', '18')


@dataclass
class ConfigLayout:
    align = set_option('align',  Config.Layout, 'getboolean', 'false')
    orientation = set_option('orientation',  Config.Layout, 'get', 'right')
    x = set_option('x',  Config.Layout, 'getfloat', '100')
    y = set_option('y',  Config.Layout, 'getfloat', '0')


@dataclass
class ConfigColors:
    text_color = set_option('text_color',  Config.Colors, 'get', 'aquamarine')
    background_color = set_option('background_color',  Config.Colors, 'get', 'darkslategray')
    text_transparency = set_option('text_transparency',  Config.Colors, 'getfloat', '100')
    background_transparency = set_option(
        'background_transparency',
        Config.Colors,
        'getfloat',
        '60'
    )
