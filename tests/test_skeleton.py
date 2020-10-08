# -*- coding: utf-8 -*-

import pytest

from id2020.skeleton import fib

__author__ = "Richard Wolff"
__copyright__ = "Richard Wolff"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
