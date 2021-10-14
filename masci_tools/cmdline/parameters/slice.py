# -*- coding: utf-8 -*-

import click


class IntegerSlice(click.ParamType):
    """
    Click parameter for specifiying a range of numbers
    """
    name = 'integer-range'

    def convert(self, value, param, ctx):
        if isinstance(value, int):
            return value

        if '-' in value:
            start, stop = value.split('-')
            return slice(int(start), int(stop) + 1)
        else:
            return int(value)
