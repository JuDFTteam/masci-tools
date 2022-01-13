"""
Click parameters for easily selecting multiple elements from a list via indices
"""
try:
    from typing import SupportsIndex
except ImportError:
    from typing_extensions import SupportsIndex
import click


class IntegerSlice(click.ParamType):
    """
    Click parameter for specifiying a range of numbers
    """
    name = 'integer-range'

    def convert(self, value, param, ctx):
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


class ListElement(IntegerSlice):
    """
    Click parameter for choosing an (or multiple) element(s) from a list
    """

    def __init__(self, data: SupportsIndex, return_list=False) -> None:
        self.data = data
        self.return_list = return_list
        super().__init__()

    def convert(self, value, param, ctx):
        indices = super().convert(value, param, ctx)

        try:
            values = self.data[indices]
            if not isinstance(values, list) and self.return_list:
                values = [values]
        except IndexError as exc:
            raise click.BadParameter(
                f'Please provide indices in the range of a list with length {len(self.data)}') from exc
        return values
