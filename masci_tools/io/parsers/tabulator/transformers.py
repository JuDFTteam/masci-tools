# pylint: disable=unused-import
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
"""This subpackage contains transformers for the tabulator subpackage, which turns
properties of a collections of objects into a table.

Transformers let you transform properties while they get tabulated.
"""

import abc as _abc
import typing as _typing
import dataclasses as _dc


@_dc.dataclass(init=True, repr=True, eq=True, order=False, frozen=False)
class TransformedValue:
    """Return type of the :py:class:`~.Transformer`."""
    is_transformed: bool = False
    value: _typing.Union[object, dict] = None
    dtypes: _typing.Union[object, dict] = None
    error: _typing.Optional[Exception] = None


class Transformer(_abc.ABC):
    """Specify how to transformer an object's properties for use in :py:class:`Tabulator`.

    To subclass, you have to implement the :py:meth:`~transformer` method.

    TODO: increase memory performance:

    The following points are meant for transformers using the aiida-jutools `NodeTabulator` implementation of
    Tabulator, but may be of interest  for other implementations. See also TODO in Tabulator docstring.

    - Add documentation for the as yet unmentioned TransformedValue member 'dtypes': a dict of same shape as
      'value' ({new_name: transformed_value}), but with its dict values being the desired dtypes string. This
      is optional, otherwise Tabulator will use standard dtypes or try to guess best dtypes for data on its own.
    """

    @_abc.abstractmethod
    def transform(self,
                  keypath: _typing.Union[str, _typing.List[str]],
                  value: _typing.Any,
                  obj: _typing.Any = None,
                  **kwargs) -> TransformedValue:
        """Specify how to transform properties, based on their keypath and type.

        Extends :py:meth:`~.Transformer.transform`. See also its docstring.

        This default transformer returns all property values unchanged, and so has no effect. To define
        transformations, create a subclass and overwrite with a custom transform method.

         Example: Say, a nested dictionary is passed. It has a property
         `a_dict:{outputs:{last_calc_output_parameters:{attributes:{total_charge_per_atom:[...]`, which
         is a numerical list. We would like the list, and its maximum tabulated as individual columns.
         All other properties included in the tabulation shall be not transformed. We would write
         that transformation rule like this.

        .. code-block:: python

           if keypath == ['outputs', 'last_calc_output_parameters', 'total_charge_per_atom']:
               # assert isinstance(value, list) # optional
               return TransformedValue(True,
                                       {'total_charge_per_atom': value,
                                       'maximum_total_charge': max(value)},
                                       None)

           return TransformedValue(False, value, None)

        All kinds of transformation rules for all kinds of properties can be tailored in this way
        to the specific use-case. Keep in mind that if a include list is used, the property (path) has
        to be included in the include list.

        The keyword arguments `**kwargs` can be used to pass additional arguments, such as external functions, say,
        like `func = external_transform_func`.

        If used in `aiida-jutools`: For accessing process node inputs and outputs Dict nodes properties:
        first key in keypath is 'inputs' or 'outputs', the second is the input or output name that `node.outputs.`
        displays on tab completion (which, under the hood, comes from the in- or outgoing link_label).

        :param keypath: A list of keys, one per nesting level. First key in keypath is usually the object's attribute
        name.
        :param value: The value of the current property.
        :param obj: Optionally, the object containing the property can be passed along. This enables to
                    transform the current property value in combination with other property values.
        :param kwargs: Additional keyword arguments for subclasses.
        :return: A tuple (transformed_value:object, with_new_columns flag:bool). If the flag is False, this
                 means the transformed output property has the same name as the input property (in/out referring
                 here to the input/output of the transform method, not the input/output properties of the object). If
                 the value is a dict, and the flag is set to True, this is understood such that new output
                 properties were created from the input property, and the output value should be interpreted as
                 {property_name: property_value}, possibly with one being the original property name. In a tabulator,
                 new columns would be created for these new properties.
        """
        pass


class DefaultTransformer(Transformer):
    """Extends :py:class:`~Transformer`.

    This default transformer does nothing (invariant operation): it just returns the value it received, along with
    the new columns flag with value 'False'.
    """

    def transform(self,
                  keypath: _typing.Union[str, _typing.List[str]],
                  value: _typing.Any,
                  obj: _typing.Any = None,
                  **kwargs) -> _typing.Tuple[_typing.Union[None, _typing.Any, dict], bool]:
        return TransformedValue(is_transformed=False, value=value, error=None)
