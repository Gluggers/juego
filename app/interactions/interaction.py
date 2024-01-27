import pygame
import logging

from enum import Enum
from app.viewing import viewing
from lang import language
from util import timekeeper

GATHERING_START_DELAY_MS = 500
GATHERING_EXHAUST_DELAY_MS = 1000

DEFAULT_INTERACTION_MESSAGE_INFO = language.MultiLanguageText(
    en="Default interaction with {0}.",
    es="Interacción por defecto con {0}.",
)

INVENTORY_FULL_MESSAGE_INFO = language.MultiLanguageText(
    en="You can't hold any more items.",
    es="No puedes guardar más cosas.",
)

NOT_HIGH_ENOUGH_LEVEL_MESSAGE_INFO = language.MultiLanguageText(
    en="You need a level of {0} in {1}.",
    es="Se necesita un nivel de {0} en {1}.",
)

# Number of milliseconds in a gathering skilling interval.
GATHERING_INTERVAL_MS = 1000
GATHERING_INTERVAL_NUM_TICKS = int(
    timekeeper.TICKS_PER_SECOND * (GATHERING_INTERVAL_MS / timekeeper.MS_PER_SECOND)
)

# Number of milliseconds between switching character gathering image IDs.
GATHERING_IMAGE_INTERVAL_MS = int(timekeeper.MS_PER_SECOND / 4)
GATHERING_IMAGE_INTERVAL_NUM_TICKS = int(
    timekeeper.TICKS_PER_SECOND * (GATHERING_IMAGE_INTERVAL_MS / timekeeper.MS_PER_SECOND)
)

# Number of game ticks to hold the resource gather message.
NUM_TICK_HOLD_RESOURCE_GATHER_MESSAGE = int(timekeeper.TICKS_PER_SECOND * 2)

SKILLING_EXIT_KEYS = {
    pygame.K_BACKSPACE,
    pygame.K_ESCAPE,
    pygame.K_RIGHT,
    pygame.K_DOWN,
    pygame.K_LEFT,
    pygame.K_UP,
}


class InteractionID(Enum):
    DEFAULT = 0x000002
    CHOP_TREE = 0x300001
    MINE_ROCK = 0x300021
    CATCH_FISH_ROD = 0x300031
    CATCH_FISH_NET = 0x300032
    CATCH_FISH_HARPOON = 0x300033
    COOKING = 0x300041
    HERBLORE_GATHER = 0x300051


