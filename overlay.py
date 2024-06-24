import re
import sys
import time
import cursor
from ahk import AHK, Position
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColorConstants
from modules.mhxx import get_xx_data, MonstersXX
from modules.mh3u_mh3g import get_3u_3g_data, Monsters3U3G
from modules.mh4u_mh4g import get_4u_4g_data, Monsters4U4G
from modules.config import ConfigOverlay, ConfigLayout, ConfigColors
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy
from modules.utils import (
    TextColor,
    prevent_keyboard_exit_error,
    rgba_int,
    clear_screen,
    check_connection,
    header,
    current_game,
    max_monsters
)


def validate_not_responding(win_array, expression):
    result = False
    for window in win_array:
        if re.search(expression, window.get_title()):
            result = True
    return result


class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.is_borderless = False
        self.running = False
        self.is_open_window = False
        self.initial_window_state: Position = Position(0, 0, 600, 500)
        self.win_title = ""
        self.timeout = (20 * 60) + 1  # 20 minutes
        self.counter = self.timeout
        self.timeout_start = time.time()
        self.orientation = ConfigLayout.orientation
        self.x = ConfigLayout.x
        self.y = ConfigLayout.y
        self.fix_offset = dict(x=ConfigLayout.fix_x, y=ConfigLayout.fix_y)
        self.hotkey = ConfigOverlay.hotkey
        self.hp_update_time = round(ConfigOverlay.hp_update_time * 1000)
        self.initialize_ui()

    def initialize_ui(self):
        target_window_title = (
            "(MONSTER HUNTER |MH)(3 ULTIMATE|3U|3 \\(tri-\\) G|4 ULTIMATE|4U|4G|XX)"
        )
        if ConfigOverlay.target_window == "primary":
            target_window_title += " \\| Primary Window"
        if ConfigOverlay.target_window == "secondary":
            target_window_title += " \\| Secondary Window"

        target_window_title += "$"

        ahk = AHK(version="v2")
        self.setWindowTitle("Overlay")
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet(
            f"""
            font-family: {ConfigOverlay.font_family}; 
            font-weight: {ConfigOverlay.font_weight};
            font-size: {ConfigOverlay.font_size}px;
            border-radius: 5px;
            """
        )

        color = rgba_int(
            getattr(QColorConstants.Svg, ConfigColors.text_color).rgb(),
            ConfigColors.text_transparency,
        )
        background_color = rgba_int(
            getattr(QColorConstants.Svg, ConfigColors.background_color).rgb(),
            ConfigColors.background_transparency,
        )

        labels = []
        for i in range(0, max_monsters):
            label = QLabel()
            label.setStyleSheet(
                f"""
                color: {color};
                background-color: {background_color};
                padding: 5px {15 if self.orientation == 'center' else 10}px;
                """
            )
            label.setSizePolicy(
                QSizePolicy.Policy.Expanding if ConfigLayout.align else QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Fixed
            )
            if self.orientation == "right":
                label.setAlignment(Qt.AlignmentFlag.AlignRight)
            elif self.orientation == "left":
                label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            else:
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            labels.append(label)

        lm_layout = QVBoxLayout()
        lm_layout.setContentsMargins(0, 0, 0, 0)
        lm_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sm_layout = QVBoxLayout()
        sm_layout.setContentsMargins(0, 0, 0, 0)
        sm_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(lm_layout)
        layout.addLayout(sm_layout)

        self.update_position(ahk, target_window_title)

        ahk.add_hotkey(
            self.hotkey,
            callback=lambda: self.toggle_borderless_screen(ahk, target_window_title),
        )
        ahk.start_hotkeys()

        timer1 = QTimer(self)
        timer1.timeout.connect(lambda: self.update_position(ahk, target_window_title))
        timer1.start(1)

        timer2 = QTimer(self)
        timer2.timeout.connect(lambda: self.update_show(lm_layout, sm_layout, labels))
        timer2.start(self.hp_update_time)

        timer3 = QTimer(self)
        timer3.timeout.connect(self.wait_init_game)
        timer3.start(1000)

    def toggle_borderless_screen(self, ahk, target_window_title):
        try:
            win = ahk.find_window(title=target_window_title, title_match_mode="RegEx")
            monitor = self.screen().geometry()
            target = win.get_position()
            win.set_style("^0xC00000")
            win.set_style("^0x40000")
            if self.is_borderless:
                win.set_style("+0xC00000")
                win.set_style("+0x40000")
                win.move(
                    x=self.initial_window_state.x,
                    y=self.initial_window_state.y,
                    width=self.initial_window_state.width,
                    height=self.initial_window_state.height,
                )
            else:
                if (
                    monitor.width() != target.width
                    and monitor.height() != target.height
                ):
                    self.initial_window_state = target
                    win.set_style("-0xC00000")
                    win.set_style("-0x40000")
                    win.move(
                        x=monitor.x(),
                        y=monitor.y(),
                        width=monitor.width(),
                        height=monitor.height() + 1,
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
            if self.counter >= 0:
                red_text = TextColor.red("No game running.")
                yellow_text = TextColor.yellow(f"{m:02d}:{s:02d}")
                text = f"{red_text} Waiting {yellow_text}, then it will close."
                print(f"\r{text}", end="", flush=True)
            if time.time() > self.timeout_start + self.timeout:
                sys.exit()
        else:
            if not self.running:
                clear_screen()
                header()
                check_connection()
            self.running = True
            self.counter = self.timeout
            self.timeout_start = time.time()
            game = current_game(self.win_title)
            text = TextColor.green(f"{game} running.")
            print(f"\r{text}", end="", flush=True)

    def update_show(self, lm_layout, sm_layout, labels):
        pointers = []
        for index, label in enumerate(labels):
            label_layout = QVBoxLayout()
            label_layout.setContentsMargins(0, 0, 0, 0)
            try:
                if self.is_open_window:
                    large_monster = dict(name="", hp=0)
                    small_monster = dict(name="", hp=0)
                    is_3u3g = current_game(self.win_title) in ("MH3U", "MH3G")
                    is_4u4g = current_game(self.win_title) in ("MH4U", "MH4G")

                    data = (
                        get_3u_3g_data(index)
                        if is_3u3g else get_4u_4g_data(index)
                        if is_4u4g else get_xx_data(index)
                    )
                    large_monster_name = (
                        Monsters3U3G.large_monsters.get(data[0])
                        if is_3u3g else Monsters4U4G.large_monsters.get(data[0])
                        if is_4u4g else MonstersXX.large_monsters.get(data[0])
                    )
                    small_monster_name = (
                        Monsters3U3G.small_monsters.get(data[0])
                        if is_3u3g else Monsters4U4G.small_monsters.get(data[0])
                        if is_4u4g else MonstersXX.small_monsters.get(data[0])
                    )

                    if data[2] and data[3] not in pointers:
                        large_monster = dict(
                            name=large_monster_name,
                            hp=data[1],
                        )
                        small_monster = dict(
                            name=small_monster_name,
                            hp=data[1],
                        )
                    pointers.append(data[3])

                    if self.orientation == "right":
                        label_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
                    elif self.orientation == "left":
                        label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
                    else:
                        label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                    l_name = large_monster["name"]
                    l_hp = large_monster["hp"]
                    s_name = small_monster["name"]
                    s_hp = small_monster["hp"]

                    if l_name:
                        label.setText(f"{l_name}: {l_hp}")
                        label_layout.addWidget(label)
                        lm_layout.addLayout(label_layout)
                    elif not s_name:
                        label.setParent(None)
                        label_layout.removeWidget(label)

                    if ConfigOverlay.show_small_monsters:
                        if s_name and s_hp < 20000:
                            label.setText(f"{s_name}: {s_hp}")
                            label_layout.addWidget(label)
                            sm_layout.addLayout(label_layout)
                        elif not l_name:
                            label.setParent(None)
                            label_layout.removeWidget(label)
                    self.show()
                else:
                    label.setParent(None)
                    label_layout.removeWidget(label)
            except (Exception,):
                label.setParent(None)
                label_layout.removeWidget(label)

    def update_position(self, ahk, target_window_title):
        try:
            target_not_responding_window = target_window_title.replace("$", " \\([\\w\\W\\s]+\\)$")
            win = None
            if not validate_not_responding(ahk.list_windows(), target_not_responding_window):
                win = ahk.find_window(
                    title=target_window_title, title_match_mode="RegEx"
                )
            target = win.get_position()
            monitor = self.screen().geometry()
            self.win_title = win.get_title()
            is_main_window = ConfigOverlay.target_window == "main"
            self.resize(self.minimumSizeHint())
            self.is_borderless = (
                monitor.width() == target.width
                and monitor.height() == target.height - 1
            )
            fix_position = dict(x=0 + self.fix_offset["x"], y=23 + self.fix_offset["y"])

            fix_right = self.fix_offset["x"]

            if self.is_borderless:
                fix_position["y"] = -8 + self.fix_offset["y"]
                fix_position["x"] = -9 + self.fix_offset["x"]
                fix_right = abs(fix_position["x"] + self.fix_offset["x"])

            fix_bottom = -self.fix_offset["y"]

            if is_main_window:
                fix_position["y"] = 47 + self.fix_offset["y"]
                fix_bottom = 30 - self.fix_offset["y"]
                if self.is_borderless:
                    fix_position["y"] = 16 + self.fix_offset["y"]
                    fix_bottom = 22 - self.fix_offset["y"]

            offset_x = (
                (target.width - self.geometry().width() - fix_position["x"] + fix_right)
                * self.x
                / 100
            )
            offset_y = (
                (
                    target.height
                    - self.geometry().height()
                    - fix_position["y"]
                    - fix_bottom
                )
                * self.y
                / 100
            )
            self.move(
                target.x + fix_position["x"] + int(offset_x),
                target.y + fix_position["y"] + int(offset_y),
            )
            self.is_open_window = True
        except (Exception,):
            self.is_open_window = False


if __name__ == "__main__":
    prevent_keyboard_exit_error()
    cursor.hide()
    header()
    app = QApplication(sys.argv)
    overlay = Overlay()
    sys.exit(app.exec())
