import os
from util import util

DISPLAY_PATH = os.path.join(util.get_images_path(), 'interfaces') + os.sep
DISPLAY_PATTERN_PATH = os.path.join(DISPLAY_PATH, 'patterns') + os.sep
SPRITES_PATH = os.path.join(util.get_images_path(), 'sprites') + os.sep
PROTAGONIST_SPRITES_PATH = os.path.join(SPRITES_PATH, 'main_char_ow') + os.sep
ICONS_PATH = os.path.join(util.get_images_path(), 'icons') + os.sep
EQUIPMENT_ICON_PATH = os.path.join(ICONS_PATH, 'equipment') + os.sep

DEFAULT_TEXT_CONTINUE_ICON_PATH = DISPLAY_PATH + 'text_continue_icon2_10x10.png'  # [0]
DEFAULT_MENU_SELECTION_ICON_PATH = DISPLAY_PATH + 'menu_selection_icon2_10x10.png'  # [0]
OW_TOP_DISPLAY_BACKGROUND_PATH = DISPLAY_PATH + 'ow_top_display_background_672x48.png'  # [0]
OW_TOP_HEALTH_DISPLAY_BACKGROUND_PATH = DISPLAY_PATH + 'ow_top_health_display_264x56.png'  # [0]
OW_BOTTOM_TEXT_DISPLAY_BACKGROUND_PATH = DISPLAY_PATH + 'ow_bottom_text_display_640x96.png'  # [0]
OW_SIDE_MENU_BACKGROUND_PATH = DISPLAY_PATH + 'ow_side_menu_220x416.png'  # [0]
INVENTORY_BACKGROUND_PATH = DISPLAY_PATH + 'inventory_background_672x480.png'  # [0]
INVENTORY_BASIC_TITLE_BACKGROUND_PATH = DISPLAY_PATH + ''  # [0]
INVENTORY_BASIC_ITEM_LISTING_FULL_BACKGROUND_PATH = DISPLAY_PATH + ''  # [0]
INVENTORY_BASIC_ITEM_LISTING_SHORT_BACKGROUND_PATH = DISPLAY_PATH + ''  # [0]
INVENTORY_BASIC_ITEM_DETAILS_BACKGROUND_PATH = DISPLAY_PATH + ''  # [0]
INVENTORY_BASIC_INSTRUCTIONS_BACKGROUND_PATH = DISPLAY_PATH + ''  # [0]
ITEM_LISTING_SELECTED_DEFAULT_PATH = DISPLAY_PATH + 'item_listing_selected_image2_60x60.png'  # [0]
ITEM_LISTING_UNSELECTED_DEFAULT_PATH = DISPLAY_PATH + 'item_listing_unselected_image3_60x60.png'  # [0]
ITEM_LISTING_SELECTED_ENLARGED_BACKGROUND_PATH = DISPLAY_PATH \
                                                 + 'item_listing_selected_image_background_enlarged2_120x120.png'
ITEM_LISTING_CONT_UP_PATH = DISPLAY_PATH + 'item_listing_continue_up_icon_30x30.png'  # [0]
ITEM_LISTING_CONT_DOWN_PATH = DISPLAY_PATH + 'item_listing_continue_down_icon_30x30.png'  # [0]

EQUIPMENT_ICON_HEAD_PATH = EQUIPMENT_ICON_PATH + "head_icon_50x50_dk.png"  # [0]
EQUIPMENT_ICON_NECK_PATH = EQUIPMENT_ICON_PATH + "neck_icon_50x50_dk.png"  # [0]
EQUIPMENT_ICON_BODY_PATH = EQUIPMENT_ICON_PATH + "head_icon_50x50_dk.png"  # [0]
EQUIPMENT_ICON_LEGS_PATH = EQUIPMENT_ICON_PATH + "legs_icon_50x50_dk.png"  # [0]
EQUIPMENT_ICON_FEET_PATH = EQUIPMENT_ICON_PATH + "head_icon_50x50_dk.png"  # [0]
EQUIPMENT_ICON_AMMO_PATH = EQUIPMENT_ICON_PATH + "head_icon_50x50_dk.png"  # [0]
EQUIPMENT_ICON_BACK_PATH = EQUIPMENT_ICON_PATH + "head_icon_50x50_dk.png"  # [0]
EQUIPMENT_ICON_MAIN_HAND_PATH = EQUIPMENT_ICON_PATH + "head_icon_50x50_dk.png"  # [0]
EQUIPMENT_ICON_OFF_HAND_PATH = EQUIPMENT_ICON_PATH + "head_icon_50x50_dk.png"  # [0]
EQUIPMENT_ICON_HANDS_PATH = EQUIPMENT_ICON_PATH + "head_icon_50x50_dk.png"  # [0]
EQUIPMENT_ICON_WRIST_PATH = EQUIPMENT_ICON_PATH + "head_icon_50x50_dk.png"  # [0]
EQUIPMENT_ICON_RING_PATH = EQUIPMENT_ICON_PATH + "head_icon_50x50_dk.png"  # [0]

