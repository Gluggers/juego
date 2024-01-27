# -*- coding: utf-8 -*-
"""Contains functions and constants for ViewingIcon overworld_obj."""

import pygame
from enum import Enum
from lang import language


class IconField(Enum):
    NAME_INFO = 0x1  # Dict mapping language ID to string.
    IMAGE_PATH_DICT = 0x2  # Maps image ID to image path.
    DESCRIPTION_INFO = 0x3  # Maps language ID to string.
    OPTION_ID_LIST = 0x4  # List of option IDs for this object.


class ViewingIcon(pygame.sprite.Sprite):
    """A class used to represent icons for selection viewings.

    ViewingIcon overworld_obj are used in selection viewings such as inventory
    viewings, skill viewings, and equipment viewings. The ViewingIcon overworld_obj
    represent a selectable object within that viewing; in the example of the
    inventory viewing, the corresponding ViewingIcon object is an Item object,
    which extends the ViewingIcon class.  Other child classes of ViewingIcon
    object can include skill icons, equipment slots, and spells.

    Attributes:
        icon_id: the ID number for this icon. Must be unique
            within the child class.
        icon: the pygame Surface object representing the icon image for
            the ViewingIcon.
        enlarged_icon: pygame Surface object representing the enlarged icon
            image for the ViewingIcon object. Enlarged Icons are set to be
            twice as large (double the width and height) as the regular
            icon.
        curr_image_id: the current image ID being used by the object.
            This value will change for animated overworld_obj that change
            sprites after a certain number of game ticks.
        menu_option_ids: list of option ID values that represent the
            menu options to display when the ViewingIcon is selected
            in a viewing.
    """

    def __init__(self, icon_id, name_info, description_info, image_path=None, enlarged_image_path=None,
                 menu_option_ids=None):
        # Call the parent class (Sprite) init.
        pygame.sprite.Sprite.__init__(self)

        # Set up icon.
        self._icon_id = icon_id
        self._name_info = name_info if name_info else language.MultiLanguageText()
        self._description_info = description_info if description_info else language.MultiLanguageText()
        self._icon = pygame.image.load(image_path).convert_alpha() if image_path else None
        self._enlarged_icon = None
        if enlarged_image_path:
            self._enlarged_icon = pygame.image.load(enlarged_image_path).convert_alpha()
        elif self._icon:
            self._enlarged_icon = pygame.transform.scale(
                self._icon, (self._icon.get_width() * 2, self._icon.get_height() * 2)
            )
        self._menu_option_ids = []
        if menu_option_ids:
            for option_id in menu_option_ids:
                self._menu_option_ids.append(option_id)

    def get_name(self):
        """Returns the ViewingIcon's name according to the current game language.
        Returns:
            String representing the ViewingIcon name.
        """

        return self._name_info.get_text()

    @property
    def enlarged_icon(self):
        """Returns the enlarged icon for the object.

        Enlarged icons are twice as large as the standard icon.
        """

        return self._enlarged_icon

    @property
    def icon(self):
        """Returns the regular icon for the object."""

        return self._icon

    @property
    def icon_id(self):
        """Returns the object's icon ID."""

        return self._icon_id

    @property
    def menu_option_ids(self):
        """Returns the list of menu option ID values for the object."""

        return self._menu_option_ids

    # Returns the appropriate language translation for the item's description
    # info string.
    def get_description_info(self):
        """Returns the ViewingIcon's description according to the current game language.
        If no description is available, will return the name according to the current language.

        Returns:
            String representing the ViewingIcon description.
        """
        desc_str = self._description_info.get_text()
        if desc_str:
            return desc_str
        return self.get_name()

    # Overridable by child.
    def get_info_text(self):
        """Returns the ViewingIcon's information text according to the current game
        language, and the information is equivalent to the description.

        Child classes can define their own implementation of the information
        text by overriding this method.

        Returns:
            String representing the ViewingIcon information text.
        """

        return self.get_description_info()
