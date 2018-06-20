
"""micro:bit Micropython API

Everything directly related to interacting with the hardware lives in the
`microbit` module.  For ease of use it's recommended you start all scripts
with::

    from microbit import *

The following documentation assumes you have done this.

There are a few functions available directly::

    # sleep for the given number of milliseconds.
    sleep(ms)
    # returns the number of milliseconds since the micro:bit was last switched on.
    running_time()
    # makes the micro:bit enter panic mode (this usually happens when the DAL runs
    # out of memory, and causes a sad face to be drawn on the display). The error
    # code can be any arbitrary integer value.
    panic(error_code)
    # resets the micro:bit.
    reset()

The rest of the functionality is provided by objects and classes in the
microbit module, as described below.

Note that the API exposes integers only (ie no floats are needed, but they may
be accepted).  We thus use milliseconds for the standard time unit.
"""

from . import (display as display,
    # uart as uart, spi as spi, i2c as i2c, accelerometer as accelerometer, compass as compass
    )
from mpbdd.harness import _harness


from typing import Any, overload

import time


def panic(n: int) -> None:
    """Enter a panic mode. Requires restart. Pass in an arbitrary integer <= 255
    to indicate a status::

        microbit.panic(255)
    """


def reset() -> None:
    """Restart the board."""


def sleep(n: int) -> None:
    """Wait for ``n`` milliseconds. One second is 1000 milliseconds, so::

        microbit.sleep(1000)

    will pause the execution for one second.  ``n`` can be an integer or
    a floating point number.
    """
    time.sleep(n/1000.0)


def running_time() -> int:
    """Return the number of milliseconds since the board was switched on or
    restarted.
    """


def temperature() -> int:
    """Return the temperature of the micro:bit in degrees Celcius."""


class Button:
    """Represents a button.

    .. note::
        This class is not actually available to the user, it is only used by
        the two button instances, which are provided already initialized.
        """
    def __init__(self):
        self._pressed = False
        self._count = 0

    def _set_pressed(self, boolean):
        self._pressed = boolean
        self._count += 1

    def is_pressed(self) -> bool:
        """returns True or False to indicate if the button is pressed at the time of
        the method call.
        """
        _harness.run()
        return self._pressed

    def was_pressed(self) -> bool:
        """ returns True or False to indicate if the button was pressed since the device
        started or the last time this method was called.
        """
        result = self._pressed
        self._pressed = False
        return result

    def get_presses(self) -> int:
        """Returns the running total of button presses, and resets this total
        to zero before returning.
        """
        result = self._count
        self._count = 0
        return result


button_a = Button()
"""A ``Button`` instance (see below) representing the left button."""
_harness.add_callback('button_a', button_a)

button_b = Button()
"""Represents the right button."""


class MicroBitDigitalPin:
    """
    The pull mode for a pin is automatically configured when the pin changes to an
    input mode. Input modes are when you call ``read_analog`` / ``read_digital`` /
    ``is_touched``. The pull mode for these is, respectively, ``NO_PULL``,
    ``PULL_DOWN``, ``PULL_UP``. Only when in ``read_digital`` mode can you call
    ``set_pull`` to change the pull mode from the default.
    """
    def __init__(self, pinnum):
        self._pinnum = pinnum

    NO_PULL = 0
    PULL_UP = 1
    PULL_DOWN = 2

    def read_digital(self) -> int:
        """Return 1 if the pin is high, and 0 if it's low."""

    def set_pull(self, value: int = (NO_PULL or PULL_UP or PULL_DOWN)) -> None:
        """Set the pull state to one of three possible values: ``pin.PULL_UP``,
        ``pin.PULL_DOWN`` or ``pin.NO_PULL`` (where ``pin`` is an instance of
        a pin). See below for discussion of default pull states.
        """

    def write_digital(self, value: int) -> None:
        """Set the pin to high if ``value`` is 1, or to low, if it is 0."""

    def write_analog(self, value: int) -> None:
        """Output a PWM signal on the pin, with the duty cycle proportional to
        the provided ``value``. The ``value`` may be either an integer or a
        floating point number between 0 (0% duty cycle) and 1023 (100% duty).
        """

    def set_analog_period(self, period: int) -> None:
        """Set the period of the PWM signal being output to ``period`` in
        milliseconds. The minimum valid value is 1ms.
        """

    def set_analog_period_microseconds(self, period: int) -> None:
        """Set the period of the PWM signal being output to ``period`` in
        microseconds. The minimum valid value is 35µs.
        """


