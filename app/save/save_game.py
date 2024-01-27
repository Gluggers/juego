"""This module contains constants and data for saved game files and saving
the game."""

from lang import language

# SAVE AND LOAD PROMPT TEXT
SAVE_PROMPT_TEXT = language.MultiLanguageText(
    en='Are you sure you want to overwrite the save file?',
    es='Estás seguro/a de que deseas sobreescribir el archivo guardado?',
)

LOAD_PROMPT_TEXT = language.MultiLanguageText(
    en='Are you sure you want to load from the save file? You will lose any unsaved progress.',
    es='Estás seguro/a de que deseas cargar los datos del archivo guardado? Perderás todo el progreso '
       'que no sea guardado.',
)

SAVING_GAME_TEXT = language.MultiLanguageText(
    en='Saving progress...',
    es='Guardando el progreso...',
)

# SAVE FILE DATA FIELDS
GAME_LANGUAGE = "game_language"  # 0x100
MAP_ID = "curr_map_ID"  # 0x200
PROTAG_LOCATION = "protag_tile_loc"  # 0x210
PROTAG_IMAGE_SEQUENCE_ID = "curr_protag_image_sequence_id"
PROTAG_INVENTORY = "protag_inventory"
PROTAG_TOOLBELT = "protag_toolbelt"
PROTAG_EQUIPMENT = "protag_equipment"
PROTAG_STATS = "protag_levels"
PROTAG_RUN_ON = "protag_run_on"
PROTAG_RUN_ENERGY = "protag_run_energy"
