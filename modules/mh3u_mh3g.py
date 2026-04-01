import time
from math import ceil
from collections import OrderedDict
from modules.monsters_3u3g import Monsters3U3G
from modules.utils import read, check_connection, max_monsters, ResultType, current_game
from ahk import AHK


def get_data(p0: int, offset: int):
    is_visible = False
    p1 = p0 + 0xD90
    p2 = read(p1) + 0x410
    p3 = read(p2) + offset
    p4 = read(p3) + 0x7F8
    if p4 > 0x965:
        is_visible = read(p4 + 0x14A, 2) == 0x3E8 and read(p4 - 0x78, 16) == 0x3CF5C28F

    return [read(p4 - 0x7F5, 2), read(p4), read(p4 + 0x4), is_visible, p4]


def get_3u_3g_data(show_small_monsters: bool, game: str):
    large_monsters = Monsters3U3G.large_monsters
    small_monsters = Monsters3U3G.small_monsters
    large_monster_results = []
    small_monster_results = []
    is_mh3g = game == "MH3G"
    offset = 0x4
    pointer0 = read(0x8115EF8 if is_mh3g else 0x8119DD8)

    for i in range(0, max_monsters):
        data = get_data(pointer0, offset + (0x220 * i))
        name = data[0]
        hp = data[1]
        initial_hp = data[2]
        is_visible = data[3]
        pointer = data[4]
        if large_monsters.get(name) and is_visible:
            monster_size = int(round(read(pointer - 0x764, 4, result_type=ResultType.FLOAT) * 100, 2))
            abnormal_status = OrderedDict()

            def add_abnormal_status(status_name: str, values: list):
                if values[1] != 0xFFFF:
                    abnormal_status.update({
                        status_name: values,
                    })

            add_abnormal_status(
                "Poison", [read(pointer + 0x1EC, 2), read(pointer + 0x1EA, 2)]
            )
            add_abnormal_status(
                "Sleep", [read(pointer + 0x20E, 2), read(pointer + 0x20C, 2)]
            )
            add_abnormal_status(
                "Paralysis", [read(pointer + 0x206, 2), read(pointer + 0x204, 2)]
            )
            add_abnormal_status(
                "Dizzy", [read(pointer + 0x21C, 2), read(pointer + 0x21E, 2)]
            )
            add_abnormal_status(
                "Exhaust", [read(pointer + 0x224, 2), read(pointer + 0x226, 2)]
            )
            add_abnormal_status(
                "Slime", [read(pointer + 0x22E, 2), read(pointer + 0x22C, 2)]
            )
            abnormal_status.update({
                "Rage": int(ceil(read(pointer + 0x158, 4, result_type=ResultType.FLOAT) / 60))
            })
            prev_pointer = 0
            if len(large_monster_results) >= 1:
                prev_pointer = large_monster_results[-1][5]
            if prev_pointer != pointer:
                large_monster_results.append([name, hp, initial_hp, monster_size, abnormal_status, pointer])
        if small_monsters.get(name) and is_visible and show_small_monsters:
            small_monster_results.append([name, hp, initial_hp])

    return {
        "monsters": large_monster_results + small_monster_results,
        "total": [len(large_monster_results), len(small_monster_results)]
    }


def get_3u_3g_monster_selected(game):
    is_mh3g = game == "MH3G"
    p0 = read(0x8210680 if is_mh3g else 0x8119D90) + 0x2208
    if read(p0, 2) == 0x100:
        return 1
    elif read(p0, 2) == 0x101:
        return 2
    return 0


if __name__ == "__main__":
    start_time = time.time()
    check_connection()
    target_window_title = (
        "(MONSTER HUNTER |MH)(3 ULTIMATE|3U|3 \\(tri-\\) G|4|4 ULTIMATE|4U|4G|X|GEN|XX)"
    )
    ahk = AHK(version="v2")
    win = ahk.find_window(
        title=target_window_title, title_match_mode="RegEx"
    )
    game = current_game(win.title)
    data = get_3u_3g_data(True, game)
    monsters = data['monsters']
    for monster in monsters:
        large_monster = Monsters3U3G.large_monsters.get(monster[0])
        small_monster_name = Monsters3U3G.small_monsters.get(monster[0])
        if large_monster:
            print([large_monster["name"], *monster[1::]])
        if small_monster_name:
            print([small_monster_name, *monster[1::]])
    end_time = time.time()
    print(end_time - start_time)
