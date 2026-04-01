import time
from math import ceil
from collections import OrderedDict
from modules.monsters_xx import MonstersXX
from modules.utils import read, check_connection, max_monsters, ResultType, current_game
from ahk import AHK


def get_data(p0: int, offset: int, is_mhx_g: bool):
    is_visible = False
    p1 = p0 + offset
    p2 = read(p1) + (0xFAC if is_mhx_g else 0x10A8)
    p3 = read(p2) + 0x360
    if p3 > (0x1308 if is_mhx_g else 0x1408):
        is_visible = (
                read(p3 - (0x1308 if is_mhx_g else 0x1408), 1) != 0x7 or
                read(p3, 2) != 0x0
        )

    return [
        read(p3 + (0x59DC if is_mhx_g else 0x5A18), 2),
        read(p3),
        read(p3 + 0x4),
        is_visible,
        p3,
    ]


def get_xx_data(show_small_monsters: bool, game: str):
    is_mhx_g = game in ("MHX", "MHGEN")
    large_monsters = MonstersXX.large_monsters
    small_monsters = MonstersXX.small_monsters
    large_monster_results = []
    small_monster_results = []
    pointer0 = 0
    if is_mhx_g:
        addresses = {
            0xDA2DA8: {0x8334970, 0x8334390},
            0xDB9DA8: {0x8323500, 0x83234D0},
            0xDD2DA8: {0x8325200}
        }
    else:
        addresses = {
            0xD2CAA0: {0x82B7720, 0x82B9660},
            0xD30AA0: {0x82B98B0},
            0xD3A8E0: {0x82D0760}
        }

    for address, target_value in addresses.items():
        pointer0 = read(address)
        if pointer0 in target_value:
            break

    for i in range(0, max_monsters):
        data = get_data(pointer0, 0x14 + (0x4 * i), is_mhx_g)
        name = data[0]
        hp = data[1]
        initial_hp = data[2]
        is_visible = data[3]
        pointer = data[4]
        if large_monsters.get(name) and is_visible:
            monster_size = int(round(read(pointer - 0x1B0, 4, result_type=ResultType.FLOAT) * 100, 2))
            abnormal_status = OrderedDict()

            def add_abnormal_status(status_name: str, values: list):
                if values[1] != 0xFFFF:
                    abnormal_status.update({
                        status_name: values,
                    })

            add_abnormal_status("Poison", [
                read(pointer + (0x54FC if is_mhx_g else 0x54E4), 2),
                read(pointer + (0x5508 if is_mhx_g else 0x54F0), 2)
            ])
            add_abnormal_status("Sleep", [
                read(pointer + (0x5500 if is_mhx_g else 0x54E8), 2),
                read(pointer + (0x54FE if is_mhx_g else 0x54E6), 2)
            ])
            add_abnormal_status("Paralysis", [
                read(pointer + (0x5516 if is_mhx_g else 0x54FE), 2),
                read(pointer + (0x5514 if is_mhx_g else 0x54FC), 2)
            ])
            add_abnormal_status("Dizzy", [
                read(pointer + (0x55D6 if is_mhx_g else 0x55BE), 2),
                read(pointer + (0x55D8 if is_mhx_g else 0x55C0), 2)
            ])
            add_abnormal_status("Jump", [
                read(pointer + (0x55FA if is_mhx_g else 0x55E2), 2),
                read(pointer + (0x55FC if is_mhx_g else 0x55E4), 2)
            ])
            add_abnormal_status("Exhaust", [
                read(pointer + (0x55E2 if is_mhx_g else 0x55CA), 2),
                read(pointer + (0x55E4 if is_mhx_g else 0x55CC), 2)
            ])
            add_abnormal_status("Blast", [
                read(pointer + (0x560A if is_mhx_g else 0x55F2), 2),
                read(pointer + (0x5608 if is_mhx_g else 0x55F0), 2)
            ])
            abnormal_status.update({
                "Rage": int(ceil(
                    read(pointer + (0x154 if is_mhx_g else 0x18C), 4, result_type=ResultType.FLOAT) / 60
                ))
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


def get_xx_monster_selected(game: str):
    is_mhx_g = game in ("MHX", "MHGEN")
    if is_mhx_g:
        addresses = [0xDD2360, 0xDA2360, 0xDB9360]
        p0 = 0
        for address in addresses:
            p0 = read(address) + 0x1C
            if read(address - 0x4, 4) == 0xFFFFFFFF:
                break
        p1 = read(p0) + 0x7E1
        return read(p1, 1)
    return read(0x3003BD11, 1)


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
    data = get_xx_data(True, game)
    monsters = data['monsters']
    for monster in monsters:
        large_monster = MonstersXX.large_monsters.get(monster[0])
        small_monster_name = MonstersXX.small_monsters.get(monster[0])
        if large_monster:
            print([large_monster["name"], *monster[1::]])
        if small_monster_name:
            print([small_monster_name, *monster[1::]])
    end_time = time.time()
    print(end_time - start_time)
