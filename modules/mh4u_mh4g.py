import time
from dataclasses import dataclass
from modules.utils import read, check_connection, max_monsters, ResultType


def get_data(p0: int, offset: int, is_mh4: bool):
    p1 = p0 + offset
    p2 = read(p1) + (0xE1C if is_mh4 else 0xE28)
    p3 = read(p2) + 0x3E8
    is_visible = read(p3 - 0x21E, 3) != 0xBFF0C

    return [read(p3 - 0x228, 1), read(p3, 2), read(p3 + 0x4, 2), is_visible, p3]


def get_4u_4g_data(show_small_monsters: bool):
    is_mh4 = read(0x0708AD88, 8) in [0x400000004B500, 0x4000000100900, 0x4000000105000]
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
            0xF031FC: {0x831A360},
            0xF12214: {0x831A7D0, 0x831A840},
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
            large_monster_results.append([name, hp, initial_hp, monster_size])
        if small_monsters.get(name) and is_visible and show_small_monsters:
            small_monster_results.append([name, hp, initial_hp])

    return large_monster_results + small_monster_results


@dataclass
class Monsters4U4G:
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
            "name": "Pink Rathian",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        4: {
            "name": "Azure Rathalos",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        5: {
            "name": "Gold Rathian",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        6: {
            "name": "Silver Rathalos",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        7: {
            "name": "Yian Kut-Ku",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        8: {
            "name": "Blue Yian Kut-Ku",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        9: {
            "name": "Gypceros",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        10: {
            "name": "Purple Gypceros",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        11: {
            "name": "Tigrex",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        12: {
            "name": "Brute Tigrex",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        13: {
            "name": "Gendrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        14: {
            "name": "Iodrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        15: {
            "name": "Great Jaggi",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        16: {
            "name": "Velocidrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        17: {
            "name": "Congalala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        18: {
            "name": "Emerald Congalala",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        19: {
            "name": "Rajang",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        20: {
            "name": "Kecha Wacha",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        21: {
            "name": "Tetsucabra",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        22: {
            "name": "Zamtrios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        23: {
            "name": "Najarala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        24: {
            "name": "Dalamadur (Head)",
            "crowns": {"g": None, "s": None, "m": None}
        },
        25: {
            "name": "Seltas",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        26: {
            "name": "Seltas Queen",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        27: {
            "name": "Nerscylla",
            "crowns": {"g": 118, "s": 112, "m": 90}
        },
        28: {
            "name": "Gore Magala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        29: {
            "name": "Shagaru Magala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        30: {
            "name": "Yian Garuga",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        31: {
            "name": "Kushala Daora",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        32: {
            "name": "Teostra",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        33: {
            "name": "Akantor",
            "crowns": {"g": None, "s": None, "m": None}
        },
        34: {
            "name": "Kirin",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        35: {
            "name": "Oroshi Kirin",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        36: {
            "name": "Khezu",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        37: {
            "name": "Red Khezu",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        38: {
            "name": "Basarios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        39: {
            "name": "Ruby Basarios",
            "crowns": {"g": 123, "s": 117, "m": 90}
        },
        40: {
            "name": "Gravios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        41: {
            "name": "Black Gravios",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        42: {
            "name": "Deviljho",
            "crowns": {"g": 128, "s": 121, "m": 90}
        },
        43: {
            "name": "Savage Deviljho",
            "crowns": {"g": 128, "s": 121, "m": 90}
        },
        44: {
            "name": "Brachydios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        45: {
            "name": "Golden Rajang",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        46: {
            "name": "Dah'ren Mohran",
            "crowns": {"g": None, "s": None, "m": None}
        },
        47: {
            "name": "Lagombi",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        48: {
            "name": "Zinogre",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        49: {
            "name": "Stygian Zinogre",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        77: {
            "name": "Black Fatalis",
            "crowns": {"g": None, "s": None, "m": None}
        },
        78: {
            "name": "Crimson Fatalis",
            "crowns": {"g": None, "s": None, "m": None}
        },
        79: {
            "name": "White Fatalis",
            "crowns": {"g": None, "s": None, "m": None}
        },
        80: {
            "name": "Molten Tigrex",
            "crowns": {"g": None, "s": None, "m": None}
        },
        82: {
            "name": "Rusted Kushala Daora",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        83: {
            "name": "Dalamadur (Tail)",
            "crowns": {"g": None, "s": None, "m": None}
        },
        88: {
            "name": "Seregios",
            "crowns": {"g": 109, "s": 105, "m": 90}
        },
        89: {
            "name": "Gogmazios",
            "crowns": {"g": None, "s": None, "m": None}
        },
        90: {
            "name": "Ash Kecha Wacha",
            "crowns": {"g": 114, "s": 109, "m": 90}
        },
        91: {
            "name": "Berserk Tetsucabra",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        92: {
            "name": "Tigerstripe Zamtrios",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        93: {
            "name": "Tidal Najarala",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        94: {
            "name": "Desert Seltas",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        95: {
            "name": "Desert Seltas Queen",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        96: {
            "name": "Shrouded Nerscylla",
            "crowns": {"g": 118, "s": 112, "m": 90}
        },
        97: {
            "name": "Chaotic Gore Magala",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        98: {
            "name": "Raging Brachydios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        99: {
            "name": "Diablos",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        100: {
            "name": "Black Diablos",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        101: {
            "name": "Monoblos",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        102: {
            "name": "White Monoblos",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        103: {
            "name": "Chameleos",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        105: {
            "name": "Cephadrome",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        107: {
            "name": "Daimyo Hermitaur",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        108: {
            "name": "Plum Daimyo Hermitaur",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        110: {
            "name": "Shah Dalamadur (Head)",
            "crowns": {"g": None, "s": None, "m": None}
        },
        111: {
            "name": "Shah Dalamadur (Tail)",
            "crowns": {"g": None, "s": None, "m": None}
        },
        112: {
            "name": "Rajang (Apex)",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        113: {
            "name": "Deviljho (Apex)",
            "crowns": {"g": 128, "s": 121, "m": 90}
        },
        114: {
            "name": "Zinogre (Apex)",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        115: {
            "name": "Gravios (Apex)",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        116: {
            "name": "Ukanlos",
            "crowns": {"g": None, "s": None, "m": None}
        },
        117: {
            "name": "Crimson Fatalis (Super)",
            "crowns": {"g": None, "s": None, "m": None}
        },
        119: {
            "name": "Diablos (Apex)",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        120: {
            "name": "Tidal Najarala (Apex)",
            "crowns": {"g": 123, "s": 117, "m": 97}
        },
        121: {
            "name": "Tigrex (Apex)",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        122: {
            "name": "Seregios (Apex)",
            "crowns": {"g": 109, "s": 105, "m": 90}
        },
    }

    small_monsters = {
        50: "Gargwa",
        51: "Rhenoplos",
        52: "Aptonoth",
        53: "Popo",
        54: "Slagtoth",
        55: "Slagtoth",
        56: "Jaggi",
        57: "Jaggia",
        58: "Velociprey",
        59: "Genprey",
        60: "Ioprey",
        61: "Remobra",
        62: "Delex",
        63: "Conga",
        64: "Kelbi",
        65: "Felyne",
        66: "Melynx",
        67: "Altaroth",
        68: "Bnahabra",
        69: "Bnahabra",
        70: "Bnahabra",
        71: "Bnahabra",
        72: "Zamite",
        73: "Konchu",
        74: "Konchu",
        75: "Konchu",
        76: "Konchu",
        81: "Rock",
        84: "Rock",
        85: "Rock",
        86: "Rock",
        87: "Rock",
        104: "Rock",
        106: "Cephalos",
        109: "Hermitaur",
        118: "Apceros",
        123: "Rock",
    }


if __name__ == "__main__":
    start_time = time.time()
    check_connection()
    monsters = get_4u_4g_data(True)
    for monster in monsters:
        large_monster = Monsters4U4G.large_monsters.get(monster[0])
        small_monster_name = Monsters4U4G.small_monsters.get(monster[0])
        if large_monster:
            print([large_monster["name"], *monster[1::]])
        if small_monster_name:
            print([small_monster_name, *monster[1::]])
    end_time = time.time()
    print(end_time-start_time)

