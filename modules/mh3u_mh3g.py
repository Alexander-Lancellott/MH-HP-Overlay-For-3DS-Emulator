import time
from math import ceil
from dataclasses import dataclass
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

    return [read(p4 - 0x7F5, 2), read(p4, 2), read(p4 + 0x4, 2), is_visible, p4]


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
            abnormal_status = {}

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
