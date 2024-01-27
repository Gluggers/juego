import os
import sys
import yaml
import pygame

# MAPPING BETWEEN PYGAME KEYS AND STRING VALUES
PYGAME_KEY_STR_MAPPING = {
    pygame.K_a: ("a", "A"),
    pygame.K_b: ("b", "B"),
    pygame.K_c: ("c", "C"),
    pygame.K_d: ("d", "D"),
    pygame.K_e: ("e", "E"),
    pygame.K_f: ("f", "F"),
    pygame.K_g: ("g", "G"),
    pygame.K_h: ("h", "H"),
    pygame.K_i: ("i", "I"),
    pygame.K_j: ("j", "J"),
    pygame.K_k: ("k", "K"),
    pygame.K_l: ("l", "L"),
    pygame.K_m: ("m", "M"),
    pygame.K_n: ("n", "N"),
    pygame.K_o: ("o", "O"),
    pygame.K_p: ("p", "P"),
    pygame.K_q: ("q", "Q"),
    pygame.K_r: ("r", "R"),
    pygame.K_s: ("s", "S"),
    pygame.K_t: ("t", "T"),
    pygame.K_u: ("u", "U"),
    pygame.K_v: ("v", "V"),
    pygame.K_w: ("w", "W"),
    pygame.K_x: ("x", "X"),
    pygame.K_y: ("y", "Y"),
    pygame.K_z: ("z", "Z"),
    pygame.K_1: ("1", "!"),
    pygame.K_2: ("2", "@"),
    pygame.K_3: ("3", "#"),
    pygame.K_4: ("4", "$"),
    pygame.K_5: ("5", "%"),
    pygame.K_6: ("6", "^"),
    pygame.K_7: ("7", "&"),
    pygame.K_8: ("8", "*"),
    pygame.K_9: ("9", "("),
    pygame.K_0: ("0", ")"),
    pygame.K_KP0: ("0", "0"),
    pygame.K_KP1: ("1", "1"),
    pygame.K_KP2: ("2", "2"),
    pygame.K_KP3: ("3", "3"),
    pygame.K_KP4: ("4", "4"),
    pygame.K_KP5: ("5", "5"),
    pygame.K_KP6: ("6", "6"),
    pygame.K_KP7: ("7", "7"),
    pygame.K_KP8: ("8", "8"),
    pygame.K_KP9: ("9", "9"),
    pygame.K_SPACE: (" ", " "),
}


def strip_yaml(path: str) -> list:
    if path:
        with open(path, encoding='utf-8') as yml:
            return list(yaml.safe_load_all(yml))
    return []


def get_base_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def get_resources_path():
    return os.path.join(get_base_path(), 'resources')


def get_images_path():
    return os.path.join(get_resources_path(), 'images')


def get_yaml_path():
    return os.path.join(get_resources_path(), 'yaml')


def get_fonts_path():
    return os.path.join(get_resources_path(), 'fonts')


def get_sound_path():
    return os.path.join(get_resources_path(), 'sound')


def get_music_path():
    return os.path.join(get_sound_path(), 'music')


def get_pygame_key_str(key_id, shift_on=False) -> str:
    """Returns the character string for the given key ID.

    Args:
        key_id: pygame key ID constant for the pressed key.
        shift_on: boolean that indicates whether the shift key
            was held when key_id was pressed. shift_on is used to
            get capital letters and certain special characters.

    Returns:
        String representation of the pressed key, depending on
        whether the shift button was pressed, as well.
    """
    ret_val = ''
    key_info = PYGAME_KEY_STR_MAPPING.get(key_id, None)
    if key_info:
        if shift_on:
            ret_val = key_info[1]
        else:
            ret_val = key_info[0]
    return ret_val


def parse_abbreviated_quantity(quantity_str):
    if quantity_str:
        # TODO. enhance #$$
        return int(quantity_str)
    return None


def get_abbreviated_quantity(quantity) -> str:
    """ Returns abbreviated string for the quantity.

    Abbreviates the given quantity and returns the string
    representation. Abbreviations are as follows:
        0 - 9999: as is.
        10,000 - 9,999,999: displays only the thousands. For example,
            10,982 becomes "10K", 918,999 becomes "918K", and
            5,691,192 becomes "5691K".
        10,000,000 - 9,999,999,999: displays only the millions. For
            example, 20,128,281 becomes "20M", and 5,291,289,291 becomes
            "5291M".
        10 billion and beyond: displays only the billions (B).

    Args:
        quantity: integer for which to create an abbreviated
            representation.

    Returns:
        String representation of the abbreviated quantity.
    """
    ret_string = "0"
    if quantity and quantity > 0:
        if quantity < 10000:
            ret_string = str(quantity)
        elif quantity < 10000000:
            ret_string = str(int(quantity / 1000)) + "K"
        elif quantity < 10000000000:
            ret_string = str(int(quantity / 1000000)) + "M"
        else:
            ret_string = str(int(quantity / 1000000000)) + "B"
    return ret_string
