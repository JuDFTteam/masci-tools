# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools    #
# For further information on the license, see the LICENSE.txt file            #
# For further information please visit http://www.flapw.de or                 #
#                                                                             #
###############################################################################

def get_tag_xpath(schema_dict, tag, contains=None):

    if tag not in schema_dict['tag_paths']:
        raise KeyError(f'Unknown tag: {tag}')

    paths = schema_dict['tag_paths'][tag]

    if not isinstance(paths, list):
        paths = [paths]

    if contains is not None:
        paths_copy = paths.copy()
        for xpath in paths_copy:
            if contains not in xpath:
                paths.remove(xpath)

    if len(paths) == 1:
        return paths[0]
    elif len(paths) > 1:
        raise ValueError(f'The tag {tag} has multiple possible paths with the current specification.'
                         f'These are possible: {paths}')
    else:
        raise ValueError(f'The tag {tag} has no path containing the phrase: {contains}.')


def get_attrib_xpath(schema_dict, attrib, key='attrib_paths', contains=None):

    if attrib not in schema_dict[key]:
        raise KeyError(f'Attribute {attrib} not in {key}')

    paths = schema_dict[key][attrib]

    if not isinstance(paths, list):
        paths = [paths]

    if contains is not None:
        paths_copy = paths.copy()
        for xpath in paths_copy:
            if contains not in xpath:
                paths.remove(xpath)

    if len(paths) == 1:
        return paths[0]
    elif len(paths) > 1:
        raise ValueError(f'The attrib {attrib} has multiple possible paths with the current specification.'
                         f'These are possible: {paths}')
    else:
        raise ValueError(f'The attrib {attrib} has no path containing the phrase: {contains}.')
