from re import Match
from dataclasses import dataclass
from modules.utils import read, check_connection


def get_data(p0: int, offset: int):
    p1 = p0 + offset
    p2 = read(p1) + 0xE28
    p3 = read(p2) + 0x3E8
    is_visible = read(p3 - 0x228 + 10, 3) != 786188
    return [
        read(p3 - 0x228, 1),
        read(p3, 2),
        is_visible,
        p3
    ]


def get_4u_4g_data(is_4u: Match[str] | None, slot: int):
    pointer0 = read(0xF031FC)
    if pointer0 != 137470816:
        pointer0 = read(0xF12214)

    if is_4u:
        pointer0 = read(0xF32004)

    return get_data(pointer0, 0x18 + (0x4 * slot))


@dataclass
class Monsters4U:
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
        55: "Slagtoth (Red)",
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
        68: "Bnahabra (Blue wings)",
        69: "Bnahabra (Yellow wings)",
        70: "Bnahabra (Green wings)",
        71: "Bnahabra (Red wings)",
        72: "Zamite",
        73: "Konchu (Yellow)",
        74: "Konchu (Green)",
        75: "Konchu (Blue)",
        76: "Konchu (Red)",
        81: "Rock (Large, light grey w/ green spots)",
        84: "Rock (Large, dark grey w/ dirty spots)",
        85: "Rock (Large, almost black)",
        86: "Rock (Large, icy)",
        87: "Rock (Large, icy ver 2)",
        104: "Rock (Large, brown)",
        106: "Cephalos",
        109: "Hermitaur",
        118: "Apceros",
        123: "Rock (Large, light grey no spots)"
    }


if __name__ == "__main__":
    is_4u = True
    check_connection()
    m1 = get_4u_4g_data(is_4u, 0)
    m2 = get_4u_4g_data(is_4u, 1)
    m3 = get_4u_4g_data(is_4u, 2)
    m4 = get_4u_4g_data(is_4u, 3)
    m5 = get_4u_4g_data(is_4u, 4)
    m6 = get_4u_4g_data(is_4u, 5)

    print(m1)
    print(m2)
    print(m3)
    print(m4)
    print(m5)
    print(m6)
