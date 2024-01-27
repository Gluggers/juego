from enum import Enum
# from lang import language
# from app.viewing import icon
# from app.images import image_paths, image_ids

# TODO REWORK THIS


class EquipmentSlot(Enum):
    NONE = 0  # Not equippable
    HEAD = 1  # Helmets, hats, etc.
    MAIN_HAND = 2  # Weapons.
    OFF_HAND = 3  # Shields.
    MAIN_BODY = 4  # Plate armour, chainmail, etc.
    LEGS = 5
    NECK = 6  # Amulets, necklaces, etc.
    AMMO = 7  # Arrows, etc.
    HANDS = 8  # Gloves, etc.
    FEET = 9  # Boots, etc.
    RING = 10  # Rings.
    BACK = 11  # Capes.
    WRIST = 12  # Bracelets, etc.


"""
class Equipment:
    # For default equipment slot items.
    EQUIPMENT_SLOT_DATA = {
        EquipmentSlot.HEAD: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Head Slot",
                language.LANG_ES: "Espacio de Cabeza",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For helmets, hats, and other headgear.",
                language.LANG_ES: "Para yelmos, sombreros, y otros tocados.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_HEAD_PATH,
            },
        },
        EquipmentSlot.MAIN_HAND: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Main Hand Slot",
                language.LANG_ES: "Espacio de Brazo Principal",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For swords, bows, staffs, and other weapons.",
                language.LANG_ES: "Para espadas, arcos, bastones, y otras armas.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_MAIN_HAND_PATH,
            },
        },
        EquipmentSlot.OFF_HAND: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Off Hand Slot",
                language.LANG_ES: "Espacio de Secundario",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For shields and secondary weapons.",
                language.LANG_ES: "Para escudos y armas secundarias.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_OFF_HAND_PATH,
            },
        },
        EquipmentSlot.MAIN_BODY: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Torso Slot",
                language.LANG_ES: "Espacio de Torso",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For clothing and armour for the torso.",
                language.LANG_ES: "Para ropa y armadura para el torso.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_BODY_PATH,
            },
        },
        EquipmentSlot.LEGS: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Legs Slot",
                language.LANG_ES: "Espacio de Piernas",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For clothing and armour for the legs.",
                language.LANG_ES: "Para ropa y armadura para las piernas.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_LEGS_PATH,
            },
        },
        EquipmentSlot.NECK: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Neck Slot",
                language.LANG_ES: "Espacio de Cuello",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For necklaces and other neck items.",
                language.LANG_ES: "Para collares y otras cosas para el cuello.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_NECK_PATH,
            },
        },
        EquipmentSlot.AMMO: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Ammo Slot",
                language.LANG_ES: "Espacio de Munición",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For arrows and other types of ammunition.",
                language.LANG_ES: "Para las flechas y otros tipos de munición.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_AMMO_PATH,
            },
        },
        EquipmentSlot.HANDS: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Hands Slot",
                language.LANG_ES: "Espacio de Manos",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For gloves and other hand gear.",
                language.LANG_ES: "Para guantes y otras equipo para las manos.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_HANDS_PATH,
            },
        },
        EquipmentSlot.FEET: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Feet Slot",
                language.LANG_ES: "Espacio de Pies",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For boots, shoes, and other footwear.",
                language.LANG_ES: "Para botas, zapatos, y otros calzados.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_FEET_PATH,
            },
        },
        EquipmentSlot.RING: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Ring Slot",
                language.LANG_ES: "Espacio de Anillos",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For rings.",
                language.LANG_ES: "Para anillos.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_RING_PATH,
            },
        },
        EquipmentSlot.BACK: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Back Slot.",
                language.LANG_ES: "Espacio de Espalda",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For capes and other items that go on the back.",
                language.LANG_ES: "Para capas y otras cosas para la espalda.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_BACK_PATH,
            },
        },
        EquipmentSlot.WRIST: {
            icon.IconField.NAME_INFO: {
                language.LANG_EN: "Wrist Slot",
                language.LANG_ES: "Espacio de Muñeca",
            },
            icon.IconField.DESCRIPTION_INFO: {
                language.LANG_EN: "For bracelets and other wrist items.",
                language.LANG_ES: "Para pulseras y otras cosas para la muñeca.",
            },
            icon.IconField.OPTION_ID_LIST: None,
            icon.IconField.IMAGE_PATH_DICT: {
                image_ids.ICON_IMAGE_ID: image_paths.EQUIPMENT_ICON_WRIST_PATH,
            },
        },
    }
"""