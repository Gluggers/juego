import logging
import glob
import os
from enum import Enum
from app.battle import battle
from app.equipment import equipment
from app.interactions import interaction
from app.viewing import icon, menu_options
from lang import language
from util import util


class ItemProperties:
    STACKABLE_F = 0x1
    SELLABLE_F = 0x2
    CONSUMABLE_F = 0x4
    QUEST_ITEM_F = 0x8  # Special quest-related item that shouldn't be sold or destroyed.
    ALCHABLE_F = 0x10
    COOKABLE_FIRE_F = 0x20
    COOKABLE_RANGE_F = 0x40
    TOOL_ITEM_F = 0x80


class ItemID(Enum):
    CURRENCY_GOLD_COIN = '0095bc48-4fc1-4b4f-b927-3ca54cdc3deb'
    HAMMER_TOOL = 'd9b845ce-a519-4461-9d73-f458d6e79b8e'


class Item(icon.ViewingIcon):
    ICON_WIDTH = 50
    ICON_HEIGHT = 50
    ICON_DIMENSIONS = (ICON_WIDTH, ICON_HEIGHT)
    DEFAULT_ITEM_PROPERTIES = ItemProperties.SELLABLE_F | ItemProperties.ALCHABLE_F

    # Master dict mapping item IDs to item overworld_obj.
    item_listing = {}

    def __init__(self, item_id, name_info, description_info, usage_info=None, image_path=None,
                 enlarged_image_path=None, base_value_low=0,
                 base_value_high=0, properties=DEFAULT_ITEM_PROPERTIES, interaction_id=None,
                 required_creation_items=None, required_creation_levels=None, required_creation_quests=None,
                 menu_option_ids=menu_options.MenuOptionsList.DEFAULT_ITEM_MENU_OPTION_IDS):
        # Call the parent class (Sprite) init
        icon.ViewingIcon.__init__(self, item_id, name_info, description_info, image_path=image_path,
                                  enlarged_image_path=enlarged_image_path, menu_option_ids=menu_option_ids)

        self.item_id = item_id
        self.usage_info = usage_info if usage_info else language.MultiLanguageText()
        self.equipment_slot_id = equipment.EquipmentSlot.NONE
        self.base_value_low = base_value_low
        self.base_value_high = base_value_high
        self.properties = properties
        self.interaction_id = interaction_id

        self.required_creation_item_mapping = {}
        if required_creation_items:
            for item_id, quantity in required_creation_items.items():
                self.required_creation_item_mapping[item_id] = quantity

        self.required_creation_level_mapping = {}
        if required_creation_levels:
            for skill_id, level in required_creation_levels.items():
                self.required_creation_level_mapping[skill_id] = level

        self.required_creation_quests = []
        if required_creation_quests:
            for quest_id in required_creation_quests:
                self.required_creation_quests.append(quest_id)

    def get_statistics_info(self):
        # TODO
        return None

    # Overridden.
    def get_info_text(self):
        description_info = self.get_description_info()
        usage_info = self.get_usage_info()
        ret_lines = []
        if description_info:
            ret_lines.append(description_info)
        if usage_info:
            ret_lines.append(usage_info)
        return '\n'.join(ret_lines)

    # Returns the appropriate language translation for the item's usage
    # info string.
    def get_usage_info(self):
        usage_str = self.usage_info.get_text()
        if usage_str:
            return usage_str
        else:
            return self.get_name()

    def is_stackable(self):
        return self.properties & ItemProperties.STACKABLE_F

    @classmethod
    def get_item(cls, item_id):
        return cls.item_listing.get(item_id, None)

    # Adds/updates the interactive object listing for the given object ID.
    # Returns True upon success, false otherwise.
    @classmethod
    def add_item_to_listing(cls, item_id, item_obj):
        if item_obj and (item_id is not None):
            cls.item_listing[item_id] = item_obj
            logging.debug("Added item ID {0} to item listing.".format(item_id))
            return True
        else:
            return False

    # Factory method to create items that are not equipable nor
    # consumable.
    @classmethod
    def standard_item_factory(cls, item_yaml_info):
        if not item_yaml_info:
            raise Exception('Empty item yaml info')
        item_id = item_yaml_info.get('id', None)
        if not item_id:
            raise Exception('Item ID missing in yaml info')

        # Check if we already have the item made.
        item_from_listing = cls.get_item(item_id)
        if item_from_listing:
            ret_item = item_from_listing
        else:
            name_info = language.MultiLanguageText(language_dict=item_yaml_info.get('name', {}))
            description_info = language.MultiLanguageText(language_dict=item_yaml_info.get('description', {}))
            usage_info = language.MultiLanguageText(language_dict=item_yaml_info.get('usage', {}))
            image_file = item_yaml_info.get('image_file', '')
            icon_path = os.path.join(util.get_images_path(), 'items', image_file) if image_file else ''
            enlarged_image_file = item_yaml_info.get('enlarged_image_file', '')
            if enlarged_image_file:
                enlarged_icon_path = os.path.join(util.get_images_path(), 'items', enlarged_image_file)
            else:
                enlarged_icon_path = ''
            base_value_low = item_yaml_info.get('value_low', 0)
            base_value_high = item_yaml_info.get('value_high', 0)
            properties = item_yaml_info.get('properties', ItemProperties.SELLABLE_F | ItemProperties.ALCHABLE_F)
            interaction_id = item_yaml_info.get('interaction_id', None)
            required_creation_items = item_yaml_info.get('required_creation_items', None)
            required_creation_levels = item_yaml_info.get('required_creation_levels', None)
            required_creation_quests = item_yaml_info.get('required_creation_quests', None)
            if properties & ItemProperties.STACKABLE_F:
                menu_option_ids = menu_options.MenuOptionsList.DEFAULT_STACKABLE_OPTION_ID_LIST
            else:
                menu_option_ids = menu_options.MenuOptionsList.DEFAULT_ITEM_MENU_OPTION_IDS

            # Ensure we have the required fields.
            if name_info and description_info:
                new_item = Item(item_id, name_info, description_info, usage_info=usage_info,
                                image_path=icon_path, enlarged_image_path=enlarged_icon_path,
                                base_value_low=base_value_low, base_value_high=base_value_high,
                                properties=properties, interaction_id=interaction_id,
                                required_creation_items=required_creation_items,
                                required_creation_levels=required_creation_levels,
                                required_creation_quests=required_creation_quests,
                                menu_option_ids=menu_option_ids)

                logging.debug("Made item {0} with ID {1}".format(new_item.get_name(), item_id))

                # Update the item mapping.
                result = cls.add_item_to_listing(item_id, new_item)
                if result:
                    ret_item = new_item
                else:
                    raise Exception("Failed to add item ID {0} to listing.".format(item_id))
            else:
                raise Exception("Required fields not found in item data for ID {0}".format(item_id))
        return ret_item

    @classmethod
    def build_standard_items(cls):
        logging.info("Building standard items.")
        try:
            for item_yaml in glob.glob(os.path.join(util.get_yaml_path(), 'items', 'standard', '*.yml')):
                stripped = util.strip_yaml(item_yaml)
                if not stripped:
                    raise Exception('Empty item yaml {} provided'.format(item_yaml))
                for item_yaml_info in stripped[0]:
                    if not cls.standard_item_factory(item_yaml_info):
                        raise Exception('Failed to build items from yaml file {}'.format(item_yaml))
        except Exception as e:
            raise Exception('Failed to build items: {}', e)


