import os
import re
import sys
import time
from art import *
from enum import StrEnum
from colorama import Fore
from modules.citra import Citra

green = Fore.GREEN
yellow = Fore.YELLOW
red = Fore.RED
reset = Fore.RESET

c = Citra()


class ResultType(StrEnum):
    INT = 'int'
    HEX = 'hex'


def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


def rgba_int(rgb_int, alpha=100):
    return f'rgba{rgb_int // 256 // 256 % 256, rgb_int // 256 % 256, rgb_int % 256, alpha / 100}'


def read(address: int, size=4, result_type: ResultType = ResultType.INT):
    value = c.read_memory(address, size)
    value = int.from_bytes(value, byteorder='little')
    if result_type == ResultType.HEX:
        value = hex(value)[2:].upper()

    return value


def path(file_path):
    relative_dir = os.path.dirname(file_path)
    absolute_dir = os.path.dirname(os.path.abspath(file_path))
    return absolute_dir if file_path.split('/')[0] == '..' else relative_dir


def end():
    time.sleep(2)
    sys.exit()


def header():
    tprint('MH HP Overlay\n', font='tarty1')
    print(f'Exit with {TextColor.yellow('Ctrl + C')} or close the application.\n')


class TextColor:
    @staticmethod
    def green(text):
        return f'{green}{text}{reset}'

    @staticmethod
    def yellow(text):
        return f'{yellow}{text}{reset}'

    @staticmethod
    def red(text):
        return f'{red}{text}{reset}'


def current_game(win_title):
    if re.search('4 ULTIMATE', win_title):
        return 'MH4U'
    elif re.search('4G', win_title):
        return 'MH4G'
    elif re.search('XX', win_title):
        return 'MHXX'


def check_connection():
    if c.is_connected():
        try:
            test = c.read_memory(0x100000, 4)
            return type(test) is bytes and test != b'\x04\xf0\x1f\xe5'
        except (Exception, ):
            print(TextColor.red('\nFailed to connect to Citra RPC Server'))
            end()
