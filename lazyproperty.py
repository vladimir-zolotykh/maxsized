#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable
import types
from functools import wraps
import time


class lazyproperty:
    def __init__(self, func: Callable):
        self.func = func
        self.cache_name = f"_cache_{func.__name__}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if not hasattr(instance, self.cache_name):
            setattr(instance, self.cache_name, {})
        # cache = getattr(instance, self.cache_name)
        return types.MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        instance, n = args
        return self.func(*args)


def perf_count(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        res = func(*args, **kwargs)
        print("elapsed {}".format(time.perf_counter() - t0))
        return res

    return wrapper


class Fibonacci:
    # @perf_count
    @lazyproperty
    def fib(self, n):
        return self.fib(n - 2) + self.fib(n - 1) if n >= 2 else n


if __name__ == "__main__":
    t0 = time.perf_counter()
    res = Fibonacci().fib(33)
    print(f"{res = }")
    print("Elapsed: {}".format(time.perf_counter() - t0))
