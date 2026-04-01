import time
from math import ceil
from collections import OrderedDict
from modules.monsters_4u4g import Monsters4U4G, apex_ids
from modules.utils import read, check_connection, max_monsters, ResultType, current_game
from ahk import AHK


def get_data(p0: int, offset: int, is_mh4: bool):
    p1 = p0 + offset
    p2 = read(p1) + (0xE1C if is_mh4 else 0xE28)
    p3 = read(p2) + 0x3E8
    is_visible = read(p3 - 0x21E, 3) != 0xBFF0C

    return [read(p3 - 0x228, 1), read(p3), read(p3 + 0x4), is_visible, p3]


def get_4u_4g_data(show_small_monsters: bool, game: str):
    is_mh4 = game == "MH4"
    large_monsters = Monsters4U4G.large_monsters
    small_monsters = Monsters4U4G.small_monsters
    large_monster_results = []
    small_monster_results = []
    pointer0 = 0
    if is_mh4:
        addresses = {
            0xD7F588: {0x82DAC20},
            0xD7F590: {0x82DAC20},
            0xD7F598: {0x82DAC20},
            0xD7F5A0: {0x82DAC20},
            0xD810E0: {0x82DC430},
            0xD890E8: {0x82DC430}
        }
    else:
        addresses = {
            0xEF6D94: {0x8332CC0},
            0xF031FC: {0x831A360},
            0xF12214: {0x831A7D0, 0x831A840, 0x831D8A0, 0x831D510},
            0xF32004: {0x83531A0, 0x8353610}
        }

    for address, target_value in addresses.items():
        pointer0 = read(address)
        if pointer0 in target_value:
            break

    for i in range(0, max_monsters):
        data = get_data(pointer0, 0x18 + (0x4 * i), is_mh4)
        name = data[0]
        hp = data[1]
        initial_hp = data[2]
        is_visible = data[3]
        pointer = data[4]
        if large_monsters.get(name) and is_visible:
            monster_size = int(round(read(pointer - 0x22C, 4, result_type=ResultType.FLOAT) * 100, 2))
            abnormal_status = OrderedDict()
            is_apex_monster = name in apex_ids

            def add_abnormal_status(status_name: str, values: list):
                if values[1] != 0xFFFF:
                    abnormal_status.update({
                        status_name: values,
                    })

            add_abnormal_status("Poison", [
                read(pointer + (0x7520 if is_mh4 else 0x7574), 2),
                read(pointer + (0x752C if is_mh4 else 0x7580), 2)
            ])
            add_abnormal_status("Sleep", [
                read(pointer + (0x7524 if is_mh4 else 0x7578), 2),
                read(pointer + (0x7522 if is_mh4 else 0x7576), 2)
            ])
            add_abnormal_status("Paralysis", [
                read(pointer + (0x753A if is_mh4 else 0x758E), 2),
                read(pointer + (0x7538 if is_mh4 else 0x758C), 2)
            ])
            add_abnormal_status("Dizzy", [
                read(pointer + (0x763E if is_mh4 else 0x7696), 2),
                read(pointer + (0x7640 if is_mh4 else 0x7698), 2)
            ])
            add_abnormal_status("Exhaust", [
                read(pointer + (0x764A if is_mh4 else 0x76A2), 2),
                read(pointer + (0x764C if is_mh4 else 0x76A4), 2)
            ])
            add_abnormal_status("Jump", [
                read(pointer + (0x7662 if is_mh4 else 0x76BA), 2),
                read(pointer + (0x7664 if is_mh4 else 0x76BC), 2)
            ])
            add_abnormal_status("Blast", [
                read(pointer + (0x7672 if is_mh4 else 0x76CA), 2),
                read(pointer + (0x7670 if is_mh4 else 0x76C8), 2)
            ])
            apex_frenzy_cooldown = int(ceil(read(pointer + 0x158, 4, result_type=ResultType.FLOAT) / 60))
            if is_apex_monster:
                is_apex = bool(read(pointer + 0x7A98, 1))
                add_abnormal_status("Wystone", [
                    read(pointer + 0x7702, 2),
                    read(pointer + 0x7700, 2)
                ])
                if is_apex:
                    abnormal_status.update({
                        "Apex CD": apex_frenzy_cooldown
                    })
                else:
                    abnormal_status.update({
                        "Apex": int(ceil(read(pointer + 0x76F8, 4, result_type=ResultType.FLOAT) / 60))
                    })
            else:
                is_frenzy = bool(read(pointer + 0x152, 1))
                if not is_mh4:
                    add_abnormal_status("Wystone", [
                        read(pointer + 0x770E, 2),
                        read(pointer + 0x770C, 2)
                    ])
                frenzy_in = int(ceil(
                    (
                        read(pointer + 0x154, 4, result_type=ResultType.FLOAT) +
                        read(pointer + 0x160, 4, result_type=ResultType.FLOAT)
                    ) / 60
                ))
                if not is_mh4 and is_frenzy:
                    abnormal_status.update({
                        "Frenzy CD": apex_frenzy_cooldown
                    })
                else:
                    abnormal_status.update({
                        "Frenzy": 0 if is_frenzy else frenzy_in
                    })

            abnormal_status.update({
                "Rage": int(ceil(read(pointer + 0x144, 4, result_type=ResultType.FLOAT) / 60))
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


def get_4u_4g_monster_selected(game):
    is_mh4 = game == "MH4"
    if is_mh4:
        p0 = read(0xFFFDB64) + 0x334
        p1 = read(p0) + 0x34
        p2 = read(p1) + 0xED5
        return read(p2, 1)
    else:
        p0 = read(0xFFFDB78)
        p1 = read(p0) + 0x1E8
        p2 = read(p1) + 0xC
        p3 = read(p2) + 0xED5
        return read(p3, 1)


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
    data = get_4u_4g_data(True, game)
    monsters = data['monsters']
    for monster in monsters:
        large_monster = Monsters4U4G.large_monsters.get(monster[0])
        small_monster_name = Monsters4U4G.small_monsters.get(monster[0])
        if large_monster:
            print([large_monster["name"], *monster[1::]])
        if small_monster_name:
            print([small_monster_name, *monster[1::]])
    end_time = time.time()
    print(end_time - start_time)
