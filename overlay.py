import math
import os
import sys
import time
import cursor
import win32gui
from ahk import AHK, Position
from ahk_wmutil import wmutil_extension
from PySide6.QtCore import QTimer, Qt, QThread, Signal, qInstallMessageHandler
from PySide6.QtGui import QColorConstants
from modules.mhxx import get_xx_data, get_xx_monster_selected, MonstersXX
from modules.mh3u_mh3g import get_3u_3g_data, get_3u_3g_monster_selected, Monsters3U3G
from modules.mh4u_mh4g import get_4u_4g_data, get_4u_4g_monster_selected, Monsters4U4G
from modules.config import ConfigOverlay, ConfigLayout, ConfigColors
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy

from modules.utils import (
    TextColor,
    PassiveTimer,
    prevent_keyboard_exit_error,
    rgba_int,
    get_crown,
    clear_screen,
    check_connection,
    header,
    current_game,
    max_monsters,
    max_status,
    logger_init,
    log_timer,
    log_error,
    is_connected
)


class DataFetcher(QThread):
    data_fetched = Signal(dict)

    def __init__(self, game, show_small_monsters):
        super().__init__()
        self.show_small_monsters = show_small_monsters
        self.is_3u3g = game in ("MH3U", "MH3G")
        self.is_4u4g = game in ("MH4U", "MH4G", "MH4")
        self.game = game

    def run(self):
        while True:
            data = {"monsters": [], "total": []}
            try:
                data = (
                    get_3u_3g_data(self.show_small_monsters, self.game)
                    if self.is_3u3g else get_4u_4g_data(self.show_small_monsters, self.game)
                    if self.is_4u4g else get_xx_data(self.show_small_monsters, self.game)
                )
            except (Exception,):
                pass
            self.data_fetched.emit(data)
            self.msleep(round(ConfigOverlay.hp_update_time * 1000))


