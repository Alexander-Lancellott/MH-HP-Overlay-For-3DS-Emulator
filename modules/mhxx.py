import time
from math import ceil
from dataclasses import dataclass
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
        read(p3, 2),
        read(p3 + 0x4, 2),
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
            abnormal_status = {}

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


@dataclass
class MonstersXX:
    large_monsters = {
        1: {
            "name": "Rathian",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        2: {
            "name": "Rathalos",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        3: {
            "name": "Khezu",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        4: {
            "name": "Basarios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        5: {
            "name": "Gravios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        7: {
            "name": "Diablos",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        8: {
            "name": "Yian Kut-ku",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        9: {
            "name": "Gypceros",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        10: {
            "name": "Plesioth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        11: {
            "name": "Kirin",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        12: {
            "name": "Lao-Shan Lung",
            "crowns": {"g": None, "s": None, "m": None}
        },
        13: {
            "name": "Fatalis",
            "crowns": {"g": None, "s": None, "m": None}
        },
        14: {
            "name": "Velocidrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        15: {
            "name": "Gendrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        16: {
            "name": "Iodrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        17: {
            "name": "Cephadrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        18: {
            "name": "Yian Garuga",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        19: {
            "name": "Daimyo Hermitaur",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        20: {
            "name": "Shogun Ceanataur",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        21: {
            "name": "Congalala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        22: {
            "name": "Blangonga",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        23: {
            "name": "Rajang",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        24: {
            "name": "Kushala Daora",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        25: {
            "name": "Chameleos",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        27: {
            "name": "Teostra",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        30: {
            "name": "Bulldrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        32: {
            "name": "Tigrex",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        33: {
            "name": "Akantor",
            "crowns": {"g": None, "s": None, "m": None}
        },
        34: {
            "name": "Giadrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        36: {
            "name": "Lavasioth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        37: {
            "name": "Nargacuga",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        38: {
            "name": "Ukanlos",
            "crowns": {"g": None, "s": None, "m": None}
        },
        42: {
            "name": "Barioth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        43: {
            "name": "Deviljho",
            "crowns": {"g": 128, "s": 120, "m": 90}
        },
        44: {
            "name": "Barroth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        45: {
            "name": "Uragaan",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        46: {
            "name": "Lagiacrus",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        47: {
            "name": "Royal Ludroth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        49: {
            "name": "Agnaktor",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        50: {
            "name": "Alatreon",
            "crowns": {"g": None, "s": None, "m": None}
        },
        55: {
            "name": "Duramboros",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        56: {
            "name": "Niblesnarf",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        57: {
            "name": "Zinogre",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        58: {
            "name": "Amatsu",
            "crowns": {"g": None, "s": None, "m": None}
        },
        60: {
            "name": "Arzuros",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        61: {
            "name": "Lagombi",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        62: {
            "name": "Volvidon",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        63: {
            "name": "Brachydios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        65: {
            "name": "Kecha Wacha",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        66: {
            "name": "Tetsucabra",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        67: {
            "name": "Zamtrios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        68: {
            "name": "Najarala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        69: {
            "name": "Seltas Queen",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        70: {
            "name": "Nerscylla",
            "crowns": {"g": 118, "s": 112, "m": 90}
        },
        71: {
            "name": "Gore Magala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        72: {
            "name": "Shagaru Magala",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        76: {
            "name": "Seltas",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        77: {
            "name": "Seregios",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        79: {
            "name": "Malfestio",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        80: {
            "name": "Glavenus",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        81: {
            "name": "Astalos",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        82: {
            "name": "Mizutsune",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        83: {
            "name": "Gammoth",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        84: {
            "name": "Nakarkos",
            "crowns": {"g": None, "s": None, "m": None}
        },
        85: {
            "name": "Great Maccao",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        86: {
            "name": "Valstrax",
            "crowns": {"g": 118, "s": 112, "m": 90}
        },
        87: {
            "name": "Ahtal-Neset",
            "crowns": {"g": None, "s": None, "m": None}
        },
        88: {
            "name": "Ahtal-Ka",
            "crowns": {"g": None, "s": None, "m": None}
        },
        269: {
            "name": "Crimson Fatalis",
            "crowns": {"g": None, "s": None, "m": None}
        },
        513: {
            "name": "Gold Rathian",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        514: {
            "name": "Silver Rathalos",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        525: {
            "name": "White Fatalis",
            "crowns": {"g": None, "s": None, "m": None}
        },
        1025: {
            "name": "Dreadqueen Rathian",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1026: {
            "name": "Dreadking Rathalos",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1031: {
            "name": "Bloodbath Diablos",
            "crowns": {"g": 114, "s": 110, "m": 96}
        },
        1042: {
            "name": "Deadeye Yian Garuga",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        1043: {
            "name": "Stonefist Hermitaur",
            "crowns": {"g": 119, "s": 114, "m": 97}
        },
        1044: {
            "name": "Rustrazor Ceanataur",
            "crowns": {"g": 114, "s": 110, "m": 96}
        },
        1056: {
            "name": "Grimclaw Tigrex",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1061: {
            "name": "Silverwind Nargacuga",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        1069: {
            "name": "Crystalbeard Uragaan",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1081: {
            "name": "Thunderlord Zinogre",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        1084: {
            "name": "Redhelm Arzuros",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1085: {
            "name": "Snowbaron Lagombi",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        1090: {
            "name": "Drilltusk Tetsucabra",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1103: {
            "name": "Nightcloak Malfestio",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        1104: {
            "name": "Hellblade Glavenus",
            "crowns": {"g": 119, "s": 114, "m": 97}
        },
        1105: {
            "name": "Boltreaver Astalos",
            "crowns": {"g": 109, "s": 105, "m": 96}
        },
        1106: {
            "name": "Soulseer Mizutsune",
            "crowns": {"g": 114, "s": 110, "m": 97}
        },
        1107: {
            "name": "Elderfrost Gammoth",
            "crowns": {"g": 114, "s": 110, "m": 97}
        },
        1303: {
            "name": "Furious Rajang",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        1323: {
            "name": "Savage Deviljho",
            "crowns": {"g": 128, "s": 120, "m": 90}
        },
        1343: {
            "name": "Raging Brachydios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        1351: {
            "name": "Chaotic Gore Magala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
    }

    small_monsters = {
        4097: "Aptonoth",
        4098: "Apceros",
        4099: "Kelbi",
        4100: "Mosswine",
        4101: "Hornetaur",
        4102: "Vespoid",
        4103: "Felyne",
        4104: "Melynx",
        4105: "Velociprey",
        4106: "Genprey",
        4107: "Ioprey",
        4108: "Cephalos",
        4109: "Bullfango",
        4110: "Popo",
        4111: "Giaprey",
        4112: "Anteka",
        4113: "Great Thunderbug",
        4115: "Remobra",
        4116: "Hermitaur",
        4117: "Ceanataur",
        4118: "Conga",
        4119: "Blango",
        4121: "Rhenophlos",
        4122: "Bnahabra",
        4123: "Altaroth",
        4130: "Jaggi",
        4131: "Jaggia",
        4135: "Ludroth",
        4136: "Uroktor",
        4137: "Slagtoth",
        4138: "Gargwa",
        4140: "Zamite",
        4141: "Konchu",
        4142: "Maccao",
        4143: "Larinoth",
        4144: "Moofah",
        4197: "Rock",
    }


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