PATTERN_1_CORNER_NW_PATH = DISPLAY_PATTERN_PATH + 'background_1_corner_nw_11x11.png'  # [0]
PATTERN_1_CORNER_NE_PATH = DISPLAY_PATTERN_PATH + 'background_1_corner_ne_11x11.png'  # [0]
PATTERN_1_CORNER_SE_PATH = DISPLAY_PATTERN_PATH + 'background_1_corner_se_11x11.png'  # [0]
PATTERN_1_CORNER_SW_PATH = DISPLAY_PATTERN_PATH + 'background_1_corner_sw_11x11.png'  # [0]

PROT_RANGER_F_OW_DEFAULT = PROTAGONIST_SPRITES_PATH + "ranger_f_face_south_32x36_af.png"  # [3]
PROT_RANGER_F_OW_FACE_NORTH = PROTAGONIST_SPRITES_PATH + "ranger_f_face_north_32x36_af.png"  # [3]
PROT_RANGER_F_OW_FACE_EAST = PROTAGONIST_SPRITES_PATH + "ranger_f_face_east_32x36_af.png"  # [3]
PROT_RANGER_F_OW_FACE_SOUTH = PROTAGONIST_SPRITES_PATH + "ranger_f_face_south_32x36_af.png"  # [3]
PROT_RANGER_F_OW_FACE_WEST = PROTAGONIST_SPRITES_PATH + "ranger_f_face_west_32x36_af.png"  # [3]
PROT_RANGER_F_OW_WALK1_NORTH = PROTAGONIST_SPRITES_PATH + "ranger_f_walk1_north_32x36_af.png"  # [3]
PROT_RANGER_F_OW_WALK1_EAST = PROTAGONIST_SPRITES_PATH + "ranger_f_walk1_east_32x36_af.png"  # [3]
PROT_RANGER_F_OW_WALK1_SOUTH = PROTAGONIST_SPRITES_PATH + "ranger_f_walk1_south_32x36_af.png"  # [3]
PROT_RANGER_F_OW_WALK1_WEST = PROTAGONIST_SPRITES_PATH + "ranger_f_walk1_west_32x36_af.png"  # [3]
PROT_RANGER_F_OW_WALK2_NORTH = PROTAGONIST_SPRITES_PATH + "ranger_f_walk2_north_32x36_af.png"  # [3]
PROT_RANGER_F_OW_WALK2_EAST = PROTAGONIST_SPRITES_PATH + "ranger_f_walk2_east_32x36_af.png"  # [3]
PROT_RANGER_F_OW_WALK2_SOUTH = PROTAGONIST_SPRITES_PATH + "ranger_f_walk2_south_32x36_af.png"  # [3]
PROT_RANGER_F_OW_WALK2_WEST = PROTAGONIST_SPRITES_PATH + "ranger_f_walk2_west_32x36_af.png"  # [3]
PROT_RANGER_F_BATTLE_DEFAULT = PROTAGONIST_SPRITES_PATH + "ranger_f_face_south_32x36_af.png"  # [3]
PROT_RANGER_F_BATTLE_STAND = PROTAGONIST_SPRITES_PATH + "ranger_f_face_south_32x36_af.png"  # [3]
PROT_RANGER_F_BATTLE_ATTACK = PROTAGONIST_SPRITES_PATH + "ranger_f_face_south_32x36_af.png"  # [3]
PROT_RANGER_F_BATTLE_FAINTED = PROTAGONIST_SPRITES_PATH + "ranger_f_face_south_32x36_af.png"  # [3]
