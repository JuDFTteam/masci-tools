"""
Module for utilities for parsing. Should be independent of the actual parsing functions
"""
from __future__ import annotations

from typing import NamedTuple, Any


class Conversion(NamedTuple):
    name: str
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}
