# -*- coding: utf-8 -*-

"""
Tests the timing library functionality available through the `Timer` class.
"""

import time
import pytest
from utils import ResultChecker, is_close
from timing import Timer, TimerStateError, TimerResult


def check_is_close(checker: ResultChecker, val: TimerResult, ref: TimerResult) -> None:
    """ Checks if the stored result and given value match and are close to the reference value. """
    assert checker.is_equal(val)
    assert checker.is_close(ref)


def test_basic() -> None:
    """ Test the `Timer`'s basic functionality by calling all methods. """
    checker = ResultChecker()
    timer = Timer(callback=checker.set_result)
    with pytest.raises(TimerStateError):
        timer.current()
    with pytest.raises(TimerStateError):
        timer.stop()
    with pytest.raises(TimerStateError):
        timer.restart()
    with pytest.raises(TimerStateError):
        timer.get()
    assert checker.is_unset()
    timer.start()
    time.sleep(.1)
    assert checker.is_unset()
    elapsed = timer.stop()
    check_is_close(checker, elapsed, .1)
    with timer:
        time.sleep(.2)
    assert checker.is_close(.2)
    timer.measure(lambda: time.sleep(.3), callback=checker.set_result)
    assert checker.is_close(.3)
    timed_func1 = timer.wrap(lambda: time.sleep(.4), callback=checker.set_result)
    assert checker.is_close(.3)
    timed_func1()
    assert checker.is_close(.4)

    @timer.wrap(callback=checker.set_result)
    def timed_func2() -> None:
        time.sleep(.5)

    assert checker.is_close(.4)
    timed_func2()
    assert checker.is_close(.5)

def test_units() -> None:
    """ Test the unit options. """
    checker = ResultChecker()
    timer = Timer(callback=checker.set_result)
    with timer:
        time.sleep(.1)
    assert is_close(timer.get("seconds"), .1)
    assert is_close(timer.get("milliseconds"), 100)
    assert is_close(timer.get("microseconds"), 100_000)
    assert is_close(timer.get("nanoseconds"), 100_000_000)
    with timer:
        time.sleep(.2)
    assert is_close(timer.get("seconds"), .2)
    assert is_close(timer.get("milliseconds"), 200)
    assert is_close(timer.get("microseconds"), 200_000)
    assert is_close(timer.get("nanoseconds"), 200_000_000)

