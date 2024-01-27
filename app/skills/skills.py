"""This module contains constants related to skills for the game.

The module contains skill IDs, skill names and their various translations,
and experience and level information and methods.

For experience, the following formula is used:
- Level 1 = 0 experience
- To calculate the experience for levels N for N = 2 to 100:
    - Take the sum from x = 1 to N-1 of floor(100*2^(x/11) + 32x + 49.425)

1,000,000 experience is required to reach level 100. Characters cannot have
more than 1 million experience in a given skill.
"""

import logging
from enum import Enum
from lang import language


class SkillID(Enum):
    SMITHING = 0x8
    HERBLORE = 0x9
    CRAFTING = 0xa
    COOKING = 0xb
    FIREMAKING = 0xc
    CONSTRUCTION = 0xd
    MINING = 0x11
    FARMING = 0x12
    FISHING = 0x13
    WOODCUTTING = 0x14


# TODO - turn these into individual classes
class Skill:
    # Maps skill IDs to their names in the various languages.
    SKILL_ID_NAME_MAPPING = {
        SkillID.SMITHING: language.MultiLanguageText(en='SMITHING', es='HERRERÍA'),
        SkillID.HERBLORE: language.MultiLanguageText(en='HERBLORE', es='BOTÁNICA'),
        SkillID.CRAFTING: language.MultiLanguageText(en='CRAFTING', es='ARTESANÍA'),
        SkillID.COOKING: language.MultiLanguageText(en='COOKING', es='COCINA'),
        SkillID.FIREMAKING: language.MultiLanguageText(en='FIREMAKING', es='DOMINIO DEL FUEGO'),
        SkillID.CONSTRUCTION: language.MultiLanguageText(en='CONSTRUCTION', es='CONSTRUCCIÓN'),
        SkillID.MINING: language.MultiLanguageText(en='MINING', es='MINERÍA'),
        SkillID.FARMING: language.MultiLanguageText(en='FARMING', es='AGRICULTURA'),
        SkillID.FISHING: language.MultiLanguageText(en='FISHING', es='PESCA'),
        SkillID.WOODCUTTING: language.MultiLanguageText(en='WOODCUTTING', es='TALA DE ÁRBOLES'),
    }

    SKILL_ID_LIST = list(SKILL_ID_NAME_MAPPING.keys())

    LEVEL_UP_MESSAGE_INFO = language.MultiLanguageText(
        en='You gained {0} level(s) in {1}! You are now level {2} in {1}.',
        es='Has logrado {0} nivel(es) en {1}! Ya tienes un nivel de {2} en {1}',
    )

    DEFAULT_LEVEL = 1
    DEFAULT_EXP = 0
    MIN_LEVEL = 1
    MIN_EXP = 0

    LEVEL_EXP_MAPPING = {
        1: 0,
        2: 187,
        3: 413,
        4: 679,
        5: 985,
        6: 1331,
        7: 1718,
        8: 2146,
        9: 2616,
        10: 3129,
        11: 3686,
        12: 4287,
        13: 4933,
        14: 5625,
        15: 6364,
        16: 7150,
        17: 7985,
        18: 8870,
        19: 9806,
        20: 10794,
        21: 11836,
        22: 12932,
        23: 14085,
        24: 15296,
        25: 16567,
        26: 17899,
        27: 19295,
        28: 20756,
        29: 22285,
        30: 23884,
        31: 25555,
        32: 27301,
        33: 29125,
        34: 31030,
        35: 33019,
        36: 35095,
        37: 37262,
        38: 39524,
        39: 41885,
        40: 44350,
        41: 46922,
        42: 49607,
        43: 52410,
        44: 55337,
        45: 58394,
        46: 61587,
        47: 64923,
        48: 68409,
        49: 72053,
        50: 75862,
        51: 79846,
        52: 84014,
        53: 88376,
        54: 92942,
        55: 97724,
        56: 102733,
        57: 107982,
        58: 113485,
        59: 119256,
        60: 125310,
        61: 131664,
        62: 138335,
        63: 145342,
        64: 152705,
        65: 160444,
        66: 168582,
        67: 177143,
        68: 186152,
        69: 195637,
        70: 205626,
        71: 216150,
        72: 227241,
        73: 238935,
        74: 251268,
        75: 264280,
        76: 278013,
        77: 292512,
        78: 307825,
        79: 324002,
        80: 341098,
        81: 359170,
        82: 378280,
        83: 398493,
        84: 419879,
        85: 442512,
        86: 466471,
        87: 491841,
        88: 518711,
        89: 547176,
        90: 577338,
        91: 609305,
        92: 643193,
        93: 679125,
        94: 717231,
        95: 757651,
        96: 800533,
        97: 846035,
        98: 894325,
        99: 945583,
        100: 1000000,
    }

    MAX_LEVEL = len(LEVEL_EXP_MAPPING)
    DEFAULT_MAX_XP = 1000000
    MAX_EXP = LEVEL_EXP_MAPPING.get(MAX_LEVEL, DEFAULT_MAX_XP)

    # Returns the lowest level that the given experience will satisfy.
    @staticmethod
    def get_level_from_experience(experience):
        """Returns the lowest level possible for the given experience."""

        ret_level = Skill.MIN_LEVEL
        for i in range(Skill.MAX_LEVEL):
            if Skill.LEVEL_EXP_MAPPING.get(i + 1, Skill.DEFAULT_MAX_XP) <= experience:
                ret_level = i + 1
            else:
                break

        return ret_level

    @staticmethod
    def get_experience_from_level(level):
        """Returns the minimum required experience for the given level."""

        ret_exp = Skill.MIN_EXP
        if level and (level >= Skill.MIN_LEVEL) and (level <= Skill.MAX_LEVEL):
            ret_exp = Skill.LEVEL_EXP_MAPPING.get(level, Skill.DEFAULT_MAX_XP)

        logging.debug("Exp for level %d is %d", level, ret_exp)
        return ret_exp

    # Assumes exp is a valid experience value for the level.
    @staticmethod
    def get_experience_to_next_level(level, curr_exp):
        """Returns the remaining experience for the specified level.

        Args:
            level: the level to reach.
            curr_exp: the current starting experience.

        Returns:
            The remaining experience to go from curr_exp to the experience
            required for the specified level. Returns 0 for invalid
            argument values or if curr_exp already achieves the specified level.
        """

        ret_exp = 0

        if (curr_exp is not None) \
                and curr_exp >= Skill.MIN_EXP \
                and level \
                and (level < Skill.MAX_LEVEL) \
                and (level >= Skill.MIN_LEVEL):
            next_level = level + 1
            next_level_exp = Skill.get_experience_from_level(next_level)

            if next_level_exp:
                ret_exp = max(0, next_level_exp - curr_exp)

        return ret_exp

    @staticmethod
    def get_skill_name(skill_id):
        """Returns the skill name for the given skill ID """

        ret_name = ''
        if skill_id is not None:
            ret_name = Skill.SKILL_ID_NAME_MAPPING.get(skill_id, language.MultiLanguageText).get_text()
        return ret_name
