
from masci_tools.io.parsers.fleur_schema_parser_functions import create_schema_dict, load_schema_dict
import os

SCHEMA_FOLDER_PATHS = [
    './fleur_schema/input/0.27', './fleur_schema/input/0.28', './fleur_schema/input/0.29',
    './fleur_schema/input/0.30', './fleur_schema/input/0.31', './fleur_schema/input/0.32',
    './fleur_schema/input/0.33',
]

PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def update_schema_dicts():

    for schema_folder in SCHEMA_FOLDER_PATHS:
        create_schema_dict(os.path.abspath(os.path.join(PACKAGE_DIRECTORY, schema_folder)))


update_schema_dicts()