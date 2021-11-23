# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
#                                                                             #
###############################################################################
"""
This module contains Classes for building complex XPath expressions based on
general attribute conditions from simple XPath expressions
"""
from typing import Dict, Any, cast
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

    .. note::
        Filters dictionary syntax (TODO)

    :param simple_path: basic simple XPath expression to start from
    :param filters: dictionary with filters
    :param compile_path: bool if True the path property will be compiled as etree.XPath
    :param strict: bool if True the __str__ conversion will raise an error

    Other Kwargs will be passed on to the etree.XPath compilation if ``compile_path=True``
    """

    def __init__(self,
                 simple_path: 'etree._xpath',
                 filters: Dict[str, FilterType] = None,
                 compile_path: bool = False,
                 strict: bool = False,
                 **kwargs) -> None:
        self.compile_path = compile_path
        self.strict = strict
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
        self.value_conditions: int = 0
        if filters is not None:
            for key, val in filters.items():
                self.add_filter(key, val)

    def add_filter(self, tag: str, conditions: FilterType) -> None:
        """
        Add a filter to the filters dictionary

        :param tag: str name of the tag name to add a filter to
        :param conditions: dictionary specifying the filter
        """
        if tag not in self.components:
            raise ValueError(f"The tag {tag} is not part of the given xpath expression: {'/'.join(self.components)}")

        self.filters[tag] = {**self.filters.get(tag, {}), **conditions}

    def append_tag(self, tag: str) -> None:
        """
        Append another tag to the end of the simple xpath expression

        :param tag: str name of the tag to append
        """
        if tag in self.components:
            raise NotImplementedError(
                f"The tag {tag} is already part of the given xpath expression: {'/'.join(self.components)}")

        self.components.append(tag)

    def strip_off_tag(self) -> str:
        """
        Strip off the last tag of the simple xpath expression
        """
        if not self.components:
            raise ValueError('Cannot strip off tag. Path is empty')

        #TODO: Check if the filters contains filters for the last tag

        return self.components.pop(-1)

    def get_predicate(self, tag, condition):
        """
        Construct the predicate for the given tag and condition

        :param tag: str name of the tag
        :param condition: condition specified, either dict or single value
        """

        if not isinstance(condition, dict):
            condition = {'=': condition}

        if len(condition) > 1:
            raise ValueError('Only one key allowed in condition')

        operator, content = dict(condition).popitem()
        if operator == '==':
            operator = '='

        return self.process_condition(tag, operator, content)

    def process_condition(self, tag, operator, content):
        """
        Process the condition for the given tag and condition

        :param tag: str name of the tag
        :param operator: operator for condition
        :param content: content of condition
        """

        if operator == 'and':
            if not isinstance(content, (list, tuple)):
                raise TypeError('For and operator and provide the conditions as a list')
            predicates = [self.get_predicate(tag, condition_part) for condition_part in content]
            predicate = ' and '.join(predicates)
        elif operator == 'or':
            if not isinstance(content, (list, tuple)):
                raise TypeError('For or operator and provide the conditions as a list')
            predicates = [self.get_predicate(tag, condition_part) for condition_part in content]
            predicate = ' or '.join(predicates)
        elif operator == 'has':
            predicate = f'${tag}_has'
            self.path_variables[f'{tag}_has'] = content
        elif operator == 'has-not':
            predicate = f'${tag}_has_not'
            self.path_variables[f'{tag}_has_not'] = content
        elif operator == 'index':
            if isinstance(content, int):
                if content == -1:
                    predicate = 'last()'
                elif content == 1:
                    predicate = 'first()'
                elif content < 0:
                    predicate = f'last() - ${tag}_index'
                    self.path_variables[f'{tag}_index'] = content + 1
                else:
                    predicate = f'${tag}_index'
                    self.path_variables[f'{tag}_index'] = content
            else:
                cond, index = dict(content).popitem()
                predicate = f'position() {cond} ${tag}_index'
                self.path_variables[f'{tag}_index'] = index
        elif '/' not in operator:
            if not isinstance(content, dict):
                content = {'=': content}
            cond, value = dict(content).popitem()

            variable_name = f'{tag}_cond_{self.value_conditions}_name'
            value_variable_name = f'{tag}_cond_{self.value_conditions}'

            if cond == 'contains':
                predicate = f'contains(@*[local-name()=${variable_name}],${value_variable_name})'
            elif cond == 'not-contains':
                predicate = f'not contains(@*[local-name()=${variable_name}],${value_variable_name})'
            else:
                predicate = f'@*[local-name()=${variable_name}] {cond} ${value_variable_name}'

            self.path_variables[variable_name] = operator
            self.path_variables[value_variable_name] = value
            self.value_conditions += 1
        else:
            if not isinstance(content, dict):
                content = {'=': content}
            cond, value = dict(content).popitem()
            parts = operator.strip('/').split('/')
            variable_name = f'{tag}_cond_{self.value_conditions}_name'
            value_variable_name = f'{tag}_cond_{self.value_conditions}'

            path_variable = []
            for indx, part in enumerate(parts):
                path_variable.append(f"{'@' if '@' in part else ''}*[local-name()=${variable_name}_{indx}]")
                self.path_variables[f'{variable_name}_{indx}'] = part.lstrip('@')
            path_variable = '/'.join(path_variable)

            if cond == 'contains':
                predicate = f'contains({path_variable},${value_variable_name})'
            elif cond == 'not-contains':
                predicate = f'not contains({path_variable},${value_variable_name})'
            else:
                predicate = f'{path_variable} {cond} ${value_variable_name}'

            self.path_variables[variable_name] = operator
            self.path_variables[value_variable_name] = value
            self.value_conditions += 1

        return predicate

    @property
    def path(self) -> 'etree._xpath':
        """
        Property for constructing the complex Xpath
        """

        predicates = [''] * len(self.components)
        self.path_variables = {}
        self.value_conditions = 0

        for tag, condition in self.filters.items():
            component_index = self.components.index(tag)
            predicates[component_index] = self.get_predicate(tag, condition)

        path = '/'.join(
            [f'{tag}[{predicate}]' if predicate else tag for tag, predicate in zip(self.components, predicates)])
        if self.compile_path:
            return etree.XPath(path, **self.path_kwargs)
        return path

    def __repr__(self):
        return f"{self.__class__.__qualname__}({'/'.join(self.components)!r}, {self.filters!r}, compile_path={self.compile_path!r}, strict={self.strict!r})"

    def __str__(self) -> str:
        if self.strict:
            raise ValueError(f'Implicit string conversion for {self.__class__.__qualname__}.')
        path = self.path
        if isinstance(path, etree.XPath):
            path = path.path  #type: ignore
        path = cast(str, path)

        for name, value in sorted(self.path_variables.items(), key=lambda x: len(x[0]), reverse=True):
            path = path.replace(f'${name}', f'{value!r}')
        return path
