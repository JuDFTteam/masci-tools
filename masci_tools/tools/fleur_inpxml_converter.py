# -*- coding: utf-8 -*-

from masci_tools.io.parsers.fleur_schema import InputSchemaDict
from masci_tools.io.io_fleurxml import load_inpxml
from masci_tools.util.schema_dict_util import evaluate_attribute
from masci_tools.util.xml.xml_setters_basic import xml_delete_tag, xml_delete_att, xml_create_tag
from masci_tools.util.xml.xml_setters_names import set_attrib_value
from masci_tools.util.xml.common_functions import split_off_attrib, split_off_tag, eval_xpath, validate_xml
from masci_tools.cmdline.parameters.slice import IntegerSlice
from masci_tools.cmdline.utils import echo
from collections import UserList, defaultdict
from typing import NamedTuple, Tuple
import tabulate
import json
from lxml import etree

import click
from pathlib import Path

FILE_DIRECTORY = Path(__file__).parent.resolve()


#These are the possible conversions that we can do
class MoveAction(NamedTuple):
    old_name: str
    new_name: str
    old_path: str
    new_path: str
    attrib: bool = False


class NormalizedMoveAction(NamedTuple):
    old_name: str
    new_name: str
    old_path: str
    new_path: str
    actual_path: str
    attrib: bool = False


class AmbiguousAction(NamedTuple):
    name: str
    old_paths: Tuple[str]
    new_paths: Tuple[str]
    attrib: bool


class RemoveAction(NamedTuple):
    name: str
    path: str
    attrib: bool = False


class CreateAction(NamedTuple):
    name: str
    path: str
    attrib: bool = False
    element: str = None


def analyse_paths(schema_start, schema_target, path_entries):

    if not isinstance(path_entries, list):
        path_entries = [path_entries]

    paths_start = defaultdict(list)
    paths_target = defaultdict(list)
    for path_entry in path_entries:
        new_paths = schema_start[path_entry]
        for name, paths in new_paths.items():
            if isinstance(paths, str):
                paths = [paths]
            paths_start[name].extend(paths)
        new_paths = schema_target[path_entry]
        for name, paths in new_paths.items():
            if isinstance(paths, str):
                paths = [paths]
            paths_target[name].extend(paths)

    removed_keys = paths_start.keys() - paths_target.keys()
    remove = []
    for key in removed_keys:
        paths = paths_start[key]
        if not isinstance(paths, (list, UserList)):
            paths = [paths]
        for path in paths:
            attrib = '@' in path
            if attrib:
                path, name = split_off_attrib(path)
            else:
                _, name = split_off_tag(path)
            remove.append(RemoveAction(name=name, path=path, attrib=attrib))

    new_keys = paths_target.keys() - paths_start.keys()
    create = []
    for key in new_keys:
        paths = paths_target[key]
        if not isinstance(paths, (list, UserList)):
            paths = [paths]
        for path in paths:
            attrib = '@' in path
            if attrib:
                path, name = split_off_attrib(path)
            else:
                _, name = split_off_tag(path)
            create.append(CreateAction(name=name, path=path, attrib=attrib))

    move = []
    ambiguous = []
    possible_change_keys = paths_start.keys() & paths_target.keys()
    for key in possible_change_keys:
        old_paths = paths_start[key]
        new_paths = paths_target[key]

        if old_paths == new_paths:
            continue

        if not isinstance(old_paths, (list, UserList)):
            old_paths = [old_paths]

        if not isinstance(new_paths, (list, UserList)):
            new_paths = [new_paths]

        old_paths = set(old_paths)
        new_paths = set(new_paths)

        different_paths = old_paths.symmetric_difference(new_paths)
        if len(different_paths) == 1:
            path = different_paths.pop()
            if path in old_paths:
                attrib = '@' in path
                if attrib:
                    path, name = split_off_attrib(path)
                else:
                    _, name = split_off_tag(path)
                remove.append(RemoveAction(name=name, path=path, attrib=attrib))
            else:
                attrib = '@' in path
                if attrib:
                    path, name = split_off_attrib(path)
                else:
                    _, name = split_off_tag(path)
                create.append(CreateAction(name=name, path=path, attrib=attrib))
        elif len(different_paths) == 2:
            if all(path in old_paths for path in different_paths):
                for path in different_paths:
                    attrib = '@' in path
                    if attrib:
                        path, name = split_off_attrib(path)
                    else:
                        _, name = split_off_tag(path)
                    remove.append(RemoveAction(name=name, path=path, attrib=attrib))
                continue
            if all(path in new_paths for path in different_paths):
                for path in different_paths:
                    attrib = '@' in path
                    if attrib:
                        path, name = split_off_attrib(path)
                    else:
                        _, name = split_off_tag(path)
                    create.append(CreateAction(name=name, path=path, attrib=attrib))
                continue
            first_path = different_paths.pop()
            attrib = '@' in first_path
            if attrib:
                first_path, first_name = split_off_attrib(first_path)
            else:
                _, first_name = split_off_tag(first_path)

            second_path = different_paths.pop()
            if attrib:
                second_path, second_name = split_off_attrib(second_path)
            else:
                _, second_name = split_off_tag(second_path)

            if first_path in old_paths:
                move.append(
                    MoveAction(old_name=first_name, old_path=first_path, new_name=second_name, new_path=second_path))
            else:
                move.append(
                    MoveAction(old_name=second_name, old_path=second_path, new_name=first_name, new_path=first_path))
        else:
            path = list(old_paths)[0]
            attrib = '@' in path
            if attrib:
                path, name = split_off_attrib(path)
            else:
                _, name = split_off_tag(path)
            ambiguous.append(
                AmbiguousAction(name=name, old_paths=tuple(old_paths), new_paths=tuple(new_paths), attrib=attrib))

    return remove, create, move, ambiguous


