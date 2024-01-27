import pygame
import logging
import sys

from app.viewing import viewing, display, colors, fonts, menu_options
from app.images import image_paths
from lang import language
from util import timekeeper, util


class SelectionGridViewing(viewing.BaseView):
    # TODO update documentation
    # background color is fill color for background in case no
    # background image is available.
    # bottom_text_display_height indicates the pixel height for the
    # area where text will appear at the bottom of the viewing.
    # bottom_text is the text to blit in the bottom_text_rect.
    # allowed_selection_option_set is a set of allowed option IDs to show for
    # icons selected in this viewing. Set to None or empty set to allow
    # no options.
    def __init__(self, main_display_surface, selection_icon_dimensions, display_pattern=display.PatternID.PATTERN_2,
                 enlarged_selection_background_path=image_paths.ITEM_LISTING_SELECTED_ENLARGED_BACKGROUND_PATH):
        # TODO make title_info, bottom_text, and allowed_selection_option_set be
        # passed in on blit methods rather than initializer.

        viewing.BaseView.__init__(self, main_display_surface)
        # TODO handle when inventory length = 0.

        self.display_pattern = display_pattern
        self.icon_supertext_font_object = None
        self.icon_supertext_font_color = colors.COLOR_WHITE

        self.display_rect = viewing.Measurements.INVENTORY_BASIC_VIEWING_RECT
        self.selection_icon_dimensions = selection_icon_dimensions
        self.enlarged_icon_dimensions = (2 * selection_icon_dimensions[0], 2 * selection_icon_dimensions[1])

        self.enlarged_selection_background = None
        if enlarged_selection_background_path:
            self.enlarged_selection_background = pygame.image.load(enlarged_selection_background_path).convert_alpha()

        # Calculate the various base viewing rects for the inventory.
        top_display_width = int(0.6 * self.display_rect.width)
        top_display_height = 50

        self.top_display_rect = pygame.Rect(
            self.display_rect.x,
            self.display_rect.y,
            top_display_width,
            top_display_height,
        )

        selection_details_width = (self.display_rect.width - top_display_width
                                   - viewing.Measurements.GRID_VIEWING_IN_BETWEEN_PADDING)
        selection_details_height = self.display_rect.height
        self.selection_details_rect = pygame.Rect(
            self.top_display_rect.right + viewing.Measurements.GRID_VIEWING_IN_BETWEEN_PADDING,
            self.display_rect.y,
            selection_details_width,
            selection_details_height
        )

        selection_listing_width = top_display_width
        selection_listing_height = (self.display_rect.height - self.top_display_rect.height
                                    - viewing.Measurements.GRID_VIEWING_IN_BETWEEN_PADDING)

        bottom_text_width = top_display_width
        bottom_text_height = int(self.display_rect.height / 4) - viewing.Measurements.GRID_VIEWING_IN_BETWEEN_PADDING

        truncated_selection_listing_height = (selection_listing_height - bottom_text_height -
                                              viewing.Measurements.GRID_VIEWING_IN_BETWEEN_PADDING)

        self.bottom_text_rect = pygame.Rect(
            self.display_rect.x,
            self.display_rect.bottom - bottom_text_height,
            bottom_text_width,
            bottom_text_height,
        )
        self.bottom_text_display = None

        """
        if self.bottom_text:
            # Make room for bottom text.
            bottom_text_height = int(self.display_rect.height / 4) \
                                - viewingdata.GRID_VIEWING_IN_BETWEEN_PADDING
            selection_listing_height -= (
                    bottom_text_height \
                    + viewingdata.GRID_VIEWING_IN_BETWEEN_PADDING
                )
            self.bottom_text_rect = pygame.Rect(
                self.display_rect.x,
                self.display_rect.bottom - bottom_text_height,
                bottom_text_width,
                bottom_text_height,
            )
        """

        self.selection_grid_rect = pygame.Rect(
            self.display_rect.x,
            self.top_display_rect.bottom + viewing.Measurements.GRID_VIEWING_IN_BETWEEN_PADDING,
            selection_listing_width,
            selection_listing_height
        )

        # In case of bottom text.
        self.truncated_selection_grid_rect = pygame.Rect(
            self.display_rect.x,
            self.top_display_rect.bottom + viewing.Measurements.GRID_VIEWING_IN_BETWEEN_PADDING,
            selection_listing_width,
            truncated_selection_listing_height
        )

        # Will display the title.
        self.title_display = None

        # Will display the selections in the inventory.
        self.selection_grid_display = None
        self.truncated_selection_grid_display = None

        self.selection_details_side_display = display.Display(
            self.main_display_surface,
            self.selection_details_rect,
            background_pattern=self.display_pattern,
        )

    # Requires fonts to be loaded. see display.Display.init_fonts()
    # Inherited method.
    def create_title_display(self):
        logging.info("Creating title display...")
        font_obj = fonts.Fonts.get_font(fonts.SELECTION_TOP_DISPLAY_FONT_ID)
        if font_obj:
            self.title_display = display.TextDisplay(
                self.main_display_surface,
                self.top_display_rect,
                font_obj,
                background_color=None,
                # background_image_path=image_paths.INVENTORY_BASIC_TITLE_BACKGROUND_PATH,
                background_pattern=self.display_pattern,
                background_image_path=None,
                horizontal_padding=0,
                vertical_padding=0,
            )

            if not self.title_display:
                logging.error("Failed to make title display")
        else:
            logging.error("Top display font not found.")
            logging.error("Must init fonts through display.Display.init_fonts.")

    # Inherited method.
    def create_selection_grid_display(self):
        logging.info("Creating main selection grid display...")
        font_obj = fonts.Fonts.get_font(
                fonts.SELECTION_SUPERTEXT_FONT_ID
            )
        if font_obj:
            self.icon_supertext_font_object = font_obj
            self.icon_supertext_font_color = colors.COLOR_WHITE
            self.selection_grid_display = display.IconGridDisplay(
                self.main_display_surface,
                self.selection_grid_rect,
                self.selection_icon_dimensions,
                background_pattern=self.display_pattern,
                background_image_path=None,
                background_color=None,
                horizontal_padding=viewing.Measurements.ITEM_LISTING_HORIZONTAL_PADDING,
                vertical_padding=viewing.Measurements.ITEM_LISTING_VERTICAL_PADDING,
                continue_up_icon_image_path=image_paths.ITEM_LISTING_CONT_UP_PATH,
                continue_down_icon_image_path=image_paths.ITEM_LISTING_CONT_DOWN_PATH,
                selection_image_path=image_paths.ITEM_LISTING_SELECTED_DEFAULT_PATH,
            )

            if not self.selection_grid_display:
                logging.error("Failed to make selection grid display")
        else:
            logging.error("Selection grid supertext font not found.")
            logging.error("Must init fonts through display.Display.init_fonts.")

    # Inherited method.
    def create_truncated_selection_grid_display(self):
        logging.info("Creating truncated selection grid display...")
        font_obj = fonts.Fonts.get_font(fonts.SELECTION_SUPERTEXT_FONT_ID)
        if font_obj:
            self.icon_supertext_font_object = font_obj
            self.icon_supertext_font_color = colors.COLOR_WHITE
            self.truncated_selection_grid_display = display.IconGridDisplay(
                self.main_display_surface,
                self.truncated_selection_grid_rect,
                self.selection_icon_dimensions,
                background_pattern=self.display_pattern,
                background_image_path=None,
                background_color=None,
                horizontal_padding=viewing.Measurements.ITEM_LISTING_HORIZONTAL_PADDING,
                vertical_padding=viewing.Measurements.ITEM_LISTING_VERTICAL_PADDING,
                continue_up_icon_image_path=image_paths.ITEM_LISTING_CONT_UP_PATH,
                continue_down_icon_image_path=image_paths.ITEM_LISTING_CONT_DOWN_PATH,
                selection_image_path=image_paths.ITEM_LISTING_SELECTED_DEFAULT_PATH,
            )

            if not self.truncated_selection_grid_display:
                logging.error("Failed to make truncated selection grid display")
        else:
            logging.error("Selection grid supertext font not found.")
            logging.error("Must init fonts through display.Display.init_fonts.")

    # Inherited method.
    def create_bottom_text_display(self):
        if self.bottom_text_rect:
            logging.info("Creating iselection bottom text display...")
            font_obj = fonts.Fonts.get_font(fonts.SELECTION_BOTTOM_TEXT_FONT_ID)
            if font_obj:
                self.bottom_text_display = display.TextDisplay(
                    self.main_display_surface,
                    self.bottom_text_rect,
                    font_obj,
                    background_color=None,
                    background_image_path=None,
                    background_pattern=self.display_pattern,
                    horizontal_padding=20,
                    vertical_padding=20,
                )

                if not self.bottom_text_display:
                    logging.error("Failed to make inventory bottom text display")
            else:
                logging.error("Display font not found.")
                logging.error("Must init fonts through display.Display.init_fonts.")

    # Requires fonts to be loaded. see display.Display.init_fonts().
    # Inherited method.
    def create_base_displays(self):
        self.create_title_display()
        self.create_truncated_selection_grid_display()
        self.create_selection_grid_display()
        self.create_bottom_text_display()

    # Refreshes self. Does not update display.
    # Inherited method.
    def refresh_self(self):
        pass

    def refresh_and_blit_self(self):
        self.refresh_self()
        self.blit_self()

    # Blits self.
    # Inherited method.
    def blit_selection_background(self, title_info, bottom_text=None):
        # Blit details background.
        if self.selection_details_side_display:
            self.selection_details_side_display.blit_background(self.main_display_surface)

        # Handle selection title display.
        if self.title_display:
            # Get title text.
            title_text = title_info.get(language.Language.get_current_language(), None)

            if title_text:
                self.display_text_display_first_page(
                    self.title_display,
                    title_text,
                    advance_delay_ms=0,
                    auto_advance=True,
                    refresh_during=False,
                    refresh_after=False,
                )

        # Handle bottom text display.
        if bottom_text:
            self.display_text_display_first_page(
                self.bottom_text_display,
                bottom_text,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
            )
            self.truncated_selection_grid_display.blit_background(self.main_display_surface)
        else:
            self.selection_grid_display.blit_background(self.main_display_surface)

    # Does not update display.
    # This method should be called before calling display_
    def blit_self(self):
        pass

    # Overridable by child.
    def blit_main_selection_details(self, selection_info):
        pass

    # Overridable by child.
    def blit_selection_details(self, selection_info):
        pass

    # Overridable by child.
    def get_selection_options(self, selection_info, allowed_option_set=None):
        return None

    # Overridable by child.
    def display_selection_options(self, selection_info, allowed_selection_option_set=None):
        pass

    # Overridable by child.
    def convert_to_icon_data_list(self, selection_data_list):
        return None

    # Handles displaying the item listing and returns
    # the selected option and item index as a tuple
    # (None if no option is selected).
    # custom_actions is a dict that maps pygame keys to
    # option IDs to return (will return the tuple of (option ID, curr_index)).
    # Used for custom actions like having
    # the user switch from this selection grid to a different one
    # by pressing a certain key.
    # Inherited method.
    def handle_selection_grid(self, title_info, selection_data_list,  # list of [selection object, supertext]
                              starting_selected_index=0, preselected_index_list=None, custom_actions=None,
                              bottom_text=None, allowed_selection_option_set=None):
        ret_info = None
        max_index = len(selection_data_list) - 1
        icon_data_list = []

        display_to_use = self.selection_grid_display

        if bottom_text:
            display_to_use = self.truncated_selection_grid_display

        if selection_data_list:
            icon_data_list = self.convert_to_icon_data_list(selection_data_list)

        if selection_data_list and icon_data_list:
            # Start with the first item.
            curr_index = starting_selected_index
            first_viewable_row_index = display_to_use.get_row_index(curr_index)
            last_viewable_row_index = first_viewable_row_index + display_to_use.num_rows - 1

            done = False
            changed_index = True

            while not done:
                curr_selected_row = display_to_use.get_row_index(curr_index)
                if curr_selected_row < first_viewable_row_index:
                    # Scroll down.
                    first_viewable_row_index = curr_selected_row
                    last_viewable_row_index = first_viewable_row_index + display_to_use.num_rows - 1
                elif curr_selected_row > last_viewable_row_index:
                    # Scroll up.
                    last_viewable_row_index = curr_selected_row
                    first_viewable_row_index = max(0, last_viewable_row_index - display_to_use.num_rows + 1)

                logging.debug("Curr row index {0}. First viewable: {1}. Last viewable: {2}".format(
                    curr_selected_row,
                    first_viewable_row_index,
                    last_viewable_row_index
                ))

                if changed_index:
                    self.blit_selection_background(title_info, bottom_text=bottom_text)
                    pygame.display.update()

                go_down = False
                go_up = False
                go_left = False
                go_right = False
                open_options = False
                received_input = False
                curr_selection_info = selection_data_list[curr_index]

                if changed_index:
                    display_to_use.blit_icon_listing(
                        self.main_display_surface,
                        icon_data_list,
                        first_viewable_row_index,
                        curr_index,
                        preselected_index_list=preselected_index_list,
                        show_continue_icon=True,
                        alternative_top_left=None,
                    )
                    if curr_selection_info:
                        self.blit_selection_details(curr_selection_info)
                    pygame.display.update()
                while not received_input:
                    timekeeper.Timekeeper.tick()

                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key == pygame.K_ESCAPE:
                                logging.info("Leaving selection viewing.")
                                received_input = True
                                done = True
                                go_down = False
                                go_up = False
                                go_left = False
                                go_right = False
                                open_options = False
                            elif events.key == pygame.K_DOWN:
                                logging.info("Going down in grid.")
                                go_down = True
                                go_up = False
                                go_left = False
                                go_right = False
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_UP:
                                logging.info("Going up in grid.")
                                go_down = False
                                go_up = True
                                go_left = False
                                go_right = False
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_LEFT:
                                logging.info("Going left in grid.")
                                go_down = False
                                go_up = False
                                go_left = True
                                go_right = False
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_RIGHT:
                                logging.info("Going right in grid.")
                                go_down = False
                                go_up = False
                                go_left = False
                                go_right = True
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_RETURN:
                                logging.info("Opening menu")
                                go_down = False
                                go_up = False
                                go_left = False
                                go_right = False
                                open_options = True
                                received_input = True
                            elif custom_actions and events.key in custom_actions:
                                ret_option_id = custom_actions.get(events.key, None)
                                if ret_option_id:
                                    logging.info("Activating custom action {0}".format(ret_option_id))
                                    received_input = True
                                    ret_info = (ret_option_id, curr_index)
                                    done = True
                                else:
                                    received_input = False

                                go_down = False
                                go_up = False
                                go_left = False
                                go_right = False
                                open_options = False

                if received_input:
                    new_index = curr_index
                    if go_down:
                        new_index = min(max_index, curr_index + display_to_use.num_columns)
                    elif go_up:
                        new_index = max(0, curr_index - display_to_use.num_columns)
                    elif go_right:
                        new_index = min(max_index, curr_index + 1)
                    elif go_left:
                        new_index = max(0, curr_index - 1)
                    elif open_options:
                        # Show item options.
                        self.blit_selection_background(title_info, bottom_text=bottom_text)
                        ret_option = self.display_selection_options(curr_selection_info)

                        if ret_option and ret_option != menu_options.MenuOptionID.CANCEL_OPTION:
                            done = True
                            ret_info = (ret_option, curr_index)
                        else:
                            self.blit_selection_background(title_info, bottom_text=bottom_text)
                            self.blit_selection_details(curr_selection_info)

                            pygame.display.update()

                    if new_index != curr_index:
                        changed_index = True
                        curr_index = new_index
                    else:
                        changed_index = False

                    logging.info("Curr index now: {0}".format(curr_index))
                    # TODO rest

        # Handle blank selection data.
        elif len(selection_data_list) == 0:
            self.blit_selection_background(title_info, bottom_text=bottom_text)

            pygame.display.update()
            received_input = False

            while not received_input:
                timekeeper.Timekeeper.tick()

                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                    elif events.type == pygame.KEYDOWN:
                        if events.key == pygame.K_ESCAPE:
                            logging.info("Leaving selection viewing.")
                            received_input = True

        logging.info("Returning selection: {0}".format(ret_info))
        return ret_info


