"""
Tests of the commands in the fleur-schema subgroup of the masci-tools cli
"""
from pathlib import Path
import os


def test_validate_input_valid():
    """
    Test of the validat-input command with a valid input file
    """
    from masci_tools.cmdline.commands.fleur_schema import validate_inpxmlfile
    from click.testing import CliRunner

    TEST_FILE = Path(__file__).parent.resolve() / Path('../files/fleur/Max-R5/SiLOXML/files/inp.xml')
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(validate_inpxmlfile, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occurred: {result.exception}'
    assert 'validates against the schema for version 0.34' in result.output


def test_validate_input_invalid():
    """
    Test of the validate-input command with an invalid input file
    """
    from masci_tools.cmdline.commands.fleur_schema import validate_inpxmlfile
    from click.testing import CliRunner

    TEST_FILE = Path(__file__).parent.resolve() / Path('../files/fleur/aiida_fleur/nonvalid_inpxml/crab/inp.xml')
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(validate_inpxmlfile, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occurred: {result.exception}'
    assert 'Error: Input file does not validate against the schema:' in result.output


def test_validate_output_valid():
    """
    Test of the validate-output command with a valid output file
    """
    from masci_tools.cmdline.commands.fleur_schema import validate_outxmlfile
    from click.testing import CliRunner

    TEST_FILE = Path(__file__).parent.resolve() / Path('../files/fleur/Max-R5/SiLOXML/files/out.xml')
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(validate_outxmlfile, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occurred: {result.exception}'
    assert 'validates against the schema for version 0.34' in result.output


def test_validate_output_invalid():
    """
    Test of the validate-output command with an invalid output file
    """
    from masci_tools.cmdline.commands.fleur_schema import validate_outxmlfile
    from click.testing import CliRunner

    TEST_FILE = Path(__file__).parent.resolve() / Path('../files/fleur/broken_out_xml/simple_validation_error.xml')
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(validate_outxmlfile, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occurred: {result.exception}'
    assert 'Error: Output file does not validate against the schema:' in result.output


def test_add_fleur_schema_input(fake_schemas_and_test_files):
    """
    Test of the add_fleur_schema command for input schema
    """
    from masci_tools.cmdline.commands.fleur_schema import add_fleur_schema
    from click.testing import CliRunner

    runner = CliRunner()
    args = [
        os.fspath(fake_schemas_and_test_files / 'FleurInputSchema.xsd'), '--test-xml-file',
        os.fspath(fake_schemas_and_test_files / 'inp.xml')
    ]
    result = runner.invoke(add_fleur_schema, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occurred: {result.exception}'
    assert 'Copied Schema file to masci-tools repository' in result.output
    assert 'Created Schema dictionary for the given schema file' in result.output
    assert 'Parser finished for:' in result.output


def test_add_fleur_schema_output(fake_schemas_and_test_files):
    """
    Test of the add_fleur_schema command for input schema
    """
    from masci_tools.cmdline.commands.fleur_schema import add_fleur_schema
    from click.testing import CliRunner

    runner = CliRunner()
    args = [
        os.fspath(fake_schemas_and_test_files / 'FleurInputSchema.xsd'), '--test-xml-file',
        os.fspath(fake_schemas_and_test_files / 'inp.xml')
    ]
    result = runner.invoke(add_fleur_schema, args)
    assert result.exception is None, 'An unexpected exception occurred: {result.exception}'
    args = [
        os.fspath(fake_schemas_and_test_files / 'FleurOutputSchema.xsd'), '--test-xml-file',
        os.fspath(fake_schemas_and_test_files / 'out.xml')
    ]
    result = runner.invoke(add_fleur_schema, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occurred: {result.exception}'
    assert 'Copied Schema file to masci-tools repository' in result.output
    assert 'Created Schema dictionary for the given schema file' in result.output


def test_add_fleur_schema_overwrite(fake_schemas_and_test_files):
    """
    Test of the add_fleur_schema command for input schema
    """
    from masci_tools.cmdline.commands.fleur_schema import add_fleur_schema
    from click.testing import CliRunner

    runner = CliRunner()
    args = [
        os.fspath(fake_schemas_and_test_files / 'FleurInputSchema.xsd'), '--test-xml-file',
        os.fspath(fake_schemas_and_test_files / 'inp.xml')
    ]
    result = runner.invoke(add_fleur_schema, args)
    assert result.exception is None, 'An unexpected exception occurred: {result.exception}'
    args = [os.fspath(fake_schemas_and_test_files / 'FleurInputSchema.xsd')]
    result = runner.invoke(add_fleur_schema, args)

    print(result.output)
    assert result.exception is not None
    assert 'Critical: Input Schema for version 0.01 already exists. Use overwrite=True to replace the Schema' in result.output

    args = [os.fspath(fake_schemas_and_test_files / 'FleurInputSchema.xsd'), '--overwrite']
    result = runner.invoke(add_fleur_schema, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occurred: {result.exception}'
    assert 'Copied Schema file to masci-tools repository' in result.output
    assert 'Created Schema dictionary for the given schema file' in result.output


def test_list_versions():
    """
    Test of the list command for fleur-schema
    """
    from masci_tools.cmdline.commands.fleur_schema import list_available_schemas
    from click.testing import CliRunner

    runner = CliRunner()
    result = runner.invoke(list_available_schemas)

    assert result.exception is None, 'An unexpected exception occurred: {result.exception}'
    assert 'Version  Input Schema available    Output Schema available' in result.output
    assert '0.33  True                      True' in result.output
