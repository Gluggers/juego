from enum import Enum


class LanguageEnum(Enum):
    EN = 0x0
    ES = 0x1


class Language:
    DEFAULT_LANGUAGE = LanguageEnum.ES
    current_language = DEFAULT_LANGUAGE

    @classmethod
    def set_current_language(cls, new_language: LanguageEnum):
        if new_language in list(LanguageEnum):
            cls.current_language = new_language

    @classmethod
    def get_current_language(cls) -> LanguageEnum:
        return cls.current_language

    @staticmethod
    def get_language_enum_from_str(lang_val: str) -> LanguageEnum:
        try:
            return LanguageEnum[lang_val.upper()]
        except Exception:
            raise Exception('No supported language for: {}', lang_val)


class MultiLanguageText:
    """Encapsulates language translations for text."""

    def __init__(self, en='', es='', language_dict=None):
        if language_dict:
            self._translations = {
                LanguageEnum.EN: language_dict['en'],
                LanguageEnum.ES: language_dict['es'],
            }
        else:
            self._translations = {
                LanguageEnum.EN: en,
                LanguageEnum.ES: es,
            }

    def get_text(self) -> str:
        """Gets underlying text translated to the current game language."""
        return self._translations.get(Language.get_current_language(), '')
