import pygame

from app.viewing import colors
from util import util

# TODO CHANGE HOW WE LOAD FONTS - use yaml file?

# FONT ID NUMBERS
DEFAULT_FONT_ID = 0x1
OW_HEALTH_DISPLAY_FONT_ID = 0x2
OW_BOTTOM_TEXT_FONT_ID = 0x3
OW_SIDE_MENU_FONT_ID = 0x4
OW_BOTTOM_MENU_FONT_ID = 0x5
SELECTION_TOP_DISPLAY_FONT_ID = 0x10
SELECTION_NAME_FONT_ID = 0x11
SELECTION_DESCRIPTION_FONT_ID = 0x12
SELECTION_SUBTITLE_FONT_ID = 0x13
SELECTION_SUPERTEXT_FONT_ID = 0x14
SELECTION_MENU_FONT_ID = 0x15
SELECTION_BOTTOM_TEXT_FONT_ID = 0x16
CHAR_EQUIP_STATS_FONT_ID = 0x20
ITEM_EQUIP_STATS_FONT_ID = 0x21

# FONT INFO FIELDS
FONT_SIZE_FIELD = 0x1
FONT_PATH_FIELD = 0x2

# FONT INFO
FONT_INFO = {
    DEFAULT_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    OW_HEALTH_DISPLAY_FONT_ID: {
        FONT_SIZE_FIELD: 18,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    OW_BOTTOM_TEXT_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    OW_BOTTOM_MENU_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    OW_SIDE_MENU_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    SELECTION_TOP_DISPLAY_FONT_ID: {
        FONT_SIZE_FIELD: 22,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    SELECTION_NAME_FONT_ID: {
        FONT_SIZE_FIELD: 22,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    SELECTION_DESCRIPTION_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    SELECTION_SUBTITLE_FONT_ID: {
        FONT_SIZE_FIELD: 18,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    SELECTION_SUPERTEXT_FONT_ID: {
        FONT_SIZE_FIELD: 11,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    SELECTION_MENU_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    SELECTION_BOTTOM_TEXT_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    CHAR_EQUIP_STATS_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
    ITEM_EQUIP_STATS_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: util.get_fonts_path() + "/DejaVuSansMono.ttf"
    },
}

FONT_SIZE_DEFAULT = 16
FONT_COLOR_DEFAULT = colors.COLOR_BLACK
FONT_PATH_DEFAULT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"


class Fonts:
    # Will contain loaded fonts.
    font_listing = {}

    @classmethod
    def add_font_to_listing(cls, font_id, font_obj):
        if font_obj and (font_id is not None):
            cls.font_listing[font_id] = font_obj

    @classmethod
    def get_font(cls, font_id):
        return cls.font_listing.get(font_id, None)

    @classmethod
    def init_fonts(cls):
        for font_id, font_info in FONT_INFO.items():
            font_obj = pygame.font.Font(
                font_info.get(
                    FONT_PATH_FIELD,
                    FONT_PATH_DEFAULT,
                ),
                font_info.get(
                    FONT_SIZE_FIELD,
                    FONT_SIZE_DEFAULT
                )
            )

            if font_obj:
                cls.add_font_to_listing(font_id, font_obj)