class ItemSelectionGridViewing(SelectionGridViewing):
    def __init__(self, main_display_surface, item_icon_dimensions, display_pattern=display.PatternID.PATTERN_2,
                 enlarged_selection_background_path=image_paths.ITEM_LISTING_SELECTED_ENLARGED_BACKGROUND_PATH):
        SelectionGridViewing.__init__(self, main_display_surface, item_icon_dimensions,
                                      display_pattern=display_pattern,
                                      enlarged_selection_background_path=enlarged_selection_background_path)
        # Create additional display dimensions.

        # Will display item name of selected item.
        self.selection_name_display = None
        self.selection_name_rect = pygame.Rect(
            self.selection_details_rect.x,
            self.selection_details_rect.y + 15,
            self.selection_details_rect.width,
            80,
        )
        self.selection_name_rect.centerx = self.selection_details_rect.centerx

        # Will display subtitle of selected object.
        self.selection_subtitle_display = None
        self.selection_subtitle_rect = pygame.Rect(
            self.selection_details_rect.x,
            self.selection_name_rect.bottom + 10,
            self.selection_details_rect.width,
            30,
        )
        self.selection_subtitle_rect.centerx = self.selection_details_rect.centerx

        # Will display enlarged image icon of selected item.
        self.icon_enlarged_display = None
        self.icon_enlarged_rect = pygame.Rect(
            self.selection_details_rect.x,
            self.selection_subtitle_rect.bottom + 10,
            self.enlarged_icon_dimensions[0],
            self.enlarged_icon_dimensions[1]
        )
        self.icon_enlarged_rect.centerx = self.selection_details_rect.centerx

        # Will display details about a single item in the inventory.
        self.selection_description_display = None
        self.selection_description_rect = pygame.Rect(
            self.selection_details_rect.x,
            self.icon_enlarged_rect.bottom,
            self.selection_details_rect.width,
            self.selection_details_rect.bottom - self.icon_enlarged_rect.bottom
        )

        # Will display item options for a selected item.
        self.selection_option_menu_display = None
        self.selection_option_menu_rect = pygame.Rect(
            self.selection_details_rect.x,
            self.icon_enlarged_rect.bottom + 15,
            self.selection_details_rect.width - 30,
            self.selection_details_rect.bottom - self.icon_enlarged_rect.bottom - 15
        )
        self.selection_option_menu_rect.centerx = self.selection_description_rect.centerx

    def create_selection_name_display(self):
        logging.info("Creating selection name display...")
        font_obj = fonts.Fonts.get_font(fonts.SELECTION_NAME_FONT_ID)
        if font_obj:
            self.selection_name_display = display.TextDisplay(
                self.main_display_surface,
                self.selection_name_rect,
                font_obj,
                background_color=None,
                background_image_path=None,
                horizontal_padding=20,
                vertical_padding=0,
            )
            if not self.selection_name_display:
                logging.error("Failed to make selection name display")
        else:
            logging.error("Font not found.")
            logging.error("Must init fonts through display.Display.init_fonts.")

    def create_selection_subtitle_display(self):
        logging.info("Creating selection subtitle display...")
        font_obj = fonts.Fonts.get_font(fonts.SELECTION_SUBTITLE_FONT_ID)
        if font_obj:
            self.selection_subtitle_display = display.TextDisplay(
                self.main_display_surface,
                self.selection_subtitle_rect,
                font_obj,
                background_color=None,
                background_image_path=None,
                horizontal_padding=20,
                vertical_padding=0,
            )
            if not self.selection_subtitle_display:
                logging.error("Failed to make selection subtitle display")
        else:
            logging.error("Font not found.")
            logging.error("Must init fonts through display.Display.init_fonts.")

    def create_selection_description_display(self):
        logging.info("Creating selection description display...")
        font_obj = fonts.Fonts.get_font(fonts.SELECTION_DESCRIPTION_FONT_ID)
        if font_obj:
            self.selection_description_display = display.TextDisplay(
                self.main_display_surface,
                self.selection_description_rect,
                font_obj,
                background_color=None,
                background_image_path=None,
                horizontal_padding=20,
                vertical_padding=20,
            )
            if not self.selection_description_display:
                logging.error("Failed to make selection description display")
        else:
            logging.error("Display font not found.")
            logging.error("Must init fonts through display.Display.init_fonts.")

    def create_selection_options_display(self):
        logging.info("Creating selection options display...")
        font_obj = fonts.Fonts.get_font(fonts.SELECTION_MENU_FONT_ID)
        if font_obj:
            self.selection_option_menu_display = display.MenuDisplay(
                self.main_display_surface,
                self.selection_option_menu_rect,
                font_obj,
                background_color=colors.BackgroundColors.P1_BG_3_COLOR,
                background_image_path=None,
                background_pattern=None,
                horizontal_padding=20,
                vertical_padding=20,
            )
            if not self.selection_option_menu_display:
                logging.error("Failed to make selection options display")
        else:
            logging.error("Display font not found.")
            logging.error("Must init fonts through display.Display.init_fonts.")

    def display_selection_options(self, selection_info, allowed_selection_option_set=None):
        ret_option = None

        self.blit_main_selection_details(selection_info)

        # Get valid options.
        options_to_show = self.get_selection_options(
            selection_info,
            allowed_option_set=allowed_selection_option_set,
        )

        if options_to_show:
            ret_option = self.display_menu_display(
                self.selection_option_menu_display,
                options_to_show,
                horizontal_orientation=display.Orientation.CENTERED,
                vertical_orientation=display.Orientation.TOP_JUSTIFIED,
                load_delay_ms=viewing.ViewingTime.DEFAULT_MENU_LOAD_DELAY_MS,
                option_switch_delay_ms=viewing.ViewingTime.DEFAULT_MENU_OPTION_SWITCH_DELAY_MS,
                refresh_during=False,
                refresh_after=False,
                alternative_top_left=None,
            )

        return ret_option

    def create_additional_displays(self):
        self.create_selection_name_display()
        self.create_selection_subtitle_display()
        self.create_selection_description_display()
        self.create_selection_options_display()

    def blit_selected_object_name(self, selected_obj):
        if selected_obj:
            # Blit object name.
            obj_name = selected_obj.get_name()
            self.display_text_display_first_page(
                self.selection_name_display,
                obj_name,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
                horizontal_orientation=display.Orientation.CENTERED,
                vertical_orientation=display.Orientation.TOP_JUSTIFIED,
                alternative_top_left=None,
            )

    def blit_selected_object_quantity(self, quantity):
        if quantity:
            # Blit quantity.
            quantity_text = "x" + str(quantity)
            self.display_text_display_first_page(
                self.selection_subtitle_display,
                quantity_text,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
                horizontal_orientation=display.Orientation.CENTERED,
                vertical_orientation=display.Orientation.TOP_JUSTIFIED,
                alternative_top_left=None,
            )

    def blit_selected_object_enlarged_icon(self, selected_obj):
        if selected_obj:
            # Blit enlarged icon and background.
            enlarged_icon = selected_obj.get_enlarged_icon()
            if enlarged_icon:
                if self.enlarged_selection_background:
                    enlarged_background_rect = self.enlarged_selection_background.get_rect(
                        center=self.icon_enlarged_rect.center
                    )
                    self.main_display_surface.blit(
                        self.enlarged_selection_background,
                        enlarged_background_rect
                    )
                enlarged_icon_rect = enlarged_icon.get_rect(center=self.icon_enlarged_rect.center)
                self.main_display_surface.blit(enlarged_icon, enlarged_icon_rect)

    def blit_selection_description(self, selected_obj):
        # Blit item description and usage info.
        if selected_obj:
            item_info = "\n".join([
                selected_obj.get_description_info(),
                '--------',
                selected_obj.get_usage_info()
            ])
            self.display_text_display_first_page(
                self.selection_description_display,
                item_info,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
                horizontal_orientation=display.Orientation.LEFT_JUSTIFIED,
                vertical_orientation=display.Orientation.TOP_JUSTIFIED,
                alternative_top_left=None,
            )

    def blit_main_selection_details(self, selection_info):
        self.blit_selected_object_name(selection_info[0])
        self.blit_selected_object_quantity(selection_info[1])
        self.blit_selected_object_enlarged_icon(selection_info[0])

    def blit_selection_details(self, selection_info):
        self.blit_main_selection_details(selection_info)
        self.blit_selection_description(selection_info[0])

    # Overridden.
    def get_selection_options(self, selection_info, allowed_option_set=None):
        selection_options = []
        selection_obj = selection_info[0]

        option_list = selection_obj.item_menu_option_ids + [menu_options.MenuOptionID.CANCEL_OPTION]

        for option in option_list:
            if allowed_option_set and option in allowed_option_set:
                selection_options.append(option)
        return selection_options

    # Overridden.
    def convert_to_icon_data_list(self, selection_data_list):
        ret_data = None
        if selection_data_list:
            ret_data = []
            for data in selection_data_list:
                curr_object = data[0]
                curr_image = None
                quantity = data[1]
                quantity_text = None

                if curr_object:
                    curr_image = curr_object.get_icon()

                if curr_object.is_stackable():
                    quantity_text = util.get_abbreviated_quantity(quantity)

                rendered_supertext = None
                if quantity_text:
                    rendered_supertext = self.icon_supertext_font_object.render(
                        quantity_text,
                        False,
                        self.icon_supertext_font_color,
                    )
                ret_data.append([curr_image, rendered_supertext])
        return ret_data

    @classmethod
    def create_item_selection_grid_viewing(cls, main_display_surface, item_icon_dimensions,
                                           display_pattern=display.PatternID.PATTERN_2):
        ret_viewing = None
        if main_display_surface:
            ret_viewing = ItemSelectionGridViewing(
                main_display_surface,
                item_icon_dimensions,
                display_pattern=display_pattern,
            )

            # Create displays for viewing.
            ret_viewing.create_base_displays()
            ret_viewing.create_additional_displays()

        return ret_viewing
