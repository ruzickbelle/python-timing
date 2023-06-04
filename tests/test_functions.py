# -*- coding: utf-8 -*-

"""
Tests the timing library functionality available through module functions.
"""

import time
from utils import ResultChecker, is_close
import timing


def test_start() -> None:
    """ Test the `timing.start()` function. """
    timer = timing.start()
    time.sleep(.1)
    elapsed = timer.stop()
    assert is_close(elapsed, .1)


def test_measure() -> None:
    """ Test the `timing.measure()` function. """
    checker = ResultChecker()
    timing.measure(lambda: time.sleep(.1), callback=checker.set_result)
    assert checker.is_close(.1)


def test_wrap_call() -> None:
    """ Test the `timing.wrap()` function by calling it directly. """
    checker = ResultChecker()
    timed_func = timing.wrap(lambda: time.sleep(.1), callback=checker.set_result)
    assert checker.is_unset()
    timed_func()
    assert checker.is_close(.1)


def test_wrap_decorator() -> None:
    """ Test the `timing.wrap()` function by using it as a decorator generator. """
    checker = ResultChecker()

    @timing.wrap(callback=checker.set_result)
    def timed_func() -> None:
        time.sleep(.1)

    assert checker.is_unset()
    timed_func()
    assert checker.is_close(.1)
