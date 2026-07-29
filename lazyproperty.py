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
        cache = instance.__dict__[self.cache_name]
        if n in cache:
            return cache[n]
        else:
            val = self.func(*args)
            cache[n] = val
            return val
        # return self.func(*args)


def perf_count(func):
    depth = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal depth
        outermost = depth == 0
        if outermost:
            t0 = time.perf_counter()
        depth += 1
        try:
            res = func(*args, **kwargs)
        finally:
            depth -= 1
        if outermost:
            print("Elapsed {}".format(time.perf_counter() - t0))
        return res

    return wrapper


class Fibonacci:
    @lazyproperty
    @perf_count
    def fib(self, n):
        return self.fib(n - 2) + self.fib(n - 1) if n >= 2 else n


if __name__ == "__main__":
    res = Fibonacci().fib(n := 80)
    print(f"fib({n}) = {res}")
