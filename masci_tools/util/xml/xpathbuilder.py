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
from __future__ import annotations

from typing import Any, Iterable, cast
try:
    from typing import TypeAlias  #type: ignore[attr-defined]
except ImportError:
    from typing_extensions import TypeAlias

from lxml import etree

FilterType: TypeAlias = 'dict[str, Any]'
"""
Type for filters argument for XPathBuilder
"""


class XPathBuilder:
    """
    Class for building a complex xpath (restricted to adding filters)
    from a simple xpath expression

    .. note::
        passing in an etree.XPath object will not respect the options
        passed into it. Only the kwargs in __init__ are used to compile
        the path if compile_path=True

    .. note::
        Filters/Constraints (or predicates like they are called for XPaths) can either
        be added by providing the ``filters`` argument in the constructor or by calling
        the :py:meth:`add_filter()` method.

        The ``filters`` argument is a dictionary with the tag names, where to apply the condition,
        as keys and the condition as values while the :py:meth:`add_filter()` method takes these
        as it's two arguments. The tag name has to be a part of the original simple xpath expression.
        The conditition is a dictionary with one key specifying the kind of condition and the value for the
        condition. The condition can also be the name of an attribute or path, in which case the value can be another
        condition dictionary. The following conditions operators i.e. keys in the dictionary are supported:

            - ``=``/``==``: equal to
            - ``!=``: not equal to
            - ``<``: less than
            - ``>``: greater than
            - ``<=``: less than or equal to
            - ``>=``: greater than or equal to
            - ``contains``: attribute/tag contains the given value (case sensitive)
            - ``not-contains``: attribute/tag does not contains the given value
            - ``starts-with``: attribute/tag starts with the given value (case sensitive)
            - ``ends-with``: attribute/tag ends with the given value (case sensitive)
            - ``index``: Select tags based on their index in the parent tag (either explicit index or another condition)
            - ``has``: Select tags based on the presence of the given attribute/tag
            - ``has-not``: Select tags based on the absence of the given attribute/tag
            - ``number-nodes``: Compute the number of nodes in the previous path and select based on further criteria
            - ``and``: Provide multiple conditions in a list joined by ``and``
            - ``or``: Provide multiple conditions in a list joined by ``or``
            - ``in``: Select tags if the value of the path is in a given list of values
            - ``not-in``: Select tags if the value of the path is not in a given list of values
            - ``<string>``: All other strings are interpreted as paths to attributes/tags specifying conditions on their value
            - ``<tuple of paths>``: Multiple strings are interpreted as multiple node sets, which are joined with |

    Example::

        from masci_tools.util.xml.xpathbuilder import XPathBuilder

        # XPath selecting all lo tags for SCLO type LOs and Iron species
        xpath = XPathBuilder('/fleurInput/atomSpecies/species/lo',
                             filters = {'species': {
                                            'name': {'contains': 'Fe'},
                                        },
                                        'lo': {
                                            'type': 'SCLO'
                                        }
                                    })

    :param simple_path: basic simple XPath expression to start from
    :param filters: dictionary with filters
    :param compile_path: bool if True the path property will be compiled as etree.XPath
    :param strict: bool if True the __str__ conversion will raise an error

    Other Kwargs will be passed on to the etree.XPath compilation if ``compile_path=True``
    """

    BINARY_OPERATORS = {'=', '==', '!=', '<', '>', '<=', '>=', 'contains', 'not-contains', 'starts-with', 'ends-with'}
    UNARY_OPERATORS = {'has', 'has-not', 'number-nodes', 'string-length'}
    COMPOUND_OPERATORS = {'and', 'or', 'in', 'not-in'}

    #Operators, which are not formatted in the default way {left} {operator} {right}
    OPERATOR_FORMAT = {
        '==': '{left} = {right}',
        'contains': 'contains({left}, {right})',
        'not-contains': 'not(contains({left}, {right}))',
        'starts-with': 'starts-with({left}, {right})',
        'ends-with':
        '{right} = substring({left}, string-length({left}) - string-length({right}) + 1)',  #'ends-with({left}, {right})' only available in XPath 2.0
        'number-nodes': 'count({left})',
        'string-length': 'string-length({left})',
        'has': '{left}',
        'has-not': 'not({left})',
    }

    def __init__(self,
                 simple_path: etree._xpath,
                 filters: dict[str, FilterType] | None = None,
                 compile_path: bool = False,
                 strict: bool = False,
                 **kwargs: Any) -> None:
        self.compile_path = compile_path
        self.strict = strict
        if not self.compile_path and kwargs:
            raise ValueError('Keyword arguments only available for compiled Xpaths')
        if isinstance(simple_path, str):
            self.components = simple_path.rstrip('/').split('/')
        elif isinstance(simple_path, etree.XPath):
            self.components = simple_path.path.split('/')  #type: ignore
        else:
            raise TypeError(f'Wrong type for simple path. Expected str or etree.XPath. Got {type(simple_path)}')

        if len(set(self.components)) != len(self.components):
            raise NotImplementedError('The given xpath has multiple tags with the same name')

        self.path_kwargs = kwargs
        self.filters: dict[str, FilterType] = {}
        self.path_variables: dict[str, etree._XPathObject] = {}
        self.value_conditions: int = 0
        if filters is not None:
            for key, val in filters.items():
                self.add_filter(key, val)

    def add_filter(self, tag: str, conditions: FilterType | Any) -> None:
        """
        Add a filter to the filters dictionary

        :param tag: str name of the tag name to add a filter to
        :param conditions: dictionary specifying the filter
        """
        if tag not in self.components:
            raise ValueError(f"The tag {tag} is not part of the given xpath expression: {'/'.join(self.components)}")
        if not isinstance(conditions, dict):
            conditions = {'=': conditions}

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

    def get_predicate(self,
                      tag: str,
                      condition: Any,
                      compound: bool = False,
                      path: str = '.',
                      process_path: bool = False) -> str:
        """
        Construct the predicate for the given tag and condition

        :param tag: str name of the tag
        :param condition: condition specified, either dict or single value
        :param compound: bool if True the enclosing condition is a compound condition, forbidding any other compound condition
        :param path: path, to which to apply the condition
        :param process_path: bool if True the path will taken apart into its components and the components will be checked with XPath variables
        """

        if not isinstance(condition, dict):
            condition = {'=': condition}

        if len(condition) > 1:
            raise ValueError('Only one key allowed in condition')

        operator, content = dict(condition).popitem()

        if compound and operator in self.COMPOUND_OPERATORS:
            raise ValueError(f'Compound operators not allowed in already compound condition: {operator}')

        return self.process_condition(tag, operator, content, path, process_path=process_path)

    def process_condition(self, tag: str, operator: str, content: Any, path: str, process_path: bool = False) -> str:
        """
        Process the condition for the given tag and condition

        :param tag: str name of the tag
        :param operator: operator for condition
        :param content: content of condition
        :param path: path, to which to apply the condition
        :param process_path: bool if True the path will taken apart into its components and the components will be checked with XPath variables
        """

        if operator == 'and':
            if not isinstance(content, (list, tuple)):
                raise TypeError('For and operator provide the conditions as a list')
            predicates = [
                self.get_predicate(tag, condition_part, compound=True, path=path, process_path=process_path)
                for condition_part in content
            ]
            predicate = ' and '.join(predicates)
        elif operator == 'or':
            if not isinstance(content, (list, tuple)):
                raise TypeError('For or operator provide the conditions as a list')
            predicates = [
                self.get_predicate(tag, condition_part, compound=True, path=path, process_path=process_path)
                for condition_part in content
            ]
            predicate = ' or '.join(predicates)
        elif operator == 'in':
            if not isinstance(content, Iterable):
                raise TypeError('For in operator provide a sequence of possible values')
            predicate = self.get_predicate(tag, {'or': [{
                '=': value
            } for value in content]},
                                           path=path,
                                           process_path=process_path)
        elif operator == 'not-in':
            if not isinstance(content, Iterable):
                raise TypeError('For not-in operator provide a sequence of possible values')
            predicate = self.get_predicate(tag, {'and': [{
                '!=': value
            } for value in content]},
                                           path=path,
                                           process_path=process_path)
        elif operator == 'index':
            if isinstance(content, int):
                index = content
                if index == -1:
                    predicate = 'last()'
                elif index < 0:
                    index = abs(index + 1)
                    predicate = f'last() - ${tag}_index'
                else:
                    predicate = f'${tag}_index'
            else:
                cond, index = dict(content).popitem()
                if cond not in self.BINARY_OPERATORS:
                    raise ValueError(f'Operator {cond} not allowed for index')
                if index < 0:
                    index = abs(index + 1)
                    index_str = f'last() - ${tag}_index'
                else:
                    index_str = f'${tag}_index'
                operator_fmt = self.OPERATOR_FORMAT.get(cond, f'{{left}} {cond} {{right}}')
                predicate = operator_fmt.format(left='position()', right=index_str)
            self.path_variables[f'{tag}_index'] = index
        elif operator in self.BINARY_OPERATORS:
            operator_fmt = self.OPERATOR_FORMAT.get(operator, f'{{left}} {operator} {{right}}')

            variable_name = f'{tag}_cond_{self.value_conditions}'
            if process_path:
                path_variable = self._path_condition(path, tag)
            else:
                path_variable = ' | '.join(path) if isinstance(path, tuple) else path

            predicate = operator_fmt.format(left=path_variable, right=f'${variable_name}')
            self.path_variables[variable_name] = content
            self.value_conditions += 1
        elif operator in self.UNARY_OPERATORS - {'has', 'has-not'}:
            operator_fmt = self.OPERATOR_FORMAT.get(operator, '{left}')
            if process_path:
                path_variable = self._path_condition(path, tag)
            else:
                path_variable = ' | '.join(path) if isinstance(path, tuple) else path
            path_variable = operator_fmt.format(left=path_variable)
            predicate = self.get_predicate(tag, content, path=path_variable)
        elif operator in {'has', 'has-not'}:
            operator_fmt = self.OPERATOR_FORMAT.get(operator, '{left}')
            predicate = operator_fmt.format(left=self._path_condition(content, tag))
        else:
            predicate = self.get_predicate(tag, content, path=operator, process_path=True)

        return predicate

    def _path_condition(self, path: str | tuple[str, ...], prefix: str) -> str:
        """
        Prepare conditions based on variables

        :param path: str path to process
        :param prefix: str prefix to use for xpath variables
        """
        if isinstance(path, tuple):
            #Multiple node sets. Join them with union
            return ' | '.join(self._path_condition(p, f'{prefix}_{indx}') for indx, p in enumerate(path))

        parts = path.strip('/').split('/')
        variable_name = f'{prefix}_cond_{self.value_conditions}_name'

        path_variable = []
        for indx, part in enumerate(parts):
            if part != '.':
                path_variable.append(
                    f"{'@' if '@' in part or '/' not in path else ''}*[local-name()=${variable_name}_{indx}]")
            else:
                path_variable.append(part)
            self.path_variables[f'{variable_name}_{indx}'] = part.lstrip('@')

        return '/'.join(path_variable)

    @property
    def path(self) -> etree._xpath:
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

    def __repr__(self) -> str:
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