class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.running = False
        self.data_fetcher = None
        self.is_borderless = False
        self.is_open_window = False
        self.initial_window_state: Position = Position(0, 0, 800, 600)
        self.win_title = ""
        self.game = ""
        self.timeout = (20 * 60) + 1  # 20 minutes
        self.counter = self.timeout
        self.timeout_start = time.time()
        self.orientation = ConfigLayout.orientation
        self.x = ConfigLayout.x
        self.y = ConfigLayout.y
        self.fix_offset = dict(x=ConfigLayout.fix_x, y=ConfigLayout.fix_y)
        self.hotkey = ConfigOverlay.hotkey
        self.hp_update_time = round(ConfigOverlay.hp_update_time * 1000)
        self.show_initial_hp = ConfigOverlay.show_initial_hp
        self.show_hp_percentage = ConfigOverlay.show_hp_percentage
        self.show_small_monsters = ConfigOverlay.show_small_monsters
        self.show_abnormal_status = ConfigOverlay.show_abnormal_status
        self.always_show_abnormal_status = ConfigOverlay.always_show_abnormal_status
        self.show_size_multiplier = ConfigOverlay.show_size_multiplier
        self.show_crown = ConfigOverlay.show_crown
        self.is_main_window = ConfigOverlay.target_window == "main"
        self.debugger = ConfigOverlay.debugger
        self.pt = PassiveTimer()
        self.initialize_ui()

    def initialize_ui(self):
        target_window_title = (
            "(MONSTER HUNTER |MH)(3 ULTIMATE|3U|3 \\(tri-\\) G|4|4 ULTIMATE|4U|4G|X|GEN|XX)"
        )
        not_responding_title = " \\([\\w\\s]+\\)$"
        if ConfigOverlay.target_window == "primary":
            target_window_title += " \\| Primary Window"
        if ConfigOverlay.target_window == "secondary":
            target_window_title += " \\| Secondary Window"

        target_window_title += "$"

        ahk = AHK(version="v2", extensions=[wmutil_extension])

        if self.debugger:
            logger_init(".log")
            self.pt.start(5)

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
            border-radius: 5px;
            """
        )

        color = rgba_int(
            getattr(QColorConstants.Svg, ConfigColors.text_color).rgb(),
            ConfigColors.text_opacity,
        )
        background_color = rgba_int(
            getattr(QColorConstants.Svg, ConfigColors.background_color).rgb(),
            ConfigColors.background_opacity,
        )

        status_color = rgba_int(
            getattr(QColorConstants.Svg, ConfigColors.abnormal_status_text_color).rgb(),
            ConfigColors.abnormal_status_text_opacity,
        )
        status_background_color = rgba_int(
            getattr(QColorConstants.Svg, ConfigColors.abnormal_status_background_color).rgb(),
            ConfigColors.abnormal_status_background_opacity,
        )

        labels = []
        for i in range(0, max_monsters):
            label = QLabel()
            label.setStyleSheet(
                f"""
                color: {color};
                background-color: {background_color};
                padding: 5px {15 if self.orientation == 'center' else 10}px;
                font-size: {ConfigOverlay.font_size}px;
                margin: 0 0 5px;
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

        label_layouts = []
        for i in range(0, max_monsters):
            label_layout = QVBoxLayout()
            label_layout.setContentsMargins(0, 0, 0, 0)
            if self.orientation == "right":
                label_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            elif self.orientation == "left":
                label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            else:
                label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_layouts.append(label_layout)

        status_labels = []
        for i in range(0, max_status * 2):
            label = QLabel()
            label.setStyleSheet(
                f"""
                color: {status_color};
                background-color: {status_background_color};
                padding: 3px {10 if self.orientation == 'center' else 5}px;
                font-size: {int(ConfigOverlay.font_size / 1.12)}px;
                margin: 0 3px 5px 3px;
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
            status_labels.append(label)

        status_layouts = []
        for i in range(0, max_status):
            status_layout = QHBoxLayout()
            status_layout.setContentsMargins(0, 0, 0, 0)
            if self.orientation == "right":
                status_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            elif self.orientation == "left":
                status_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            else:
                status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            status_layouts.append(status_layout)

        lm_layout = QVBoxLayout()
        lm_layout.setContentsMargins(0, 0, 0, 0)
        lm_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sm_layout = QVBoxLayout()
        sm_layout.setContentsMargins(0, 0, 0, 0)
        sm_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for index, label_layout in enumerate(label_layouts):
            if 2 > index:
                label_layout.addLayout(status_layouts[index])
                label_layout.addLayout(status_layouts[index + 2])
                label_layout.addLayout(status_layouts[index + 4])
                label_layout.addLayout(status_layouts[index + 6])
                lm_layout.addLayout(label_layout)
            else:
                sm_layout.addLayout(label_layout)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(lm_layout)
        layout.addLayout(sm_layout)

        self.update_position(ahk, layout, target_window_title, not_responding_title)

        ahk.add_hotkey(
            f"{self.hotkey} Up",
            callback=lambda: self.toggle_borderless_screen(ahk, target_window_title, not_responding_title),
        )
        ahk.start_hotkeys()

        timer1 = QTimer(self)
        timer1.timeout.connect(lambda: self.update_position(ahk, layout, target_window_title, not_responding_title))
        timer1.start(3)

        timer2 = QTimer(self)
        timer2.timeout.connect(lambda: self.wait_init_game(labels, label_layouts, status_labels, status_layouts))
        timer2.start(1000)

    def start_data_fetcher(self, labels, label_layouts, status_labels, status_layouts):
        self.data_fetcher = DataFetcher(self.game, self.show_small_monsters)
        self.data_fetcher.data_fetched.connect(
            lambda data: self.update_show(data, labels, label_layouts, status_labels, status_layouts)
        )
        self.data_fetcher.start()

    @staticmethod
    def get_window(ahk, target_window_title, not_responding_title):
        win = None
        win_not_responding = ahk.find_window(
            title=target_window_title + not_responding_title, title_match_mode="RegEx"
        )
        if not win_not_responding:
            win = ahk.find_window(title=target_window_title, title_match_mode="RegEx")
        return win
    
    @staticmethod
    def get_window_position(hwnd):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return Position(x, y, width, height)

    def toggle_borderless_screen(self, ahk, target_window_title, not_responding_title):
        try:
            win = self.get_window(ahk, target_window_title, not_responding_title)
            monitor = win.get_monitor()
            target = self.get_window_position(win.id)
            win.set_style("^0xC00000")
            win.set_style("^0x40000")
            self.is_borderless = monitor.size[0] <= target.width and monitor.size[1] - 1 <= target.height
            if self.is_borderless:
                win.set_style("+0xC00000")
                win.set_style("+0x40000")
                win32gui.MoveWindow(
                    win.id,
                    self.initial_window_state.x,
                    self.initial_window_state.y,
                    self.initial_window_state.width,
                    self.initial_window_state.height,
                    True
                )
            else:
                self.initial_window_state = target
                win.set_style("-0xC00000")
                win.set_style("-0x40000")
                win32gui.MoveWindow(
                    win.id,
                    monitor.position[0],
                    monitor.position[1],
                    monitor.size[0],
                    monitor.size[1] + 1,
                    True
                )
        except Exception as error:
            if self.debugger:
                log_error(f'Toggle Borderless Error: {error}')
            pass

    def wait_init_game(self, labels, label_layouts, status_labels, status_layouts):
        if not self.is_open_window:
            if self.running:
                clear_screen()
                header()
            if self.data_fetcher:
                self.data_fetcher.terminate()
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
                self.start_data_fetcher(labels, label_layouts, status_labels, status_layouts)
            self.running = True
            self.counter = self.timeout
            self.timeout_start = time.time()
            text = TextColor.green(f"{self.game} running.")
            print(f"\r{text}", end="", flush=True)

    def update_show(self, data, labels, label_layouts, status_labels, status_layouts):
        if self.is_open_window:
            for index, label in enumerate(labels):
                if data['total'][0] == 0:
                    for i in range(0, max_status):
                        status_label = status_labels[i]
                        status_label2 = status_labels[i + max_status]
                        status_label.clear()
                        status_label.setParent(None)
                        status_label2.clear()
                        status_label2.setParent(None)
                if len(data['monsters']) > index:
                    is_3u3g = self.game in ("MH3U", "MH3G")
                    is_4u4g = self.game in ("MH4U", "MH4G", "MH4")
                    label_layout = label_layouts[index]
                    monster = data['monsters'][index]
                    monster_selected = (
                        get_3u_3g_monster_selected(self.game)
                        if is_3u3g else get_4u_4g_monster_selected(self.game)
                        if is_4u4g else get_xx_monster_selected(self.game)
                    )
                    if data['total'][0] == 1:
                        if monster_selected > 1:
                            monster_selected = 1
                    large_monster = (
                        Monsters3U3G.large_monsters.get(monster[0])
                        if is_3u3g else Monsters4U4G.large_monsters.get(monster[0])
                        if is_4u4g else MonstersXX.large_monsters.get(monster[0])
                    )
                    small_monster_name = (
                        Monsters3U3G.small_monsters.get(monster[0])
                        if is_3u3g else Monsters4U4G.small_monsters.get(monster[0])
                        if is_4u4g else MonstersXX.small_monsters.get(monster[0])
                    )
                    hp = monster[1]
                    initial_hp = monster[2]
                    if initial_hp > 5:
                        if large_monster:
                            text = ""
                            size_multiplier = None
                            monster_number = index + 1
                            abnormal_status = monster[4]
                            if self.show_size_multiplier:
                                size_multiplier = monster[3]
                                text += f"({size_multiplier}) "
                            text += f"{large_monster["name"]}{get_crown(
                                size_multiplier, large_monster["crowns"], self.show_crown
                            )}:"
                            if self.show_hp_percentage:
                                text += f" {math.ceil((hp / initial_hp) * 100)}% |"
                            text += f" {hp}"
                            if self.show_initial_hp:
                                text += f" | {initial_hp}"
                            label.setText(text)
                            if (
                                (monster_number == monster_selected or self.always_show_abnormal_status) and
                                self.show_abnormal_status
                            ):
                                i = 0
                                for key, value in abnormal_status.items():
                                    status_label = status_labels[i if monster_number == 1 else i + max_status]
                                    if key == "Rage":
                                        m, s = divmod(value, 60)
                                        status_label.setText(f"{key}: {m}:{s:02d}")
                                    else:
                                        status_label.setText(f"{key}: {value[0]}/{value[1]}")
                                    if i < 2:
                                        status_layouts[index].addWidget(status_label)
                                    elif i < 4:
                                        status_layouts[2 + index].addWidget(status_label)
                                    elif i < 6:
                                        status_layouts[4 + index].addWidget(status_label)
                                    else:
                                        status_layouts[6 + index].addWidget(status_label)
                                    i += 1

                            if self.show_abnormal_status:
                                for i in range(0, max_status):
                                    status_label = status_labels[i]
                                    status_label2 = status_labels[i + max_status]
                                    if self.always_show_abnormal_status:
                                        if data["total"][0] == 1:
                                            status_label2.clear()
                                            status_label2.setParent(None)
                                    elif monster_selected == 0:
                                        status_label.clear()
                                        status_label.setParent(None)
                                        status_label2.clear()
                                        status_label2.setParent(None)
                                    elif monster_selected == 1:
                                        status_label2.clear()
                                        status_label2.setParent(None)
                                    else:
                                        status_label.clear()
                                        status_label.setParent(None)
                            label_layout.insertWidget(0, label)
                        if self.show_small_monsters:
                            if small_monster_name and hp < 20000:
                                text = f"{small_monster_name}:"
                                if self.show_hp_percentage:
                                    text += f" {math.ceil((hp / initial_hp) * 100)}% |"
                                text += f" {hp}"
                                if self.show_initial_hp:
                                    text += f" | {initial_hp}"
                                label.setText(text)
                                label_layout.addWidget(label)
                    else:
                        label.clear()
                        label.setParent(None)
                else:
                    label.clear()
                    label.setParent(None)
                self.show()

    def update_position(self, ahk, layout, target_window_title, not_responding_title):
        try:
            conn = is_connected()
            if not conn and self.is_open_window and self.data_fetcher:
                self.data_fetcher.terminate()
                self.running = False
                self.is_open_window = False
                self.hide()
                time.sleep(5)
            win = self.get_window(ahk, target_window_title, not_responding_title)
            target = self.get_window_position(win.id)
            monitor = win.get_monitor()
            scale_factor = monitor.scale_factor
            self.win_title = win.get_title()
            self.game = current_game(self.win_title)
            self.resize(self.minimumSizeHint())
            self.is_borderless = monitor.size[0] <= target.width and monitor.size[1] - 1 <= target.height

            margin_top = 35 * scale_factor
            margin_bottom = 11 * scale_factor
            margin_left = 10 * scale_factor
            margin_right = 10 * scale_factor

            if self.is_borderless:
                margin_top = 4 * scale_factor
                margin_bottom = 6 * scale_factor
                margin_left = 4 * scale_factor
                margin_right = 4 * scale_factor

            if self.is_main_window:
                margin_top = 56 * scale_factor
                margin_bottom = 42 * scale_factor
                if self.is_borderless:
                    margin_top = 25 * scale_factor
                    margin_bottom = 34 * scale_factor

            offset_x = (target.x + (target.width - self.geometry().width()) * self.x / 100) + self.fix_offset["x"]
            offset_y = (target.y + (target.height - self.geometry().height()) * self.y / 100) + self.fix_offset["y"]
            layout.setContentsMargins(margin_left, margin_top, margin_right, margin_bottom)
            if self.debugger:
                log_timer(self.pt, [
                    dict(type="info", msg=f'Window Title: {win.title}'),
                    dict(type="info", msg=f'Window Target: {target}'),
                    dict(type="info", msg=f'Monitor: {monitor.position} {monitor.size}'),
                    dict(type="info", msg=f'Borderless: {self.is_borderless}'),
                    dict(type="info", msg=f'Offsets: {offset_x} {offset_y}'),
                ])
            self.move(offset_x, offset_y)
            if conn:
                self.is_open_window = True
        except Exception as error:
            if self.debugger:
                log_timer(self.pt, [
                    dict(type="error", msg=f'Update Position Error: {error}'),
                ])
            self.is_open_window = False


if __name__ == "__main__":
    os.environ["QT_FONT_DPI"] = '1'
    qInstallMessageHandler(object)
    prevent_keyboard_exit_error()
    cursor.hide()
    header()
    app = QApplication(sys.argv)
    overlay = Overlay()
    sys.exit(app.exec())