class MicroBitAnalogDigitalPin(MicroBitDigitalPin):
    def read_analog(self) -> int:
        """Read the voltage applied to the pin, and return it as an integer
        between 0 (meaning 0V) and 1023 (meaning 3.3V).
        """


class MicroBitTouchPin(MicroBitAnalogDigitalPin):
    def is_touched(self) -> bool:
        """Return ``True`` if the pin is being touched with a finger, otherwise
        return ``False``.

        This test is done by measuring the capacitance of the pin together with
        whatever is connected to it. Human body has quite a large capacitance,
        so touching the pin gives a dramatic change in reading, which can be
        detected.
        """

pin0 = MicroBitTouchPin(0)
"""Pad 0."""

pin1 = MicroBitTouchPin(1)
"""Pad 1."""

pin2 = MicroBitTouchPin(2)
"""Pad 2."""


pin3 = MicroBitAnalogDigitalPin(3)
"""Column 1."""

pin4 = MicroBitAnalogDigitalPin(4)
"""Column 2."""

pin5 = MicroBitDigitalPin(5)
"""Button A."""

pin6 = MicroBitDigitalPin(6)
"""Row 2."""

pin7 = MicroBitDigitalPin(7)

"""Row 1."""

pin8 = MicroBitDigitalPin(8)

pin9 = MicroBitDigitalPin(9)
"""Row 3."""

pin10 = MicroBitAnalogDigitalPin(10)
"""Column 3."""

pin11 = MicroBitDigitalPin(11)
"""Button B."""

pin12 = MicroBitDigitalPin(12)

pin13 = MicroBitDigitalPin(13)
"""SPI MOSI."""

pin14 = MicroBitDigitalPin(14)
"""SPI MISO."""

pin15 = MicroBitDigitalPin(15)
"""SPI SCK."""

pin16 = MicroBitDigitalPin(16)

pin19 = MicroBitDigitalPin(19)
"""I2C SCL."""

pin20 = MicroBitDigitalPin(20)
"""I2C SDA."""


