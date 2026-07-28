#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
class Field:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self

    def validate(self, instance, value):
        raise NotImplementedError

    def __set__(self, instance, value):
        self.validate(instance, value)
        instance.__dict__[self._name] = value


class Typed(Field):
    def validate(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{value}: expected {self.expected_type!r}")


class Integer(Typed):
    expected_type = int


class Float(Typed):
    expected_type = float


class String(Typed):
    expected_type = str


class Unsigned(Field):
    def validate(self, instance, value):
        if value < 0:
            raise TypeError(f"{value}: Must be > 0")


class MaxSized(Field):
    def validate(self, instance, value):
        if not hasattr(self, "_size"):
            raise AttributeError("Missing '_size'")
        if len(value) > self._size:
            raise ValueError(f"{value}: must not exceed {self._size} in lenght")


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    pass


class SizedString(String, MaxSized):
    pass


class Stock:
    name = SizedString(8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


if __name__ == "__main__":
    s = Stock("ACME", 50, 91.1)
    print(s)
