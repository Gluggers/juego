TILE_SIZE = 32


# TILE ACCESSIBILITY FLAGS
class Accessibility:
    TILE_NOT_ACCESSIBLE_F = 0x0  # Player cannot access this tile.
    WALKABLE_F = 0x1  # For walking.
    CANOEABLE_F = 0x2  # For canoeing.
    SAILABLE_F = 0x4  # For sailing.
    FLYABLE_F = 0x8  # For flying.

    # By default, tiles can be walked on or flown over.
    DEFAULT_ACCESSIBILITY = (WALKABLE_F | FLYABLE_F)
