#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


class Field:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def validate(self, instance, value):
        pass

    def __set__(self, instance, value):
        self.validate(instance, value)
        instance.__dict__[self._name] = value


class Typed(Field):
    def validate(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{value}: expected {self.expected_type!r}")
        super().validate(instance, value)


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
        super().validate(instance, value)


class MaxSized(Field):
    def validate(self, instance, value):
        if not hasattr(self, "size"):
            raise AttributeError("Missing 'size'")
        if len(value) > self.size:
            raise ValueError(f"{value}: must not exceed {self.size} in lenght")
        super().validate(instance, value)


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    pass


class SizedString(String, MaxSized):
    pass


class Stock:
    name = SizedString(size=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __repr__(self):
        args = ", ".join(f"{a!r}" for _, a in self.__dict__.items())
        return f"{type(self).__name__}({args})"


@pytest.fixture
def stock():
    return Stock("ACME", 50, 91.1)


def test_name(stock):
    assert stock.name == "ACME"
    with pytest.raises(ValueError, match="must not exceed 8 in lenght"):
        stock.name = "ABRACADABRA"


def test_shares(stock):
    assert stock.shares == 50
    with pytest.raises(TypeError):
        stock.shares = -75


def test_price(stock):
    with pytest.raises(TypeError):
        stock.price = "a lot"


if __name__ == "__main__":
    s = Stock("ACME", 50, 91.1)
    print(s)
