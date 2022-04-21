"""
Commands for parsing information from KKR/Fleur files
"""
from .root import cli

import click
from masci_tools.cmdline.utils import echo


@cli.group('parse')
def parse():
    """Commands for parsing information from KKR/Fleur files"""


def _load_xml_file(xml_file):
    from masci_tools.io.fleur_xml import load_inpxml, load_outxml
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.io.parsers.fleur_schema import InputSchemaDict
    from lxml import etree

    FALLBACK_VERSION = '0.34'

    try:
        xmltree, schema_dict = load_outxml(xml_file)
    except (ValueError, IndexError):
        try:
            xmltree, schema_dict = load_inpxml(xml_file)
        except ValueError:
            schema_dict = InputSchemaDict.fromVersion(FALLBACK_VERSION)
            parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
            xmltree = etree.parse(xml_file, parser)
            xmltree, _ = clear_xml(xmltree)

    return xmltree, schema_dict


@parse.command('inp-file')
@click.argument('xml-file', type=click.Path(exists=True))
def parse_inp_file(xml_file):
    """
    Parse the Fleur inp.xml into a python dictionary
    """
    from masci_tools.io.parsers.fleur import inpxml_parser

    parser_info = {}
    parser_dict = inpxml_parser(xml_file, parser_info_out=parser_info)

    echo.echo_info('Parser output:')
    echo.echo_dictionary(parser_dict)
    echo.echo_info('Parser warnings/information:')
    echo.echo_dictionary(parser_info)


@parse.command('out-file')
@click.argument('xml-file', type=click.Path(exists=True))
@click.option('--ignore-validation', is_flag=True)
def parse_out_file(xml_file, ignore_validation):
    """
    Parse the Fleur out.xml into a python dictionary
    """
    from masci_tools.io.parsers.fleur import outxml_parser

    parser_info = {}
    parser_dict = outxml_parser(xml_file, parser_info_out=parser_info, ignore_validation=ignore_validation)

    echo.echo_info('Parser output:')
    echo.echo_dictionary(parser_dict)
    echo.echo_info('Parser warnings/information:')
    echo.echo_dictionary(parser_info)


@parse.command('constants')
@click.argument('xml-file', type=click.Path(exists=True))
def parse_constants(xml_file):
    """
    Parse the mathematical constants used in the given xml-file
    """
    from masci_tools.io.fleur_xml import get_constants

    xmltree, schema_dict = _load_xml_file(xml_file)

    constants = get_constants(xmltree, schema_dict)
    echo.echo_dictionary(constants)


@parse.command('fleur-modes')
@click.argument('xml-file', type=click.Path(exists=True))
def parse_fleur_modes(xml_file):
    """
    Parse the Fleur modes of the given xml file
    """
    from masci_tools.util.xml.xml_getters import get_fleur_modes

    xmltree, schema_dict = _load_xml_file(xml_file)

    fleur_modes = get_fleur_modes(xmltree, schema_dict)
    echo.echo_dictionary(fleur_modes)


@parse.command('structure')
@click.argument('xml-file', type=click.Path(exists=True))
def parse_structure_data(xml_file):
    """
    Parse the structure information in the given Fleur xml file
    """
    from masci_tools.util.xml.xml_getters import get_structure_data

    xmltree, schema_dict = _load_xml_file(xml_file)

    atoms, cell, pbc = get_structure_data(xmltree, schema_dict)

    echo.echo_info('Atoms found:')
    echo.echo_formatted_list(atoms, ['symbol', 'kind', 'position'])
    echo.echo_info('Bravais matrix:')
    echo.echo(str(cell))
    echo.echo_info(f'Periodic boundary conditions {pbc}:')


@parse.command('cell')
@click.argument('xml-file', type=click.Path(exists=True))
def parse_cell_data(xml_file):
    """
    Parse the unit cell definition of the given xml file
    """
    from masci_tools.util.xml.xml_getters import get_cell

    xmltree, schema_dict = _load_xml_file(xml_file)

    cell, pbc = get_cell(xmltree, schema_dict)

    echo.echo_info('Bravais matrix:')
    echo.echo(str(cell))
    echo.echo_info(f'Periodic boundary conditions {pbc}:')


@parse.command('parameters')
@click.argument('xml-file', type=click.Path(exists=True))
def parse_parameter_data(xml_file):
    """
    Parse the calculation parameters of the given xml file
    """
    from masci_tools.util.xml.xml_getters import get_parameter_data

    xmltree, schema_dict = _load_xml_file(xml_file)

    params = get_parameter_data(xmltree, schema_dict)

    echo.echo_info('LAPW parameters:')
    echo.echo_dictionary(params)


@parse.command('nkpts')
@click.argument('xml-file', type=click.Path(exists=True))
def parse_nkpts(xml_file):
    """
    Extract the number of kpoints used in the given xml file
    """
    from masci_tools.util.xml.xml_getters import get_nkpts

    xmltree, schema_dict = _load_xml_file(xml_file)
    nkpts = get_nkpts(xmltree, schema_dict)

    echo.echo_info(f'Number of k-points: {nkpts}')


@parse.command('kpoints')
@click.argument('xml-file', type=click.Path(exists=True))
def parse_kpoints_data(xml_file):
    """
    Parse the used kpoints from the given xml-file
    """
    from masci_tools.util.xml.xml_getters import get_kpoints_data

    xmltree, schema_dict = _load_xml_file(xml_file)
    kpoints, weights, cell, pbc = get_kpoints_data(xmltree, schema_dict, only_used=True)

    echo.echo_info('Bravais matrix:')
    echo.echo(str(cell))
    echo.echo_info(f'Periodic boundary conditions {pbc}:')
    echo.echo_info('Kpoint coordinates (relative) and weights:')
    for kpoint, weight in zip(kpoints, weights):
        echo.echo(f'{kpoint}    w={weight}')