class Image:
    """The ``Image`` class is used to create images that can be displayed
    easily on the device's LED matrix. Given an image object it's possible to
    display it via the ``display`` API::

        display.show(Image.HAPPY)
    """

    HEART = None
    HEART_SMALL = None
    HAPPY = None
    SMILE = None
    SAD = None
    CONFUSED = None
    ANGRY = None
    ASLEEP = None
    SURPRISED = None
    SILLY = None
    FABULOUS = None
    MEH = None
    YES = None
    NO = None
    CLOCK12 = None
    CLOCK11 = None
    CLOCK10 = None
    CLOCK9 = None
    CLOCK8 = None
    CLOCK7 = None
    CLOCK6 = None
    CLOCK5 = None
    CLOCK4 = None
    CLOCK3 = None
    CLOCK2 = None
    CLOCK1 = None
    ARROW_N = None
    ARROW_NE = None
    ARROW_E = None
    ARROW_SE = None
    ARROW_S = None
    ARROW_SW = None
    ARROW_W = None
    ARROW_NW = None
    TRIANGLE = None
    TRIANGLE_LEFT = None
    CHESSBOARD = None
    DIAMOND = None
    DIAMOND_SMALL = None
    SQUARE = None
    SQUARE_SMALL = None
    RABBIT = None
    COW = None
    MUSIC_CROTCHET = None
    MUSIC_QUAVER = None
    MUSIC_QUAVERS = None
    PITCHFORK = None
    XMAS = None
    PACMAN = None
    TARGET = None
    TSHIRT = None
    ROLLERSKATE = None
    DUCK = None
    HOUSE = None
    TORTOISE = None
    BUTTERFLY = None
    STICKFIGURE = None
    GHOST = None
    SWORD = None
    GIRAFFE = None
    SKULL = None
    UMBRELLA = None
    SNAKE = None

    ALL_CLOCKS = [CLOCK1, CLOCK2, CLOCK3, CLOCK4, CLOCK5, CLOCK6,
                  CLOCK7, CLOCK8, CLOCK8, CLOCK9, CLOCK11, CLOCK12]
    ALL_ARROWS = [] # TODO: add arrows

    @overload
    def __init__(self, string: str) -> None:
        """``string`` has to consist of digits 0-9 arranged into lines,
        describing the image, for example::

            image = Image("90009:"
                          "09090:"
                          "00900:"
                          "09090:"
                          "90009")

        will create a 5×5 image of an X. The end of a line is indicated by a
        colon. It's also possible to use a newline (\n) to indicate the end of
        a line like this::

            image = Image("90009\n"
                          "09090\n"
                          "00900\n"
                          "09090\n"
                          "90009")
        """

    @overload
    def __init__(self, width: int = None, height: int = None,
                 buffer: Any = None) -> None:
        """Create an empty image with ``width`` columns and ``height`` rows.
        Optionally ``buffer`` can be an array of ``width``×``height`` integers
        in range 0-9 to initialize the image.
        """

    def width(self) -> int:
        """Return the number of columns in the image."""

    def height(self) -> int:
        """Return the numbers of rows in the image."""

    def set_pixel(self, x: int, y: int, value: int) -> None:
        """Set the brightness of the pixel at column ``x`` and row ``y`` to the
        ``value``, which has to be between 0 (dark) and 9 (bright).

        This method will raise an exception when called on any of the built-in
        read-only images, like ``Image.HEART``.
        """

    def get_pixel(self, x: int, y: int) -> int:
        """Return the brightness of pixel at column ``x`` and row ``y`` as an
        integer between 0 and 9.
        """

    def shift_left(self, n):
        """Return a new image created by shifting the picture left by ``n``
        columns.
        """

    def shift_right(self, n):
        """Same as ``image.shift_left(-n)``."""

    def shift_up(self, n):
        """Return a new image created by shifting the picture up by ``n``
        rows.
        """

    def shift_down(self, n: int):
        """Same as ``image.shift_up(-n)``."""

    def crop(self, x: int, y: int, w: int, h: int):
        """Return a new image by cropping the picture to a width of ``w`` and a
        height of ``h``, starting with the pixel at column ``x`` and row
        ``y``.
        """

    def copy(self):
        """Return an exact copy of the image."""

    def invert(self):
        """Return a new image by inverting the brightness of the pixels in the
        source image."""

    def fill(self, value: int) -> None:
        """Set the brightness of all the pixels in the image to the
        ``value``, which has to be between 0 (dark) and 9 (bright).

        This method will raise an exception when called on any of the built-in
        read-only images, like ``Image.HEART``.
        """

    def blit(self, src, x, y, w, h, xdest = 0,
             ydest = 0) -> None:
        """Copy the rectangle defined by ``x``, ``y``, ``w``, ``h`` from the
        image ``src`` into this image at ``xdest``, ``ydest``. Areas in the
        source rectangle, but outside the source image are treated as having a
        value of 0.

        ``shift_left()``, ``shift_right()``, ``shift_up()``, ``shift_down()``
        and ``crop()`` can are all implemented by using ``blit()``.

        For example, img.crop(x, y, w, h) can be implemented as::

            def crop(self, x, y, w, h):
                res = Image(w, h)
                res.blit(self, x, y, w, h)
                return res
        """

    def __repr__(self) -> str:
        """Get a compact string representation of the image."""

    def __str__(self) -> str:
        """Get a readable string representation of the image."""

    def __add__(self, other = None):
        """Create a new image by adding the brightness values from the two
        images for each pixel.
        """

    def __mul__(self, n: float):
        """Create a new image by multiplying the brightness of each pixel by
        ``n``.
        """
