# -*- coding: utf-8 -*-

from .root import cli

import click
from masci_tools.cmdline.utils import echo


@cli.group('parse')
def parse():
    """Commands for parsing information from KKR/Fleur files"""


def _load_xml_file(xml_file):
    from masci_tools.io.io_fleurxml import load_inpxml, load_outxml
    from masci_tools.util.xml.common_functions import clear_xml
    from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict
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
def parse_out_file(xml_file):
    """
    Parse the Fleur out.xml into a python dictionary
    """
    from masci_tools.io.parsers.fleur import outxml_parser

    parser_info = {}
    parser_dict = outxml_parser(xml_file, parser_info_out=parser_info)

    echo.echo_info('Parser output:')
    echo.echo_dictionary(parser_dict)
    echo.echo_info('Parser warnings/information:')
    echo.echo_dictionary(parser_info)


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

    atoms, cell, pbc = get_structure_data(xmltree, schema_dict, site_namedtuple=True)

    echo.echo_info('Atoms found:')
    echo.echo_formatted_list(atoms, ['symbol', 'kind', 'position'])
    echo.echo_info('Bravais matrix:')
    echo.echo(str(cell))
    echo.echo_info(f'Periodic boundary conditions {pbc}:')


@parse.command('cell')
@click.argument('xml-file', type=click.Path(exists=True))
def parse_cell_data(xml_file):
    """
    Parse the unit cell definition fo the given xml file
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
    echo.echo('Rotation  Translation')
    for rotation, shift in zip(rotations, shifts):
        for i in range(3):
            echo.echo(f'{rotation[i]}   {shift[i]}')
        echo.echo('')


@parse.command('attrib')
@click.option('--xml-file', '--file', '-f', type=click.Path(exists=True), help='XML file to parse')
@click.option('--name', '-n', type=str)
def parse_attrib(xml_file, parse_type, name):
    pass


@parse.command('text')
@click.option('--xml-file', '--file', '-f', type=click.Path(exists=True), help='XML file to parse')
@click.option('--name', '-n', type=str)
def parse_text(xml_file, parse_type, name):
    pass


@parse.command('all-attribs')
@click.option('--xml-file', '--file', '-f', type=click.Path(exists=True), help='XML file to parse')
@click.option('--name', '-n', type=str)
def parse_all_attribs(xml_file, parse_type, name):
    pass


@parse.command('single-value')
@click.option('--xml-file', '--file', '-f', type=click.Path(exists=True), help='XML file to parse')
@click.option('--name', '-n', type=str)
def parse_single_value(xml_file, parse_type, name):
    pass


@parse.command('parent-attribs')
@click.option('--xml-file', '--file', '-f', type=click.Path(exists=True), help='XML file to parse')
@click.option('--name', '-n', type=str)
def parse_parent_attribs(xml_file, parse_type, name):
    pass


@parse.command('tag-exists')
@click.option('--xml-file', '--file', '-f', type=click.Path(exists=True), help='XML file to parse')
@click.option('--name', '-n', type=str)
def parse_tag_exists(xml_file, parse_type, name):
    pass


@parse.command('number-nodes')
@click.option('--xml-file', '--file', '-f', type=click.Path(exists=True), help='XML file to parse')
@click.option('--name', '-n', type=str)
def parse_number_nodes(xml_file, parse_type, name):
    pass
