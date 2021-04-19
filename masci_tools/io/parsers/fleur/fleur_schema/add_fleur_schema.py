# -*- coding: utf-8 -*-
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
Contains utility to add new pairs of input/output schemas.
"""
from masci_tools.util.xml.common_functions import clear_xml
import os
import sys
import shutil
from lxml import etree

PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def add_fleur_schema(path, overwrite=False):
    """
    Adds the FleurInput/OutputSchema from the specified path (folder containing the Schemas)
    to the folder with the correct version number and creates the schema_dicts

    :param path: path to the folder containing the schema files
    :param overwrite: bool, if True and the schema with the same version exists it will be
                      overwritten. Otherwise an error is raised
    """

    schema_path = os.path.join(path, 'FleurInputSchema.xsd')
    if os.path.isfile(schema_path):
        xmlschema = etree.parse(schema_path)
        xmlschema = clear_xml(xmlschema)

        namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
        inp_version = xmlschema.xpath('/xsd:schema/@version', namespaces=namespaces)[0]

        copy_schema_folder = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, f'./{inp_version}'))
        copy_schema_file = os.path.abspath(os.path.join(copy_schema_folder, 'FleurInputSchema.xsd'))
        if os.path.isfile(copy_schema_file) and not overwrite:
            raise ValueError(
                f'Input Schema for version {inp_version} already exists. Use overwrite=True to replace the Schema')

        os.makedirs(copy_schema_folder, exist_ok=True)
        if not os.path.isfile(os.path.abspath(os.path.join(copy_schema_folder, '__init__.py'))):
            with open(os.path.abspath(os.path.join(copy_schema_folder, '__init__.py')), 'w') as f:
                pass
        shutil.copy(schema_path, copy_schema_file)

    schema_path = os.path.join(path, 'FleurOutputSchema.xsd')
    if os.path.isfile(schema_path):
        xmlschema = etree.parse(schema_path)
        xmlschema = clear_xml(xmlschema)

        namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
        out_version = xmlschema.xpath('/xsd:schema/@version', namespaces=namespaces)[0]

        copy_schema_folder = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, f'./{out_version}'))
        copy_schema_file = os.path.abspath(os.path.join(copy_schema_folder, 'FleurOutputSchema.xsd'))
        if os.path.isfile(copy_schema_file) and not overwrite:
            raise ValueError(
                f'Output Schema for version {out_version} already exists. Use overwrite=True to replace the Schema')

        os.makedirs(copy_schema_folder, exist_ok=True)
        if not os.path.isfile(os.path.abspath(os.path.join(copy_schema_folder, '__init__.py'))):
            with open(os.path.abspath(os.path.join(copy_schema_folder, '__init__.py')), 'w') as f:
                pass
        shutil.copy(schema_path, copy_schema_file)


if __name__ == '__main__':
    add_fleur_schema(sys.argv[1], overwrite=sys.argv[2])
