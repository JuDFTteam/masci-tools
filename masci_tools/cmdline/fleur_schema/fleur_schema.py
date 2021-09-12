# -*- coding: utf-8 -*-
"""
CLI commands for interacting with the fleur schemas in the masci-tools repository
"""

import masci_tools
from masci_tools.cmdline.utils import echo
from masci_tools.util.xml.common_functions import clear_xml, validate_xml
from masci_tools.io.io_fleurxml import load_inpxml, load_outxml
from masci_tools.io.parsers.fleur import inpxml_parser, outxml_parser

from pathlib import Path
import os
import sys
import shutil

import click
from lxml import etree


@click.command('add')
@click.argument('schema-file', type=click.Path(exists=True, path_type=Path, resolve_path=True))
@click.option('--overwrite', is_flag=True, help='Overwrite any exisiting schema-file')
@click.option('--test-xml-file',
              type=click.Path(exists=True, path_type=Path, resolve_path=True),
              default=None,
              help='Example xmlfile for this schema version to test the file parser against')
def add_fleur_schema(schema_file, test_xml_file, overwrite):
    """
    Adds a new xml schema file to the folder in
    `masci_tools/io/parsers/fleur/fleur_schema`
    corresponding to its version number
    """
    from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict, OutputSchemaDict

    PACKAGE_ROOT = Path(masci_tools.__file__).parent.resolve()

    xmlschema = etree.parse(os.fspath(schema_file))
    xmlschema, _ = clear_xml(xmlschema)

    namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
    schema_version = xmlschema.xpath('/xsd:schema/@version', namespaces=namespaces)[0]

    schema_folder = Path(PACKAGE_ROOT) / Path(f'io/parsers/fleur/fleur_schema/{schema_version}')

    if schema_file.name == 'FleurInputSchema.xsd':

        destination = schema_folder / 'FleurInputSchema.xsd'
        input_schema = True
        if destination.is_file() and not overwrite:
            echo.echo_critical(
                f'Input Schema for version {schema_version} already exists. Use overwrite=True to replace the Schema')

        echo.echo_info(f"Copying Input Schema for version '{schema_version}' to: '{destination}'")

    elif schema_file.name == 'FleurOutputSchema.xsd':

        input_schema = False
        destination = schema_folder / 'FleurOutputSchema.xsd'
        if destination.is_file() and not overwrite:
            echo.echo_critical(
                f'Output Schema for version {schema_version} already exists. Use overwrite=True to replace the Schema')

        echo.echo_info(f"Copying Output Schema for version '{schema_version}' to: '{destination}'")

    else:
        echo.echo_critical("Fleur file schema has to be named 'FleurInputSchema.xsd' or 'FleurOutputSchema.xsd'")

    os.makedirs(schema_folder, exist_ok=True)
    shutil.copy(schema_file, destination)

    echo.echo_success('Copied Schema file to masci-tools repository')

    #Make sure that construction of SchemaDicts works for this schema
    if input_schema:
        schema_dict = InputSchemaDict.fromVersion(schema_version, no_cache=True)
    else:
        schema_dict = OutputSchemaDict.fromVersion(schema_version, no_cache=True)
    echo.echo_success('Created Schema dictionary for the given schema file')

    if test_xml_file is not None:

        echo.echo_info(f'Testing Schema for file: {test_xml_file}')
        if input_schema:
            xmltree, schema_dict = load_inpxml(test_xml_file)

            if schema_dict['inp_version'] != schema_version:
                echo.echo_error(
                    f"Test file ({schema_dict['inp_version']}) does not correspond to input version of inserted schema ({schema_version})"
                )
                sys.exit(1)

            parser_info = {}
            parser_dict = inpxml_parser(test_xml_file, parser_info_out=parser_info)
        else:
            xmltree, schema_dict = load_outxml(test_xml_file)

            if schema_dict['out_version'] != schema_version:
                echo.echo_error(
                    f"Test file ({schema_dict['out_version']}) does not correspond to output version of inserted schema ({schema_version})"
                )
                sys.exit(1)

            parser_info = {}
            parser_dict = outxml_parser(test_xml_file, parser_info_out=parser_info)

        echo.echo_info('Parser output:')
        echo.echo_dictionary(parser_dict)
        echo.echo_info('Parser warnings/information:')
        echo.echo_dictionary(parser_info)
        echo.echo_success(f'Parser finished for: {test_xml_file}')


@click.command('validate-input')
@click.argument('xml-file', type=click.Path(exists=True))
def validate_inpxmlfile(xml_file):
    """
    Validate the given inp.xml file against the Fleur schema stored for the
    version of the input
    """
    xml_file = os.path.abspath(xml_file)

    xmltree, schema_dict = load_inpxml(xml_file)

    try:
        validate_xml(xmltree, schema_dict.xmlschema, error_header='Input file does not validate against the schema')
    except etree.DocumentInvalid as err:
        echo.echo_error(str(err))
    else:
        echo.echo_success(f"{xml_file} validates against the schema for version {schema_dict['inp_version']}")


@click.command('validate-output')
@click.argument('xml-file', type=click.Path(exists=True))
def validate_outxmlfile(xml_file):
    """
    Validate the given out.xml file against the Fleur schema stored for the
    version of the output
    """
    xml_file = os.path.abspath(xml_file)

    xmltree, schema_dict = load_outxml(xml_file)

    try:
        validate_xml(xmltree, schema_dict.xmlschema, error_header='Output file does not validate against the schema')
    except etree.DocumentInvalid as err:
        echo.echo_error(str(err))
    else:
        echo.echo_success(f"{xml_file} validates against the schema for version {schema_dict['out_version']}")
