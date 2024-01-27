"""This module contains constants and information for menu options."""
from enum import Enum
from lang import language


class MenuOptionID(Enum):
    MORE_OPTIONS_OPTION = 0xFFFF
    YES_OPTION = 0x1
    NO_OPTION = 0x2
    CANCEL_OPTION = 0x3

    # OVERWORLD SIDE MENU OPTIONS
    INVENTORY_OPTION = 0x11
    HEROES_OPTION = 0x12
    SKILLS_OPTION = 0x13
    QUESTS_OPTION = 0x14
    CONFIGURATION_OPTION = 0x15
    SAVE_GAME_OPTION = 0x16
    LOAD_GAME_OPTION = 0x17
    QUIT_GAME_OPTION = 0x18
    SPELLS_OPTION = 0x19
    TOOLS_OPTION = 0x1A

    # ITEM OPTION IDS
    # USE_OPTION = 0x30 # For using an item with another.
    LIGHT_OPTION = 0x32  # For lighting items like logs on fire.
    EQUIP_OPTION = 0x33  # For equipping equippable items.
    UNEQUIP_OPTION = 0x34  # For unequipping equippable items.
    CRAFT_OPTION = 0x35  # For craftable items.
    IDENTIFY_OPTION = 0x36  # For identifying unknown items.
    READ_OPTION = 0x37  # For identifying readable items.
    EAT_OPTION = 0x38
    DRINK_OPTION = 0x39
    VIEW_ITEM_STATS_OPTION = 0x3A
    DISCARD_OPTION = 0x3B  # For discarding nonstackable items.
    DISCARD_1_OPTION = 0x3C  # For discarding stackable items.
    DISCARD_5_OPTION = 0x3D  # For discarding stackable items.
    DISCARD_X_OPTION = 0x3E  # For discarding stackable items.
    DISCARD_ALL_OPTION = 0x3F  # For discarding stackable items.

    # STORE OPTION IDS
    BUY_1_OPTION = 0x41  # For buying items in stores.
    BUY_5_OPTION = 0x42
    BUY_X_OPTION = 0x44
    BUY_ALL_OPTION = 0x45
    SELL_1_OPTION = 0x51  # For selling items in stores.
    SELL_5_OPTION = 0x52
    SELL_X_OPTION = 0x54
    SELL_ALL_OPTION = 0x55

    # LOOT OPTION IDS
    TAKE_1_OPTION = 0x61
    TAKE_5_OPTION = 0x62
    TAKE_X_OPTION = 0x65
    TAKE_ALL_OPTION = 0x65

    DEPOSIT_1_OPTION = 0x71
    DEPOSIT_5_OPTION = 0x72
    DEPOSIT_X_OPTION = 0x74
    DEPOSIT_ALL_OPTION = 0x75


class MenuOptionsList:
    # Some convenient option ID lists for common items.
    DEFAULT_LOG_OPTION_ID_LIST = [
        MenuOptionID.LIGHT_OPTION,
        MenuOptionID.CRAFT_OPTION,
        MenuOptionID.DISCARD_OPTION,
    ]

    DEFAULT_ITEM_MENU_OPTION_IDS = [
        MenuOptionID.DISCARD_OPTION,
    ]

    DEFAULT_STACKABLE_OPTION_ID_LIST = [
        MenuOptionID.DISCARD_1_OPTION,
        MenuOptionID.DISCARD_5_OPTION,
        MenuOptionID.DISCARD_X_OPTION,
        MenuOptionID.DISCARD_ALL_OPTION,
    ]


