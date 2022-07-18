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
This module provides easy functions for loading a input/output xml file of
fleur and providing a parsed xml etree together with its corresponding schema dict
"""
from __future__ import annotations
import logging

from lxml import etree
import warnings
import os
from pathlib import Path
from functools import partial
from logging import Logger
from typing import Callable, Any, Generator
from contextlib import _GeneratorContextManager, contextmanager

from masci_tools.io.parsers import fleur_schema
from masci_tools.util.typing import XMLFileLike, XMLLike
from masci_tools.util.xml.common_functions import eval_xpath_one, normalize_xmllike

__all__ = ('load_inpxml', 'load_outxml', 'FleurXMLContext', 'get_constants', 'load_outxml_and_check_for_broken_xml',
           '_EvalContext')


def load_inpxml(inpxmlfile: XMLFileLike,
                logger: Logger | None = None,
                base_url: str | Path | None = None,
                **kwargs: Any) -> tuple[etree._ElementTree, fleur_schema.InputSchemaDict]:
    """
    Loads a inp.xml file for fleur together with its corresponding schema dictionary

    :param inpxmlfile: either path to the inp.xml file, opened file handle (in bytes modes i.e. rb)
                       or a xml etree to be parsed

    :returns: parsed xmltree of the inpxmlfile and the schema dictionary
              for the corresponding input version
    """
    from masci_tools.io.parsers.fleur_schema import InputSchemaDict

    xml_parse_func: Callable = etree.parse
    if isinstance(inpxmlfile, (str, bytes, Path)) and not os.path.isfile(inpxmlfile):
        xml_parse_func = etree.fromstring
        if base_url is None:
            warnings.warn('You provided a string of content but no base_url argument.'
                          'Setting it to the current working directory.'
                          'If the tree contains xinclude tags these could fail')
            base_url = os.getcwd()
        elif isinstance(base_url, Path):
            base_url = os.fspath(base_url)
        xml_parse_func = partial(xml_parse_func, base_url=base_url)

        #If the XML text is passed in as a string the XML parser
        #will complain since the XML declaration with encoding
        #options is contained in the string. We reencode it as utf-8 here
        #Since we do not expect fragments of a file here we should be fine
        if isinstance(inpxmlfile, str):
            inpxmlfile = inpxmlfile.encode('utf-8')

    if isinstance(inpxmlfile, etree._ElementTree):
        xmltree = inpxmlfile
    else:
        parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8', **kwargs)

        try:
            xmltree = xml_parse_func(inpxmlfile, parser)
        except etree.XMLSyntaxError as msg:
            if logger is not None:
                logger.exception('Failed to parse input file')
            raise ValueError(f'Failed to parse input file: {msg}') from msg

    if etree.iselement(xmltree):
        xmltree = xmltree.getroottree()

    if xmltree is None:
        if logger is not None:
            logger.error('No XML tree generated. Check that the given file exists')
        raise ValueError('No XML tree generated. Check that the given file exists')

    version = eval_xpath_one(xmltree, '//@fleurInputVersion', str)
    if logger is not None:
        logger.info('Got Fleur input file with file version %s', version)

    schema_dict = InputSchemaDict.fromVersion(version, logger=logger)

    return xmltree, schema_dict


def load_outxml(outxmlfile: XMLFileLike,
                logger: Logger | None = None,
                base_url: str | Path | None = None,
                **kwargs: Any) -> tuple[etree._ElementTree, fleur_schema.OutputSchemaDict]:
    """
    Loads a out.xml file for fleur together with its corresponding schema dictionary.
    Also returns whether the XML file had to be parsed with `recover=True`

    :param outxmlfile: either path to the out.xml file, opened file handle (in bytes modes i.e. rb)
                       or a xml etree to be parsed

    :returns: parsed xmltree of the outxmlfile and the schema dictionary
              for the corresponding output version
    """
    xmltree, schema_dict, _ = load_outxml_and_check_for_broken_xml(outxmlfile, logger, base_url, **kwargs)
    return xmltree, schema_dict


def load_outxml_and_check_for_broken_xml(
        outxmlfile: XMLFileLike,
        logger: Logger | None = None,
        base_url: str | Path | None = None,
        **kwargs: Any) -> tuple[etree._ElementTree, fleur_schema.OutputSchemaDict, bool]:
    """
    Loads a out.xml file for fleur together with its corresponding schema dictionary.
    Also returns whether the XML file had to be parsed with `recover=True`

    :param outxmlfile: either path to the out.xml file, opened file handle (in bytes modes i.e. rb)
                       or a xml etree to be parsed

    :returns: parsed xmltree of the outxmlfile and the schema dictionary
              for the corresponding output version and bool indicating whether the outxml is broken
    """
    from masci_tools.io.parsers.fleur_schema import OutputSchemaDict

    xml_parse_func: Callable = etree.parse
    if isinstance(outxmlfile, (str, bytes, Path)) and not os.path.isfile(outxmlfile):
        xml_parse_func = etree.fromstring
        if base_url is None:
            warnings.warn('You provided a string of content but no base_url argument.'
                          'Setting it to the current working directory.'
                          'If the tree contains xinclude tags these could fail')
            base_url = os.getcwd()
        elif isinstance(base_url, Path):
            base_url = os.fspath(base_url)
        xml_parse_func = partial(xml_parse_func, base_url=base_url)

        #If the XML text is passed in as a string the XML parser
        #will complain since the XML declaration with encoding
        #options is contained in the string. We reencode it as utf-8 here
        #Since we do not expect fragments of a file here we should be fine
        if isinstance(outxmlfile, str):
            outxmlfile = outxmlfile.encode('utf-8')

    outfile_broken = False

    if isinstance(outxmlfile, etree._ElementTree):
        xmltree = outxmlfile
    else:
        parser = etree.XMLParser(attribute_defaults=True, recover=False, encoding='utf-8', **kwargs)

        try:
            xmltree = xml_parse_func(outxmlfile, parser)
        except etree.XMLSyntaxError:
            outfile_broken = True
            if logger is None:
                warnings.warn('The out.xml file is broken I try to repair it.')
            else:
                logger.warning('The out.xml file is broken I try to repair it.')

        if outfile_broken:
            # repair xmlfile and try to parse what is possible.
            parser = etree.XMLParser(attribute_defaults=True, recover=True, encoding='utf-8', **kwargs)

            try:
                xmltree = xml_parse_func(outxmlfile, parser)
            except etree.XMLSyntaxError as err:
                raise ValueError('Skipping the parsing of the XML file. Repairing was not possible.') from err

    if etree.iselement(xmltree):
        xmltree = xmltree.getroottree()

    if xmltree is None:
        if logger is not None:
            logger.error('No XML tree generated. Check that the given file exists')
        raise ValueError('No XML tree generated. Check that the given file exists')

    out_version = eval_xpath_one(xmltree, '//@fleurOutputVersion', str)
    if out_version == '0.27':
        program_version = eval_xpath_one(xmltree, '//programVersion/@version', str)
        if program_version == 'fleur 32':
            #Max5 release (before bugfix)
            out_version = '0.33'
            inp_version = '0.33'
            if logger is not None:
                logger.warning("Ignoring '0.27' outputVersion for MaX5.0 release")
            else:
                warnings.warn("Ignoring '0.27' outputVersion for MaX5.0 release")
        elif program_version == 'fleur 31':
            #Max4 release
            out_version = '0.31'
            inp_version = '0.31'
            if logger is not None:
                logger.warning("Ignoring '0.27' outputVersion for MaX4.0 release")
            else:
                warnings.warn("Ignoring '0.27' outputVersion for MaX4.0 release")
        elif program_version == 'fleur 30':
            #Max3.1 release
            out_version = '0.30'
            inp_version = '0.30'
            if logger is not None:
                logger.warning("Ignoring '0.27' outputVersion for MaX3.1 release")
            else:
                warnings.warn("Ignoring '0.27' outputVersion for MaX3.1 release")
        elif program_version == 'fleur 27':
            #Max3.1 release
            out_version = '0.29'
            inp_version = '0.29'
            if logger is not None:
                logger.warning("Found version before MaX3.1 release falling back to file version '0.29'")
            warnings.warn(
                'out.xml files before the MaX3.1 release are not explicitly supported.'
                ' No guarantee is given that the parser will work without error', UserWarning)
        else:
            if logger is not None:
                logger.error("Unknown fleur version: File-version '%s' Program-version '%s'", out_version,
                             program_version)
            raise ValueError(f"Unknown fleur version: File-version '{out_version}' Program-version '{program_version}'")
    else:
        inp_version = eval_xpath_one(xmltree, '//@fleurInputVersion', str)

    schema_dict = OutputSchemaDict.fromVersion(out_version, inp_version=inp_version, logger=logger)

    return xmltree, schema_dict, outfile_broken


class _EvalContext:
    """
    Contextmanager to hold the relevant datastructures for evaluating values from XML files

    This holds:

        :param etree_or_element: The XML tree of the file
        :param schema_dict: The corresponding SchemaDict
        :param constants: The dictionary containing the defined mathematical constants
        :param logger: The configured logger instance
    """

    def __init__(self,
                 etree_or_element: XMLLike | etree.XPathElementEvaluator,
                 schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                 constants: dict[str, float] | None = None,
                 logger: logging.Logger | None = None) -> None:

        self.node: etree._Element | etree.XPathElementEvaluator
        if not isinstance(etree_or_element, etree.XPathElementEvaluator):
            self.node = normalize_xmllike(etree_or_element)
        else:
            self.node = etree_or_element
        self.schema_dict = schema_dict
        self.logger = logger
        self.constants = constants or get_constants(self.node, self.schema_dict, self.logger)

    def attribute(self, name: str, default: Any | None = None, **kwargs: Any) -> Any:
        """
        Alias for :py:func:`~masci_tools.util.schema_dict_util.evaluate_attribute()`

        :param name: str, name of the attribute
        :param default: value to return, if there are no values found
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                            the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other
            :param list_return: if True, the returned quantity is always a list even if only one element is in it
            :param optional: bool, if True and no logger given none or an empty list is returned

        :returns: list or single value, converted in convert_xml_attribute
        """
        from masci_tools.util.schema_dict_util import evaluate_attribute
        if default is not None:
            kwargs['optional'] = True
        res = evaluate_attribute(self.node,
                                 self.schema_dict,
                                 name,
                                 logger=self.logger,
                                 constants=self.constants,
                                 **kwargs)
        if res is None and default is not None:
            return default
        return res

    def text(self, name: str, **kwargs: Any) -> Any:
        """
        Alias for :py:func:`~masci_tools.util.schema_dict_util.evaluate_text()`

        :param name: str, name of the tag
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                            the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param list_return: if True, the returned quantity is always a list even if only one element is in it
            :param optional: bool, if True and no logger given none or an empty list is returned

        :returns: list or single value, converted in convert_xml_text
        """
        from masci_tools.util.schema_dict_util import evaluate_text
        return evaluate_text(self.node, self.schema_dict, name, logger=self.logger, constants=self.constants, **kwargs)

    def all_attributes(self, name: str, **kwargs: Any) -> Any:
        """
        Alias for :py:func:`~masci_tools.util.schema_dict_util.evaluate_tag()`

        :param name: str, name of the tag
        :param subtags: optional bool, if True the subtags of the given tag are evaluated
        :param text: optional bool, if True the text of the tag is also parsed
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                            the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param only_required: bool (optional, default False), if True only required attributes are parsed
            :param ignore: list of str (optional), attributes not to parse
            :param list_return: if True, the returned quantity is always a list even if only one element is in it
            :param strict_missing_error: if True, and no logger is given an error is raised if any attribute is not found

        """
        from masci_tools.util.schema_dict_util import evaluate_tag
        return evaluate_tag(self.node, self.schema_dict, name, logger=self.logger, constants=self.constants, **kwargs)

    def parent_attributes(self, name: str, **kwargs: Any) -> Any:
        """
        Alias for :py:func:`~masci_tools.util.schema_dict_util.evaluate_parent_tag()`

        :param name: str, name of the tag
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                            the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param only_required: bool (optional, default False), if True only required attributes are parsed
            :param ignore: list of str (optional), attributes not to parse
            :param list_return: if True, the returned quantity is always a list even if only one element is in it
            :param strict_missing_error: if True, and no logger is given an error is raised if any attribute is not found

        :returns: dict, with attribute values converted via convert_xml_attribute
        """
        from masci_tools.util.schema_dict_util import evaluate_parent_tag
        return evaluate_parent_tag(self.node,
                                   self.schema_dict,
                                   name,
                                   logger=self.logger,
                                   constants=self.constants,
                                   **kwargs)

    def single_value(self, name: str, **kwargs: Any) -> Any:
        """
        Alias for :py:func:`~masci_tools.util.schema_dict_util.evaluate_single_value_tag()`

        :param name: str, name of the tag
        :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param only_required: bool (optional, default False), if True only required attributes are parsed
            :param ignore: list of str (optional), attributes not to parse
            :param list_return: if True, the returned quantity is always a list even if only one element is in it
            :param strict_missing_error: if True, and no logger is given an error is raised if any attribute is not found
            :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                                the iteration element is constructed
            :param filters: Dict specifying constraints to apply on the xpath.
                            See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        :returns: value and unit, both converted in convert_xml_attribute
        """
        from masci_tools.util.schema_dict_util import evaluate_single_value_tag
        return evaluate_single_value_tag(self.node,
                                         self.schema_dict,
                                         name,
                                         logger=self.logger,
                                         constants=self.constants,
                                         **kwargs)

    def tag_exists(self, name: str, **kwargs: Any) -> bool:
        """
        Alias for :py:func:`~masci_tools.util.schema_dict_util.tag_exists()`

        :param name: str, name of the tag
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                            the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        :returns: bool, True if any tag exists
        """
        from masci_tools.util.schema_dict_util import tag_exists
        return tag_exists(self.node, self.schema_dict, name, logger=self.logger, **kwargs)

    def number_nodes(self, name: str, **kwargs: Any) -> int:
        """
        Alias of :py:func:`~masci_tools.util.schema_dict_util.get_number_of_nodes()`

        :param name: str, name of the tag

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                                   the iteration element is constructed
            :param filters: Dict specifying constraints to apply on the xpath.
                            See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        :returns: number of nodes of the given tag
        """
        from masci_tools.util.schema_dict_util import get_number_of_nodes
        return get_number_of_nodes(self.node, self.schema_dict, name, logger=self.logger, **kwargs)

    def attribute_exists(self, name: str, **kwargs: Any) -> bool:
        """
        Alias for :py:func:`~masci_tools.util.schema_dict_util.attrib_exists()`

        :param name: str, name of the attribute
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                            the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        Kwargs:
            :param tag_name: str, name of the tag where the attribute should be parsed
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
            :param exclude: list of str, here specific types of attributes can be excluded
                            valid values are: settable, settable_contains, other

        :returns: bool, True if any tag with the attribute exists
        """
        from masci_tools.util.schema_dict_util import attrib_exists
        return attrib_exists(self.node, self.schema_dict, name, logger=self.logger, **kwargs)

    def simple_xpath(self, name: str, **kwargs: Any) -> list[etree._Element] | etree._Element:
        """
        Alias for :py:func:`~masci_tools.util.schema_dict_util.eval_simple_xpath()`

        :param name: str, name of the tag
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                            the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
        :param list_return: bool, if True a list is always returned

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path

        :returns: etree Elements obtained via the simple xpath expression
        """
        from masci_tools.util.schema_dict_util import eval_simple_xpath
        return eval_simple_xpath(self.node, self.schema_dict, name, logger=self.logger, **kwargs)

    def find(self, name: str, **kwargs: Any) -> _GeneratorContextManager[_EvalContext]:  #pylint: disable=unsubscriptable-object
        """
        Finds the first element for the given name and constraints and gives a nested
        context for this element, i.e. inheriting the schema_dict, constants and logger

        Example::

            with FleurXMLContext(xmltree, schema_dict) as root:
                #Operations happen on the root here
                jspins = root.attribute('jspins')
                with root.find('species') as species:
                    #Operations in this block happen on the first species node
                    radius = species.attribute('radius')

        :param name: str, name of the tag
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                            the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
        """
        if 'list_return' in kwargs:
            raise ValueError('The argument list_return is not allowed in find()')

        nodes = self.simple_xpath(name, **kwargs, list_return=True)
        if nodes:
            return self.nested(nodes[0])
        raise ValueError(f'No nodes found for name {name}')

    @contextmanager
    def nested(self, etree_or_element: XMLLike) -> Generator[_EvalContext, None, None]:
        """
        Create a nested context from the current one
        inheriting the schema_dict, constants and logger only replacing the
        XML element

        Example of explicit usage::

            with FleurXMLContext(xmltree, schema_dict) as root:
                #Operations happen on the root here
                jspins = root.attribute('jspins')

                all_species_tag = root.simple_xpath('atomspecies')
                with root.nested(all_species_tag) as all_species:
                    #Operations happen on the 'atomSpecies' tag
                    mt_radii = all_species.attribute('radius')

        :param etree_or_element: Element to use for evaluation in the nested context
        """
        yield _EvalContext(etree_or_element, self.schema_dict, self.constants, logger=self.logger)

    def iter(self, name: str, **kwargs: Any) -> Generator[_EvalContext, None, None]:
        """
        Finds all elements for the given name and constraints and gives nested
        contexts for these elements to be iterated over,
        i.e. inheriting the schema_dict, constants and logger

        Example::

            with FleurXMLContext(xmltree, schema_dict) as root:
                #Operations happen on the root here
                jspins = root.attribute('jspins')
                for species in root.iter('species'):
                    #Operations happen on one species node in each iteration of the
                    #for loop. The order is the same as they appear in the XMl file
                    radius = species.attribute('radius')

        :param name: str, name of the tag
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                            the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

        Kwargs:
            :param contains: str, this string has to be in the final path
            :param not_contains: str, this string has to NOT be in the final path
        """
        if 'list_return' in kwargs:
            raise ValueError('The argument list_return is not allowed in iter()')
        nodes = self.simple_xpath(name, **kwargs, list_return=True)
        for node in nodes:
            with self.nested(node) as ctx:
                yield ctx


@contextmanager
def FleurXMLContext(etree_or_element: XMLLike | etree.XPathElementEvaluator,
                    schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                    constants: dict[str, float] | None = None,
                    logger: logging.Logger | None = None) -> Generator[_EvalContext, None, None]:
    """
    Contextmanager to hold the relevant datastructures for evaluating values from XML files

    This holds:

        :param etree_or_element: The XML tree of the file
        :param schema_dict: The corresponding SchemaDict
        :param constants: The dictionary containing the defined mathematical constants
        :param logger: The configured logger instance

    The following methods are available:
        - :py:meth:`_EvalContext.attribute()`: Evaluate attribute values
          (has an additional argument `default` to provide values for missing attributes)
        - :py:meth:`_EvalContext.text()`: Evaluate text of tags
        - :py:meth:`_EvalContext.all_attributes()`: Evaluate all attributes of a tag
        - :py:meth:`_EvalContext.parent_attributes()`: Evaluate attribute values of parent of given tag
        - :py:meth:`_EvalContext.single_value()`: Evaluate `value` and `unit` attribute of tag
        - :py:meth:`_EvalContext.tag_exists()`: Evaluate whether a given tag exists
        - :py:meth:`_EvalContext.number_nodes()`: Evaluate how many elements of the tag are present
        - :py:meth:`_EvalContext.attribute_exists()`: Evaluate whether an attribute exists
        - :py:meth:`_EvalContext.simple_xpath()`: Evaluate the simple xpath expression for a given tag
        - *Nested Context* :py:meth:`_EvalContext.find()`: Find the first occurrence of the tag and provide a nested
          context to that element
        - *Nested Context* :py:meth:`_EvalContext.iter()`: Find all occurrences of the tag and provide a nested
          context to these elements when iterated over
        - *Nested Context* :py:meth:`_EvalContext.nested()`: Explicitly inherit all the context except the
          XML tree to a new context with the XML element replaced by the given argument

    Example Usage::

        from masci_tools.io.fleur_xml import load_inpxml, FleurXMLContext
        xmltree, schema_dict = load_inpxml('/path/to/inp.xml')

        with FleurXMLContext(xmltree, schema_dict) as root:
            spins = root.attribute('jspins')
            noco = root.attribute('l_noco', default=False)

            #Not nesting the context we need to specify which elements are meant
            mt_radii = root.attribute('radius', contains='species')

            #Nesting using find
            with root.find('atomspecies') as all_species:
                mt_radii = all_species.attribute('radius')

            #Nesting using iter
            mt_radii = []
            for species in root.iter('species'):
                mt_radii.append(species.attribute('radius'))

    """
    yield _EvalContext(etree_or_element, schema_dict, constants=constants, logger=logger)


def get_constants(xmltree: XMLLike | etree.XPathElementEvaluator,
                  schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                  logger: Logger | None = None) -> dict[str, float]:
    """
    Reads in the constants defined in the inp.xml
    and returns them combined with the predefined constants from
    fleur as a dictionary

    :param root: root of the etree of the inp.xml file
    :param schema_dict: schema_dictionary of the version of the file to read (inp.xml or out.xml)
    :param logger: logger object for logging warnings, errors

    :return: a python dictionary with all defined constants
    """
    from masci_tools.util.constants import FLEUR_DEFINED_CONSTANTS
    from masci_tools.io.parsers.fleur_schema import NoPathFound
    import copy

    defined_constants = copy.deepcopy(FLEUR_DEFINED_CONSTANTS)
    with FleurXMLContext(xmltree, schema_dict, logger=logger, constants=defined_constants) as root:

        try:
            root.tag_exists('constant')
        except NoPathFound:
            warnings.warn('Cannot extract custom constants for the given root. Assuming defaults')
            return defined_constants

        if not root.tag_exists('constant'):  #Avoid warnings for empty constants
            return defined_constants

        constants = root.all_attributes('constant')
        if constants['name'] is not None:
            if not isinstance(constants['name'], list):
                constants = {key: [val] for key, val in constants.items()}
            for name, value in zip(constants['name'], constants['value']):
                if name not in defined_constants:
                    defined_constants[name] = value
                else:
                    if logger is not None:
                        logger.error('Ambiguous definition of constant %s', name)
                    raise KeyError(f'Ambiguous definition of constant {name}')

    return defined_constants
