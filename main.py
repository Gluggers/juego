import argparse
import logging
import sys
import pygame

from app import application
from app.interactions import interaction
from app.items import items
from app.maps import maps
from app.viewing import viewing, display, fonts
from conf.settings import Settings
from util.timekeeper import Timekeeper


def setup_logger(level=logging.DEBUG):
    logging.basicConfig(level=level,
                        format='[%(asctime)s] [%(levelname)-5s] (%(filename)s:%(lineno)s %(funcName)s) %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.captureWarnings(True)


def main():
    parser = argparse.ArgumentParser('Welcome to the adventure game!')
    parser.add_argument('-l', '--log', dest='logLevel', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level', default='INFO')
    args = parser.parse_args()

    setup_logger(getattr(logging, args.logLevel))

    # Get settings
    logging.info('Loading settings.')
    try:
        Settings.load_settings()
    except Exception as e:
        logging.exception('Exception when loading settings: {}'.format(e))
        sys.exit(1)
    logging.info('Loaded settings.')
    Settings.set_language_setting()
    game_name = Settings.get_game_title()
    if not game_name:
        logging.exception('No game name provided in settings.')
        sys.exit(1)

    # Initial pygame setup
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # Initialize clock
    Timekeeper.init_clock()
    logging.info('Initialized clock.')

    # TODO - load images and other game data

    # TODO - load and init resources

    # TODO - init handlers

    # TODO - init other pygame stuff
    game_surface = pygame.display.set_mode(
        (
            viewing.Measurements.MAIN_DISPLAY_WIDTH,
            viewing.Measurements.MAIN_DISPLAY_HEIGHT
        )
    )
    pygame.display.set_caption(game_name)

    # init interactions
    interaction.Interaction.init_interactions()

    # Load display information.
    fonts.Fonts.init_fonts()
    display.Display.init_background_patterns()

    # Build game application
    app = application.Application(game_surface)

    # TODO
    # Load miscellaneous objects.
    # interactive_obj.InteractiveObject.build_misc_objects()

    # Load resources.
    # resources.Resource.build_resources()

    # Load items.
    items.Item.build_standard_items()

    # Load characters. # TODO

    # load maps
    maps.Map.build_maps()

    # create protagonist
    protag_tile_loc = (32, 3)
    app.build_protagonist("Bob")

    # set map and blit
    app.set_and_blit_game_map(
        maps.MapIDs.REGION_1_ID,
        protag_tile_loc
    )

    # update screen
    pygame.display.update()

    # start looping overworld
    app.handle_overworld_loop()


if __name__ == '__main__':
    main()