def resolve_ambiguouities(ambiguous,
                          remove,
                          create,
                          move,
                          remove_move=False,
                          tag_remove=None,
                          tag_move=None):

    for action in ambiguous.copy():

        ambiguous.remove(action)

        old_paths = set(action.old_paths)
        new_paths = set(action.new_paths)

        if tag_remove is None:
            tag_remove = remove
        for old_path in old_paths.copy():
            for action2 in tag_remove:
                if action2.path in old_path:
                    old_paths.discard(old_path)

        if remove_move:
            if tag_move is None:
                tag_move = move
            for old_path in old_paths.copy():
                for new_path in new_paths.copy():
                    for action_move in tag_move:
                        if old_path == new_path:
                            continue
                        if old_path.replace(action_move.old_path,'') == new_path.replace(action_move.new_path,''):
                            old_paths.discard(old_path)
                            new_paths.discard(new_path)

        if old_paths == new_paths:
            continue

        different_paths = old_paths.symmetric_difference(new_paths)

        if all(path in new_paths for path in different_paths):
            for path in new_paths:
                attrib = '@' in path
                if attrib:
                    path, name = split_off_attrib(path)
                else:
                    _, name = split_off_tag(path)
                create.append(CreateAction(name=name, path=path, attrib=attrib))
            continue

        if all(path in old_paths for path in different_paths):
            for path in new_paths:
                attrib = '@' in path
                if attrib:
                    path, name = split_off_attrib(path)
                else:
                    _, name = split_off_tag(path)
                remove.append(RemoveAction(name=name, path=path, attrib=attrib))
            continue

        if len(different_paths) == 1:
            path = different_paths.pop()
            if path in old_paths:
                attrib = '@' in path
                if attrib:
                    path, name = split_off_attrib(path)
                else:
                    _, name = split_off_tag(path)
                remove.append(RemoveAction(name=name, path=path, attrib=attrib))
            else:
                attrib = '@' in path
                if attrib:
                    path, name = split_off_attrib(path)
                else:
                    _, name = split_off_tag(path)
                create.append(CreateAction(name=name, path=path, attrib=attrib))
        elif len(different_paths) == 2:
            if all(path in old_paths for path in different_paths):
                for path in different_paths:
                    attrib = '@' in path
                    if attrib:
                        path, name = split_off_attrib(path)
                    else:
                        _, name = split_off_tag(path)
                    remove.append(RemoveAction(name=name, path=path, attrib=attrib))
                continue
            if all(path in new_paths for path in different_paths):
                for path in different_paths:
                    attrib = '@' in path
                    if attrib:
                        path, name = split_off_attrib(path)
                    else:
                        _, name = split_off_tag(path)
                    create.append(CreateAction(name=name, path=path, attrib=attrib))
                continue
            first_path = different_paths.pop()
            attrib = '@' in first_path
            if attrib:
                first_path, first_name = split_off_attrib(first_path)
            else:
                _, first_name = split_off_tag(first_path)

            second_path = different_paths.pop()
            if attrib:
                second_path, second_name = split_off_attrib(second_path)
            else:
                _, second_name = split_off_tag(second_path)
            if first_path in old_paths:
                move.append(
                    MoveAction(old_name=first_name, old_path=first_path, new_name=second_name, new_path=second_path))
            else:
                move.append(
                    MoveAction(old_name=second_name, old_path=second_path, new_name=first_name, new_path=first_path))
        else:
            ambiguous.append(
                AmbiguousAction(name=action.name,
                                old_paths=tuple(old_paths),
                                new_paths=tuple(new_paths),
                                attrib=action.attrib))


