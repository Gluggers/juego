import pygame
import logging
from enum import Enum
from app.images import image_ids
from app.maps import directions
from app.overworld_obj import interactive_obj
from app.interactions import interaction
from app.skills import skills

MAX_RUN_ENERGY = 100.0


class EntityType(Enum):
    CHARACTER = 0x1
    MONSTER = 0x2
    RESOURCE = 0x3
    ITEM = 0x4
    OBSTACLE = 0x5
    CHEST = 0x6
    TYPE_MISC = 0x7


class EntityID(Enum):
    PROTAGONIST = 0x2


class Gender(Enum):
    NEUTRAL = 0x0
    MALE = 0x1
    FEMALE = 0x2


class Race(Enum):
    DEFAULT = 0x0
    HUMAN = 0x1


class Entity(interactive_obj.InteractiveObject):
    # id represents the object ID.
    # name_info contains name translations
    # image_path_dict maps image type IDs to the file paths for the image.
    # collision_width and collision_height define the tile dimensions
    # for the object's collision space. Must be integers greater than or equal
    # to 1?
    # skill_levels maps the skill ID to the corresponding level
    # for the entity (skill ID -> level). The method will automatically
    # calculate the experience required for the level and set it accordingly
    # for the entity.  Excluding the skill_levels dict or excluding individual
    # skill IDs will set default values.
    # equipment_dict maps the equipment slot ID to a length-3 list of form
    # [equipped item ID, item object, quantity of item].
    def __init__(self, entity_id, name_info, image_info_dict, collision_width=1, collision_height=1, skill_levels=None,
                 gender=Gender.NEUTRAL, race=Race.HUMAN, examine_info=None,
                 interaction_id=interaction.InteractionID.DEFAULT):
        """Initializes the Entity object.

        Args:
            entity_id: object ID number for the Entity. Must be unique
                among interactive overworld_obj?
            name_info: language.MultiLanguageText for name translations
            image_info_dict: dict that maps image sequence IDs to a length-2
                list of the following format:
                    [list of file paths for image files for the image sequence,
                    image sequence duration in milliseconds].
                    If image sequence duration is None, then only the first
                    image in the image sequence will be used.
            collision_width: width, in Tiles, of the collision box for the
                Entity.
            collision_height: height, in Tiles, of the collision box for the
                Entity.
            skill_levels: dict that maps the skill ID to the corresponding
                level for the entity. The method automatically calculates the
                experience required for the level and set it accordingly for
                the entity. Excluding the skill_levels dict or excluding
                individual skill IDs will set default levels for all
                applicable skills.
            gender: gender ID for the Entity.
            race: race ID for the Entity.
            examine_info: language.MultiLanguageText for examine text translations
            interaction_id: interaction ID that determines what interaction
                method to use when interacting with the Entity.
        """

        interactive_obj.InteractiveObject.__init__(
            self,
            EntityType.CHARACTER,
            entity_id,
            name_info,
            image_info_dict,
            collision_width=collision_width,
            collision_height=collision_height,
            examine_info=examine_info,
            interaction_id=interaction_id,
        )

        self.gender = gender
        self.race = race

        # Determines walk/run.
        self.run_on = False

        # Determines how much longer the entity can run.
        self.run_energy = MAX_RUN_ENERGY

        # By default, face south.
        self.facing_direction = directions.CardinalDirection.SOUTH
        self.curr_image_sequence_id = image_ids.ImageSequenceID.FACE_SOUTH

        # Set up skills. self.skill_info_mapping maps skill IDs to
        # a length-3 list
        # [skill level, current experience, experience to next level]
        self.skill_info_mapping = {}

        if skill_levels:
            for skill_id in skills.Skill.SKILL_ID_NAME_MAPPING:
                # See if caller passed in a custom level for the skill.
                skill_level = skill_levels.get(skill_id, None)

                # Default hitpoints level is different.
                if not skill_level:
                    skill_level = skills.Skill.DEFAULT_LEVEL

                # Get the required experience for the level.
                exp = skills.Skill.get_experience_from_level(skill_level)

                # Get remaining experience for next level.
                remaining_exp = skills.Skill.get_experience_to_next_level(
                    skill_level,
                    exp
                )

                logging.debug(
                    "Setting skill level %d, exp %d. exp to next level %d",
                    skill_level,
                    exp,
                    remaining_exp
                )

                # Record skill information.
                self.skill_info_mapping[skill_id] = [
                    skill_level,
                    exp,
                    remaining_exp
                ]

    # TODO - increment run energy.

    def decrement_run_energy(self, distance=1, ):
        """Reduce run energy based on distance ran and the entity's
        weight and agility level.

        Args:
            distance: number of tiles moved, not counting map
                switches, teleports, or connector tiles.
        """

        # TODO change calculation based on weight.
        if distance:
            self.run_energy = max(
                0.0,
                self.run_energy - (2 * distance)
            )

    def get_skill_level(self, skill_id):
        """Returns the entity's skill level for the given skill ID."""

        ret_level = None

        if skill_id is not None:
            skill_info = self.skill_info_mapping.get(skill_id, None)

            if skill_info:
                ret_level = skill_info[0]

        return ret_level

    def get_skill_experience(self, skill_id):
        """Returns the entity's experience for the given skill ID."""

        ret_exp = None

        if skill_id is not None:
            skill_info = self.skill_info_mapping.get(skill_id, None)

            if skill_info:
                ret_exp = skill_info[1]

        return ret_exp

    def get_experience_to_next_level(self, skill_id):
        """Returns the entity's remaining experience for the next skill level
        for the given skill ID."""

        ret_exp = None

        if skill_id is not None:
            skill_info = self.skill_info_mapping.get(skill_id, None)

            if skill_info:
                ret_exp = skill_info[2]

        return ret_exp

    # Returns the number of levels gained when adding exp to skill_id.
    def gain_experience(self, skill_id, exp):
        """Adds experience to the entity for the given skill and returns the
        number of levels gained in that skill."""

        levels_gained = 0

        if (skill_id is not None) and exp and (exp > 0):
            skill_info = self.skill_info_mapping.get(skill_id, None)
            # exp_to_process = exp

            if skill_info:
                old_level = skill_info[0]
                old_exp = skill_info[1]

                new_exp = old_exp + exp
                new_level = skills.Skill.get_level_from_experience(new_exp)
                new_exp_to_next_level = skills.Skill.get_experience_to_next_level(new_level, new_exp)

                if new_level < old_level:
                    logging.error("Error in exp gain.")
                else:
                    logging.info(
                        "Started at level %d with %d exp (%d remaining to next level.)",
                        old_level,
                        old_exp,
                        skill_info[2]
                    )
                    logging.info(
                        "Now reached level %d with %d exp (%d remaining to next level.)",
                        new_level,
                        new_exp,
                        new_exp_to_next_level,
                    )

                    skill_info[0] = new_level
                    skill_info[1] = new_exp
                    skill_info[2] = new_exp_to_next_level

                    self.skill_info_mapping[skill_id] = skill_info

                    levels_gained = max(0, new_level - old_level)

        return levels_gained

    # reblit the entity to face the specified direction.
    # Can specify either top_left_pixel or
    # bottom_left_pixel as the reference point for blitting the image.
    # bottom_left_pixel is recommended for images that are larger than
    # a single Tile image. If both top_left_pixel and bottom_left_pixel are
    # specified, the method will use bottom_left_pixel as an override.
    # top_left_pixel and bottom_left_pixel are tuples of pixel coordinates.
    # DOES NOT update surface - caller will have to do that
    def face_direction(
            self,
            surface,
            direction,
            bottom_left_pixel=None,
            top_left_pixel=None,
    ):
        if self and surface and (bottom_left_pixel or top_left_pixel):
            sequence_id = image_ids.get_direction_sequence_id(direction)

            if sequence_id is not None:
                # change direction variable and blit
                self.facing_direction = direction
                self.curr_image_sequence_id = sequence_id
                self.blit_onto_surface(
                    surface,
                    bottom_left_pixel=bottom_left_pixel,
                    top_left_pixel=top_left_pixel,
                    blit_time_ms=pygame.time.get_ticks(),
                )


