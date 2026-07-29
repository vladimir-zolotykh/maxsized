#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable
import types


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


class Fibonacci:
    @lazyproperty
    def fib(self, n):
        return self.fib(n - 2) + self.fib(n - 1) if n >= 2 else n


if __name__ == "__main__":
    print(Fibonacci().fib(5))