def trim_paths(paths):

    path_copy = paths.copy()
    for action in path_copy:
        for action2 in path_copy:
            if action == action2:
                continue
            if action.path in action2.path:
                if action2 in paths:
                    paths.remove(action2)

    return paths


def trim_attrib_paths(paths, tag_paths):

    path_copy = paths.copy()
    for tag_action in tag_paths:
        for attrib_action in path_copy:
            if tag_action.path in attrib_action.path:
                if attrib_action in paths:
                    paths.remove(attrib_action)

    return paths


def trim_move_paths(paths):

    path_copy = paths.copy()
    for action in path_copy:
        for action2 in path_copy:
            if action == action2:
                continue
            if action.old_path in action2.old_path:
                if action2.old_path.replace(action.old_path, '') == action2.new_path.replace(action.new_path, ''):
                    if action2 in paths:
                        paths.remove(action2)

    return paths


def trim_attrib_move_paths(paths, tag_paths):

    path_copy = paths.copy()
    for action in tag_paths:
        for action2 in path_copy:
            if action.old_path in action2.old_path:
                if action2.old_path.replace(action.old_path, '') == action2.new_path.replace(action.new_path, ''):
                    if action2 in paths:
                        paths.remove(action2)

    return paths


def remove_action(paths, name):

    matching = []
    for action in paths.copy():
        if action.name == name:
            paths.remove(action)
            matching.append(action)

    if not matching:
        raise ValueError(f'Action {name} not found')

    return matching


def load_conversion(from_version, to_version):
    """
    """
    filepath = FILE_DIRECTORY / f"conversion_{from_version.replace('.','')}_to_{to_version.replace('.','')}.json"

    with open(filepath, 'r', encoding='utf-8') as f:
        conversion = json.load(f)

    return conversion


@click.group('inpxml')
def inpxml():
    """
    """
    pass


