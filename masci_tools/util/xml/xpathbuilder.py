"""

"""
from typing import Dict, Any, Set
from lxml import etree

FilterType = Dict[str,Any]

class XPathBuilder:
    """
    Class for building a complex xpath (restricted to adding filters)
    from a simple xpath expression
    """

    def __init__(self, simple_path: 'etree._xpath', filters: Dict[str,FilterType]=None, compile_path:bool = False) -> None:
        self.compile_path = compile_path
        if isinstance(simple_path, str):
            self.components = simple_path.split('/')
        elif isinstance(simple_path, etree.XPath):
            self.components = simple_path.path.split('/')
        else:
            raise TypeError(f'Wrong type for simple path. Expected str or etree.Xpath. Got {type(simple_path)}')

        if len(set(self.components)) != len(self.components):
            raise NotImplementedError('The given xpath has multiple tags with the same name')

        self.filters: Dict[str,FilterType] = {}
        self.path_variables: Dict[str, 'etree._XPathObject'] = {}
        if filters is not None:
            for key, val in filters.items():
                self.add_filter(key, val)

    def add_filter(self, tag, conditions: FilterType):
        """
        """
        if tag not in self.components:
            raise ValueError(f"The tag {tag} is not part of the given xpath expression: {'/'.join(self.components)}")

        self.filters[tag] = {**self.filters.get(tag,{}),**conditions}

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
                        predicate = f'{predicate} or ${tag}_has'
                    else:
                        predicate = f'${tag}_has'
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
                        predicate = f'{predicate} or {index_condition}'
                    else:
                        predicate = index_condition
                else:
                    cond, value = dict(condition).popitem()

                    value_condition = f'${tag}_cond_{value_conditions} {cond} ${tag}_cond_{value_conditions}_value'

                    self.path_variables[f'{tag}_cond_{value_conditions}'] = condition_name
                    self.path_variables[f'{tag}_cond_{value_conditions}_value'] = value

                    value_conditions += 1

                    if predicate:
                        predicate = f'{predicate} or {value_condition}'
                    else:
                        predicate = value_condition

            predicates[component_index] = predicate

        path = '/'.join([f'{tag}[{predicate}]' if predicate else tag for tag, predicate in zip(self.components, predicates)])
        if self.compile_path:
            return etree.XPath(path)
        return path

    def __repr__(self):
        return f"{self.__class__.__qualname__}({'/'.join(self.components)!r}, {self.filters!r}, compile_path={self.compile_path!r})"

    def __str__(self) -> str:
        path = self.path
        if not isinstance(path, str):
            path = path.path

        for name, value in self.path_variables.items():
            path = path.replace(f'${name}', str(value))
        return path