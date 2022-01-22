"""
Click parameters for easily selecting multiple elements from a list via indices
"""
from __future__ import annotations

from typing import Generic, Sequence, TypeVar, Any
import click

T = TypeVar('T')
"""
Generic Type variable
"""


class IntegerSlice(click.ParamType):
    """
    Click parameter for specifying a range of numbers
    """
    name = 'integer-range'

    def convert(self, value: Any, param: click.Parameter | None, ctx: click.Context | None) -> int | slice:
        if isinstance(value, int):
            return value

        try:
            if '-' in value:
                start, stop = value.split('-')
                return slice(int(start), int(stop) + 1)
            return int(value)
        except TypeError as exc:
            raise click.BadParameter(
                'Please provide either an integer number or two integer numbers separated by -') from exc


class ListElement(IntegerSlice, Generic[T]):
    """
    Click parameter for choosing an (or multiple) element(s) from a list
    """

    def __init__(self, data: Sequence[T], return_list: bool = False) -> None:
        self.data = data
        self.return_list = return_list
        super().__init__()

    def convert(  #type:ignore[override]
            self, value: Any, param: click.Parameter | None, ctx: click.Context | None) -> T | Sequence[T]:
        indices = super().convert(value, param, ctx)

        try:
            values = self.data[indices]
            if not isinstance(values, list) and self.return_list:
                values = [values]  #type:ignore
        except IndexError as exc:
            raise click.BadParameter(
                f'Please provide indices in the range of a list with length {len(self.data)}') from exc
        return values