@inpxml.command('convert')
@click.argument('xml-file', type=click.Path(exists=True))
@click.argument('to_version', type=str)
@click.pass_context
def convert_inpxml(ctx, xml_file, to_version):
    """
    """

    xmltree, schema_dict = load_inpxml(xml_file)
    schema_dict_target = InputSchemaDict.fromVersion(to_version)

    from_version = evaluate_attribute(xmltree, schema_dict, 'fleurInputVersion')

    try:
        conversion = load_conversion(from_version, to_version)
    except FileNotFoundError:
        echo.echo_warning(f'No conversion available between versions {from_version} to {to_version}')
        if click.confirm('Do you want to generate this conversion now'):
            conversion = ctx.invoke(generate_inp_conversion, from_version=from_version, to_version=to_version)
        else:
            echo.echo_critical('Cannot convert')

    set_attrib_value(xmltree, schema_dict_target, 'fleurInputVersion', to_version)
    for action in conversion['tag']['remove']:
        action = RemoveAction(*action)
        xml_delete_tag(xmltree, action.path)

    for action in conversion['attrib']['remove']:
        action = RemoveAction(*action)
        xml_delete_att(xmltree, action.path, action.name)

    for action in conversion['tag']['move']:
        if len(action) == 6:
            action = NormalizedMoveAction(*action)
        else:
            action = MoveAction(*action)

        if isinstance(action, NormalizedMoveAction):
            print(action.actual_path)
            nodes = eval_xpath(xmltree, action.actual_path, list_return=True)
            xml_delete_tag(xmltree, action.actual_path)
        else:
            nodes = eval_xpath(xmltree, action.old_path, list_return=True)
            xml_delete_tag(xmltree, action.old_path)
        for node in nodes:
            path, _ = split_off_tag(action.new_path)
            old_path, _ = split_off_tag(action.old_path)
            node.tag = action.new_name

            order = schema_dict['tag_info'][old_path]['order'].get_unlocked()
            order += schema_dict_target['tag_info'][path]['order'].get_unlocked()

            if not order:
                order = None

            #xml_create_tag cannot create subtags, but since we know that we have simple xpaths
            #we can do it here
            parent_nodes = eval_xpath(xmltree, path, list_return=True)
            to_create = []
            while not parent_nodes:
                parent_path, parent_name = split_off_tag(path)
                to_create.append((parent_path, parent_name))
                parent_nodes = eval_xpath(xmltree, parent_path, list_return=True)

            for parent_path, name in reversed(to_create):
                xml_create_tag(xmltree, parent_path, name)

            xml_create_tag(xmltree, path, node, tag_order=order)

    for action in conversion['tag']['create']:
        action = CreateAction(*action)
        if action.element is not None:
            path, _ = split_off_tag(action.path)
            order = schema_dict_target['tag_info'][path]['order'].get_unlocked()

            if not order:
                order = None

            #xml_create_tag cannot create subtags, but since we know that we have simple xpaths
            #we can do it here
            parent_nodes = eval_xpath(xmltree, path, list_return=True)
            to_create = []
            while not parent_nodes:
                parent_path, parent_name = split_off_tag(path)
                to_create.append((parent_path, parent_name))
                parent_nodes = eval_xpath(xmltree, parent_path, list_return=True)

            for parent_path, name in reversed(to_create):
                xml_create_tag(xmltree, parent_path, name)

            node = etree.fromstring(action.element)
            xml_create_tag(xmltree, path, node, tag_order=order)        


    print(etree.tostring(xmltree, encoding='unicode', pretty_print=True))

    try:
        validate_xml(xmltree,
                     schema_dict_target.xmlschema,
                     error_header='Input file does not validate against the schema')
    except etree.DocumentInvalid as err:
        echo.echo_critical(
            f'inp.xml conversion did not finish successfully. The resulting file violates the XML schema with:\n {err}')


