# -*- coding: utf-8 -*-

"""
Yet another timing library. It aims to support every timing pattern:
* Functions:    start() / stop() / measure(fn: Callable)
* Decorators:   wrap(fn: Callable) / @wrap
* Contexts:     with Timer() as timer: pass

For repeated performance measurements (microbenchmarks), use the builtin `timeit` library.
"""

from .timing import *
