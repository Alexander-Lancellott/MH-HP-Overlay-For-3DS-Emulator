from dataclasses import dataclass
from modules.utils import read, check_connection


def get_data(p0: int, offset: int):
    is_visible = True
    p1 = p0 + offset
    p2 = read(p1) + 0x10A8
    p3 = read(p2) + 0x360
    if p3 > 0x1408:
        is_visible = read(p3 - 0x1408, 1) != 7

    return [
        read(p3 + 0x59F0 + 40, 2),
        read(p3, 2),
        is_visible,
        p3
    ]


def get_xx_data(slot: int):
    pointer0 = read(0xD2CAA0)
    if pointer0 not in (137066272, 137074272):
        pointer0 = read(0xD30AA0)
        if pointer0 != 137074864:
            pointer0 = read(0xD3A8E0)

    return get_data(pointer0, 0x14 + (0x4 * slot))


@dataclass
class MonstersXX:
    large_monsters = {
        1: 'Rathian',
        2: 'Rathalos',
        3: 'Khezu',
        4: 'Basarios',
        5: 'Gravios',
        7: 'Diablos',
        8: 'Yian Kut-ku',
        9: 'Gypceros',
        10: 'Plesioth',
        11: 'Kirin',
        12: 'Lao-Shan Lung',
        13: 'Fatalis',
        14: 'Velocidrome',
        15: 'Gendrome',
        16: 'Iodrome',
        17: 'Cephadrome',
        18: 'Yian Garuga',
        19: 'Daimyo Hermitaur',
        20: 'Shogun Ceanataur',
        21: 'Congalala',
        22: 'Blangonga',
        23: 'Rajang',
        24: 'Kushala Daora',
        25: 'Chameleos',
        27: 'Teostra',
        30: 'Bulldrome',
        32: 'Tigrex',
        33: 'Akantor',
        34: 'Giadrome',
        36: 'Lavasioth',
        37: 'Nargacuga',
        38: 'Ukanlos',
        42: 'Barioth',
        43: 'Deviljho',
        44: 'Barroth',
        45: 'Uragaan',
        46: 'Lagiacrus',
        47: 'Royal Ludroth',
        49: 'Agnaktor',
        50: 'Alatreon',
        55: 'Duramboros',
        56: 'Niblesnarf',
        57: 'Zinogre',
        58: 'Amatsu',
        60: 'Arzuros',
        61: 'Lagombi',
        62: 'Volvidon',
        63: 'Brachydios',
        65: 'Kecha Wacha',
        66: 'Tetsucabra',
        67: 'Zamtrios',
        68: 'Najarala',
        69: 'Seltas Queen',
        70: 'Nerscylla',
        71: 'Gore Magala',
        72: 'Shagaru Magala',
        76: 'Seltas',
        77: 'Seregios',
        79: 'Malfestio',
        80: 'Glavenus',
        81: 'Astalos',
        82: 'Mizutsune',
        83: 'Gammoth',
        84: 'Nakarkos',
        85: 'Great Maccao',
        86: 'Valstrax',
        87: 'Ahtal-Neset',
        88: 'Ahtal-Ka',
        269: 'Crimson Fatalis',
        513: 'Gold Rathian',
        514: 'Silver Rathalos',
        525: 'White Fatalis',
        1025: 'Dreadqueen Rathian',
        1026: 'Dreadking Rathalos',
        1031: 'Bloodbath Diablos',
        1042: 'Deadeye Yian Garuga',
        1043: 'Stonefist Hermitaur',
        1044: 'Rustrazor Ceanataur',
        1056: 'Grimclaw Tigrex',
        1061: 'Silverwind Nargacuga',
        1069: 'Crystalbeard Uragaan',
        1081: 'Thunderlord Zinogre',
        1084: 'Redhelm Arzuros',
        1085: 'Snowbaron Lagombi',
        1090: 'Drilltusk Tetsucabra',
        1103: 'Nightcloak Malfestio',
        1104: 'Hellblade Glavenus',
        1105: 'Boltreaver Astalos',
        1106: 'Soulseer Mizutsune',
        1107: 'Elderfrost Gammoth',
        1303: 'Furious Rajang',
        1323: 'Savage Deviljho',
        1343: 'Raging Brachydios',
        1351: 'Chaotic Gore Magala',
    }

    small_monsters = {
        4097: 'Aptonoth',
        4098: 'Apceros',
        4099: 'Kelbi',
        4100: 'Mosswine',
        4101: 'Hornetaur',
        4102: 'Vespoid',
        4103: 'Felyne',
        4104: 'Melynx',
        4105: 'Velociprey',
        4106: 'Genprey',
        4107: 'Ioprey',
        4108: 'Cephalos',
        4109: 'Bullfango',
        4110: 'Popo',
        4111: 'Giaprey',
        4112: 'Anteka',
        4113: 'Great Thunderbug',
        4115: 'Remobra',
        4116: 'Hermitaur',
        4117: 'Ceanataur',
        4118: 'Conga',
        4119: 'Blango',
        4121: 'Rhenophlos',
        4122: 'Bnahabra',
        4123: 'Altaroth',
        4130: 'Jaggi',
        4131: 'Jaggia',
        4135: 'Ludroth',
        4136: 'Uroktor',
        4137: 'Slagtoth',
        4138: 'Gargwa',
        4140: 'Zamite',
        4141: 'Konchu',
        4142: 'Maccao',
        4143: 'Larinoth',
        4144: 'Moofah',
        4197: 'Expl. Rock'
    }


if __name__ == "__main__":
    check_connection()
    for i in range(0, 7):
        data = get_xx_data(i)
        monster_names = {**MonstersXX.large_monsters, **MonstersXX.small_monsters}
        if data[2]:
            print([monster_names.get(data[0]), *data[1:]])