@parse.command('relaxation')
@click.argument('xml-file', type=click.Path(exists=True))
def parse_relaxation_data(xml_file):
    """
    Parse the relaxation information for the given xml file
    """
    from masci_tools.util.xml.xml_getters import get_relaxation_information

    xmltree, schema_dict = _load_xml_file(xml_file)
    relax_info = get_relaxation_information(xmltree, schema_dict)

    echo.echo_info('Relaxation Information:')
    echo.echo_dictionary(relax_info)


@parse.command('symmetry')
@click.argument('xml-file', type=click.Path(exists=True))
def parse_symmetry_information(xml_file):
    """
    Parse the symmetry information for the given xml file
    """
    from masci_tools.util.xml.xml_getters import get_symmetry_information

    xmltree, schema_dict = _load_xml_file(xml_file)
    rotations, shifts = get_symmetry_information(xmltree, schema_dict)

    echo.echo_info('Symmetry information:')
    for rotation, shift in zip(rotations, shifts):
        echo.echo('Rotation:')
        echo.echo(str(rotation))
        echo.echo('Translation:')
        echo.echo(str(shift))
        echo.echo('')


@parse.command('attrib')
@click.argument('xml-file', type=click.Path(exists=True))
@click.option('--name', '-n', type=str)
@click.option('--contains', '-c', type=str, multiple=True)
@click.option('--not-contains', '-nc', type=str, multiple=True)
@click.option('--tag', '-t', type=str)
def parse_attrib(xml_file, name, contains, not_contains, tag):
    """
    Parse the specified attribute from the given xml file
    """
    from masci_tools.util.schema_dict_util import evaluate_attribute

    xmltree, schema_dict = _load_xml_file(xml_file)
    attribv = evaluate_attribute(xmltree, schema_dict, name, contains=contains, not_contains=not_contains, tag_name=tag)

    echo.echo(f'Value for attribute {name}: {attribv}')


@parse.command('text')
@click.argument('xml-file', type=click.Path(exists=True))
@click.option('--name', '-n', type=str)
@click.option('--contains', '-c', type=str, multiple=True)
@click.option('--not-contains', '-nc', type=str, multiple=True)
def parse_text(xml_file, name, contains, not_contains):
    """
    Parse the text of the specified tag from the given xml file
    """
    from masci_tools.util.schema_dict_util import evaluate_text

    xmltree, schema_dict = _load_xml_file(xml_file)
    textv = evaluate_text(xmltree, schema_dict, name, contains=contains, not_contains=not_contains)

    echo.echo(f'Text for tag {name}: {textv}')


@parse.command('all-attribs')
@click.argument('xml-file', type=click.Path(exists=True))
@click.option('--name', '-n', type=str)
@click.option('--contains', '-c', type=str, multiple=True)
@click.option('--not-contains', '-nc', type=str, multiple=True)
@click.option('--subtags', is_flag=True)
@click.option('--text', is_flag=True)
def parse_all_attribs(xml_file, name, contains, not_contains, subtags, text):
    """
    Parse all attributes of the specified tag from the given xml file
    """
    from masci_tools.util.schema_dict_util import evaluate_tag

    xmltree, schema_dict = _load_xml_file(xml_file)
    res = evaluate_tag(xmltree,
                       schema_dict,
                       name,
                       contains=contains,
                       not_contains=not_contains,
                       subtags=subtags,
                       text=text)

    echo.echo(f'Tag {name}:')
    echo.echo_dictionary(res)


@parse.command('parent-attribs')
@click.argument('xml-file', type=click.Path(exists=True))
@click.option('--name', '-n', type=str)
@click.option('--contains', '-c', type=str, multiple=True)
@click.option('--not-contains', '-nc', type=str, multiple=True)
def parse_parent_attribs(xml_file, name, contains, not_contains):
    """
    Parse all attributes of the parent of the specified tag from the given xml file
    """
    from masci_tools.util.schema_dict_util import evaluate_parent_tag

    xmltree, schema_dict = _load_xml_file(xml_file)
    res = evaluate_parent_tag(xmltree, schema_dict, name, contains=contains, not_contains=not_contains)

    echo.echo(f'Tag {name}:')
    echo.echo_dictionary(res)


@parse.command('tag-exists')
@click.argument('xml-file', type=click.Path(exists=True))
@click.option('--name', '-n', type=str)
@click.option('--contains', '-c', type=str, multiple=True)
@click.option('--not-contains', '-nc', type=str, multiple=True)
def parse_tag_exists(xml_file, name, contains, not_contains):
    """
    Return whether the specified tag exists in the given xml file
    """
    from masci_tools.util.schema_dict_util import tag_exists

    xmltree, schema_dict = _load_xml_file(xml_file)
    res = tag_exists(xmltree, schema_dict, name, contains=contains, not_contains=not_contains)

    echo.echo(f"Tag {name}: {'exists' if res else 'does not exist'}")


@parse.command('number-nodes')
@click.argument('xml-file', type=click.Path(exists=True))
@click.option('--name', '-n', type=str)
@click.option('--contains', '-c', type=str, multiple=True)
@click.option('--not-contains', '-nc', type=str, multiple=True)
def parse_number_nodes(xml_file, name, contains, not_contains):
    """
    Return how often the specified tag occurs in the given xml file
    """
    from masci_tools.util.schema_dict_util import get_number_of_nodes

    xmltree, schema_dict = _load_xml_file(xml_file)
    res = get_number_of_nodes(xmltree, schema_dict, name, contains=contains, not_contains=not_contains)

    echo.echo(f'Tag {name}: {res} times')
