"""
CLI commands for interacting with the fleur schemas in the masci-tools repository
"""
from .root import cli
import click

import masci_tools
from masci_tools.cmdline.utils import echo
from masci_tools.util.xml.common_functions import clear_xml
from masci_tools.util.xml.converters import convert_str_version_number
from masci_tools.io.fleur_xml import load_inpxml, load_outxml
from masci_tools.io.parsers.fleur import inpxml_parser, outxml_parser
from masci_tools.io.parsers.fleur_schema import InputSchemaDict, OutputSchemaDict, list_available_versions

from pathlib import Path
import os
import sys
import shutil
import tempfile
import tabulate

from lxml import etree

GITLAB_URL = 'https://iffgit.fz-juelich.de'
try:
    import gitlab
except ImportError:
    gitlab = None


@cli.group('fleur-schema')
def fleur_schema():
    """Commands related to the Fleur XML Schemas"""


@fleur_schema.command('pull')
@click.argument('branch', type=str)
@click.option('--api-key', type=str, help='API key for access to the Iff Gitlab instance', default='')
@click.option('--test-xml-file',
              type=click.Path(exists=True, path_type=Path, resolve_path=True),
              default=None,
              help='Example xmlfile for this schema version to test the file parser against')
@click.pass_context
def pull_fleur_schema(ctx, branch, test_xml_file, api_key):
    """
    Pull the default XML schema files from the iffgit
    and store them in the subfolder of `masci_tools/io/parsers/fleur_schema`
    corresponding to its version number
    """
    ctx.invoke(add_fleur_schema,
               schema_file='FleurInputSchema.xsd',
               branch=branch,
               from_git=True,
               api_key=api_key,
               overwrite=True,
               test_xml_file=test_xml_file)
    ctx.invoke(add_fleur_schema,
               schema_file='FleurOutputSchema.xsd',
               branch=branch,
               from_git=True,
               api_key=api_key,
               overwrite=True,
               test_xml_file=test_xml_file)


@fleur_schema.command('add')
@click.argument('schema-file', type=click.Path(path_type=Path, resolve_path=True))
@click.option('--overwrite', is_flag=True, help='Overwrite any existing schema-file')
@click.option('--branch',
              type=str,
              help='If the file does not exist the branch can be specified in the fleur git',
              default='develop')
@click.option('--api-key', type=str, help='API key for access to the Iff Gitlab instance', default='')
@click.option('--test-xml-file',
              type=click.Path(exists=True, path_type=Path, resolve_path=True),
              default=None,
              help='Example xmlfile for this schema version to test the file parser against')
