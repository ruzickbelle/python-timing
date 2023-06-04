# -*- coding: utf-8 -*-

"""
Utilities for testing.
"""

import typing
from timing import TimerResult


def is_close(val: TimerResult, ref: TimerResult) -> bool:
    """ Returns if the result is in a 10% margin of the reference value. """
    return ref <= val <= 1.1 * ref


class ResultChecker:
    """ Checks the result of a timer by providing a callback for storing the result. """
    __slots__ = ("result",)
    result: typing.Optional[TimerResult]

    def __init__(self):
        self.result = None

    def set_result(self, val: TimerResult) -> None:
        """ Store the result. """
        self.result = val

    def is_unset(self) -> bool:
        """ Check if there is currently no result stored. """
        return self.result is None

    def is_equal(self, ref: TimerResult) -> bool:
        """ Checks if the stored result is equal to the given reference value. """
        assert self.result is not None
        return self.result == ref

    def is_close(self, ref: TimerResult) -> bool:
        """ Checks if the stored result is close to the given reference value. """
        assert self.result is not None
        return is_close(self.result, ref)
