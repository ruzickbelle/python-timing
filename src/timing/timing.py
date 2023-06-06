# -*- coding: utf-8 -*-

"""
Classes and types for the timing library.
"""

import typing
import time

TimerUnit = typing.Literal["seconds", "milliseconds", "microseconds", "nanoseconds"]
TimerResult = typing.Union[int, float]
TimerCallback = typing.Callable[[TimerResult], None]


class TimerStateError(Exception):
    """ Raised if the operation is not permitted in the current timer state. """
    __slots__ = ()


class Timer:
    """
    Timer class supporting multiple timing patterns:
    * Functions:    start() / stop() / measure(fn: Callable)
    * Decorators:   wrap(fn: Callable) / @wrap
    * Contexts:     with Timer() as timer: pass
    """
    __slots__ = ("starttime", "result", "unit", "callback")
    starttime: typing.Optional[int]
    result: typing.Optional[int]
    unit: TimerUnit
    callback: typing.Optional[TimerCallback]

    def __init__(self, unit: TimerUnit = "seconds", callback: typing.Optional[TimerCallback] = None) -> None:
        self.starttime = None
        self.result = None
        self.unit = unit
        self.callback = callback

    def start(self, replace: bool = False, clear: bool = True) -> None:
        """
        Starts the timer and clears the result.
        * Give `replace=True` to replace a running timer.
        * Give `clear=False` to keep the current result.
        * Raises `TimerStateError` if the timer is already running and `replace` is falsy.
        """
        if self.starttime is not None and not replace:
            raise TimerStateError("The timer is already running. Give `replace=True` to restart the timer anyway.")
        self.starttime = time.time_ns()
        if clear:
            self.result = None

    def current(self, unit: typing.Optional[TimerUnit] = None, callback: typing.Union[bool, TimerCallback] = True) -> TimerResult:
        """
        Saves the currently elapsed time as the result but does not stop the timer.
        * Returns the current result. See `get()` for help of the `unit` argument.
        * Calls the given callback with the result:
            * If `callback is True`, `self.callback` will be used.
            * If `callback is False`, no callback will be called.
            * Otherwise the argument is called.
        * Raises `TimerStateError` if the timer is not running.
        * Raises `ValueError` if the unit is not supported.
        """
        if self.starttime is None:
            raise TimerStateError("The timer is not running.")
        self.result = time.time_ns() - self.starttime
        return self._get_and_callback(unit=unit, callback=callback)

    def stop(self, unit: typing.Optional[TimerUnit] = None, callback: typing.Union[bool, TimerCallback] = True) -> TimerResult:
        """
        Stops the timer.
        * Returns the current result. See `get()` for help of the `unit` argument.
        * Calls the given callback with the result:
            * If `callback is True`, `self.callback` will be used.
            * If `callback is False`, no callback will be called.
            * Otherwise the argument is called.
        * Raises `TimerStateError` if the timer is not running.
        * Raises `ValueError` if the unit is not supported.
        """
        if self.starttime is None:
            raise TimerStateError("The timer is not running.")
        self.result = time.time_ns() - self.starttime
        self.starttime = None
        return self._get_and_callback(unit=unit, callback=callback)

    def restart(self, clear: bool = True, unit: typing.Optional[TimerUnit] = None, callback: typing.Union[bool, TimerCallback] = True) -> TimerResult:
        """
        Stops the timer and restarts it again.
        * Give `clear=False` to keep the previous result.
        * Returns the previous result. See `get()` for help of the `unit` argument.
        * Calls the given callback with the result:
            * If `callback is True`, `self.callback` will be used.
            * If `callback` is falsy, no callback will be called.
            * If `callback` is truthy, it is considered callable and called with the timer result.
        * Raises `TimerStateError` if the timer is not running.
        * Raises `ValueError` if the unit is not supported.
        """
        ret = self.stop(unit=unit, callback=callback)
        self.start(clear=clear)
        return ret

    def get(self, unit: typing.Optional[TimerUnit] = None) -> TimerResult:
        """
        Gets the current result in the given unit. Defaults to `self.unit` if no unit is given.
        * Raises `TimerStateError` if no result is available.
        * Raises `ValueError` if the unit is not supported.
        """
        if self.result is None:
            raise TimerStateError("No result available. Use `stop()` or exit the context before accessing the result.")
        if unit is None:
            unit = self.unit
        ret = self.result
        if unit == "nanoseconds":
            return ret
        if unit == "microseconds":
            return ret / 1e3
        if unit == "milliseconds":
            return ret / 1e6
        if unit == "seconds":
            return ret / 1e9
        else:
            raise ValueError(f"Unsupported unit \"{unit}\".")

    def _get_and_callback(self, unit: typing.Optional[TimerUnit] = None, callback: typing.Union[None, bool, TimerCallback] = True) -> TimerResult:
        """
        Gets the current result and calls the callback.
        * The unit defaults to `self.unit` if no unit is given.
        * Calls the given callback with the result:
            * If `callback is True`, `self.callback` will be used.
            * If `callback` is falsy, no callback will be called.
            * If `callback` is truthy, it is considered callable and called with the timer result.
        * Raises `TimerStateError` if no result is available.
        * Raises `ValueError` if the unit is not supported.
        """
        ret = self.get(unit=unit)
        if callback is True:
            callback = self.callback
        if callback:
            callback(ret)
        return ret

    def __enter__(self) -> "Timer":
        """ Calls `start()` and returns `self`. """
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Calls `stop()`.
        If an exception was raised in the context, the callback will not be called, but the timer will be stopped anyway.
        """
        callback = not bool(exc_type)  # don't call the callback if an exception was raised
        self.stop(callback=callback)
        return False  # don't suppress the exception

    def measure(self, fn: typing.Callable, unit: typing.Optional[TimerUnit] = None, callback: typing.Union[bool, TimerCallback] = True) -> typing.Any:
        """
        Times the Callable `fn` using this timer.
        * Returns the result of the Callable `fn`.
        * See `get()` for help of the `unit` argument.
        * Calls the given callback with the timer result:
            * If `callback is True`, `self.callback` will be used.
            * If `callback is False`, no callback will be called.
            * Otherwise the argument is called.
            * If the Callable `fn` raises an exception, no callback will be stopped, but the timer will be stopped anyway.
        * Raises `TimerStateError` if the timer is already running.
        * Raises `ValueError` if the unit is not supported.
        """
        self.start()
        try:
            ret = fn()
        except:
            self.stop(callback=False)
            raise
        else:
            self.stop(unit=unit, callback=callback)
        return ret

    def wrap(self, fn: typing.Optional[typing.Callable] = None, **kwargs) -> typing.Callable:
        """
        Implements the decorator pattern for the `measure()` method:
        * Decorator:             wrap(fn: Callable, **kwargs) / @wrap
        * Decorator Generator:   wrap(**kwargs)(fn: Callable) / @wrap(**kwargs)
        """
        if fn:
            def timed():
                return self.measure(fn, **kwargs)
            return timed
        else:
            def decorator(fn: typing.Callable):
                def timed():
                    return self.measure(fn, **kwargs)
                return timed
            return decorator
