import pygame
import logging

from app.images import image_ids, image_paths
from app.overworld_obj import entity, interactive_obj
from app.skills import skills
from app.items import inventory, items
from lang import language

START_NUM_GOLD_COINS = 100

# Run energy recovery rate in points per minute.
DEFAULT_RUN_REGEN_PER_MIN = 30

IMAGE_INFO_DICT = {
    image_ids.ImageSequenceID.DEFAULT: image_paths.PROT_RANGER_F_OW_DEFAULT,
    image_ids.ImageSequenceID.FACE_NORTH: image_paths.PROT_RANGER_F_OW_FACE_NORTH,
    image_ids.ImageSequenceID.FACE_EAST: image_paths.PROT_RANGER_F_OW_FACE_EAST,
    image_ids.ImageSequenceID.FACE_SOUTH: image_paths.PROT_RANGER_F_OW_FACE_SOUTH,
    image_ids.ImageSequenceID.FACE_WEST: image_paths.PROT_RANGER_F_OW_FACE_WEST,
    image_ids.ImageSequenceID.WALK_NORTH: [
        [
            image_paths.PROT_RANGER_F_OW_WALK1_NORTH,
            image_paths.PROT_RANGER_F_OW_FACE_NORTH,
            image_paths.PROT_RANGER_F_OW_WALK2_NORTH,
            image_paths.PROT_RANGER_F_OW_FACE_NORTH,
        ],
        None
    ],
    image_ids.ImageSequenceID.WALK_EAST: [
        [
            image_paths.PROT_RANGER_F_OW_WALK1_EAST,
            image_paths.PROT_RANGER_F_OW_FACE_EAST,
            image_paths.PROT_RANGER_F_OW_WALK2_EAST,
            image_paths.PROT_RANGER_F_OW_FACE_EAST,
        ],
        None
    ],
    image_ids.ImageSequenceID.WALK_SOUTH: [
        [
            image_paths.PROT_RANGER_F_OW_WALK1_SOUTH,
            image_paths.PROT_RANGER_F_OW_FACE_SOUTH,
            image_paths.PROT_RANGER_F_OW_WALK2_SOUTH,
            image_paths.PROT_RANGER_F_OW_FACE_SOUTH,
        ],
        None
    ],
    image_ids.ImageSequenceID.WALK_WEST: [
        [
            image_paths.PROT_RANGER_F_OW_WALK1_WEST,
            image_paths.PROT_RANGER_F_OW_FACE_WEST,
            image_paths.PROT_RANGER_F_OW_WALK2_WEST,
            image_paths.PROT_RANGER_F_OW_FACE_WEST,
        ],
        None
    ],
}


