from dataclasses import dataclass
from modules.utils import read, check_connection, max_monsters


def get_data(p0: int, offset: int):
    is_visible = False
    p1 = p0 + offset
    p2 = read(p1) + 0x7F8
    if p2 > 0x965:
        is_visible = read(p2 + 0x149, 3) == 0x3E800

    return [read(p2 - 0x7F5, 2), read(p2, 2), is_visible, p2]


def get_3u_3g_data(slot: int):
    is_eur = read(0x0708AD88, 8) == 0x40000000B1D00
    offset = 0x9AC if is_eur else 0x56C
    pointer0 = read(0xBEB670)
    if read(0xBEB670) != 0x8209168:
        pointer0 = read(0xBE17D8)
    return get_data(pointer0, offset + (0x220 * slot))


@dataclass
class Monsters3U3G:
    large_monsters = {
        257: "Rathian",
        258: "Rathalos",
        259: "Qurupeco",
        260: "Gigginox",
        261: "Barioth",
        262: "Diablos",
        263: "Deviljho",
        264: "Barroth",
        265: "Uragaan",
        268: "Great Jaggi",
        270: "Great Baggi",
        271: "Lagiacrus",
        272: "Royal Ludroth",
        274: "Gobul",
        275: "Agnaktor",
        276: "Ceadeus",
        280: "Alatreon",
        281: "Jhen Mohran",
        297: "Zinogre",
        298: "Arzuros",
        299: "Lagombi",
        300: "Volvidon",
        301: "Great Wroggi",
        302: "Duramboros",
        303: "Nibelsnarf",
        307: "Crimson Qurupeco",
        308: "Baleful Gigginox",
        309: "Sand Barioth",
        310: "Jade Barroth",
        311: "Steel Uragaan",
        312: "Purple Ludroth",
        313: "Glacial Agnaktor",
        314: "Black Diablos",
        315: "Nargacuga",
        316: "Green Nargacuga",
        317: "Lucent Nargacuga",
        318: "Pink Rathian",
        319: "Gold Rathian",
        320: "Azure Rathalos",
        321: "Silver Rathalos",
        322: "Plesioth",
        323: "Green Plesioth",
        324: "Ivory Lagiacrus",
        325: "Abyssal Lagiacrus",
        326: "Goldbeard Ceadeus",
        327: "Savage Deviljho",
        328: "Stygian Zinogre",
        329: "Rust Duramboros",
        330: "Brachydios",
        331: "Dire Miralis",
        341: "Hallowed Jhen Mohran",
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
    check_connection()
    pointers = []
    for i in range(0, max_monsters):
        data = get_3u_3g_data(i)
        monster_names = {**Monsters3U3G.large_monsters, **Monsters3U3G.small_monsters}
        if data[2] and data[3] not in pointers:
            print([monster_names.get(data[0]), *data[1:]])
        pointers.append(data[3])