class EquipableItem(Item):
    def __init__(self, item_id, name_info, equipment_slot_id, description_info, usage_info=None, image_path=None,
                 enlarged_image_path=None, base_value_low=0, base_value_high=0, properties=Item.DEFAULT_ITEM_PROPERTIES,
                 interaction_id=interaction.InteractionID.DEFAULT, required_creation_items=None,
                 required_creation_levels=None, required_creation_quests=None,
                 menu_option_ids=menu_options.MenuOptionsList.DEFAULT_ITEM_MENU_OPTION_IDS,
                 combat_type=battle.CombatType.NONE, stats=None, combat_boost_info=None, required_equip_levels=None,
                 required_equip_quests=None):
        Item.__init__(self, item_id, name_info, description_info, usage_info=usage_info, image_path=image_path,
                      enlarged_image_path=enlarged_image_path, base_value_low=base_value_low,
                      base_value_high=base_value_high, properties=properties, interaction_id=interaction_id,
                      required_creation_items=required_creation_items,
                      required_creation_levels=required_creation_levels,
                      required_creation_quests=required_creation_quests, menu_option_ids=menu_option_ids)
        self.equipment_slot_id = equipment_slot_id
        self.combat_type = combat_type
        self.stats = {}
        if stats:
            for stat_type, value in stats.items():
                self.stats[stat_type] = value

        self.combat_boost_info = {}
        if combat_boost_info:
            for boost_type, value_tuple in combat_boost_info.items():
                self.combat_boost_info[boost_type] = value_tuple

        self.required_equip_level_mapping = {}
        if required_equip_levels:
            for skill_id, level in required_equip_levels.items():
                self.required_equip_level_mapping[skill_id] = level

        self.required_equip_quests = []
        if required_equip_quests:
            for quest_id in required_equip_quests:
                self.required_equip_quests.append(quest_id)


"""
class ConsumableItem(Item):
    def __init__(
            self,
            item_id,
            name_info,
            description_info,
            heal_value=0,
            usage_info={},
            image_path_dict={},
            base_value_low=0,
            base_value_high=0,
            weight_points=0,
            properties=(ItemProperties.SELLABLE_F | ItemProperties.ALCHABLE_F),
            interaction_id=interactiondata.DEFAULT_ID,
            required_creation_items={},
            required_creation_levels={},
            required_creation_quests=[],
            item_menu_option_ids=menuoptions.DEFAULT_ITEM_MENU_OPTION_IDS,
            skill_effect_info={},
            combat_boost_info={},
            required_consume_quests=[],
        ):
        Item.__init__(
            self,
            item_id,
            name_info,
            description_info,
            usage_info=usage_info,
            image_path_dict=image_path_dict,
            base_value_low=base_value_low,
            base_value_high=base_value_high,
            weight_points=weight_points,
            properties=properties,
            interaction_id=interaction_id,
            required_creation_items=required_creation_items,
            required_creation_levels=required_creation_levels,
            required_creation_quests=required_creation_quests,
            item_menu_option_ids=item_menu_option_ids,
        )

        self.heal_value = 0
        self.skill_effect_info = {}
        for skill_id, effect_info in skill_effect_info.items():
            self.skill_effect_info[skill_id] = effect_info

        self.combat_boost_info = {}
        for boost_type, value_tuple in combat_boost_info.items():
            self.combat_boost_info[boost_type] = value_tuple

        self.required_consume_quests = []
        for quest_id in required_consume_quests:
            self.required_consume_quests.append(quest_id)
"""

# TODO set boost type IDs
# TODO set boost effect type IDs
# TODO set damage type IDs
