from mpbdd.harness import _harness
from typing import overload


def get_pixel(x: int, y: int) -> int:
    pass

def set_pixel(x: int, y: int, value: int) -> None:
    pass

def clear() -> None:
    pass

class Image():
    pass

@overload
def show(image: Image) -> None:
    pass



@overload
def show(iterable, delay: int = 400, *,
         wait: bool = True, loop: bool =False, clear: bool = False) -> None:
    pass


def scroll(string: str, delay: int = 150, *, wait: bool = True,
           loop: bool = False, monospace: bool = False) -> None:
    _harness.monitor.debug('scrolls <%s>' % string)
    _harness.send_message('display', string)


def on() -> None:
    pass


def off() -> None:
    pass


def is_on() -> bool:
    pass
