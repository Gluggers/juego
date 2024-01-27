import pygame

TICKS_PER_SECOND = 30

# Number of milliseconds in a second.
MS_PER_SECOND = 1000

# Number of milliseconds per clock tick.
MS_PER_TICK = MS_PER_SECOND // TICKS_PER_SECOND

# Number of ticks between refreshing map.
MAP_REFRESH_TICK_INTERVAL = 30

# Number of ticks between reblitting overworld.
OVERWORLD_REBLIT_TICK_INTERVAL = 3


class Timekeeper:
    """Handles time-based methods and functions, such as ticks.

    The user should not generate Timekeeper overworld_obj, as the class
    is primarily for class methods related to time and the
    pygame clock.
    """

    # Class pygame Clock object.
    _clock = None

    @classmethod
    def init_clock(cls):
        """Sets up the pygame Clock object."""

        cls._clock = pygame.time.Clock()

    @classmethod
    def tick(cls, tick_amount=TICKS_PER_SECOND):
        """Have the class Clock object tick.

        Args:
            cls: class object.
            tick_amount: integer to determine the tick length. Higher tick
                means pausing for a shorter amount of time (time paused is
                approximately equal to 1 second / tick_amount).
                Defaults to 30 ticks per second.
        """

        cls._clock.tick(tick_amount)
