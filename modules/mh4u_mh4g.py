from dataclasses import dataclass
from modules.utils import read, check_connection


def get_data(p0: int, offset: int):
    p1 = p0 + offset
    p2 = read(p1) + 0xE28
    p3 = read(p2) + 0x3E8
    is_visible = read(p3 - 0x21E, 3) != 0xBFF0C

    return [read(p3 - 0x228, 1), read(p3, 2), is_visible, p3]


def get_4u_4g_data(slot: int):
    pointer0 = read(0xF031FC)
    if pointer0 != 0x831A360:
        pointer0 = read(0xF12214)
        if pointer0 not in (0x831A7D0, 0x831A840):
            pointer0 = read(0xF32004)

    return get_data(pointer0, 0x18 + (0x4 * slot))


@dataclass
class Monsters4U4G:
    large_monsters = {
        1: "Rathian",
        2: "Rathalos",
        3: "Pink Rathian",
        4: "Azure Rathalos",
        5: "Gold Rathian",
        6: "Silver Rathalos",
        7: "Yian Kut-Ku",
        8: "Blue Yian Kut-Ku",
        9: "Gypceros",
        10: "Purple Gypceros",
        11: "Tigrex",
        12: "Brute Tigrex",
        13: "Gendrome",
        14: "Iodrome",
        15: "Great Jaggi",
        16: "Velocidrome",
        17: "Congalala",
        18: "Emerald Congalala",
        19: "Rajang",
        20: "Kecha Wacha",
        21: "Tetsucabra",
        22: "Zamtrios",
        23: "Najarala",
        24: "Dalamadur (Head)",
        25: "Seltas",
        26: "Seltas Queen",
        27: "Nerscylla",
        28: "Gore Magala",
        29: "Shagaru Magala",
        30: "Yian Garuga",
        31: "Kushala Daora",
        32: "Teostra",
        33: "Akantor",
        34: "Kirin",
        35: "Oroshi Kirin",
        36: "Khezu",
        37: "Red Khezu",
        38: "Basarios",
        39: "Ruby Basarios",
        40: "Gravios",
        41: "Black Gravios",
        42: "Deviljho",
        43: "Savage Deviljho",
        44: "Brachydios",
        45: "Golden Rajang",
        46: "Dah'ren Mohran",
        47: "Lagombi",
        48: "Zinogre",
        49: "Stygian Zinogre",
        77: "Black Fatalis",
        78: "Crimson Fatalis",
        79: "White Fatalis",
        80: "Molten Tigrex",
        82: "Rusted Kushala Daora",
        83: "Dalamadur (Tail)",
        88: "Seregios",
        89: "Gogmazios",
        90: "Ash Kecha Wacha",
        91: "Berserk Tetsucabra",
        92: "Tigerstripe Zamtrios",
        93: "Tidal Najarala",
        94: "Desert Seltas",
        95: "Desert Seltas Queen",
        96: "Shrouded Nerscylla",
        97: "Chaotic Gore Magala",
        98: "Raging Brachydios",
        99: "Diablos",
        100: "Black Diablos",
        101: "Monoblos",
        102: "White Monoblos",
        103: "Chameleos",
        105: "Cephadrome",
        107: "Daimyo Hermitaur",
        108: "Plum Daimyo Hermitaur",
        110: "Shah Dalamadur (Head)",
        111: "Shah Dalamadur (Tail)",
        112: "Rajang (Apex)",
        113: "Deviljho (Apex)",
        114: "Zinogre (Apex)",
        115: "Gravios (Apex)",
        116: "Ukanlos",
        117: "Crimson Fatalis (Super)",
        119: "Diablos (Apex)",
        120: "Tidal Najarala (Apex)",
        121: "Tigrex (Apex)",
        122: "Seregios (Apex)",
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
    check_connection()
    for i in range(0, 7):
        data = get_4u_4g_data(i)
        monster_names = {**Monsters4U4G.large_monsters, **Monsters4U4G.small_monsters}
        if data[2]:
            print([monster_names.get(data[0]), *data[1:]])
