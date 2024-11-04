import time
from dataclasses import dataclass
from modules.utils import read, check_connection, max_monsters, ResultType


def get_data(p0: int, offset: int):
    is_visible = False
    p1 = p0 + offset
    p2 = read(p1) + 0x7F8
    if p2 > 0x965:
        is_visible = (
            read(p2 + 0x14A, 2) == 0x3E8
            and read(p2 + 0x8, 4) == 0x3F800000
            and read(p2 + 0xC, 2) == read(p2 + 0x4, 2)
        )

    return [read(p2 - 0x7F5, 2), read(p2, 2), read(p2 + 0x4, 2), is_visible, p2]


def get_3u_3g_data(show_small_monsters: bool):
    large_monsters = Monsters3U3G.large_monsters
    small_monsters = Monsters3U3G.small_monsters
    large_monster_results = []
    small_monster_results = []
    is_eur = read(0x0708AD88, 8) == 0x40000000B1D00
    offset = 0x9AC if is_eur else 0x56C
    pointer0 = 0
    addresses = {
        0xBEB670: {0x8209168},
        0xBE17D8: {0x8205288}
    }
    for address, target_value in addresses.items():
        pointer0 = read(address)
        if pointer0 in target_value:
            break

    for i in range(0, max_monsters):
        data = get_data(pointer0, offset + (0x220 * i))
        name = data[0]
        hp = data[1]
        initial_hp = data[2]
        is_visible = data[3]
        pointer = data[4]
        if large_monsters.get(name) and is_visible:
            monster_size = int(round(read(pointer - 0x764, 4, result_type=ResultType.FLOAT) * 100, 2))
            large_monster_results.append([name, hp, initial_hp, monster_size])
        if small_monsters.get(name) and is_visible and show_small_monsters:
            small_monster_results.append([name, hp, initial_hp])

    return large_monster_results + small_monster_results


@dataclass
class Monsters3U3G:
    large_monsters = {
        257: {
            "name": "Rathian",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        258: {
            "name": "Rathalos",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        259: {
            "name": "Qurupeco",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        260: {
            "name": "Gigginox",
            "crowns": {"g": 116, "s": 111, "m": 92}
        },
        261: {
            "name": "Barioth",
            "crowns": {"g": 116, "s": 111, "m": 92}
        },
        262: {
            "name": "Diablos",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        263: {
            "name": "Deviljho",
            "crowns": {"g": 128, "s": 120, "m": 90}
        },
        264: {
            "name": "Barroth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        265: {
            "name": "Uragaan",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        268: {
            "name": "Great Jaggi",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        270: {
            "name": "Great Baggi",
            "crowns": {"g": 137, "s": 125, "m": 83}
        },
        271: {
            "name": "Lagiacrus",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        272: {
            "name": "Royal Ludroth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        274: {
            "name": "Gobul",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        275: {
            "name": "Agnaktor",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        276: {
            "name": "Ceadeus",
            "crowns": {"g": None, "s": None, "m": None}
        },
        280: {
            "name": "Alatreon",
            "crowns": {"g": None, "s": None, "m": None}
        },
        281: {
            "name": "Jhen Mohran",
            "crowns": {"g": None, "s": None, "m": None}
        },
        297: {
            "name": "Zinogre",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        298: {
            "name": "Arzuros",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        299: {
            "name": "Lagombi",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        300: {
            "name": "Volvidon",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        301: {
            "name": "Great Wroggi",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        302: {
            "name": "Duramboros",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        303: {
            "name": "Nibelsnarf",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        307: {
            "name": "Crimson Qurupeco",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        308: {
            "name": "Baleful Gigginox",
            "crowns": {"g": 116, "s": 111, "m": 92}
        },
        309: {
            "name": "Sand Barioth",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        310: {
            "name": "Jade Barroth",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        311: {
            "name": "Steel Uragaan",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        312: {
            "name": "Purple Ludroth",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        313: {
            "name": "Glacial Agnaktor",
            "crowns": {"g": 116, "s": 111, "m": 92}
        },
        314: {
            "name": "Black Diablos",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        315: {
            "name": "Nargacuga",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        316: {
            "name": "Green Nargacuga",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        317: {
            "name": "Lucent Nargacuga",
            "crowns": {"g": None, "s": None, "m": None}
        },
        318: {
            "name": "Pink Rathian",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        319: {
            "name": "Gold Rathian",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        320: {
            "name": "Azure Rathalos",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        321: {
            "name": "Silver Rathalos",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        322: {
            "name": "Plesioth",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        323: {
            "name": "Green Plesioth",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        324: {
            "name": "Ivory Lagiacrus",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        325: {
            "name": "Abyssal Lagiacrus",
            "crowns": {"g": None, "s": None, "m": None}
        },
        326: {
            "name": "Goldbeard Ceadeus",
            "crowns": {"g": None, "s": None, "m": None}
        },
        327: {
            "name": "Savage Deviljho",
            "crowns": {"g": 128, "s": 120, "m": 90}
        },
        328: {
            "name": "Stygian Zinogre",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        329: {
            "name": "Rust Duramboros",
            "crowns": {"g": 123, "s": 117, "m": 98}
        },
        330: {
            "name": "Brachydios",
            "crowns": {"g": 123, "s": 115, "m": 90}
        },
        331: {
            "name": "Dire Miralis",
            "crowns": {"g": None, "s": None, "m": None}
        },
        341: {
            "name": "Hallowed Jhen Mohran",
            "crowns": {"g": None, "s": None, "m": None}
        },
    }

    small_monsters = {
        266: "Jaggi",
        267: "Jaggia",
        269: "Baggi",
        273: "Ludroth",
        277: "Uroktor",
        278: "Delex",
        279: "Epioth",
        282: "Giggi",
        283: "Aptonoth",
        284: "Popo",
        285: "Rhenoplos",
        286: "Felyne",
        287: "Melynx",
        288: "Fish",
        289: "Altaroth",
        290: "Kelbi",
        291: "Giggi Sac",
        292: "Bnahabra",
        293: "Bnahabra",
        294: "Bnahabra",
        295: "Bnahabra",
        296: "Rock",
        304: "Wroggi",
        305: "Slagtoth",
        306: "Gargwa",
        332: "Bullfango",
        333: "Anteka",
        334: "Slagtoth",
        335: "Rock",
        336: "Rock",
        337: "Rock",
        338: "Rock",
        339: "Rock",
        340: "Rock",
    }


if __name__ == "__main__":
    start_time = time.time()
    check_connection()
    monsters = get_3u_3g_data(True)
    for monster in monsters:
        large_monster = Monsters3U3G.large_monsters.get(monster[0])
        small_monster_name = Monsters3U3G.small_monsters.get(monster[0])
        if large_monster:
            print([large_monster["name"], *monster[1::]])
        if small_monster_name:
            print([small_monster_name, *monster[1::]])
    end_time = time.time()
    print(end_time - start_time)