# Maps option ID to dict that maps language ID to the option name.
OPTION_NAME_INFO = {
    MenuOptionID.CANCEL_OPTION: language.MultiLanguageText(en='Cancel', es='Cancelar'),
    MenuOptionID.YES_OPTION: language.MultiLanguageText(en='Yes', es='Sí'),
    MenuOptionID.NO_OPTION: language.MultiLanguageText(en='No', es='No'),
    MenuOptionID.INVENTORY_OPTION: language.MultiLanguageText(en='Inventory', es='Inventario'),
    MenuOptionID.HEROES_OPTION: language.MultiLanguageText(en='Heroes', es='Heroes'),
    MenuOptionID.SKILLS_OPTION: language.MultiLanguageText(en='Skills', es='Habilidades'),
    MenuOptionID.QUESTS_OPTION: language.MultiLanguageText(en='Quests', es='Misiones'),
    MenuOptionID.CONFIGURATION_OPTION: language.MultiLanguageText(en='Configuration', es='Configuración'),
    MenuOptionID.SAVE_GAME_OPTION: language.MultiLanguageText(en='Save Game', es='Guardar Juego'),
    MenuOptionID.LOAD_GAME_OPTION: language.MultiLanguageText(en='Load Game', es='Cargar Juego'),
    MenuOptionID.QUIT_GAME_OPTION: language.MultiLanguageText(en='Quit Game', es='Salir del Juego'),
    MenuOptionID.SPELLS_OPTION: language.MultiLanguageText(en='Spells', es='Hechizos'),
    MenuOptionID.TOOLS_OPTION: language.MultiLanguageText(en='Toolbelt', es='Herramientas'),
    MenuOptionID.MORE_OPTIONS_OPTION: language.MultiLanguageText(en='More Options...', es='Más Opciones...'),
    MenuOptionID.DISCARD_OPTION: language.MultiLanguageText(en='Discard', es='Botar'),
    MenuOptionID.DISCARD_1_OPTION: language.MultiLanguageText(en='Discard 1', es='Botar 1'),
    MenuOptionID.DISCARD_5_OPTION: language.MultiLanguageText(en='Discard 5', es='Botar 5'),
    MenuOptionID.DISCARD_X_OPTION: language.MultiLanguageText(en='Discard X', es='Botar X'),
    MenuOptionID.DISCARD_ALL_OPTION: language.MultiLanguageText(en='Discard ALL', es='Botar TODOS'),
    MenuOptionID.LIGHT_OPTION: language.MultiLanguageText(en='Light', es='Encender'),
    MenuOptionID.EQUIP_OPTION: language.MultiLanguageText(en='Equip', es='Equipar'),
    MenuOptionID.UNEQUIP_OPTION: language.MultiLanguageText(en='Unequip', es='Desequipar'),
    MenuOptionID.CRAFT_OPTION: language.MultiLanguageText(en='Craft', es='Elaborar'),
    MenuOptionID.IDENTIFY_OPTION: language.MultiLanguageText(en='Identify', es='Identificar'),
    MenuOptionID.READ_OPTION: language.MultiLanguageText(en='Read', es='Leer'),
    MenuOptionID.EAT_OPTION: language.MultiLanguageText(en='Eat', es='Comer'),
    MenuOptionID.DRINK_OPTION: language.MultiLanguageText(en='Drink', es='Tomar'),
    MenuOptionID.VIEW_ITEM_STATS_OPTION: language.MultiLanguageText(en='Item Stats', es='Datos del Artículo'),
    MenuOptionID.BUY_1_OPTION: language.MultiLanguageText(en='Buy 1', es='Comprar 1'),
    MenuOptionID.SELL_1_OPTION: language.MultiLanguageText(en='Sell 1', es='Vender 1'),
    MenuOptionID.BUY_5_OPTION: language.MultiLanguageText(en='Buy 5', es='Comprar 5'),
    MenuOptionID.SELL_5_OPTION: language.MultiLanguageText(en='Sell 5', es='Vender 5'),
    MenuOptionID.BUY_ALL_OPTION: language.MultiLanguageText(en='Buy ALL', es='Comprar TODOS'),
    MenuOptionID.BUY_X_OPTION: language.MultiLanguageText(en='Buy X', es='Comprar X'),
    MenuOptionID.SELL_ALL_OPTION: language.MultiLanguageText(en='Sell ALL', es='Vender TODOS'),
    MenuOptionID.SELL_X_OPTION: language.MultiLanguageText(en='Sell X', es='Vender X'),
    MenuOptionID.TAKE_1_OPTION: language.MultiLanguageText(en='Take 1', es='Recoger 1'),
    MenuOptionID.TAKE_5_OPTION: language.MultiLanguageText(en='Take 5', es='Recoger 5'),
    MenuOptionID.TAKE_X_OPTION: language.MultiLanguageText(en='Take X', es='Recoger X'),
    MenuOptionID.TAKE_ALL_OPTION: language.MultiLanguageText(en='Take ALL', es='Recoger TODOS'),
}