class Character(Entity):
    # Maps character-related object IDs to Character overworld_obj.
    character_listing = {}

    def __init__(
            self,
            entity_id,
            name_info,
            image_path_dict,
            collision_width=1,
            collision_height=1,
            skill_levels=None,
            gender=Gender.NEUTRAL,
            race=Race.HUMAN,
            examine_info=None,
            interaction_id=interaction.InteractionID.DEFAULT,
    ):

        # a Character is an Entity type of interactive object
        Entity.__init__(
            self,
            entity_id,
            name_info,
            image_path_dict,
            collision_width=collision_width,
            collision_height=collision_height,
            skill_levels=skill_levels,
            gender=gender,
            race=race,
            examine_info=examine_info,
            interaction_id=interaction_id,
        )

        # TODO Fill in rest

    # given object id, returns character if it pertains to object ID
    # do not use this to build protagonist
    @classmethod
    def character_factory(cls, object_id):
        ret_character = None

        # reject if object ID is for protagonist
        if object_id == EntityID.PROTAGONIST:
            logging.warning("Cannot use character_factory to build protagonist.")
        else:
            # check if we already have this object
            char_from_listing = Character.character_listing.get(
                object_id,
                None
            )

            if char_from_listing:
                ret_character = char_from_listing
            else:
                # we need to make character ourselves
                # TODO
                pass

                # check if object id pertains to a character

        return ret_character
