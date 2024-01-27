import logging
import math
import pygame
from enum import Enum

from app.viewing import colors, menu_options
from app.images import image_paths

SIZE_TEST_STRING = "abcdefghijklmnopqrstuvwxyz" \
                    + "1234567890" \
                    + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                    + ":;[]{},./?<>-_=+~`!@#$%^&*()\\|\"'"


class Spacing:
    # Space between text and the continue icon.
    CONTINUE_ICON_HORIZ_SPACE = 6

    # Space between text and the selected option icon.
    SELECTION_ICON_HORIZ_SPACE = 8

    # Spacing factors for space between lines.
    DEFAULT_LINE_SPACING_FACTOR = 1.1
    TEXT_BOX_LINE_SPACING_FACTOR = 1.1
    MENU_LINE_SPACING_FACTOR = 1.5

    # Number of pixels in between each icon slot.
    ICON_VIEWING_PIXEL_SPACING = 15


class Orientation(Enum):
    CENTERED = 0x1
    LEFT_JUSTIFIED = 0x2
    RIGHT_JUSTIFIED = 0x3
    TOP_JUSTIFIED = 0x4
    BOTTOM_JUSTIFIED = 0x5


class PatternID(Enum):
    DEFAULT = 0x1
    PATTERN_1 = 0x11
    PATTERN_2 = 0x12


class DisplayCorner(Enum):
    NW_CORNER = 0x1
    NE_CORNER = 0x2
    SE_CORNER = 0x3
    SW_CORNER = 0x4

# TODO - just have pages be lists of the rendered texts...


class TextPage:
    """A class used to represent a single text page for a text display.

    Each TextPage object will contain a list of strings that make up
    the text for one text box.

    This class is a helper class for Display classes. Non-Display classes
    should not be directly creating TextPage overworld_obj except through
    using Display methods.

    Attributes:
        text_lines: list of Strings, where each String is a single text line
            for the text page.
    """

    def __init__(self, line_list, font_object, font_color):
        """Creates a TextPage object with the given text lines.

        Args
            line_list: list of Strings representing the text lines for the
                TextPage object to hold.
        """
        self._text_lines = []
        self._rendered_text_lines = []

        if line_list and font_object and font_color:
            for item in line_list:
                rendered_text = font_object.render(
                    item,
                    False,
                    font_color,
                )
                self._rendered_text_lines.append(rendered_text)
                self._text_lines.append(item)

    """
    @classmethod
    def merge_pages(cls, page_list):
        ret_page = None

        if page_list:
            ret_page = TextPage(None, None, None)

            for page in page_list:
                ret_page._text_lines += page.text_lines
                ret_page._rendered_text_lines += page.rendered_text_lines

        return ret_page
    """

    @property
    def text_lines(self):
        """Returns the array of text lines for the page."""
        return self._text_lines

    @property
    def rendered_text_lines(self):
        """Returns the array of rendered text lines for the page."""
        return self._rendered_text_lines

    def get_num_text_lines(self):
        return len(self._text_lines)

    def get_num_rendered_lines(self):
        return len(self._rendered_text_lines)


class MenuPage:
    """A class used to represent a single menu page for a menu display.

    Each MenuPage object will contain a list of option ID numbers that make up
    the options for one menu page. The order of the option IDs in the list
    determine the order in which the options are shown.

    One option ID corresponds to one line in the menu page.

    This class is a helper class for Display classes. Non-Display classes
    should not be directly creating MenuPage overworld_obj except through
    using Display methods.

    Attributes:
        option_id_list: list of integers, where each integer represents the
            option ID for the option to show on the menu page.
    """

    def __init__(
            self,
            option_id_list,
            font_object,
            font_color=colors.COLOR_BLACK):
        """Creates a MenuPage object with the given option IDs.

        Args:
            option_id_list: list of integers representing the options for the
                MenuPage object to hold.
        """
        # List of tuples of (option ID, rendered option text).
        self._option_list = []
        self.font_object = font_object

        if option_id_list:
            for option_id in option_id_list:
                # $$ TODO
                option_text = menu_options.get_option_name(option_id)

                if option_text:
                    rendered_text = self.font_object.render(
                        option_text,
                        False,
                        font_color,
                    )
                    if rendered_text:
                        self._option_list.append((option_id, rendered_text))

    def get_num_options(self):
        """Returns the number of options for this menu page."""
        return len(self._option_list)

    def get_option_info(self, index):
        """Returns the option info at the given index.
        The method assumes that the index is within bounds.

        Args:
            self: calling object.
            index: array index for the option ID.
        """
        return self._option_list[index]

    def get_option_id(self, index):
        """Returns the option ID at the given index.
        The method assumes that the index is within bounds.

        Args:
            self: calling object.
            index: array index for the option ID.
        """
        return self._option_list[index][0]

    @property
    def option_list(self):
        """Returns the array of option IDs for the page."""
        return self._option_list


