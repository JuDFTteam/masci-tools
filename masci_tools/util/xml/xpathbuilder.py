# -*- coding: utf-8 -*-
"""

"""
from typing import Dict, Any, Set, cast
from lxml import etree

FilterType = Dict[str, Any]


class XPathBuilder:
    """
    Class for building a complex xpath (restricted to adding filters)
    from a simple xpath expression

    .. note::
        passing in an etree.XPath object will not respect the options
        passed into it. Only the kwargs in __init__ are used to compile
        the path if compile_path=True

    """

    def __init__(self,
                 simple_path: 'etree._xpath',
                 filters: Dict[str, FilterType] = None,
                 compile_path: bool = False,
                 **kwargs) -> None:
        self.compile_path = compile_path
        if not self.compile_path and kwargs:
            raise ValueError('Keyword arguments only available for compiled Xpaths')
        if isinstance(simple_path, str):
            self.components = simple_path.split('/')
        elif isinstance(simple_path, etree.XPath):
            self.components = simple_path.path.split('/')  #type: ignore
        else:
            raise TypeError(f'Wrong type for simple path. Expected str or etree.XPath. Got {type(simple_path)}')

        if len(set(self.components)) != len(self.components):
            raise NotImplementedError('The given xpath has multiple tags with the same name')

        self.path_kwargs = kwargs
        self.filters: Dict[str, FilterType] = {}
        self.path_variables: Dict[str, 'etree._XPathObject'] = {}
        if filters is not None:
            for key, val in filters.items():
                self.add_filter(key, val)

    def add_filter(self, tag: str, conditions: FilterType) -> None:
        """
        """
        if tag not in self.components:
            raise ValueError(f"The tag {tag} is not part of the given xpath expression: {'/'.join(self.components)}")

        self.filters[tag] = {**self.filters.get(tag, {}), **conditions}

    def append_tag(self, tag: str) -> None:
        """
        """
        if tag in self.components:
            raise NotImplementedError(
                f"The tag {tag} is already part of the given xpath expression: {'/'.join(self.components)}")

        self.components.append(tag)

    def strip_off_tag(self) -> str:
        """
        """
        if not self.components:
            raise ValueError('Cannot strip off tag. Path is empty')

        return self.components.pop(-1)

    @property
    def path(self) -> 'etree._xpath':

        predicates = [''] * len(self.components)
        self.path_variables = {}

        for tag, conditions in self.filters.items():

            component_index = self.components.index(tag)
            predicate = ''

            value_conditions = 0
            for condition_name, condition in conditions.items():

                if condition_name == 'has':
                    if predicate:
                        predicate = f'{predicate} and ${tag}_has'
                    else:
                        predicate = f'${tag}_has'
                    self.path_variables[f'{tag}_has'] = condition
                if condition_name == 'has-not':
                    if predicate:
                        predicate = f'{predicate} and ${tag}_has_not'
                    else:
                        predicate = f'${tag}_has_not'
                    self.path_variables[f'{tag}_has'] = condition
                elif condition_name == 'index':
                    if isinstance(condition, int):
                        if condition == -1:
                            index_condition = 'last()'
                        elif condition == 1:
                            index_condition = 'first()'
                        elif condition < 0:
                            index_condition = f'last() - ${tag}_index'
                            self.path_variables[f'{tag}_index'] = condition + 1
                        else:
                            index_condition = f'${tag}_index'
                            self.path_variables[f'{tag}_index'] = condition
                    else:
                        cond, index = dict(condition).popitem()
                        index_condition = f'position() {cond} ${tag}_index'
                        self.path_variables[f'{tag}_index'] = index

                    if predicate:
                        predicate = f'{predicate} and {index_condition}'
                    else:
                        predicate = index_condition
                elif '/' not in condition_name:
                    cond, value = dict(condition).popitem()
                    if cond == 'contains':
                        value_condition = f'contains(@*[local-name()=${tag}_cond_{value_conditions}_name],${tag}_cond_{value_conditions})'
                    elif cond == 'not-contains':
                        value_condition = f'not contains(@*[local-name()=${tag}_cond_{value_conditions}_name],${tag}_cond_{value_conditions})'
                    else:
                        value_condition = f'@*[local-name()=${tag}_cond_{value_conditions}_name] {cond} ${tag}_cond_{value_conditions}'

                    self.path_variables[f'{tag}_cond_{value_conditions}_name'] = condition_name
                    self.path_variables[f'{tag}_cond_{value_conditions}'] = value
                    value_conditions += 1

                    if predicate:
                        predicate = f'{predicate} and {value_condition}'
                    else:
                        predicate = value_condition
                else:
                    raise NotImplementedError('Conditions based on subtags not implemented')

            predicates[component_index] = predicate

        path = '/'.join(
            [f'{tag}[{predicate}]' if predicate else tag for tag, predicate in zip(self.components, predicates)])
        if self.compile_path:
            return etree.XPath(path, **self.path_kwargs)
        return path

    def __repr__(self):
        return f"{self.__class__.__qualname__}({'/'.join(self.components)!r}, {self.filters!r}, compile_path={self.compile_path!r})"

    def __str__(self) -> str:
        path = self.path
        if isinstance(path, etree.XPath):
            path = path.path  #type: ignore
        path = cast(str, path)

        for name, value in sorted(self.path_variables.items(), key=lambda x: len(x[0]), reverse=True):
            path = path.replace(f'${name}', f'{value!r}')
        return path
