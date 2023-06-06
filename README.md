# timing
**timing** is a Python timing library providing timer functionality.

This library is one of many providing timers, but aims to:
* incorporate all patterns for timing execution times
* of functions and code blocks in any situation
* while being minimalistic in complexity but powerful nonetheless.

Some of the library's features are:
* It is compatible with Python 3.8+,
* fully typed, allowing your IDE to provide useful completions,
* tested using `pytest` and
* well documented by docstrings

Example program:
```python
import time
from timing import Timer

timer = Timer(callback=lambda x: print(f"Took {x:.2f} seconds."))
with timer:
    print("Executing step 1...")
    time.sleep(1)
with timer:
    print("Executing step 2...")
    time.sleep(2)
```
Output:
```
Executing step 1...
Took 1.00 seconds.
Executing step 2...
Took 2.00 seconds.
```


## Installation

**timing** can be installed using
```bash
$ python -m pip install timering
```

Note that on some systems, the Python 3 executable is called `python3` instead.


## [Release Notes](https://github.com/ruzickbelle/python-timing/blob/main/CHANGELOG.md)


## Supported Patterns

### Start and Stop

Create a timer, start and stop it:

```python
>>> from timing import Timer
>>> timer = Timer()
>>> timer.start()
>>> timer.stop()
2.442877164
```

Note that `timing.start()` creates a new `Timer`, starts and returns it directly.


### Context

Create a timer and measure the execution duration of a context:

```python
>>> with timer:
...     time.sleep(1)
...
>>> timer.get()
1.001198509
```


### Measure Functions

Create a timer and measure a given function:

```python
>>> import time
>>> timer.measure(lambda: time.sleep(2))
>>> timer.get()
2.002377642
```

Note that `timing.measure()` creates a new `Timer` and measures the given function with it. To retrieve the result, pass
a `callback` to `timing.measure()` or use `timing.prevtimer.get()` if you are certain it wasn't replaced since the start
of your `timing.measure()` call.


### Decorator Pattern / Wrapping Functions

Create a timer and wrap a function to measure its execution duration:

```python
>>> timed_func = timer.wrap(lambda: time.sleep(3))
>>> timed_func()
>>> timer.get()
3.003535439
>>> # alternatively
>>> @timer.wrap
... def timed_func():
...     time.sleep(2)
...
>>> timed_func()
>>> timer.get()
2.002481228
```

Note that there is also a `timing.wrap()` method available.


### Decorator Generator Pattern

To use Python's `@decorator` pattern with arguments, libraries often provide functionality for generating decorators:

```python
>>> @timer.wrap()
... def timed_func():
...     time.sleep(1)
...
>>> timed_func()
>>> timer.get()
1.001287624
```

Note that there is also a `timing.wrap()` method available.


## Configuration

The `Timer` constructor accepts a `unit` used for the returned results and a `callback` called with the result everytime
the timer stops. Every method also accepts the applicable arguments to override them once.

**Be careful** when calling `stop()` with a `unit` when a `callback` is defined as the `callback` will be called with
the result in the new unit and not the one given to the constructor.


## Contributing / Feedback

I happily accept feedback and pull requests.

Some ideas:
* Should I add support for registering multiple callbacks with different units?