@inpxml.command('generate-conversion')
@click.argument('from_version', type=str)
@click.argument('to_version', type=str)
def generate_inp_conversion(from_version, to_version):
    """
    """
    TAG_ENTRY = 'tag_paths'
    ATTRIB_ENTRIES = ['unique_attribs', 'unique_path_attribs', 'other_attribs']

    from_schema = InputSchemaDict.fromVersion(from_version)
    to_schema = InputSchemaDict.fromVersion(to_version)

    remove_tags, create_tags, move_tags, ambiguous_tags = analyse_paths(from_schema, to_schema, TAG_ENTRY)

    remove_tags = trim_paths(remove_tags)
    create_tags = trim_paths(create_tags)
    move_tags = trim_move_paths(move_tags)

    rename = True
    while remove_tags and create_tags and rename:
        click.echo('The following tags are not found in the target version:')
        click.echo(tabulate.tabulate(remove_tags, showindex=True))
        click.echo('The following tags are not found in the start version:')
        click.echo(tabulate.tabulate(create_tags, showindex=True))

        rename = click.confirm('Are there tags that were renamed?')

        if rename:
            old_name = click.prompt(f'Name in version {from_version}')
            new_name = click.prompt(f'Name in version {to_version}')

            remove = remove_action(remove_tags, old_name)
            create = remove_action(create_tags, new_name)

            if len(remove) != len(create):
                raise ValueError('Not supported')

            for old, new in zip(remove, create):
                move_tags.append(MoveAction(old_name=old.name, old_path=old.path, new_name=new.name, new_path=new.path))
            move_tags = trim_move_paths(move_tags)

    #Check again if we can now resolve ambiguouities
    resolve_ambiguouities(ambiguous_tags, remove_tags, create_tags, move_tags)
    remove_tags = trim_paths(remove_tags)
    create_tags = trim_paths(create_tags)
    move_tags = trim_move_paths(move_tags)

    remove_tags = sorted(remove_tags, key=lambda x: x.name)
    create_tags = sorted(create_tags, key=lambda x: x.name)
    move_tags = sorted(move_tags, key=lambda x: x.new_name)

    click.echo('The following tags will be moved:')
    click.echo(tabulate.tabulate(move_tags, showindex=True))

    while ambiguous_tags:
        click.echo('The following tags could not be resolved automatically:')
        click.echo(tabulate.tabulate(ambiguous_tags, showindex=True))

        row = click.prompt('Enter the row you want to clarify')

    #Make move_tags consistent
    for indx, action in enumerate(move_tags):
        #When the tag has been moved all paths afterward have to be adjusted
        if indx == len(move_tags) - 1:
            continue
        for indx_after, action_after in enumerate(move_tags[indx + 1:]):
            if action.old_path in action_after.old_path:
                action_after_new = NormalizedMoveAction(
                    old_name=action_after.old_name,
                    new_name=action_after.new_name,
                    old_path=action_after.old_path,
                    actual_path=action_after.old_path.replace(action.old_path, action.new_path),
                    new_path=action_after.new_path,
                )
                move_tags[indx_after + indx + 1] = action_after_new

    click.echo('The following tags will be moved (Paths normalized):')
    click.echo(tabulate.tabulate(move_tags, showindex=True))

    create = True
    while create_tags and create:
        click.echo('The following tags will be created:')
        click.echo(tabulate.tabulate(create_tags, showindex=True))

        create = click.confirm('Do you want to set a element to create?')

        if create:
            name = click.prompt('Enter the name of the tag to specify')
            create_action = remove_action(create_tags, name)

            if len(create_action) != 1:
                raise ValueError('Not implemented')
            create_action = create_action[0]

            _, name = split_off_tag(create_action.path)

            allowed_attribs = to_schema['tag_info'][create_action.path]['attribs']

            attribs = {}
            for attrib in allowed_attribs:
                if click.confirm(f'Do you want to set a value for attribute {attrib}?'):
                    attribs[attrib] = click.prompt(f'Value for {attrib}')
            
            elem = etree.tostring(etree.Element(name, **attribs), encoding='unicode', pretty_print=True)
            echo.echo_info(f"The following element will be created: {elem}")

            create_tags.append(create_action._replace(element=elem))

    create_tags = sorted(create_tags, key=lambda x: x.name)

    remove_attrib, create_attrib, move_attrib, ambiguous_attrib = analyse_paths(from_schema, to_schema, ATTRIB_ENTRIES)

    remove_attrib = trim_attrib_paths(remove_attrib, remove_tags)
    create_attrib = trim_attrib_paths(create_attrib, create_tags)
    move_attrib = trim_attrib_move_paths(move_attrib, move_tags)

    rename = True
    while remove_attrib and create_attrib and rename:
        click.echo('The following attribs are not found in the target version:')
        click.echo(tabulate.tabulate(remove_attrib, showindex=True))
        click.echo('The following attribs are not found in the start version:')
        click.echo(tabulate.tabulate(create_attrib, showindex=True))

        rename = click.confirm('Are there attribs that were renamed?')

        if rename:
            old_name = click.prompt(f'Name in version {from_version}')
            new_name = click.prompt(f'Name in version {to_version}')

            remove = remove_action(remove_attrib, old_name)
            create = remove_action(create_attrib, new_name)

            if len(remove) != len(create):
                raise ValueError('Not supported')

            for old, new in zip(remove, create):
                move_attrib.append(MoveAction(old_name=old.name, old_path=old.path, new_name=new.name, new_path=new.path))
            move_attrib = trim_move_paths(move_attrib)

    #Check again if we can now resolve ambiguouities
    resolve_ambiguouities(ambiguous_attrib,
                          remove_attrib,
                          create_attrib,
                          move_attrib,
                          remove_move=True,
                          tag_remove=remove_tags,
                          tag_move=move_tags)

    click.echo('The following attribs will be moved:')
    click.echo(tabulate.tabulate(move_attrib, showindex=True))

    while ambiguous_attrib:
        click.echo('The following attribs could not be resolved automatically:')
        click.echo(tabulate.tabulate(ambiguous_attrib, showindex=True))

        row = click.prompt('Enter the row you want to clarify', type=int)

        entry = ambiguous_attrib[row]

        click.echo(f'Entry {entry.name}:')

        old_paths = sorted(entry.old_paths)
        new_paths = sorted(entry.new_paths)

        while (new_paths or old_paths) and new_paths != old_paths:
            old_paths_display, new_paths_display = old_paths.copy(), new_paths.copy()
            if len(old_paths) < len(new_paths):
                old_paths_display += [None] * (len(new_paths) - len(old_paths))
            elif len(new_paths) < len(old_paths):
                new_paths_display += [None] * (len(old_paths) - len(new_paths))

            click.echo(tabulate.tabulate(list(zip(old_paths_display, new_paths_display)), showindex=True))

            action = click.prompt('Which action should be performed', type=click.Choice(['create', 'remove', 'move']))

            if action == 'remove':
                path_row = click.prompt('Enter the row you want to remove from the old paths', type=IntegerSlice())
                paths = old_paths[path_row]
                if not isinstance(paths, list):
                    paths = [paths]
                for path in paths:
                    old_paths.remove(path)
                    remove_attrib.append(RemoveAction(name=entry.name, path=path, attrib=entry.attrib))
            elif action == 'create':
                path_row = click.prompt('Enter the row you want to create from the new paths', type=IntegerSlice())
                paths = new_paths[path_row]
                if not isinstance(paths, list):
                    paths = [paths]
                for path in paths:
                    new_paths.remove(path)
                    create_attrib.append(CreateAction(name=entry.name, path=path, attrib=entry.attrib))
            elif action == 'move':
                old_path_row = click.prompt('Enter the row you want to remove from the old paths', type=int)
                new_path_row = click.prompt('Enter the row you want to remove from the new paths', type=int)
                old_path = old_paths.pop(old_path_row)
                new_path = new_paths.pop(new_path_row)
                move_attrib.append(
                    MoveAction(old_name=entry.name,
                               old_path=old_path,
                               new_name=entry.name,
                               new_path=new_path,
                               attrib=entry.attrib))

        click.echo('Ambiguouity successfully resolved')
        ambiguous_attrib.remove(entry)
    
    click.echo('The following attribs are removed:')
    click.echo(tabulate.tabulate(remove_attrib, showindex=True))
    click.echo('The following attribs are created:')
    click.echo(tabulate.tabulate(create_attrib, showindex=True))
    click.echo('The following attribs are moved:')
    click.echo(tabulate.tabulate(move_attrib, showindex=True))

    conversion = {
        'from': from_version,
        'to': to_version,
        'tag': {
            'remove': remove_tags,
            'create': create_tags,
            'move': move_tags
        },
        'attrib': {
            'remove': remove_attrib,
            'create': create_attrib,
            'move': move_attrib
        }
    }

    filepath = FILE_DIRECTORY / f"conversion_{from_version.replace('.','')}_to_{to_version.replace('.','')}.json"

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(conversion, f, indent=2)
    return conversion


@inpxml.command('show-conversion')
@click.argument('from_version', type=str)
@click.argument('to_version', type=str)
def show_inp_conversion(from_version, to_version):
    """
    """
    try:
        conversion = load_conversion(from_version, to_version)
    except FileNotFoundError:
        echo.echo_critical(f'No conversion available between versions {from_version} to {to_version}')

    echo.echo_dictionary(conversion)