# List of menu option IDs that are for the overworld menu.
OVERWORLD_MENU_OPTION_IDS = [
    MenuOptionID.INVENTORY_OPTION,
    MenuOptionID.HEROES_OPTION,
    MenuOptionID.SKILLS_OPTION,
    MenuOptionID.SPELLS_OPTION,
    MenuOptionID.TOOLS_OPTION,
    MenuOptionID.QUESTS_OPTION,
    MenuOptionID.CONFIGURATION_OPTION,
    MenuOptionID.SAVE_GAME_OPTION,
    MenuOptionID.LOAD_GAME_OPTION,
    MenuOptionID.QUIT_GAME_OPTION,
    MenuOptionID.CANCEL_OPTION,
]

COMPREHENSIVE_INVENTORY_ITEM_OPTION_SET = {
    MenuOptionID.VIEW_ITEM_STATS_OPTION,
    MenuOptionID.DISCARD_OPTION,
    MenuOptionID.DISCARD_1_OPTION,
    MenuOptionID.DISCARD_5_OPTION,
    MenuOptionID.DISCARD_X_OPTION,
    MenuOptionID.DISCARD_ALL_OPTION,
    MenuOptionID.LIGHT_OPTION,
    MenuOptionID.EQUIP_OPTION,
    MenuOptionID.CRAFT_OPTION,
    MenuOptionID.IDENTIFY_OPTION,
    MenuOptionID.READ_OPTION,
    MenuOptionID.EAT_OPTION,
    MenuOptionID.DRINK_OPTION,
    MenuOptionID.CANCEL_OPTION,
}

OVERWORLD_INVENTORY_ITEM_OPTION_SET = {
    MenuOptionID.VIEW_ITEM_STATS_OPTION,
    MenuOptionID.DISCARD_OPTION,
    MenuOptionID.DISCARD_1_OPTION,
    MenuOptionID.DISCARD_5_OPTION,
    MenuOptionID.DISCARD_X_OPTION,
    MenuOptionID.DISCARD_ALL_OPTION,
    MenuOptionID.LIGHT_OPTION,
    MenuOptionID.EQUIP_OPTION,
    MenuOptionID.CRAFT_OPTION,
    MenuOptionID.IDENTIFY_OPTION,
    MenuOptionID.READ_OPTION,
    MenuOptionID.EAT_OPTION,
    MenuOptionID.DRINK_OPTION,
    MenuOptionID.CANCEL_OPTION,
}

OVERWORLD_EQUIPMENT_ITEM_OPTION_SET = {
    MenuOptionID.VIEW_ITEM_STATS_OPTION,
    MenuOptionID.UNEQUIP_OPTION,
    MenuOptionID.CANCEL_OPTION,
}

SHOP_ITEM_OPTION_SET = {
    MenuOptionID.BUY_1_OPTION,
    MenuOptionID.BUY_5_OPTION,
    MenuOptionID.BUY_X_OPTION,
    MenuOptionID.BUY_ALL_OPTION,
    MenuOptionID.CANCEL_OPTION,
}

SHOP_MODE_INVENTORY_ITEM_OPTION_SET = {
    MenuOptionID.SELL_1_OPTION,
    MenuOptionID.SELL_5_OPTION,
    MenuOptionID.SELL_X_OPTION,
    MenuOptionID.SELL_ALL_OPTION,
    MenuOptionID.CANCEL_OPTION,
}

BATTLE_MODE_INVENTORY_ITEM_OPTION_SET = {
    MenuOptionID.DISCARD_OPTION,
    MenuOptionID.DISCARD_1_OPTION,
    MenuOptionID.DISCARD_5_OPTION,
    MenuOptionID.DISCARD_X_OPTION,
    MenuOptionID.DISCARD_ALL_OPTION,
    MenuOptionID.VIEW_ITEM_STATS_OPTION,
    MenuOptionID.EQUIP_OPTION,
    MenuOptionID.EAT_OPTION,
    MenuOptionID.DRINK_OPTION,
    MenuOptionID.CANCEL_OPTION,
}

BATTLE_LOOT_ITEM_OPTION_SET = {
    MenuOptionID.TAKE_1_OPTION,
    MenuOptionID.TAKE_5_OPTION,
    MenuOptionID.TAKE_X_OPTION,
    MenuOptionID.TAKE_ALL_OPTION,
    MenuOptionID.CANCEL_OPTION,
}


def get_option_name(option_id):
    return OPTION_NAME_INFO.get(option_id, language.MultiLanguageText()).get_text()