class Protagonist(entity.Character):
    def __init__(self, entity_id, name_info, image_path_dict, skill_levels=None, gender=entity.Gender.NEUTRAL,
                 race=entity.Race.HUMAN):
        entity.Character.__init__(self, entity_id, name_info, image_path_dict, collision_width=1, collision_height=1,
                                  skill_levels=skill_levels, gender=gender, race=race)
        self.quest_journal = {}

        # Time in MS of last refresh.
        self.last_refresh_time_ms = pygame.time.get_ticks()

        # Maps Item IDs to the number of items held.
        self.inventory = inventory.Inventory.inventory_factory()

        # TODO make max_size constant. Add items here?
        self.tool_inventory = inventory.Inventory.inventory_factory(max_size=10)

    def inventory_full(self):
        """Returns True if inventory is full, False otherwise."""

        return self.inventory.is_full()

    def add_item_to_inventory(self, item_id, quantity=1):
        """Adds the corresponding number of items to the inventory and
        returns True upon success, False upon failure.

        Args:
            item_id: ID number for the Item to add.
            quantity: amount of item_id to add.

        Returns:
            True upon successful addition to the inventory, False otherwise.
        """

        return self.inventory.add_item(item_id, quantity=quantity)

    def add_item_to_toolbelt(self, item_id, quantity=1):
        """Adds the corresponding number of items to the toolbelt and
        returns True upon success, False upon failure.

        Args:
            item_id: ID number for the tool Item to add.
            quantity: amount of item_id to add.

        Returns:
            True upon successful addition to the toolbelt, False otherwise.
        """

        return self.tool_inventory.add_item(item_id, quantity=quantity)

    def has_tool(self, item_id):
        """Returns True if entity has the corresponding tool in its toolbelt,
        False otherwise."""

        return self.tool_inventory.has_item(item_id)

    def has_item(self, item_id):
        """Returns True if entity has the corresponding item, False otherwise.

        The item can be in the inventory, toolbelt, or equipment.
        """

        return self.inventory.has_item(item_id) or self.has_tool(item_id)

    def clear_all_items(self):
        """Removes all items from entity."""
        self.inventory.clear_items()
        self.tool_inventory.clear_items()

    def refresh_self(self):
        """Refreshes self, including attributes like run energy."""

        # Get elapsed time since last refresh.
        curr_time_ms = pygame.time.get_ticks()

        elapsed_ms = curr_time_ms - self.last_refresh_time_ms

        self.last_refresh_time_ms = curr_time_ms

        if elapsed_ms < 0:
            raise Exception("Error in elapsed time %d", elapsed_ms)

        elapsed_min = elapsed_ms / 60000

        # Regenerate some run energy.
        if self.run_energy < entity.MAX_RUN_ENERGY:
            self.run_energy = min(
                entity.MAX_RUN_ENERGY,
                self.run_energy + (elapsed_min * DEFAULT_RUN_REGEN_PER_MIN)
            )

        logging.debug("Protag run energy %d", self.run_energy)

    @classmethod
    def protagonist_factory(cls, name):
        """Creates protagonist with given name and gives default attributes.

        The returned protagonist will have the all of its stats at level 1
        by default and will have the following starting items:
            Inventory:
                - 100 gold coins
            Equipment: None
            Toolbelt:
                - Hammer
                - Knife
                - Tinderbox
                - Needle
        """

        # TODO check if we already have protagonist?

        # Build fields.
        protag_id = entity.EntityID.PROTAGONIST
        protag_name_info = language.MultiLanguageText(en=name, es=name)
        protag_image_path_dict = IMAGE_INFO_DICT
        protag_skill_levels = {
            skills.SkillID.WOODCUTTING: 40,  # TESTING.
            skills.SkillID.MINING: 40,  # TESTING.
            skills.SkillID.FISHING: 60,  # TESTING.
        }

        protagonist = Protagonist(
            protag_id,
            protag_name_info,
            protag_image_path_dict,
            skill_levels=protag_skill_levels,
            gender=entity.Gender.MALE,
            race=entity.Race.HUMAN,
        )

        logging.debug("Protagonist ID: %s", protagonist.object_id)
        logging.debug(
            "Protagonist obj type: %s",
            protagonist.object_type
        )
        logging.debug("Protagonist name: %s", protagonist.name_info.get_text())
        logging.debug("Protagonist gender: %s", protagonist.gender)
        logging.debug("Protagonist race: %s", protagonist.race)

        # Set initial money.
        protagonist.add_item_to_inventory(
            items.ItemID.CURRENCY_GOLD_COIN.value,
            quantity=START_NUM_GOLD_COINS,
        )

        # Set tool belt.
        protagonist.add_item_to_toolbelt(
            items.ItemID.HAMMER_TOOL.value,
            quantity=1,
        )

        """
        protagonist.add_item_to_toolbelt(
            itemdata.KNIFE_ID,
        )
        protagonist.add_item_to_toolbelt(
            itemdata.NEEDLE_ID,
        )
        protagonist.add_item_to_toolbelt(
            itemdata.TINDERBOX_ID,
        )
        """

        # TODO rest of setup

        # Add protagonist to object listing
        interactive_obj.InteractiveObject.add_interactive_obj_to_listing(entity.EntityID.PROTAGONIST, protagonist)
        return protagonist