class Display:
    # Maps pattern IDs to dicts that map pattern portion IDs to images.
    pattern_data = {}

    def __init__(
            self,
            main_display_surface,
            display_rect,
            background_pattern=None,
            background_image_path=None,
            background_color=colors.COLOR_WHITE):
        """ Initializes the base Display object.

        Args:
            self: self object.
            main_display_surface: pygame Surface object to use for blitting
                text and other display elements on.
            display_rect: pygame Rect object to define the dimensions of
                the Display object.
            background_pattern: integer representing the background pattern
                ID for the Display. Set to None to avoid using a background
                pattern.
            background_image_path: String for the file path leading to
                the image for the Display's background. Set to None to
                avoid giving the Display a background image.
                If no background image is assigned, the Display will use
                the background_color as a fill color if applicable.
                For best results, the background image should be the same
                size the as display_rect dimensions.
            background_color: length-3 tuple for the color representation
                (e.g. (255, 255, 255) for black) to use in the case of
                no background image. The color will be the fill color
                for the Display. Defaults to white (0, 0, 0).
                Can set to None to skip using any background fill color.
        """
        self.main_display_surface = main_display_surface
        self.display_rect = display_rect
        self.background_color = background_color
        self.background_pattern_id = background_pattern
        self.background_image_path = background_image_path
        self.background_image = None
        self.get_background_image()

    # Does not update display, caller must do that.
    def blit_background(
            self,
            surface,
            alternative_top_left=None,
            alternative_height=None):
        """Blits the Display background.

        Does not update the display. Caller must do that.
        If a background pattern is set, the pattern will determine
        the background. Otherwise, if no background pattern is set, and if
        a background image is set, image will get blitted.
        If no background image is set and no pattern is set, the
        background color will be used to fill the background.
        If neither a pattern nor an image nor fill color are set,
        no background work will be done.

        By default, the method will blit the background according to the
        Display object's Rect dimensions. If the caller wishes to change
        the location of where the blit the background, then the caller
        can specify a new top left coordinate using the
        alternative_top_left parameter.

        Args:
            self: calling object.
            surface: pygame Surface object to blit the Display background on.
            alternative_top_left: Optional parameter to change the top-left
                pixel location to start blitting the Display background.
                The format is a tuple of the x,y pixel coordinates.
            alternative_height: Optional parameter to change the height of
                the blitted background.
        """

        if surface:
            target_rect = self.display_rect

            # Change top left starting point if needed.
            if alternative_top_left is not None:
                target_rect = pygame.Rect(
                    alternative_top_left,
                    (self.display_rect.width, self.display_rect.height)
                )

            # Change height of rect if needed.
            if alternative_height is not None:
                target_rect.height = alternative_height

            # Blit the background image/default fill color.
            # TODO handle background pattern.
            if self.background_image:
                surface.blit(self.background_image, target_rect)
            elif self.background_color:
                pygame.draw.rect(surface, self.background_color, target_rect)

    @classmethod
    def get_background_pattern_default(cls, width, height):
        background = None
        if width and height:
            background = pygame.Surface((width, height), flags=pygame.SRCALPHA, depth=32).convert_alpha()
            background.fill(colors.COLOR_WHITE)
        return background

    @classmethod
    def get_background_pattern_1(cls, width, height):
        background = None
        if width and height:
            background = pygame.Surface((width, height), flags=pygame.SRCALPHA, depth=32).convert_alpha()

            # Add pattern #1 corners.
            nw_corner = Display.pattern_data.get(PatternID.PATTERN_1, {}).get(DisplayCorner.NW_CORNER, None)
            ne_corner = Display.pattern_data.get(PatternID.PATTERN_1, {}).get(DisplayCorner.NE_CORNER, None)
            se_corner = Display.pattern_data.get(PatternID.PATTERN_1, {}).get(DisplayCorner.SE_CORNER, None)
            sw_corner = Display.pattern_data.get(PatternID.PATTERN_1, {}).get(DisplayCorner.SW_CORNER, None)

            first_rect = pygame.Rect(3, 3, width - 6, height - 6)
            second_rect = pygame.Rect(5, 5, width - 10, height - 10)
            third_rect = pygame.Rect(9, 9, width - 18, height - 18)

            background.fill(colors.BackgroundColors.P1_BG_1_COLOR, rect=first_rect)
            background.fill(colors.BackgroundColors.P1_BG_2_COLOR, rect=second_rect)
            background.fill(colors.BackgroundColors.P1_BG_3_COLOR, rect=third_rect)

            if nw_corner:
                result = background.blit(nw_corner, (0, 0))
                logging.debug(result)
            else:
                logging.warning("No NW Corner for pattern 1.")

            if ne_corner:
                result = background.blit(
                    ne_corner,
                    (background.get_width() - ne_corner.get_width(), 0)
                )
                logging.debug(result)
            else:
                logging.warning("No NE Corner for pattern 1.")

            if se_corner:
                result = background.blit(
                    se_corner,
                    (background.get_width() - se_corner.get_width(), background.get_height() - se_corner.get_height())
                )
                logging.debug(result)
            else:
                logging.warning("No SE Corner for pattern 1.")

            if sw_corner:
                result = background.blit(
                    sw_corner,
                    (0, background.get_height() - sw_corner.get_height())
                )
                logging.debug(result)
            else:
                logging.warning("No SW Corner for pattern 1.")

        return background

    @classmethod
    def get_background_pattern_2(cls, width, height):
        background = None

        if width and height:
            background = pygame.Surface(
                (width, height),
                flags=pygame.SRCALPHA,
                depth=32,
            ).convert_alpha()

            first_rect = pygame.Rect(
                0,
                0,
                width,
                height
            )

            second_rect = pygame.Rect(
                2,
                2,
                width - 4,
                height - 4
            )

            third_rect = pygame.Rect(
                6,
                6,
                width - 12,
                height - 12
            )

            background.fill(
                colors.BackgroundColors.P1_BG_1_COLOR,
                rect=first_rect,
            )
            background.fill(
                colors.BackgroundColors.P1_BG_2_COLOR,
                rect=second_rect
            )
            background.fill(
                colors.BackgroundColors.P1_BG_3_COLOR,
                rect=third_rect
            )

        return background

    def get_background_image(self):
        """Builds background image for display object."""
        background = None

        if self.background_pattern_id is not None:
            if self.background_pattern_id == PatternID.DEFAULT:
                background = Display.get_background_pattern_default(
                    self.display_rect.width,
                    self.display_rect.height,
                )
            elif self.background_pattern_id == PatternID.PATTERN_1:
                background = Display.get_background_pattern_1(
                    self.display_rect.width,
                    self.display_rect.height,
                )
            elif self.background_pattern_id == PatternID.PATTERN_2:
                background = Display.get_background_pattern_2(
                    self.display_rect.width,
                    self.display_rect.height,
                )
            else:
                logging.error("Unrecognized pattern {0}".format(self.background_pattern_id))
        elif self.background_image_path:
            # Load image if path is provided.
            background = pygame.image.load(
                self.background_image_path
            ).convert_alpha()
        elif self.background_color:
            background = pygame.Surface(
                (self.display_rect.width, self.display_rect.height),
                flags=pygame.SRCALPHA,
                depth=32,
            ).convert_alpha()
            background.fill(self.background_color)

        if background:
            self.background_image = background

    @classmethod
    def init_background_patterns(cls):
        cls.pattern_data[PatternID.PATTERN_1] = {}
        cls.pattern_data[PatternID.PATTERN_1][DisplayCorner.NW_CORNER] = pygame.image.load(
            image_paths.PATTERN_1_CORNER_NW_PATH
        ).convert_alpha()
        cls.pattern_data[PatternID.PATTERN_1][DisplayCorner.NE_CORNER] = pygame.image.load(
            image_paths.PATTERN_1_CORNER_NE_PATH
        ).convert_alpha()
        cls.pattern_data[PatternID.PATTERN_1][DisplayCorner.SE_CORNER] = pygame.image.load(
            image_paths.PATTERN_1_CORNER_SE_PATH
        ).convert_alpha()
        cls.pattern_data[PatternID.PATTERN_1][DisplayCorner.SW_CORNER] = pygame.image.load(
            image_paths.PATTERN_1_CORNER_SW_PATH
        ).convert_alpha()


