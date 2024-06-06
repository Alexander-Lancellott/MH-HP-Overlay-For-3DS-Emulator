import os
import re
import sys
import time
import signal
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
    INT = "int"
    HEX = "hex"


def clear_screen():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


def rgba_int(rgb_int, alpha=100):
    return f"rgba{rgb_int // 256 // 256 % 256, rgb_int // 256 % 256, rgb_int % 256, alpha / 100}"


def read(address: int, size=4, result_type: ResultType = ResultType.INT):
    value = c.read_memory(address, size)
    value = int.from_bytes(value, byteorder="little")
    if result_type == ResultType.HEX:
        value = hex(value)[2:].upper()

    return value


def absolute_path(path: str = ""):
    return os.path.abspath(path).replace("\\modules", "")


def end():
    time.sleep(8)
    sys.exit()


def prevent_keyboard_exit_error():
    def handler(signum, frame):
        sys.exit()

    return signal.signal(signal.SIGINT, handler)


class TextColor:
    @staticmethod
    def green(text):
        return f"{green}{text}{reset}"

    @staticmethod
    def yellow(text):
        return f"{yellow}{text}{reset}"

    @staticmethod
    def red(text):
        return f"{red}{text}{reset}"


def header():
    tprint("MH HP Overlay\n", font="tarty1")
    exit_hotkey = TextColor.yellow("Ctrl + C")
    print(f"Exit with {exit_hotkey} or close the application.\n")


def current_game(win_title):
    if re.search("3 ULTIMATE", win_title) or re.search("3U", win_title):
        return "MH3U"
    if re.search("3 \\(tri-\\) G", win_title):
        return "MH3G"
    if re.search("4 ULTIMATE", win_title) or re.search("4U", win_title):
        return "MH4U"
    elif re.search("4G", win_title):
        return "MH4G"
    elif re.search("XX", win_title):
        return "MHXX"


def check_connection():
    if c.is_connected():
        try:
            test = c.read_memory(0x100000, 4)
            return type(test) is bytes and test != b"\x04\xf0\x1f\xe5"
        except (Exception,):
            print(TextColor.red("\nFailed to connect to Citra RPC Server"))
            end()