class Interaction:
    # Maps interaction IDs to methods
    interaction_mapping = {}

    @classmethod
    def default_interaction(cls, interaction_id, game_object, acting_object, target_object, acting_object_loc,
                            target_object_loc):
        if game_object and acting_object and target_object:
            game_object.display_overworld_bottom_text(
                DEFAULT_INTERACTION_MESSAGE_INFO.get_text().format(target_object.get_name()),
                refresh_after=True,
            )

    @classmethod
    def meets_resource_level(cls, acting_object, target_object):
        """Returns True if the acting object has a high enough level to interact
        with the target object, False otherwise.

        Args:
            acting_object: the object trying to interact with the target_object
                resource.
            target_object: the object being interacted with, typically a
                resource object.
        """

        meets_level = False
        if acting_object and target_object:
            # Check we have the required level.
            skill = target_object.related_skill_id
            min_required_level = target_object.min_required_level
            if acting_object.get_skill_level(skill) >= min_required_level:
                meets_level = True
        return meets_level

    @classmethod
    def display_inventory_full_message(cls, game_object):
        """Displays message indicating that the inventory is full."""

        if game_object:
            game_object.display_overworld_bottom_text(
                INVENTORY_FULL_MESSAGE_INFO.get_text(),
                auto_advance=False,
                advance_delay_ms=viewing.ViewingTime.DEFAULT_ADVANCE_DELAY_MS,
                refresh_after=True,
            )

    # Main skilling text must be 1 page or less.
    @classmethod
    def gathering_interaction(cls, interaction_id, game_object, acting_object, target_object, acting_object_loc,
                              target_object_loc, main_skilling_text, skill_id, resource_exhaust_text=None,
                              intro_skilling_text=None):

        """
        if (game_object and game_object.overworld_viewing and acting_object and target_object and acting_object_loc
                and target_object_loc and (interaction_id is not None) and main_skilling_text
                and (skill_id is not None)):
            # Check if inventory is full and if we have the right level
            # and equipment. TODO equipment check.
            if acting_object.inventory_full():
                # Inventory is full.
                cls.display_inventory_full_message(game_object)
            elif not Interaction.meets_resource_level(
                    acting_object,
                    target_object
                ):
                # Don't have a high enough level.
                min_required_level = target_object.min_required_level
                skill_name = skills.get_skill_name(
                    target_object.related_skill_id,
                    language.Language.current_language_id
                )

                reject_message = NOT_HIGH_ENOUGH_LEVEL_MESSAGE_INFO.get(
                    language.Language.current_language_id,
                    ""
                ).format(min_required_level, skill_name)

                game_object.display_overworld_bottom_text(
                    reject_message,
                    auto_advance=False,
                    advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
                    refresh_after=True,
                    refresh_during=True,
                )
            # TODO equipment check
            else:
                # Display intro skilling text if needed.
                if intro_skilling_text:
                    game_object.display_overworld_bottom_text(
                        intro_skilling_text,
                        auto_advance=False,
                        advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
                        refresh_after=True,
                        refresh_during=True,
                    )

                # Display main skilling text. Pause before we start skilling.
                game_object.display_overworld_bottom_text_first_page(
                    main_skilling_text,
                    auto_advance=True,
                    advance_delay_ms=GATHERING_START_DELAY_MS,
                    refresh_after=False,
                    refresh_during=False
                )

                logging.info("Beginning gathering.")

                # Start skilling.
                skilling = True
                resource_exhausted = False
                num_skill_ticks = 0
                image_id_index = 0
                pygame.event.clear()
                prev_sequence = acting_object.curr_image_sequence

                while skilling and not resource_exhausted:
                    timekeeper.Timekeeper.tick()

                    num_skill_ticks = num_skill_ticks + 1

                    # TODO set next character image ID for skilling.
                    if (num_skill_ticks \
                            % GATHERING_IMAGE_INTERVAL_NUM_TICKS) == 0:
                        logging.debug("Switch image IDs here.")
                        game_object.refresh_and_blit_overworld_viewing(
                            display_update=False
                        )
                    elif (num_skill_ticks \
                            % timekeeper.REFRESH_INTERVAL_NUM_TICKS) == 0:
                        # Refresh and reblit overworld.
                        game_object.refresh_and_blit_overworld_viewing(
                            display_update=False
                        )
                    elif (num_skill_ticks \
                            % timekeeper.OW_REBLIT_INTERVAL_NUM_TICKS) == 0:
                        game_object.overworld_viewing.blit_self()

                    # This will update display for us.
                    game_object.display_overworld_bottom_text_first_page(
                        main_skilling_text,
                        auto_advance=True,
                        advance_delay_ms=0,
                        refresh_after=False,
                        refresh_during=False,
                    )

                    # Check if user is ending early by pressing a valid key.
                    exit_key_pressed = False
                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            logging.info("Quitting.")
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key in SKILLING_EXIT_KEYS:
                                logging.info("Quitting gathering early.")
                                exit_key_pressed = True

                    if exit_key_pressed:
                        skilling = False

                    # Chance to generate a resource after every gathering
                    # interval.
                    elif (num_skill_ticks \
                            % GATHERING_INTERVAL_NUM_TICKS) == 0:
                        # Check if we have generated a resource.
                        # (for now, just use strict probability. later,
                        # implement function that determines generation based on
                        # resource required level and character level and
                        # character equipment)
                        #if random.randint(0,4) == 0:
                        if random.randint(0,1) == 0:
                            # We generated a resource.
                            logging.info("Gathered resource!")

                            # Determine which resource we obtained.
                            resource_gather_text = None
                            gained_resource = None
                            resource_exp = None

                            resource_item_info = \
                                target_object.select_resource_item_info(
                                    acting_object.get_skill_level(
                                        target_object.related_skill_id
                                    )
                                )

                            logging.info(
                                "Resource item info: %s",
                                resource_item_info,
                            )

                            if resource_item_info:
                                gained_resource = items.Item.get_item(
                                    resource_item_info[0]
                                )
                                # TODO handle cases of boosted exp?
                                resource_exp = resource_item_info[1]

                            if gained_resource:
                                resource_gather_text = \
                                    interactiondata.GATHERING_RESOURCE_GAIN_MESSAGES.get(
                                        interaction_id,
                                        {}
                                    ).get(
                                        language.Language.current_language_id,
                                        ""
                                    ).format(
                                        gained_resource.get_name(),
                                        resource_exp
                                    )

                                # Add item to inventory.
                                acting_object.add_item_to_inventory(
                                    gained_resource.item_id
                                )

                                # Check if resource has been exhausted.
                                if random.randint(0, 100) < int(
                                            100 \
                                            * target_object.exhaustion_probability
                                        ):
                                    # Resource has been exhausted.
                                    skilling = False
                                    resource_exhausted = True
                                    logging.info("Resource exhausted.")

                                    # Set respawn.
                                    game_object.set_object_respawn(
                                        target_object,
                                        target_object_loc,
                                    )

                                game_object.refresh_and_blit_overworld_viewing()

                            # Display the resource gather message.
                            if resource_gather_text:
                                game_object.display_overworld_bottom_text_first_page(
                                    resource_gather_text,
                                    auto_advance=False,
                                    refresh_after=True,
                                    refresh_during=True,
                                )
                            else:
                                game_object.refresh_and_blit_overworld_viewing()

                            # This will display level up message if needed.
                            levels_gained = game_object.gain_experience(
                                acting_object,
                                skill_id,
                                resource_exp,
                            )

                            # Stop skilling if we level up.
                            if levels_gained and levels_gained > 0:
                                skilling = False

                            if resource_exhausted:
                                # Display exhaust message.
                                game_object.display_overworld_bottom_text_first_page(
                                    resource_exhaust_text,
                                    auto_advance=False,
                                    advance_delay_ms=GATHERING_EXHAUST_DELAY_MS,
                                    refresh_after=True,
                                    refresh_during=True,
                                )

                                #game_object.refresh_and_blit_overworld_viewing()

                            if skilling and acting_object.inventory_full():
                                # Inventory is full.
                                skilling = False
                                cls.display_inventory_full_message()
                                game_object.refresh_and_blit_overworld_viewing()

        pygame.event.clear()

        acting_object.curr_image_sequence = prev_sequence_id

        # Update overworld and display.
        game_object.refresh_and_blit_overworld_viewing()
        pygame.display.update()
        """
        logging.info("Place gathering interaction here.")

    @classmethod
    def chop_tree_interaction(
            cls,
            # interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
    ):

        """
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            obj_name = target_object.get_name()

            main_skilling_text = interactiondata.GATHERING_MAIN_MESSAGES.get(
                #interaction_id,
                interactiondata.CHOP_TREE_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            resource_exhaust_text = interactiondata.GATHERING_RESOURCE_EXHAUST_MESSAGES.get(
                #interaction_id,
                interactiondata.CHOP_TREE_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            cls.gathering_interaction(
                #interaction_id,
                interactiondata.CHOP_TREE_ID,
                game_object,
                acting_object,
                target_object,
                acting_object_loc,
                target_object_loc,
                main_skilling_text,
                skills.SKILL_ID_WOODCUTTING,
                resource_exhaust_text=resource_exhaust_text,
            )
        """
        logging.info("Place chopping interaction here.")

    @classmethod
    def mine_rock_interaction(
            cls,
            # interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
    ):

        """
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            obj_name = target_object.get_name()

            main_skilling_text = interactiondata.GATHERING_MAIN_MESSAGES.get(
                #interaction_id,
                interactiondata.MINE_ROCK_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            resource_exhaust_text = interactiondata.GATHERING_RESOURCE_EXHAUST_MESSAGES.get(
                #interaction_id,
                interactiondata.MINE_ROCK_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            cls.gathering_interaction(
                #interaction_id,
                interactiondata.MINE_ROCK_ID,
                game_object,
                acting_object,
                target_object,
                acting_object_loc,
                target_object_loc,
                main_skilling_text,
                skills.SKILL_ID_MINING,
                resource_exhaust_text=resource_exhaust_text,
            )
        """
        logging.info("Place mining interaction here.")

    @classmethod
    def fishing_rod_interaction(
            cls,
            # interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
    ):

        """
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            obj_name = target_object.get_name()

            main_skilling_text = interactiondata.GATHERING_MAIN_MESSAGES.get(
                #interaction_id,
                interactiondata.CATCH_FISH_ROD_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            resource_exhaust_text = interactiondata.GATHERING_RESOURCE_EXHAUST_MESSAGES.get(
                #interaction_id,
                interactiondata.CATCH_FISH_ROD_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            cls.gathering_interaction(
                interactiondata.CATCH_FISH_ROD_ID,
                game_object,
                acting_object,
                target_object,
                acting_object_loc,
                target_object_loc,
                main_skilling_text,
                skills.SKILL_ID_FISHING,
                resource_exhaust_text=resource_exhaust_text,
            )
        """

        logging.info("Place fishign rod  interaction here.")

    @classmethod
    def fishing_net_interaction(
            cls,
            # interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
    ):
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            pass

    @classmethod
    def cooking_interaction(
            cls,
            # interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
    ):
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            pass

    @classmethod
    def herblore_gather_interaction(
            cls,
            # interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
    ):
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            logging.info("Place herb gather interaction here.")

    @classmethod
    def get_interaction_method(cls, interaction_id):
        ret_method = Interaction.default_interaction
        if interaction_id is not None:
            ret_method = Interaction.interaction_mapping.get(
                interaction_id,
                Interaction.default_interaction
            )
        return ret_method

    @classmethod
    def init_interactions(cls):
        for interaction_id, method in ID_TO_METHOD_MAPPING.items():
            Interaction.interaction_mapping[interaction_id] = method


# MAP INTERACTION IDS TO METHODS
ID_TO_METHOD_MAPPING = {
    InteractionID.DEFAULT: Interaction.default_interaction,
    InteractionID.CHOP_TREE: Interaction.chop_tree_interaction,
    InteractionID.MINE_ROCK: Interaction.mine_rock_interaction,
    InteractionID.CATCH_FISH_ROD: Interaction.fishing_rod_interaction,
    InteractionID.CATCH_FISH_NET: Interaction.fishing_net_interaction,
    InteractionID.COOKING: Interaction.cooking_interaction,
    InteractionID.HERBLORE_GATHER: Interaction.herblore_gather_interaction,
}
