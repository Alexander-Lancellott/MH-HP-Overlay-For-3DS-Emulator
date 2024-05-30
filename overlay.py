import re
import sys
import time
import signal
import cursor
from typing import Any
from modules.utils import TextColor, rgba_int, clear_screen, check_connection, header, current_game
from modules.mh4u_mh4g import get_4u_4g_data, Monsters4U
from modules.mhxx import get_xx_data, MonstersXX
from modules.config import ConfigOverlay, ConfigLayout, ConfigColors
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColorConstants
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QSizePolicy,
)
from ahk import AHK, Position


class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.is_borderless = False
        self.running = False
        self.is_open_window = False
        self.initial_window_state: Position = Position(0, 0, 600, 500)
        self.win_title = ''
        self.timeout = int(20 * 60) + 1  # 20 minutes
        self.counter = self.timeout
        self.timeout_start = time.time()
        self.orientation = ConfigLayout.orientation
        self.x = ConfigLayout.x
        self.y = ConfigLayout.y
        self.hotkey = ConfigOverlay.hotkey
        self.hp_update_time = round(ConfigOverlay.hp_update_time * 1000)
        self.initialize_ui()

    def initialize_ui(self):
        target_window_title = "MONSTER HUNTER (4 ULTIMATE|4G|XX)"

        if ConfigOverlay.emu_window == 'primary':
            target_window_title += ' | Primary Window'
        if ConfigOverlay.emu_window == 'secondary':
            target_window_title += ' | Secondary Window'

        target_window_title += '$'

        ahk = AHK(version='v2')
        self.setWindowTitle("Overlay")
        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet(
            f'''
            font-family: {ConfigOverlay.font_family}; 
            font-weight: {ConfigOverlay.font_weight};
            font-size: {ConfigOverlay.font_size}px;
            border-radius: 5px;
            '''
        )

        color = rgba_int(
            getattr(QColorConstants.Svg, ConfigColors.text_color).rgb(),
            ConfigColors.text_transparency
        )
        background_color = rgba_int(
            getattr(QColorConstants.Svg, ConfigColors.background_color).rgb(),
            ConfigColors.background_transparency
        )

        labels = []
        for i in range(0, 7):
            label = QLabel()
            label.setStyleSheet(
                f'''
                color: {color};
                background-color: {background_color};
                padding: 5px 10px;
                '''
            )
            if ConfigLayout.align:
                label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                if self.orientation == 'right':
                    label.setAlignment(Qt.AlignmentFlag.AlignRight)
                elif self.orientation == 'left':
                    label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                else:
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            labels.append(label)

        lm_layout = QVBoxLayout()
        lm_layout.setContentsMargins(0, 0, 0, 0)
        sm_layout = QVBoxLayout()
        sm_layout.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout(self)
        layout.addLayout(lm_layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(sm_layout)

        self.update_position(ahk, target_window_title)

        ahk.add_hotkey(self.hotkey, callback=lambda: self.toggle_borderless_screen(ahk, target_window_title))
        ahk.start_hotkeys()

        timer1 = QTimer(self)
        timer1.timeout.connect(self.wait_init_game)
        timer1.start(1000)

        timer1 = QTimer(self)
        timer1.timeout.connect(lambda: self.update_show(lm_layout, sm_layout, labels))
        timer1.start(self.hp_update_time)

        timer2 = QTimer(self)
        timer2.timeout.connect(lambda: self.update_position(ahk, target_window_title))
        timer2.start(1)

    def toggle_borderless_screen(self, ahk, target_window_title) -> Any:
        try:
            win = ahk.find_window(
                title=target_window_title,
                title_match_mode="RegEx",
            )
            monitor = self.screen().geometry()
            win.set_style("^0xC00000")
            win.set_style("^0x40000")
            if self.is_borderless:
                win.move(
                    x=self.initial_window_state.x,
                    y=self.initial_window_state.y,
                    width=self.initial_window_state.width,
                    height=self.initial_window_state.height
                )
            else:
                self.initial_window_state = win.get_position()
                win.move(
                    x=monitor.x(),
                    y=monitor.y(),
                    width=monitor.width(),
                    height=monitor.height() + 1
                )
        except (Exception,):
            pass

    def wait_init_game(self):
        if not self.is_open_window:
            if self.running:
                clear_screen()
                header()
            self.running = False
            self.hide()
            self.counter -= 1
            m, s = divmod(self.counter, 60)
            text = (
                f'{TextColor.red('No game is running.')} '
                f'Waiting {TextColor.yellow(f'{m:02d}:{s:02d}')}, then it will close.'
            )
            print(f'\r{text}',  end="",  flush=True)
            if time.time() > self.timeout_start + self.timeout:
                sys.exit()

        else:
            if not self.running:
                clear_screen()
                header()
            self.running = True
            self.counter = self.timeout
            self.timeout_start = time.time()
            game = current_game(self.win_title)
            text = f'{TextColor.green(f'{game} is running.')}'
            print(f'\r{text}', end="", flush=True)
            check_connection()

    def update_show(self, lm_layout, sm_layout, labels):
        if self.is_open_window:
            for index, label in enumerate(labels):
                large_monster = dict(name='', hp=0)
                small_monster = dict(name='', hp=0)
                is_4u = current_game(self.win_title) == 'MH4U'
                is_4g = current_game(self.win_title) == 'MH4G'
                is_xx = current_game(self.win_title) == 'MHXX'
                if is_4u or is_4g:
                    data = get_4u_4g_data(is_4u, index)
                    if data[2]:
                        large_monster = dict(name=Monsters4U.large_monsters.get(data[0]), hp=data[1])
                        small_monster = dict(name=Monsters4U.small_monsters.get(data[0]), hp=data[1])

                if is_xx:
                    data = get_xx_data(index)
                    if data[2]:
                        large_monster = dict(name=MonstersXX.large_monsters.get(data[0]), hp=data[1])
                        small_monster = dict(name=MonstersXX.small_monsters.get(data[0]), hp=data[1])

                label_layout = QVBoxLayout()
                label_layout.setContentsMargins(0, 0, 0, 0)
                if not ConfigLayout.align:
                    if self.orientation == 'right':
                        label_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
                    elif self.orientation == 'left':
                        label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
                    else:
                        label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                if large_monster['name']:
                    label.setText(f'{large_monster['name']}: {large_monster['hp']}')
                    label_layout.addWidget(label)
                    lm_layout.addLayout(label_layout)
                elif not small_monster['name']:
                    label.setParent(None)
                    label_layout.removeWidget(label)

                if ConfigOverlay.show_small_monsters:
                    if small_monster['name'] and small_monster['hp'] < 20000:
                        label.setText(f'{small_monster['name']}: {small_monster['hp']}')
                        label_layout.addWidget(label)
                        sm_layout.addLayout(label_layout)
                    elif not large_monster['name']:
                        label.setParent(None)
                        label_layout.removeWidget(label)
            self.show()

    def update_position(self, ahk, target_window_title):
        try:
            win = ahk.find_window(title=target_window_title, title_match_mode='RegEx')
            target = win.get_position()
            monitor = self.screen().geometry()
            self.win_title = win.get_title()
            is_main_window = not re.search('(Primary|Secondary)', target_window_title)
            self.resize(self.minimumSizeHint())
            self.is_borderless = monitor.width() == target.width and monitor.height() == target.height - 1
            fix_position = dict(x=0, y=23)

            if self.is_borderless:
                fix_position["y"] = -8
                fix_position["x"] = -9

            if is_main_window:
                fix_position["y"] = 55
                if self.is_borderless:
                    fix_position["y"] = 24

            offset_x = (
                target.width -
                self.geometry().width() -
                (fix_position["x"] * 2 if self.is_borderless else fix_position["x"])
            ) * self.x / 100
            offset_y = (
                target.height -
                self.geometry().height() -
                (
                    fix_position["y"] * 2 if self.is_borderless else fix_position["y"] +
                    (30 if is_main_window else 0)
                )
            ) * self.y / 100
            self.move(
                target.x + fix_position["x"] + int(offset_x),
                target.y + fix_position["y"] + int(offset_y)
            )
            self.is_open_window = True
        except (Exception, ):
            self.is_open_window = False


if __name__ == "__main__":
    def handler(signum, frame):
        sys.exit()
    signal.signal(signal.SIGINT, handler)
    cursor.hide()
    header()
    app = QApplication(sys.argv)
    overlay = Overlay()
    sys.exit(app.exec())
