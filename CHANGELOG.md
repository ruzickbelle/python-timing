## Version 1.0.2

* `timing.Timer.measure()` will now stop the timer but not call the callback, when the given `Callable` raises an
exception, similar to `timing.Timer.__exit__()`.
* Moved functions and `timing.prevtimer` to the module's `__init__.py`.
* Minor docstring changes.


## Version 1.0.1

* Initial Release
