from masci_tools.io.parsers.inpschema_todict import create_inpschema_dict
from masci_tools.io.parsers.outschema_todict import create_outschema_dict
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def update_schema_dicts():

    for root, dirs, files in os.walk(PACKAGE_DIRECTORY):
        for file in files:
            path = os.path.abspath(root)
            if file == 'FleurInputSchema.xsd':
                create_inpschema_dict(path)
            elif file == 'FleurOutputSchema.xsd':
                if not os.path.isfile(os.path.join(path,'inpschema_dict.py')):
                    create_inpschema_dict(path)
                create_outschema_dict(path)