class TextDisplay(Display):
    # If no background image is specified, default to background_color.
    # For best results, ensure that background_image_path points to an image
    # of size equal to the display_rect dimension values.
    # continue_icon_image_path points to the image path for an icon
    # to blit after the last line of a page if needed. The icon should be
    # small.
    def __init__(
            self,
            main_display_surface,
            display_rect,
            font_object,
            background_pattern=None,
            background_image_path=None,
            background_color=colors.COLOR_WHITE,
            horizontal_padding=0,
            vertical_padding=0,
            continue_icon_image_path=None,
            spacing_factor_between_lines=Spacing.DEFAULT_LINE_SPACING_FACTOR):
        Display.__init__(
            self,
            main_display_surface,
            display_rect,
            background_pattern=background_pattern,
            background_image_path=background_image_path,
            background_color=background_color,
        )

        self.font_object = font_object
        self.horizontal_padding = horizontal_padding
        self.vertical_padding = vertical_padding
        self.spacing_factor_between_lines = spacing_factor_between_lines

        # Define text space limits.
        self.text_space_horizontal = self.display_rect.width - (2 * self.horizontal_padding)
        self.text_space_vertical = self.display_rect.height - (2 * self.vertical_padding)
        self.text_space_top_left = (
            self.display_rect.x + self.horizontal_padding,
            self.display_rect.y + self.vertical_padding
        )

        logging.debug("Text Space {0} x {1}. Top left: {2}".format(
            self.text_space_horizontal,
            self.text_space_vertical,
            self.text_space_top_left
        ))

        self.text_space_rect = pygame.Rect(
            self.text_space_top_left,
            (self.text_space_horizontal, self.text_space_vertical)
        )

        self.text_height = self.font_object.get_linesize()

        # Get max number of characters that we can blit per line.
        # Assuming monospaced font.
        self.char_per_line = TextDisplay.get_char_per_line(
            self.text_space_horizontal,
            self.font_object
        )

        # Get max number of lines that we can blit per page.
        # Assuming monospaced font.
        self.lines_per_page = TextDisplay.get_num_lines_per_page(
            self.text_space_vertical,
            self.font_object,
            self.spacing_factor_between_lines
        )

        logging.debug(
            "Char per line {0}, line per page {1}".format(
                self.char_per_line,
                self.lines_per_page
            )
        )

        # Define background image if possible.
        """
        self.background_image = None
        if background_image_path:
            # Load image if path is provided.
            self.background_image = pygame.image.load(
                background_image_path
            ).convert_alpha()
        """

        # Define continuation icon if possible.
        self.continue_icon = None
        if continue_icon_image_path:
            # Load image if path is provided.
            self.continue_icon = pygame.image.load(continue_icon_image_path).convert_alpha()

    @classmethod
    def get_char_per_line(cls, horizontal_pixels, font_object):
        num_char = 0

        if horizontal_pixels and (horizontal_pixels > 0) and font_object:
            avg_char_width = 0

            # TODO for char in SIZE_TEST_STRING:
            str_size_info = font_object.size(SIZE_TEST_STRING)

            if str_size_info:
                avg_char_width = int(
                    max(
                        avg_char_width,
                        math.ceil(
                            str_size_info[0] / (1.0 * len(SIZE_TEST_STRING))
                        )
                    )
                )

            if avg_char_width > 0:
                # Allow for some extra space?
                num_char = int(horizontal_pixels / avg_char_width)

        return num_char

    # Includes spaces in between the lines, as well.
    # spacing_factor_between_lines is a float that determines
    # spacing in between lines (e.g. 1.25 means add 0.25 of the text height
    # as spacing in between lines)
    @classmethod
    def get_num_lines_per_page(
            cls,
            vertical_pixel_height,
            font_object,
            spacing_factor_between_lines=Spacing.DEFAULT_LINE_SPACING_FACTOR):
        num_lines = 0

        if vertical_pixel_height and (vertical_pixel_height > 0) and font_object:
            text_height = font_object.get_linesize()

            # Let x be number of total lines that fit in
            # vertical_pixel_height v.
            # Let pixels_between_lines be p.
            # Then x*text_height + (x - 1)*p = v.
            # x(text_height + p) - p = v.
            # x = (v + p) / (text_height + p).
            pixels_between_lines = int(
                text_height * max(0.0, spacing_factor_between_lines - 1)
            )

            num_lines = int(
                (vertical_pixel_height + pixels_between_lines) / (text_height + pixels_between_lines)
            )

        return num_lines

    @classmethod
    def convert_to_word_list(cls, text_string):
        ret_list = []

        if text_string:
            # Split string based on whitespace.
            # word_list = text_string.split()

            # Split string based on spaces.
            word_list = text_string.split(' ')

            if word_list:
                # Add a space to every word except the last one.
                for i in range(len(word_list) - 1):
                    ret_list.append(word_list[i] + " ")

                last_word = word_list[len(word_list) - 1]
                if last_word:
                    ret_list.append(last_word)

        logging.debug(
            "Converted {0} to word list {1}".format(
                text_string,
                ret_list
            )
        )

        return ret_list

    # Given a text string to display, returns a list of strings,
    # where each string takes up at most one line of display space.
    def get_text_lines(self, text_string):
        # List of strings
        ret_lines = []
        text_lines = []

        # Convert string to list of words to print. Newlines in the
        # string will carry over to a new text line.
        if text_string:
            text_string_lines = []

            # Separate out the string based on newlines.
            for x in text_string.split('\n'):
                if x:
                    text_string_lines.append(x)
            # text_string_lines = [x.strip() for x in text_string.split('\n')]

            for line in text_string_lines:
                word_list = TextDisplay.convert_to_word_list(line)

                logging.debug("Get text lines. Text: {0}\nWord List:{1}".format(line, word_list))

                curr_length = 0
                start_index = 0

                num_words = len(word_list)

                if num_words == 1:
                    # Simple case. Just 1 word.
                    text_lines.append(word_list[0])
                elif num_words > 1:
                    for index in range(num_words):
                        sub_list = None
                        word_length = len(word_list[index])

                        logging.debug(
                            "Word length for {0} is {1}".format(
                                word_list[index],
                                word_length
                            )
                        )

                        # Check if we can add this word or not.
                        if (curr_length + word_length) > self.char_per_line:
                            # Adding this word would bring us over the limit.
                            # Collect all the words from the last end point up
                            # to the word before.
                            if start_index < index:
                                sub_list = word_list[start_index:index]
                            else:
                                sub_list = [word_list[index]]

                            start_index = index

                            # Reset counter, and throw in the length of the
                            # overflow word.
                            curr_length = word_length
                        else:
                            if index == (num_words - 1):
                                # We reached the end of the word list and
                                # did not overpass to the next line.
                                sub_list = word_list[start_index:]
                            else:
                                curr_length = curr_length + word_length

                        # Create line.
                        if sub_list:
                            str_to_add = ''.join(sub_list).strip()

                            if str_to_add:
                                text_lines.append(str_to_add)
                                logging.debug(
                                    "Adding string {0} to text lines".format(
                                        str_to_add
                                    )
                                )

                    if start_index == (num_words - 1):
                        # We still need to add the last word.
                        str_to_add = word_list[start_index]
                        text_lines.append(str_to_add)
                        logging.debug(
                            "Adding string {0} to text lines".format(str_to_add)
                        )

        if text_lines:
            ret_lines = text_lines

        logging.debug("Converted text \n{0}\nto lines\n{1}\n".format(text_string, ret_lines))
        return ret_lines

    @classmethod
    def get_text_lines_test(cls, text_string, char_per_line):
        # List of strings
        ret_lines = []
        text_lines = []

        # Convert string to list of words to print. Newlines in the
        # string will carry over to a new text line.
        if text_string:
            # Separate out the string based on newlines.
            text_string_lines = [x.strip() for x in text_string.split('\n')]

            for line in text_string_lines:
                word_list = TextDisplay.convert_to_word_list(line)

                logging.debug(
                    "Get text lines. Text: {0}\nWord List:{1}".format(
                        line,
                        word_list
                    )
                )

                curr_length = 0
                start_index = 0

                num_words = len(word_list)

                logging.debug("Max char in line: {0}".format(char_per_line))

                if num_words == 1:
                    # Simple case. Just 1 word.
                    text_lines.append(word_list[0])
                elif num_words > 1:
                    for index in range(num_words):
                        sub_list = None
                        word_length = len(word_list[index])

                        logging.debug(
                            "Word length for {0} is {1}".format(
                                word_list[index],
                                word_length
                            )
                        )

                        # Check if we can add this word or not.
                        if (curr_length + word_length) > char_per_line:
                            # Adding this word would bring us over the limit.
                            # Collect all the words from the last end point up
                            # to the word before.
                            if start_index < index:
                                sub_list = word_list[start_index:index]
                            else:
                                sub_list = [word_list[index]]

                            start_index = index

                            # Reset counter, and throw in the length of the
                            # overflow word.
                            curr_length = word_length
                        else:
                            if index == (num_words - 1):
                                # We reached the end of the word list and
                                # did not overpass to the next line.
                                sub_list = word_list[start_index:]
                            else:
                                curr_length = curr_length + word_length

                        # Create line.
                        if sub_list:
                            str_to_add = ''.join(sub_list).strip()

                            if str_to_add:
                                text_lines.append(str_to_add)
                                logging.debug(
                                    "Adding string {0} to text lines".format(
                                        str_to_add
                                    )
                                )

                    if start_index == (num_words - 1):
                        # We still need to add the last word.
                        str_to_add = word_list[start_index]
                        text_lines.append(str_to_add)
                        logging.debug(
                            "Adding string {0} to text lines".format(str_to_add)
                        )

        if text_lines:
            ret_lines = text_lines

        logging.debug(
            "Converted text \n{0}\nto lines\n{1}\n".format(
                text_string, ret_lines
            )
        )

        return ret_lines

    def consolidate_pages(self, page_list):
        ret_list = []

        rendered_lines = []
        text_lines = []

        for page in page_list:
            rendered_lines += page.rendered_text_lines
            text_lines += page.text_lines

        if rendered_lines and text_lines:
            curr_index = 0
            num_lines = len(rendered_lines)

            while curr_index < num_lines:
                # Set blank page and manually add lines.
                curr_page = TextPage(None, None, None)
                end_index = min(curr_index + self.lines_per_page, num_lines)

                curr_page._text_lines = text_lines[curr_index:end_index]
                curr_page._rendered_text_lines = \
                    rendered_lines[curr_index:end_index]

                ret_list.append(curr_page)

                curr_index = end_index

        return ret_list

    # Returns list of TextPage overworld_obj, each containing
    # a list of strings, where each string represents one line of text
    # to place on display.
    # If text_to_display is a list of strings, each string will be
    # included and deliminated as a new line where possible.
    # font_color can be a single tuple representing a font color, or
    # a list of tuples representing font colors for each line of
    # text_to_display. List values of font_color are only valid if
    # text_to_display is a list of strings, and each index of the list
    # will correspond to the next. If text_to_display is a list of strings
    # and font_color is a single tuple, then that color will apply
    # to each text string in text_to_display.
    def get_text_pages(self, text_to_display, font_color=colors.COLOR_BLACK):
        ret_page_list = []
        page_list = []
        strings_to_process = []
        font_color_to_use = None
        use_color_list = False

        # Get lines of text to print.
        if isinstance(text_to_display, str):
            if isinstance(font_color, tuple):
                strings_to_process.append(text_to_display)
                font_color_to_use = font_color
            else:
                logging.error("Invalid format for font color with single string for text_to_display.")
        elif isinstance(text_to_display, list):
            strings_to_process = text_to_display

            if isinstance(font_color, list):
                use_color_list = True
            elif isinstance(font_color, tuple):
                font_color_to_use = font_color
            else:
                logging.error("Invalid format for font_color")
        else:
            logging.error("Invalid format for text_to_display")

        for index in range(len(strings_to_process)):
            text_to_process = strings_to_process[index]

            lines_to_print = self.get_text_lines(text_to_process)

            logging.debug(
                "Get text pages. Text: {0}\nLines:{1}".format(
                    text_to_process,
                    lines_to_print
                )
            )

            if use_color_list:
                font_color_to_use = font_color[index]

            if lines_to_print and font_color_to_use:
                num_lines = len(lines_to_print)

                if num_lines > self.lines_per_page:
                    num_lines_processed = 0
                    remaining_lines = num_lines

                    while remaining_lines > 0:
                        # Get number of lines to add to page.
                        num_lines_to_add = min(self.lines_per_page, remaining_lines)

                        # Get indices for list slicing.
                        start_index = num_lines_processed
                        end_index = start_index + num_lines_to_add

                        page_lines = lines_to_print[start_index:end_index]

                        # Create page and add to page list.
                        page_list.append(
                            TextPage(page_lines, self.font_object, font_color_to_use)
                        )

                        num_lines_processed = num_lines_processed + num_lines_to_add
                        remaining_lines = remaining_lines - num_lines_to_add
                else:
                    # All lines can fit on a single page.
                    page_list.append(
                        TextPage(
                            lines_to_print,
                            self.font_object,
                            font_color_to_use,
                        )
                    )

        if page_list:
            if len(page_list) > 1:
                # Consolidate page lines.
                ret_page_list = self.consolidate_pages(page_list)
            else:
                ret_page_list = page_list
        else:
            logging.warning("No page made.")

        # Debugging
        for page in ret_page_list:
            logging.debug(
                "Made page: {0}".format('\n#\n'.join(page.text_lines))
            )

        return ret_page_list

    def get_page_height(self, num_lines_in_page):
        ret_height = 0

        if num_lines_in_page:
            # Total height = n*(text_height) + (n - 1)*(pixels_between_lines),
            # where n is number of lines.
            # = n*(text_height + pixels_between_lines) - pixels_between_lines.
            text_height = self.font_object.get_linesize()
            pixels_between_lines = int(
                text_height * max(0.0, self.spacing_factor_between_lines - 1)
            )

            ret_height = \
                (num_lines_in_page * (text_height + pixels_between_lines)) \
                - pixels_between_lines

        return ret_height

    # Blit text for the single page.
    # Does not update display, caller will need to do that.
    # If continue_icon is set to True, we will blit the object's continue
    # icon after the last line of the page.
    def blit_page(
            self,
            surface,
            text_page,
            show_continue_icon=False,
            alternative_top_left=None,
            horizontal_orientation=Orientation.CENTERED,
            vertical_orientation=Orientation.CENTERED):
        if surface and text_page:
            text_space_rect = self.text_space_rect

            if alternative_top_left:
                text_space_rect = pygame.Rect(
                    alternative_top_left[0] + self.horizontal_padding,
                    alternative_top_left[1] + self.vertical_padding,
                    self.text_space_horizontal,
                    self.text_space_vertical,
                )

            # Blit background
            self.blit_background(
                surface,
                alternative_top_left=alternative_top_left,
            )

            num_lines = len(text_page.rendered_text_lines)

            page_height = self.get_page_height(num_lines)

            # Determine offsets based on placement.
            vertical_offset = 0
            if vertical_orientation == Orientation.CENTERED:
                vertical_offset = int(
                    max(0, self.text_space_vertical - page_height) / 2
                )
            elif vertical_orientation == Orientation.TOP_JUSTIFIED:
                vertical_offset = 0
            elif vertical_orientation == Orientation.BOTTOM_JUSTIFIED:
                vertical_offset = text_space_rect.bottom - page_height
            else:
                logging.error("Invalid vertical orientation.")

            for index in range(num_lines):
                rendered_text = text_page.rendered_text_lines[index]

                rendered_text_dimensions = rendered_text.get_size()
                text_width = rendered_text_dimensions[0]

                # Determine horizontal placement.
                text_top_left = None
                if horizontal_orientation == Orientation.CENTERED:
                    text_top_left = (
                        text_space_rect.centerx - int(text_width / 2),
                        text_space_rect.y + vertical_offset
                    )
                elif horizontal_orientation == Orientation.LEFT_JUSTIFIED:
                    text_top_left = (
                        text_space_rect.x,
                        text_space_rect.y + vertical_offset
                    )
                elif horizontal_orientation == Orientation.RIGHT_JUSTIFIED:
                    text_top_left = (
                        text_space_rect.right - text_width,
                        text_space_rect.y + vertical_offset
                    )
                else:
                    logging.error("Invalid horizontal orientation.")

                if text_top_left:
                    # Blit the text.
                    surface.blit(
                        rendered_text,
                        text_top_left
                    )

                    # Blit the continue icon if we are on the last line.
                    if (index == (num_lines - 1)) and self.continue_icon and show_continue_icon:
                        text_height = rendered_text_dimensions[1]
                        icon_top_left = (
                            text_top_left[0] + text_width + Spacing.CONTINUE_ICON_HORIZ_SPACE,
                            text_top_left[1] + text_height - self.continue_icon.get_height() - 4
                        )

                        surface.blit(
                            self.continue_icon,
                            icon_top_left
                        )

                # Move to spot for next line.
                vertical_offset += int(self.spacing_factor_between_lines * self.text_height)


