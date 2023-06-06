# -*- coding: utf-8 -*-

"""
Yet another timing library. It aims to support every timing pattern:
* Functions:    start() / stop() / measure(fn: Callable)
* Decorators:   wrap(fn: Callable) / @wrap
* Contexts:     with Timer() as timer: pass

For repeated performance measurements (microbenchmarks), use the builtin `timeit` library.
"""

import typing
from .timing import (
    Timer,
    TimerStateError,
    TimerUnit,
    TimerResult,
    TimerCallback,
)

prevtimer = None


def start(*args, **kwargs) -> Timer:
    """
    Creates a new `Timer`, starts and returns it.
    * All arguments are passed to the `Timer` constructor.
    * The created `Timer` may also be found in the module attribute `prevtimer`.
    """
    global prevtimer
    timer = Timer(*args, **kwargs)
    prevtimer = timer
    timer.start()
    return timer


def measure(fn: typing.Callable, **kwargs) -> typing.Any:
    """
    Creates a new `Timer`, times the Callable `fn` and returns the result.
    * All keyword arguments are passed to the `Timer` constructor.
    * The created `Timer` may also be found in the module attribute `prevtimer`.
    """
    global prevtimer
    timer = Timer(**kwargs)
    prevtimer = timer
    return timer.measure(fn)


def wrap(fn: typing.Optional[typing.Callable] = None, **kwargs) -> typing.Callable:
    """
    Creates a new `Timer`, wraps the Callable `fn` and returns the wrapped callable.
    * Decorator:             wrap(fn: Callable, **kwargs) / @wrap
    * Decorator Generator:   wrap(**kwargs)(fn: Callable) / @wrap(**kwargs)
    * All keyword arguments are passed to the `Timer` constructor.
    * The created `Timer` may also be found in the module attribute `prevtimer`, directly after wrapping.
    """
    global prevtimer
    timer = Timer(**kwargs)
    prevtimer = timer
    if fn:
        def timed():
            return timer.measure(fn)
        return timed
    else:
        def decorator(fn: typing.Callable):
            def timed():
                return timer.measure(fn)
            return timed
        return decorator
