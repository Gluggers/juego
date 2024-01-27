import glob
import logging
import os
import pygame

from app.maps import directions
from app.overworld_obj import entity, interactive_obj
from app.viewing import viewing
from app.tiles import tiles
from util import util


class MapIDs:
    # MAP ID CONSTANTS
    REGION_1_ID = '30477bb1-0061-402e-a39d-1c2555cc214d'


class Map:
    # Maps map IDs to map overworld_obj.
    map_listing = {}

    # Create a Map object.
    # accessibility_grid must be a 2-dimensional list of ints representing the allowed
    # transportation access methods for each tile coordinate in the map.
    # accessibility_grid must have a valid rectangular dimension, meaning
    # each inner List must be of the same size.
    # accessibility_grid inner lists can be None or empty to shortcut indicate that
    # the entire row cannot be accessed by the character.
    #
    # connector_tile_dict must be a dict that maps a tuple of integers
    # (representing the X and Y tile coordinates of the map, NOT
    # pixel coordinates) to a corresponding Connector object.
    #
    # adj_map_dict must be a dict that maps a direction ID to a tuple
    # (Map ID, destination location coordinate) to represent the neighboring map and
    # where the Entity will end up by walking past the map boundary.
    #
    # top_left represents the (x,y) pixel coordinate on the display screen where the
    # top left corner of the map should start.
    def __init__(self, map_id, image_path, width_px, height_px, accessibility_grid, connector_tile_dict=None,
                 adj_map_dict=None, top_left=(0, 0), music_file=''):
        self.height_in_tiles = 0
        self.width_in_tiles = 0
        self.height_in_px = height_px
        self.width_in_px = width_px
        self.map_id = map_id
        self.accessibility_grid = []
        self.connector_tile_dict = {}
        self.adj_map_dict = dict()
        self.top_left_position = top_left
        self.last_refresh_time_ms = pygame.time.get_ticks()
        self.music_file = music_file

        # Maps bottom left tile location tuples
        # to the object ID of the original interactive obj on the tile
        # (No entry in dict for tile locations that are not
        # bottom left tile locations).
        self.original_bottom_left_tile_obj_mapping = {}

        # Maps tile location tuples to
        # the tile ID for the new tile at the location.
        self.changed_tile_mapping = {}

        # Dict that maps tile location tuple
        # to list of [object ID for object to place on tile
        # (None if removing object), entry time or time of last refresh
        # for object, and remaining time in
        # milliseconds].
        # TODO - when saving game, update everything. When loading game,
        # set entry times to current loading time.
        self.pending_spawn_actions = {}

        # maps bottom left tile coordinate tuple to
        # a length-2 list of [object ID, collision tile set],
        # where collision tile set is a set of Tile coordinates that
        # make up the object's collision rect
        self.bottom_left_tile_obj_mapping = {}

        # dict that maps a tile coordinate tuple to the bottom left
        # tile coordinate tuple of the object whose collision rect occupies
        # that tile. If no object occupies the tile, then the dict
        # should not have an entry for that tile location.
        # TODO - collision set, not just collision rect
        self.occupied_tile_to_bottom_left = {}

        # (x,y) tuple representing location of protagonist.
        self._protagonist_location = None

        # maps Tile grid location (x,y) tuple to a
        # [interactive obj, remaining ticks to respawn] list
        # that indicates when the corresponding interactive object should
        # respawn. For delayed respawns only
        self.pending_respawns = {}

        # Set up image
        self._rendered_map_image = pygame.image.load(image_path).convert_alpha()
        if not self._rendered_map_image:
            raise Exception('Failed to load map image')

        if accessibility_grid:
            grid_width = 0
            grid_height = len(accessibility_grid)

            # ensure our grid dimensions are correct
            for grid_row in accessibility_grid:
                if grid_row:
                    grid_width = len(grid_row)
                    if grid_width != len(grid_row):
                        raise Exception('Transportation grid must have consistent width')
            if grid_width == 0:
                raise Exception('Transportation grid must have non-zero width')

            # build accessibility grid
            for grid_row in accessibility_grid:
                if grid_row:
                    for x in grid_row:
                        if not isinstance(x, int):
                            raise Exception('Accessibility grid must only contain ints')
                    row_to_copy = [x for x in grid_row]
                else:
                    row_to_copy = [tiles.Accessibility.TILE_NOT_ACCESSIBLE_F] * grid_width
                self.accessibility_grid.append(row_to_copy)
            logging.info(self.accessibility_grid)
            self.height_in_tiles = grid_height
            self.width_in_tiles = grid_width
            total_tile_width_in_px = self.width_in_tiles * tiles.TILE_SIZE
            total_tile_height_in_px = self.height_in_tiles * tiles.TILE_SIZE
            if total_tile_width_in_px != self.width_in_px:
                raise Exception('Mismatch between provided map pixel width {0} and total pixel width from accessibility'
                                ' grid {1}'.format(self.width_in_px, total_tile_width_in_px))
            if total_tile_height_in_px != self.height_in_px:
                raise Exception('Mismatch between provided map pixel height {0} and total pixel height from '
                                'accessibility grid {1}'.format(self.height_in_px, total_tile_height_in_px))

            # get connector tiles
            if connector_tile_dict:
                for x, y in connector_tile_dict.items():
                    self.connector_tile_dict[x] = y

            # get neighboring maps
            if adj_map_dict:
                for x, y in adj_map_dict.items():
                    self.adj_map_dict[x] = y

    """
    # interactive_obj_dict must be a dict that maps a tuple of integers
    # (representing the X and Y tile coordinates of the map, NOT
    # pixel coordinates), representing the bottom left tiles of interactive
    # objects, to the interactive object ID.
    # The caller must take care to ensure that the objects do not collide
    # with each other when all fully placed on the map - otherwise, the method
    # will not fully place all the objects
    # This method must only be called during the map factory method
    # Returns True if all items set successfully, false otherwise
    def init_interactive_obj(self, interactive_obj_dict):
        successful = True

        if self.original_bottom_left_tile_obj_mapping is not None:
            # set up initial interactive objects for map
            for bottom_left_tile_loc, object_id in interactive_obj_dict.items():
                if (object_id is not None) and bottom_left_tile_loc:
                    LOGGER.debug(
                        "About to set object %d at %s",
                        object_id,
                        bottom_left_tile_loc,
                    )

                    if not self.set_interactive_object(object_id, bottom_left_tile_loc):
                        successful = False
                        LOGGER.warn(
                            "Could not place object %s at %s",
                            object_id,
                            bottom_left_tile_loc
                        )
                    else:
                        # Mark the original interactive obj for the bottom left tile.
                        self.original_bottom_left_tile_obj_mapping[bottom_left_tile_loc] = object_id
            LOGGER.info(
                "Original bottom left tile obj mapping for %s: %s",
                self.map_id,
                self.original_bottom_left_tile_obj_mapping
            )
        else:
            successful = False
            LOGGER.error(
                "Error: did not set original bottom left tile obj mapping for map id %d",
                self.map_id,
            )
            sys.exit(2)

        return successful
    """

    @property
    def protagonist_location(self):
        """Return the protagonist location on map."""
        return self._protagonist_location

    @protagonist_location.setter
    def protagonist_location(self, new_location):
        """Set the protagonist location on map."""
        if new_location:
            # Check if new location is occupied
            if self.tile_occupied(new_location):
                logging.error(
                    'Cannot move main character from {0} to {1}'.format(self._protagonist_location, new_location)
                )
            else:
                if self._protagonist_location:
                    # Clear old tile location
                    self.bottom_left_tile_obj_mapping.pop(self._protagonist_location, None)
                    self.occupied_tile_to_bottom_left.pop(self._protagonist_location, None)

                # Mark new location as occupied
                self.bottom_left_tile_obj_mapping[new_location] = [entity.EntityID.PROTAGONIST, {new_location}]
                self.occupied_tile_to_bottom_left[new_location] = new_location

                logging.debug('Moving main character from {0} to {1}'.format(
                    self._protagonist_location,
                    new_location))

                self._protagonist_location = new_location

    """
    # TODO - document
    def add_adjacent_map(self, direction, dest_map_id, dest_location_coordinate):
        # TODO - more arg checks?
        if self and dest_location_coordinate:
            self.adj_map_dict[direction] = (int(dest_map_id), \
                    (dest_location_coordinate[0], dest_location_coordinate[1]))

    # removes map that is adjacent according to direction
    def remove_adjacent_map(self, direction):
        if self:
            self.adj_map_dict.pop(direction, None)

    # get (Map ID, destination tile coordinate) tuple for the map
    # that is adjacent to this map in the given direction.
    # None if no such neighboring map exists
    def get_adjacent_map_info(self, direction):
        return self.adj_map_dict.get(direction, None)
    """

    # Returns bottom left tile location tuple of the bottom left
    # tile associated with the object occupying the given tile location tuple,
    # None if the provided tile location tuple is not occupied.
    def get_bottom_left_tile_of_occupied_tile(self, tile_loc):
        return self.occupied_tile_to_bottom_left.get(tile_loc, None)

    """
    # Sets an interactive object corresponding to obj_id
    # such that the bottom left tile of the
    # object is at the specified Tile coordinate
    # location (x, y) tuple on the Map.
    # Returns True if successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    #   - interactive object already exists at the location
    # Caller will need to reblit the map and update the surface to show
    # the new images
    def set_interactive_object(self, obj_id, bottom_left_tile_loc):
        success = False
        can_set = True
        obj_to_set = interactiveobj.InteractiveObject.get_interactive_object(obj_id)

        if not obj_to_set:
            LOGGER.debug("Could not find object with ID %d", obj_id)

        if self and obj_to_set and bottom_left_tile_loc and self.tile_grid:
            # Check that each tile in the colliion rect is within map
            # bounds and is not already occupied by another interactive
            # object.
            collision_tile_set = obj_to_set.get_collision_tile_set(bottom_left_tile_loc)
            for tile_loc in collision_tile_set:
                curr_tile_x = tile_loc[0]
                curr_tile_y = tile_loc[1]

                if self.location_within_bounds(tile_loc):
                    # We are within map bounds. Check for occupied tiles.
                    if self.tile_occupied(tile_loc):
                        can_set = False
                        # tile is occupied
                        LOGGER.warn(
                            "Obj already exists at location %s.",
                            str(tile_loc)
                        )
                    # TODO check if the tile is walkable before putting an object on it?
                else:
                    can_set = False
                    LOGGER.warn(
                        "Out of bounds location at: %s.",
                        tile_loc,
                    )
            # Set if we can.
            if can_set:
                # Associate object id and collision rect with the bottom left tile coordinate.
                self.bottom_left_tile_obj_mapping[bottom_left_tile_loc] = [obj_id, collision_tile_set]
                LOGGER.debug(
                    "Setting obj ID %d to bottom left tile %s",
                    obj_to_set.object_id,
                    bottom_left_tile_loc,
                )

                # Mark all tiles within object's collision rect as occupied
                for tile_loc in collision_tile_set:
                    self.occupied_tile_dict[tile_loc] = bottom_left_tile_loc
                    LOGGER.debug("Marking %s as occupied",tile_loc)

                success = True

        return success

    # Spawns an interactive object at the specified Tile coordinate
    # location (x,y) tuple on the Map, and also blits.
    # DOES NOT update the display - caller will have to do that
    # TODO CHANGE ^^??
    # Returns True if spawn was successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    #   - interactive object already exists at the location
    def spawn_interactive_object(self, surface, obj_to_respawn, tile_location):
        # TODO
        return False

    # Removes an interactive object that occupies the tile_location
    # coordinate (x,y) on the Map. Note that for interactive overworld_obj
    # that take up more than one tile, passing in just one of the tiles
    # will remove the object.
    # Returns the object ID of removed object if successful, None otherwise.
    # Reasons for failure include:
    #   - Map is empty
    #   - location is invalid
    #   - invalid or no tile location specified
    # If no interactive object has a bottom left tile at the location,
    # the method still returns None.
    # Caller will need to reblit the map and update the surface to show
    # the updated images
    def unset_interactive_object(self, tile_location):
        removed_id = None

        if self and tile_location and self.tile_grid:
            # make sure (x,y) location is in bounds
            if self.location_within_bounds(tile_location):
                # Check if the tile location maps to an object's
                # bottom left tile location.
                bottom_left_tile_loc = \
                    self.get_bottom_left_tile_of_occupied_tile(tile_location)

                if bottom_left_tile_loc:
                    # Get object to remove and remove from map
                    obj_info =                                      \
                        self.bottom_left_tile_obj_mapping.pop(      \
                            bottom_left_tile_loc,                   \
                            None                                    \
                        )
                    if obj_info:
                        obj_id = obj_info[0]
                        collision_set = obj_info[1]

                        LOGGER.debug(
                            "Removing object %d from %s",
                            obj_id,
                            bottom_left_tile_loc,
                        )

                        # Clear object's collision tiles on map
                        for tile_loc in collision_set:
                            self.occupied_tile_dict.pop(tile_loc, None)
                            LOGGER.debug("Freed tile %s",tile_loc)

                        if obj_id is not None:
                            removed_id = obj_id
            else:
                LOGGER.warn(
                    "Invalid location %s for unset_interactive_object",
                    str(tile_location)
                )

        return removed_id

    # removes an interactive object from the specified Tile coordinate
    # (x,y) location on the Map.
    # Also blits the surface.
    # DOES NOT update the display - caller will have to do that
    # Returns True if removal was successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    # If no interactive object exists at the location, the method still returns
    # True.
    def remove_interactive_object(self, surface, tile_location):
        # # TODO
        return False
    """

    # Returns None if invalid direction, invalid initial tile position,
    # or adjacent tile is out of bounds (does not look for adjacent maps).
    def get_adjacent_tile_position(self, tile_position, adjacent_direction):
        if tile_position and (adjacent_direction is not None):
            # Only proceed if we're within bounds.
            if self.location_within_bounds(tile_position):
                adj_tile_pos = None
                if adjacent_direction == directions.CardinalDirection.NORTH:
                    # Adjacent tile position is above.
                    adj_tile_pos = (tile_position[0], tile_position[1] - 1)
                elif adjacent_direction == directions.CardinalDirection.SOUTH:
                    # Adjacent tile position is below.
                    adj_tile_pos = (tile_position[0], tile_position[1] + 1)
                elif adjacent_direction == directions.CardinalDirection.EAST:
                    # Adjacent tile position is to the right.
                    adj_tile_pos = (tile_position[0] + 1, tile_position[1])
                elif adjacent_direction == directions.CardinalDirection.WEST:
                    # Adjacent tile position is to the left.
                    adj_tile_pos = (tile_position[0] - 1, tile_position[1])

                if adj_tile_pos and self.location_within_bounds(adj_tile_pos):
                    return adj_tile_pos
        return None

    """
    # Returns None if invalid direction, invalid initial tile position,
    # or adjacent tile is out of bounds (does not look for adjacent maps).
    def get_adjacent_tile(self, tile_position, adjacent_direction):
        ret_tile = None

        if tile_position and (adjacent_direction is not None):
            # Get adjacent tile position, and then get tile from there.
            adj_tile_pos = self.get_adjacent_tile_position(
                tile_position,
                adjacent_direction
            )

            if adj_tile_pos:
                ret_tile = self.get_tile_from_pos(adj_tile_pos)

        return ret_tile
    """

    def get_object_occupying_tile(self, tile_position):
        occupying_object = None
        if tile_position and self.location_within_bounds(tile_position):
            # Check if the tile is part of an object's collision space.
            bottom_left_tile_pos = self.get_bottom_left_tile_of_occupied_tile(tile_position)

            if bottom_left_tile_pos:
                # Get ID of object occupying the space.
                obj_id = self.bottom_left_tile_obj_mapping.get(bottom_left_tile_pos, [None])[0]

                if obj_id:
                    # Get object.
                    occupying_object = interactive_obj.InteractiveObject.get_interactive_object(obj_id)
        return occupying_object

    """
    # Returns dict mapping bottom left tile location tuple to
    # object ID of object that is different from the object that
    # was originally using that bottom left tile (or a blank tile).
    def get_changed_object_location_mapping(self):
        ret_dict = {}

        for tile_loc, obj_info in self.bottom_left_tile_obj_mapping.items():
            if tile_loc and obj_info:
                # Compare current object with original one.
                curr_id = obj_info[0]
                original_id = self.original_bottom_left_tile_obj_mapping.get(
                        tile_loc,
                        None
                    )
                if (curr_id is not None) and (curr_id != original_id):
                    # Changed from original.
                    ret_dict[tile_loc] = curr_id

        return ret_dict
    """

    """
    # Returns list of bottom left tile location tuples that used to
    # be the bottom left tile of an interactive object but no longer
    # hold one.
    def get_removed_object_bottom_left_locations(self):
        ret_list = []

        for tile_loc, obj_id in self.original_bottom_left_tile_obj_mapping.items():
            if tile_loc and obj_id:
                # Check if the originally occupied tile no longer has an obj.
                curr_obj_info = self.bottom_left_tile_obj_mapping.get(
                        tile_loc,
                        None
                    )
                if not curr_obj_info:
                    ret_list.append(tile_loc)

        return ret_list
    """

    """
    # bottom_left_tile_loc is the location tuple of the bottom left tile
    # location where the spawn action will take place.
    # If object_id is None (meaning the spawn action is to
    # remove an object), then the object occupying bottom_left_tile_loc will
    # be removed if there is one there after countdown_time_s seconds has
    # passed.
    # If object_id is not None,
    # then the object will be placed at the tile such that the bottom left
    # collision tile for the object is at bottom_left_tile_loc, after
    # the designated countdown time.
    # If the tile location already has a pending spawn action, the method
    # will not do anything, including overwriting it. # TODO - change?
    # Caller needs to refresh the map.
    def set_pending_spawn_action(self, bottom_left_tile_loc, object_id=None, countdown_time_s=0):
        if bottom_left_tile_loc \
                and not self.pending_spawn_actions.get(
                    bottom_left_tile_loc,
                    None
                ):
            countdown_ms = int(countdown_time_s * 1000)
            if countdown_ms <= 0:
                # Immediate action.
                self.execute_spawn_action(bottom_left_tile_loc, object_id)
            else:
                # Timed action.
                #curr_time_ms = timekeeper.Timekeeper.time_ms()
                curr_time_ms = pygame.time.get_ticks()
                spawn_info = [object_id, curr_time_ms, countdown_ms]
                self.pending_spawn_actions[bottom_left_tile_loc] = spawn_info
                logger.info("Added pending spawn action to tile location {0}: {1}".format(
                    bottom_left_tile_loc,
                    spawn_info
                ))
    """

    def tile_occupied(self, tile_loc):
        if tile_loc:
            if self.get_bottom_left_tile_of_occupied_tile(tile_loc):
                return True
            if self.bottom_left_tile_obj_mapping.get(tile_loc, None):
                return True
        return False

    # returns True if the tile position to check is within current map
    # boundaries
    def location_within_bounds(self, tile_pos_to_check):
        x_pos = tile_pos_to_check[0]
        y_pos = tile_pos_to_check[1]
        return (x_pos >= 0) and (y_pos >= 0) and (x_pos < self.width_in_tiles) and (y_pos < self.height_in_tiles)

    def get_accessibility_flags_from_pos(self, tile_pos):
        if self.location_within_bounds(tile_pos):
            # y,x
            return self.accessibility_grid[tile_pos[1]][tile_pos[0]]
        return tiles.Accessibility.TILE_NOT_ACCESSIBLE_F

    def can_access_tile(self, dest_tile_pos, access_method):
        accessibility_flags = self.get_accessibility_flags_from_pos(dest_tile_pos)
        return access_method & accessibility_flags > 0

    # Blits base map image starting at current top left position
    # caller needs to update surface after method
    # tile_subset_rect is rect of tile coordinates that indicates which
    # section of the map base image to blit, rather than blitting the whole map.
    # Setting to None will blit the whole map
    def blit_base_image(self, surface, tile_subset_rect=None):
        if surface and self._rendered_map_image and self.top_left_position:
            if tile_subset_rect:
                if len(tile_subset_rect) != 4:
                    raise Exception('Invalid tile subset rect length: {}'.format(len(tile_subset_rect)))
                area = pygame.Rect(
                    tile_subset_rect[0] * tiles.TILE_SIZE,
                    tile_subset_rect[1] * tiles.TILE_SIZE,
                    tile_subset_rect[2] * tiles.TILE_SIZE,
                    tile_subset_rect[3] * tiles.TILE_SIZE,
                )
                dest = (
                    self.top_left_position[0] + tile_subset_rect[0] * tiles.TILE_SIZE,
                    self.top_left_position[1] + tile_subset_rect[1] * tiles.TILE_SIZE
                )
                surface.blit(self._rendered_map_image, dest, area=area)
            else:
                surface.blit(self._rendered_map_image, self.top_left_position)

    # Blits spawned interactive overworld_obj starting at current
    # top left position of map
    # Caller needs to update surface after method
    # tile_subset_rect is rect of tile coordinates that indicates which
    # tiles to include for blitting, rather than blitting the whole map.
    # Setting to None will blit all the current spawned overworld_obj on
    # the map.
    def blit_interactive_objects(self, surface, tile_subset_rect=None, blit_time_ms=None):
        """Blits the interactive objects on the Map, left to right, top
        to down.

        Caller needs to update the pygame display surface.

        Args:
            surface: pygame Surface object to blit the objects. on.
            tile_subset_rect: rect of Tile coordinates (top left x,
                top left y, width, height) that indicates which
                Map subsection to blit, rather than blitting the whole map.
                Setting to None will blit all the Tiles in the Map.
            blit_time_ms: the system time in milliseconds to use for blitting
                the individual interactive objects. This time is used to determine
                which image to use from the object's image sequence. If None,
                or if the object doesn't have an image sequence duration,
                only the first object image will be blitted.
        """

        if surface and self.top_left_position:
            tile_subset = (0, 0, self.width_in_tiles, self.height_in_tiles)
            if tile_subset_rect:
                tile_subset = tile_subset_rect

            start_tile_x = tile_subset[0]
            start_tile_y = tile_subset[1]
            end_tile_x = start_tile_x + tile_subset[2] - 1
            end_tile_y = start_tile_y + tile_subset[3] - 1

            if (start_tile_x >= 0)                           \
                    and (start_tile_y >= 0)                  \
                    and (end_tile_x <= self.width_in_tiles)  \
                    and (end_tile_y <= self.height_in_tiles) \
                    and (end_tile_x >= start_tile_x)         \
                    and (end_tile_y >= start_tile_y):
                # Check if the Tile is occupied. Go by order of bottom left tile
                for grid_row in range(start_tile_y, end_tile_y + 1):
                    for tile_index in range(start_tile_x, end_tile_x + 1):
                        tile_loc = (tile_index, grid_row)

                        # Check if this tile is a bottom left tile for an
                        # interactive object.
                        # TODO - adjust if object is moving?
                        obj_info = self.bottom_left_tile_obj_mapping.get(tile_loc, [])
                        if obj_info:
                            obj_to_blit = interactive_obj.InteractiveObject.get_interactive_object(obj_info[0])
                            if obj_to_blit:
                                if obj_info[0] == entity.EntityID.PROTAGONIST:
                                    bottom_left_pixel = viewing.Measurements.CENTER_OW_TILE_BOTTOM_LEFT
                                    obj_to_blit.blit_onto_surface(
                                        surface,
                                        bottom_left_pixel=bottom_left_pixel,
                                        blit_time_ms=blit_time_ms,
                                    )
                                else:
                                    bottom_left_pixel = (
                                        self.top_left_position[0] + (tile_loc[0] * tiles.TILE_SIZE),
                                        self.top_left_position[1] + ((tile_loc[1] + 1) * tiles.TILE_SIZE)
                                    )

                                    # Blit the object.
                                    # TODO - change image ID depending on object type?
                                    obj_to_blit.blit_onto_surface(
                                        surface,
                                        bottom_left_pixel=bottom_left_pixel,
                                        blit_time_ms=blit_time_ms,
                                    )

    # blit entire map, including interactive overworld_obj.
    # caller needs to update surface after method
    # tile_subset_rect is a rect of tile coordinates that indicates which
    # subset of the map to blit, rather than blitting all overworld_obj on the map.
    # Setting to None will blit the entire map
    def blit_onto_surface(self, surface, tile_subset_rect=None, blit_time_ms=None):
        if self and surface and self.top_left_position:
            self.blit_base_image(surface, tile_subset_rect=tile_subset_rect)
            self.blit_interactive_objects(surface, tile_subset_rect=tile_subset_rect, blit_time_ms=blit_time_ms)

    # scroll map in the indicated direction for the indicated distance
    # also pass in surface object to blit on and update
    # does NOT update the main display - caller will have to do that
    def scroll(self, surface, scroll_direction, distance, tile_subset_rect=None):
        if self and surface and distance > 0:
            new_pixel_location = None
            curr_top_left = self.top_left_position

            if scroll_direction == directions.CardinalDirection.NORTH:
                # scroll up
                new_pixel_location = (curr_top_left[0], curr_top_left[1] - distance)
            elif scroll_direction == directions.CardinalDirection.EAST:
                # scroll right
                new_pixel_location = (curr_top_left[0] + distance, curr_top_left[1])
            elif scroll_direction == directions.CardinalDirection.SOUTH:
                new_pixel_location = (curr_top_left[0], curr_top_left[1] + distance)
            elif scroll_direction == directions.CardinalDirection.WEST:
                # scroll left
                new_pixel_location = (curr_top_left[0] - distance, curr_top_left[1])
            else:
                # invalid scroll direction
                logging.error('Invalid scroll direction {0}'.format(scroll_direction))

            if new_pixel_location:
                # Update map top left and blit map.
                self.top_left_position = new_pixel_location
                self.blit_onto_surface(surface, tile_subset_rect=tile_subset_rect)

    """
    def execute_spawn_action(self, tile_loc, obj_id):
        if tile_loc:
            # Remove the object, if any, currently on the tile.
            logger.info("Removing obj at {0}".format(tile_loc))
            removed_id = self.unset_interactive_object(tile_loc)

            if removed_id is not None:
                logger.info("Removed object id {0} from {1}".format(
                    removed_id,
                    tile_loc
                ))

            if obj_id is not None:
                # We are adding in a new object.
                logger.info("Spawning object ID {0} at {1}".format(
                    obj_id,
                    tile_loc
                ))

                self.set_interactive_object(obj_id, tile_loc)
    """

    """
    # Refreshes map. Check for respawns.
    # Does not reblit map - caller will have to do that.
    def refresh_self(
                self,
                #surface,
                #tile_subset_rect=None,
            ):
        # Update remaining timers for spawn actions.
        if self.pending_spawn_actions:
            logging.debug('Refreshing map')

            #curr_time_ms = timekeeper.Timekeeper.time_ms()
            curr_time_ms = pygame.time.get_ticks()
            to_finish = []

            for tile_loc_tuple, action_info in self.pending_spawn_actions.items():
                # action_info is of the form [object ID for object to place on tile
                # (None if removing object), time of entry or last refresh of object,
                # and remaining time in milliseconds].
                if action_info and (len(action_info) == 3):
                    elapsed_time_ms = curr_time_ms - action_info[1]
                    if elapsed_time_ms < 0:
                        logger.error("Error in elapsed time for pending spawn for map {0}".format(self.map_id))
                    else:
                        remaining_time = action_info[2] - elapsed_time_ms
                        action_info[2] = remaining_time
                        action_info[1] = curr_time_ms
                        self.pending_spawn_actions[tile_loc_tuple] = action_info

                        if remaining_time <= 0:
                            # Add to processing list.
                            to_finish.append(tile_loc_tuple)
                else:
                    logger.error("Invalid spawn action info {0}.".format(action_info))

            # Remove spawn action from the pending dict and execute
            # the spawn action.
            for loc_tuple in to_finish:
                spawn_action = self.pending_spawn_actions.pop(loc_tuple, None)

                if spawn_action:
                    obj_id = spawn_action[0]

                    self.execute_spawn_action(loc_tuple, obj_id)

            logger.debug("Remaining spawns: {0}".format(self.pending_spawn_actions))
    """

    @staticmethod
    def convert_grid_str_to_nested_int_list(grid_str):
        if not grid_str:
            return []
        ret = []
        for line in grid_str.splitlines():
            row = []
            for c in line.strip():
                row.append(int(c, 16))
            ret.append(row)
        return ret

    @staticmethod
    def get_map_images_dir_path():
        return os.path.join(util.get_images_path(), 'maps')

    # Builds map based on given map yaml file. If the yaml file contains
    # valid map info, adds the map to the class map_listing variable and returns the map
    @classmethod
    def map_factory(cls, map_yaml_path):
        stripped = util.strip_yaml(map_yaml_path)
        if not stripped:
            raise Exception('No map data provided in {}'.format(map_yaml_path))
        map_data = stripped[0]
        if not stripped[0]:
            raise Exception('No map data provided in {}'.format(map_yaml_path))
        logging.debug('Parsing map data from {}'.format(map_yaml_path))

        # parse fields
        map_id = map_data.get('id', None)
        if not map_id:
            raise Exception('No map ID provided from {}'.format(map_yaml_path))

        image_file = map_data.get('image_file', None)
        if not image_file:
            raise Exception('No map image file provided from {}'.format(map_yaml_path))
        image_path = os.path.join(cls.get_map_images_dir_path(), image_file)
        if not os.path.isfile(image_path):
            raise Exception('Map image file {} not found.'.format(image_path))
        image_width = map_data.get('image_width_px', None)
        image_height = map_data.get('image_height_px', None)
        if not image_width:
            raise Exception('No map image width provided from {}'.format(map_yaml_path))
        if not image_height:
            raise Exception('No map image height provided from {}'.format(map_yaml_path))

        accessibility_grid_str = map_data.get('accessibility_grid', None)
        if not accessibility_grid_str:
            raise Exception('No accessibility_grid field provided from {}'.format(map_yaml_path))

        accessibility_grid = cls.convert_grid_str_to_nested_int_list(accessibility_grid_str)
        if not accessibility_grid:
            raise Exception('Could not parse accessibility grid from {}'.format(map_yaml_path))

        music_file = map_data.get('music_file', '')
        if music_file:
            music_file = os.path.join(util.get_music_path(), music_file)
            if not os.path.isfile(music_file):
                raise Exception('Map music file {} not found.'.format(music_file))

        # TODO connector tile dict

        # TODO adjacent map dict

        logging.debug('Creating map with ID {0}, image path {1}, image width {2}, image height {3}'.format(
            map_id,
            image_path,
            image_width,
            image_height,
        ))

        ret_map = Map(
            map_id,
            image_path,
            image_width,
            image_height,
            accessibility_grid,
            music_file=music_file,
        )

        # TODO - init interactive overworld_obj

        Map.map_listing[map_id] = ret_map
        return ret_map

    @classmethod
    def get_map(cls, map_id):
        ret_map = Map.map_listing.get(map_id, None)
        if not ret_map:
            logging.warning('Get_map: No map found for map id {0}'.format(map_id))
        return ret_map

    @classmethod
    def build_maps(cls):
        logging.info('Building maps')
        try:
            for map_yaml in glob.glob(os.path.join(util.get_yaml_path(), 'maps', '*.yml')):
                if not Map.map_factory(map_yaml):
                    raise Exception('Failed to build map for {}'.format(map_yaml))
        except Exception as e:
            raise Exception('Failed to build maps: {}', e)