class MenuDisplay(TextDisplay):
    # If no background image is specified, default to background_color.
    # For best results, ensure that background_image_path points to an image
    # of size equal to the display_rect dimension values.
    # For best results, ensure that selection_icon_image_path points to an
    # image of small enough size.
    def __init__(
            self,
            main_display_surface,
            display_rect,
            font_object,
            background_pattern=None,
            background_image_path=None,
            background_color=colors.COLOR_WHITE,
            horizontal_padding=0,
            vertical_padding=0,
            selection_icon_image_path=image_paths.DEFAULT_MENU_SELECTION_ICON_PATH,
            spacing_factor_between_lines=Spacing.MENU_LINE_SPACING_FACTOR):
        TextDisplay.__init__(
            self,
            main_display_surface,
            display_rect,
            font_object,
            background_pattern=background_pattern,
            background_image_path=background_image_path,
            background_color=background_color,
            horizontal_padding=horizontal_padding,
            vertical_padding=vertical_padding,
            spacing_factor_between_lines=spacing_factor_between_lines,
        )

        # Define selection icon.
        self.selection_icon = None
        if selection_icon_image_path:
            # Load image if path is provided.
            self.selection_icon = pygame.image.load(
                selection_icon_image_path
            ).convert_alpha()

        if not self.selection_icon:
            logging.error("Error setting up selection icon for menu.")

        # determine max number of options (one option per line)
        # that can be blitted per page.
        self.max_options_per_page = TextDisplay.get_num_lines_per_page(
            self.text_space_vertical,
            self.font_object,
            self.spacing_factor_between_lines
        )

        logging.debug(
            "Max options per menu page: {0}".format(self.max_options_per_page)
        )

    # Returns list of Menu Pages containing the menu option names.
    # If the returned list contains multiple Menu Pages, then each
    # Menu Page (including the final one) will have its last
    # option name be the "MORE OPTIONS" option to indicate that there
    # are additional menu options. The "MORE OPTIONS" option on the final
    # page will lead to the first page to allow looping.
    # option_id_list is a list of integers representing the option IDs
    # for the menu. They cannot be equal to MORE_OPTIONS_OPTION_ID.
    # additional options on a subsequent menu page.
    # max_options_per_page indicates how many options (lines) fit on one page.
    def get_menu_page_list(
            self,
            option_id_list,
            font_color=colors.COLOR_BLACK):
        ret_pages = []

        if option_id_list and self.max_options_per_page:
            logging.debug('Adding {0} options to page with max of {1} options per page'.format(
                len(option_id_list),
                self.max_options_per_page
            ))

            if len(option_id_list) <= self.max_options_per_page:
                # We can add all options on one page.
                logging.debug(
                    "Adding remaining {0} pages to menu page: {1}".format(
                        len(option_id_list),
                        option_id_list
                    )
                )

                if option_id_list:
                    curr_page = MenuPage(
                        option_id_list,
                        self.font_object,
                        font_color=font_color,
                    )
                    ret_pages.append(curr_page)
            else:
                # Leave room for the "more options" option.
                options_per_page = self.max_options_per_page - 1

                # Get the number of menu pages required.
                num_pages = math.ceil(
                    len(option_id_list) / options_per_page
                )

                logging.debug(
                    "%d options, %d options per page, %d menu pages",
                    len(option_id_list),
                    self.max_options_per_page,
                    num_pages,
                )

                for i in range(num_pages):
                    start_index = i * options_per_page
                    end_index = start_index + options_per_page

                    logging.debug(
                        "Start index %d, end index %d",
                        start_index,
                        end_index,
                    )

                    # Options will carry on to next page.
                    options_to_add = option_id_list[start_index:end_index]
                    options_to_add.append(menu_options.MenuOptionID.MORE_OPTIONS_OPTION)
                    logging.debug('Adding {0} options plus "more options" to menu page: {1}'.format(
                        len(options_to_add) - 1,
                        options_to_add
                    ))

                    if options_to_add:
                        curr_page = MenuPage(
                            options_to_add,
                            self.font_object,
                            font_color=font_color,
                        )
                        ret_pages.append(curr_page)

        return ret_pages

    """
    def get_rendered_menu_option_text(self, option_id):
        return self.rendered_menu_option_mapping.get(
            option_id,
            {}
        ).get(
            language.Language.current_language_id,
            None
        )
    """

    # Does not update display.
    def blit_menu_page(
            self,
            surface,
            menu_page,
            curr_selected_index,
            alternative_top_left=None,
            horizontal_orientation=Orientation.CENTERED,
            vertical_orientation=Orientation.CENTERED):
        if surface and menu_page and curr_selected_index >= 0:
            num_options = menu_page.get_num_options()

            if num_options <= self.max_options_per_page:
                # Blit background.
                self.blit_background(
                    surface,
                    alternative_top_left=alternative_top_left,
                )

                page_height = self.get_page_height(num_options)

                # Determine space to blit text.
                target_rect = self.text_space_rect
                if alternative_top_left:
                    target_rect = pygame.Rect(
                        alternative_top_left[0] + self.horizontal_padding,
                        alternative_top_left[1] + self.vertical_padding,
                        self.text_space_horizontal,
                        self.text_space_vertical,
                    )

                # Determine offsets based on placement.
                vertical_offset = 0
                if vertical_orientation == Orientation.CENTERED:
                    vertical_offset = int(
                        max(0, self.text_space_vertical - page_height) / 2
                    )
                elif vertical_orientation == Orientation.TOP_JUSTIFIED:
                    vertical_offset = 0
                elif vertical_orientation == Orientation.BOTTOM_JUSTIFIED:
                    vertical_offset = target_rect.bottom - page_height
                else:
                    logging.error("Invalid vertical orientation.")

                for index in range(num_options):
                    curr_option_info = menu_page.get_option_info(index)

                    # Get rendered text and dimensions.
                    rendered_text = curr_option_info[1]

                    if rendered_text:
                        rendered_text_dimensions = rendered_text.get_size()
                        text_width = rendered_text_dimensions[0]
                        text_height = rendered_text_dimensions[1]

                        text_top_left = None

                        if horizontal_orientation == Orientation.CENTERED:
                            # Get top left for centered option text.
                            # Center the text horizontally.
                            text_top_left = (
                                target_rect.centerx - int(text_width / 2),
                                target_rect.y + vertical_offset
                            )
                        elif horizontal_orientation == Orientation.LEFT_JUSTIFIED:
                            text_top_left = (
                                target_rect.x,
                                target_rect.y + vertical_offset
                            )
                        elif horizontal_orientation == Orientation.RIGHT_JUSTIFIED:
                            text_top_left = (
                                target_rect.right - text_width,
                                target_rect.y + vertical_offset
                            )

                        if text_top_left:
                            # Blit the text.
                            surface.blit(
                                rendered_text,
                                text_top_left
                            )

                            # Blit the selection icon if we
                            # are on the selected index.
                            if index == curr_selected_index \
                                    and self.selection_icon:
                                # Vertically center the selection
                                # icon with the option.
                                icon_top_left = (
                                    text_top_left[0] - self.selection_icon.get_width() -
                                    Spacing.SELECTION_ICON_HORIZ_SPACE,
                                    text_top_left[1] + int(text_height / 2) - int(self.selection_icon.get_height() / 2)
                                )

                                surface.blit(
                                    self.selection_icon,
                                    icon_top_left
                                )

                        # Advance.
                        vertical_offset += \
                            + int(self.spacing_factor_between_lines * text_height)


