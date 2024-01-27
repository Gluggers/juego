import os
import logging

from util import util
from lang import language

SETTINGS_FILE = os.path.join(util.get_base_path(), 'conf', 'settings.yml')
DEFAULT_SAVE_FILE_NAME = 'savegame.json'


class Settings:
    _configuration = dict()

    @classmethod
    def load_settings(cls):
        settings = util.strip_yaml(SETTINGS_FILE)
        if settings:
            cls._configuration = settings[0]
            logging.debug(cls._configuration)
        else:
            raise Exception('No settings provided.')

    @classmethod
    def get_setting(cls, prop, default=None):
        return cls._configuration.get(prop, default)

    @classmethod
    def update_setting(cls, prop, val):
        cls._configuration[prop] = val

    @classmethod
    def get_language_setting(cls):
        lang_val = cls.get_setting('lang', '')
        if lang_val:
            return language.LanguageEnum[lang_val.upper()]
        else:
            return language.Language.DEFAULT_LANGUAGE

    @classmethod
    def set_language_setting(cls):
        lang_val = cls.get_language_setting()
        language.Language.set_current_language(lang_val)

    @classmethod
    def get_game_title(cls):
        return language.MultiLanguageText(language_dict=cls.get_setting('game_title', dict())).get_text()
