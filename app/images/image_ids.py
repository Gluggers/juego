from enum import Enum

from app.maps import directions

ICON_IMAGE_ID = 10


class ImageSequenceID(Enum):
    DEFAULT = 1
    OBJ_SPRITE = 20

    FACE_NORTH = 100
    FACE_EAST = 101
    FACE_SOUTH = 102
    FACE_WEST = 103
    WALK_NORTH = 110
    WALK_EAST = 120
    WALK_SOUTH = 130
    WALK_WEST = 140


# Maps entity animation IDs to a dict that maps direction IDs
# to a list of image_ids that represent the sequence of sprite images
# to blit when the protagonist performs the particular skill
# when facing the particular direction.
# If the list contains in an index, then that represents
# blitting the previous standing overworld image for the Protagonist.
# An empty list means just use the previous standing overworld image.
def get_direction_sequence_id(direction):
    """Returns image sequence ID for the sprite for facing the specified
    direction.

    Args:
        direction: direction ID for which to retrieve the image sequence ID.
    """
    if direction == directions.CardinalDirection.NORTH:
        return ImageSequenceID.FACE_NORTH
    elif direction == directions.CardinalDirection.EAST:
        return ImageSequenceID.FACE_EAST
    elif direction == directions.CardinalDirection.SOUTH:
        return ImageSequenceID.FACE_SOUTH
    elif direction == directions.CardinalDirection.WEST:
        return ImageSequenceID.FACE_WEST
    return None