class IconGridDisplay(Display):
    def __init__(
            self,
            main_display_surface,
            display_rect,
            icon_dimensions,
            background_pattern=None,
            background_image_path=None,
            background_color=colors.COLOR_WHITE,
            horizontal_padding=0,
            vertical_padding=0,
            space_between_icons=Spacing.ICON_VIEWING_PIXEL_SPACING,
            continue_up_icon_image_path=None,
            continue_down_icon_image_path=None,
            selection_image_path=image_paths.ITEM_LISTING_SELECTED_DEFAULT_PATH):
        Display.__init__(
            self,
            main_display_surface,
            display_rect,
            background_pattern=background_pattern,
            background_image_path=background_image_path,
            background_color=background_color,
        )
        self.horizontal_padding = horizontal_padding
        self.vertical_padding = vertical_padding
        self.pixels_between_icons = space_between_icons
        self.icon_dimensions = icon_dimensions

        # Define continue icons if possible.
        self.continue_up_icon = None
        self.continue_down_icon = None
        continue_icon_width = 0

        if continue_up_icon_image_path:
            self.continue_up_icon = pygame.image.load(
                continue_up_icon_image_path
            ).convert_alpha()

            continue_icon_width = max(
                continue_icon_width,
                self.continue_up_icon.get_width()
            )

        if continue_down_icon_image_path:
            self.continue_down_icon = pygame.image.load(
                continue_down_icon_image_path
            ).convert_alpha()

            continue_icon_width = max(
                continue_icon_width,
                self.continue_down_icon.get_width()
            )

        self.icon_viewing_top_left = (
            self.display_rect.x + 15 + continue_icon_width + 15,
            self.display_rect.y + self.vertical_padding,
        )

        self.icon_viewing_space_horizontal = (self.display_rect.right - self.icon_viewing_top_left[0]
                                              - self.horizontal_padding)
        self.icon_viewing_space_vertical = self.display_rect.height - (2 * self.vertical_padding)
        logging.debug("icon viewing space: {0}x{1}".format(
            self.icon_viewing_space_horizontal,
            self.icon_viewing_space_vertical
        ))

        self.icon_viewing_space_rect = pygame.Rect(
            self.icon_viewing_top_left[0],
            self.icon_viewing_top_left[1],
            self.icon_viewing_space_horizontal,
            self.icon_viewing_space_vertical
        )

        # Row, col dimensions.
        self.icon_viewing_grid_dimensions = \
            IconGridDisplay.get_icon_viewing_grid_dimensions(
                self.icon_viewing_space_horizontal,
                self.icon_viewing_space_vertical,
                self.icon_dimensions,
            )
        self.num_columns = \
            self.icon_viewing_grid_dimensions[0]
        self.num_rows = \
            self.icon_viewing_grid_dimensions[1]

        self.max_num_icons = self.num_columns * self.num_rows

        # Get vertical space to blit max number of rows.
        required_vertical_icon_space = \
            self.num_rows * (self.icon_dimensions[1] + self.pixels_between_icons) \
            - self.pixels_between_icons

        required_icon_space_rect = pygame.Rect(
            self.icon_viewing_space_rect.topleft,
            (self.icon_viewing_space_rect.width, required_vertical_icon_space)
        )

        self.selection_image = None
        if selection_image_path:
            self.selection_image = pygame.image.load(
                selection_image_path
            ).convert_alpha()

        # Set up continue icon rects.
        self.continue_up_rect = None
        self.continue_down_rect = None

        if self.continue_up_icon:
            self.continue_up_rect = self.continue_up_icon.get_rect(
                center=required_icon_space_rect.center
            )

            self.continue_up_rect.centery -= 40

            self.continue_up_rect.centerx = (self.icon_viewing_space_rect.left -
                                             int((self.icon_viewing_space_rect.left - self.display_rect.left) / 2) + 4)

        # TODO make this in between last possible icon row
        # and the bottom of the self.display_rect
        if self.continue_down_icon:
            self.continue_down_rect = self.continue_down_icon.get_rect(
                center=required_icon_space_rect.center
            )

            self.continue_down_rect.centery += 40

            self.continue_down_rect.centerx = (self.icon_viewing_space_rect.left -
                                               int((self.icon_viewing_space_rect.left - self.display_rect.left) / 2)
                                               + 4)

    @classmethod
    def get_icon_viewing_grid_dimensions(
            cls,
            horizontal_space,
            vertical_space,
            icon_dimensions,
            space_between_icons=Spacing.ICON_VIEWING_PIXEL_SPACING):
        dimensions = (0, 0)

        if horizontal_space and vertical_space and icon_dimensions:
            # Let n be number of icons in the row,
            # Let s be the space between icons.
            # Let h be the horizontal space available.
            # Then (n * icon_width) + (n - 1) * s = h.
            # n * (icon_width + s) - s = h.
            # n = (h + s) / (icon_width + s).
            num_row_icons = int(
                (horizontal_space + space_between_icons) / (icon_dimensions[0] + space_between_icons)
            )

            num_column_icons = int(
                (vertical_space + space_between_icons) / (icon_dimensions[1] + space_between_icons)
            )

            if num_row_icons and num_column_icons:
                dimensions = (num_row_icons, num_column_icons)

        return dimensions

    def get_row_index(self, icon_listing_index):
        return int(icon_listing_index / self.num_columns)

    def get_column_index(self, icon_listing_index):
        return icon_listing_index % self.num_columns

    # Icon listing data must be list of length-2 lists of the form
    # [icon image, rendered supertext].
    # selected_index is the index in icon_data_list for the
    # icon currently selected.
    # first_viewable_row_index is the row index for the first row of icons
    # to be visible in the viewing.
    def blit_icon_listing(
            self,
            surface,
            icon_data_list,
            first_viewable_row_index,
            selected_index,
            preselected_index_list=None,
            show_continue_icon=True,
            alternative_top_left=None):
        if surface and icon_data_list \
                and selected_index >= 0 and first_viewable_row_index >= 0:
            icon_space_rect = self.icon_viewing_space_rect

            if alternative_top_left:
                icon_space_rect = pygame.Rect(
                    alternative_top_left[0] + self.horizontal_padding,
                    alternative_top_left[1] + self.vertical_padding,
                    self.icon_viewing_space_rect.width,
                    self.icon_viewing_space_rect.height
                )

            # Blit background
            self.blit_background(
                surface,
                alternative_top_left=alternative_top_left,
            )

            logging.debug("Icon space top left: {0}".format(
                icon_space_rect.topleft
            ))

            # Blit the icons, starting with the first viewable row.
            starting_index = \
                first_viewable_row_index * self.num_columns

            # Go until we run out of space or icons.
            total_icons = len(icon_data_list)
            last_index = min(
                starting_index + self.max_num_icons - 1,
                total_icons - 1
            )

            curr_index = starting_index
            logging.debug("Starting with icon index {0}".format(curr_index))

            horizontal_offset = 0
            vertical_offset = 0

            # Blit icon and quantity text if needed.
            icon_rect = pygame.Rect(
                icon_space_rect.x + horizontal_offset,
                icon_space_rect.y + vertical_offset,
                self.icon_dimensions[0],
                self.icon_dimensions[1],
            )

            while curr_index <= last_index:
                curr_viewing_row = int(
                    (curr_index - starting_index) / self.num_columns
                )

                horizontal_offset = \
                    ((curr_index - starting_index) % self.num_columns) \
                    * (self.icon_dimensions[0] + self.pixels_between_icons)

                vertical_offset = \
                    curr_viewing_row \
                    * (self.icon_dimensions[1] + self.pixels_between_icons)

                curr_icon_info = icon_data_list[curr_index]
                icon_image = curr_icon_info[0]
                rendered_supertext = curr_icon_info[1]

                # Blit icon image and quantity text if needed.
                icon_rect.topleft = (
                    icon_space_rect.x + horizontal_offset,
                    icon_space_rect.y + vertical_offset,
                )

                # Check if this is the selected icon. If so,
                # blit the selection background.
                if ((selected_index == curr_index) or
                   (preselected_index_list is not None and selected_index in preselected_index_list)) \
                   and self.selection_image:
                    # Center on the icon.
                    select_image_rect = self.selection_image.get_rect(
                        center=icon_rect.center
                    )

                    surface.blit(
                        self.selection_image,
                        select_image_rect,
                    )

                if icon_image:
                    surface.blit(
                        icon_image,
                        icon_rect,
                    )

                if rendered_supertext:
                    text_top_left = icon_rect.topleft
                    surface.blit(
                        rendered_supertext,
                        text_top_left,
                    )

                curr_index += 1

            # Blit the up and down arrows if there are icons above/below.
            if (starting_index >= self.num_columns) and show_continue_icon:
                # We have at least 1 row above us.
                surface.blit(
                    self.continue_up_icon,
                    self.continue_up_rect
                )

            if (total_icons - starting_index) > self.max_num_icons and show_continue_icon:
                # We have icons after us.
                surface.blit(
                    self.continue_down_icon,
                    self.continue_down_rect
                )