@click.option('--from-git', is_flag=True, help='Add the schema from the fleur git repository')
def add_fleur_schema(schema_file, test_xml_file, overwrite, branch, api_key, from_git):
    """
    Adds a new xml schema file to the folder in
    `masci_tools/io/parsers/fleur_schema`
    corresponding to its version number
    """

    PACKAGE_ROOT = Path(masci_tools.__file__).parent.resolve()

    if not isinstance(schema_file, Path):
        if isinstance(schema_file, bytes):
            schema_file = os.fsdecode(schema_file)
        schema_file = Path(schema_file)

    file_name = schema_file.name
    if file_name not in ('FleurInputSchema.xsd', 'FleurOutputSchema.xsd'):
        echo.echo_critical(
            "The Fleur file schema has to be named either 'FleurInputSchema.xsd' or 'FleurOutputSchema.xsd'")

    tmp_dir = None
    if from_git or not schema_file.is_file():
        if not from_git:
            echo.echo_warning(f'{schema_file} does not exist')
            if not click.confirm(f'Do you want to download from the fleur git ({branch})'):
                echo.echo_critical('Cannot add Schema file')

        if gitlab is None:
            echo.echo_critical(
                'Cannot download Schema file. Please install python-gitlab or the cmdline-extras requirements')

        api_key = api_key or os.getenv('IFFGIT_APIKEY', '')
        gl = gitlab.Gitlab(GITLAB_URL, private_token=api_key)

        try:
            gl.auth()
        except gitlab.exceptions.GitlabAuthenticationError:
            echo.echo_critical('I am not authorized to access the fleur repository.\n'
                               'Please set the environment variable IFFGIT_APIKEY to access the gitlab instance')

        groups = gl.groups.list(search='fleur')
        for g in groups:
            if g.name == 'fleur':
                repo_id = [repo.id for repo in g.projects.list(all=True) if repo.name == 'fleur'][0]
                project = gl.projects.get(repo_id)
                break
        tmp_dir = tempfile.mkdtemp()
        schema_file = Path(tmp_dir) / file_name
        echo.echo_info(f'Downloading {file_name} from branch {branch} to {schema_file}')
        with open(schema_file, 'wb') as f:
            project.files.raw(file_path=f'io/xml/{file_name}', ref=branch, streamed=True, action=f.write)
        echo.echo_success('Download successful')

    xmlschema = etree.parse(schema_file)
    xmlschema, _ = clear_xml(xmlschema)

    namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
    schema_version = xmlschema.xpath('/xsd:schema/@version', namespaces=namespaces)[0]

    schema_folder = Path(PACKAGE_ROOT) / Path(f'io/parsers/fleur_schema/{schema_version}')

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
    if tmp_dir is not None:
        shutil.rmtree(tmp_dir)

    #Make sure that construction of SchemaDicts works for this schema
    if input_schema:
        InputSchemaDict.fromVersion(schema_version, no_cache=True)
    else:
        OutputSchemaDict.fromVersion(schema_version, no_cache=True)
    echo.echo_success('Created Schema dictionary for the given schema file')

    if test_xml_file is not None:

        echo.echo_info(f'Testing Schema for file: {test_xml_file}')
        if input_schema:
            _, schema_dict = load_inpxml(test_xml_file)

            if schema_dict['inp_version'] != schema_version:
                echo.echo_error(
                    f"Test file ({schema_dict['inp_version']}) does not correspond to input version of inserted schema ({schema_version})"
                )
                sys.exit(1)

            parser_info = {}
            parser_dict = inpxml_parser(test_xml_file, parser_info_out=parser_info)
        else:
            _, schema_dict = load_outxml(test_xml_file)

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


@fleur_schema.command('validate-input')
@click.argument('xml-file', type=click.Path(exists=True))
def validate_inpxmlfile(xml_file):
    """
    Validate the given inp.xml file against the Fleur schema stored for the
    version of the input
    """

    xml_file = os.path.abspath(xml_file)

    xmltree, schema_dict = load_inpxml(xml_file)
    try:
        schema_dict.validate(xmltree)
    except ValueError as err:
        echo.echo_error(str(err))
    else:
        echo.echo_success(f"{xml_file} validates against the schema for version {schema_dict['inp_version']}")


@fleur_schema.command('validate-output')
@click.argument('xml-file', type=click.Path(exists=True))
def validate_outxmlfile(xml_file):
    """
    Validate the given out.xml file against the Fleur schema stored for the
    version of the output
    """
    xml_file = os.path.abspath(xml_file)

    xmltree, schema_dict = load_outxml(xml_file)
    try:
        schema_dict.validate(xmltree)
    except ValueError as err:
        echo.echo_error(str(err))
    else:
        echo.echo_success(f"{xml_file} validates against the schema for version {schema_dict['out_version']}")


@fleur_schema.command('list')
def list_available_schemas():
    """
    Show the available fleur schemas
    """
    input_versions = list_available_versions(output_schema=False)
    output_versions = list_available_versions(output_schema=True)

    all_versions = set(input_versions) | set(output_versions)
    all_versions = sorted(all_versions, key=convert_str_version_number)

    input_versions = [version in input_versions for version in all_versions]
    output_versions = [version in output_versions for version in all_versions]

    echo.echo_info('The following Schemas were found')
    echo.echo(
        tabulate.tabulate(list(zip(all_versions, input_versions, output_versions)),
                          headers=['Version', 'Input Schema available', 'Output Schema available']))
