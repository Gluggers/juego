from enum import Enum


class CombatType(Enum):
    NONE = 0x1  # Not combat-related.
    MELEE = 0x2
    RANGED = 0x3
    WHITE_MAGIC = 0x4
    BLACK_MAGIC = 0x4


class DamageType(Enum):
    NONE = 0x1  # No damage
    NEUTRAL = 0x2
    MELEE = 0x100
    RANGED = 0x200
    MAGIC_AIR = 0x300
    MAGIC_WATER = 0x301
    MAGIC_EARTH = 0x302
    MAGIC_FIRE = 0x303
    MAGIC_ICE = 0x310
    MAGIC_ELECTRIC = 0x311
    MAGIC_NATURE = 0x312
    MAGIC_HOLY = 0x313
    MAGIC_DARK = 0x314
    POISON = 0x500
