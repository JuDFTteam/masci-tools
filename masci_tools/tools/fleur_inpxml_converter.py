# -*- coding: utf-8 -*-

from masci_tools.io.parsers.fleur_schema import InputSchemaDict
from masci_tools.io.io_fleurxml import load_inpxml
from masci_tools.util.schema_dict_util import evaluate_attribute
from masci_tools.util.xml.xml_setters_basic import xml_delete_tag, xml_delete_att, xml_create_tag, _reorder_tags
from masci_tools.util.xml.xml_setters_names import set_attrib_value
from masci_tools.util.xml.common_functions import split_off_attrib, split_off_tag, eval_xpath, validate_xml
from masci_tools.cmdline.parameters.slice import IntegerSlice, ListElement
from masci_tools.cmdline.utils import echo
from collections import defaultdict
from typing import Iterable, List, NamedTuple, Tuple, Union
import tabulate
import json
from lxml import etree

import click
from pathlib import Path

FILE_DIRECTORY = Path(__file__).parent.resolve()


#These are the possible conversions that we can do
class MoveAction(NamedTuple):
    """
    NamedTuple representing the action of moving a tag/attribute to a different place.
    The name of this tag/attribute can also be changed
    """
    old_name: str
    new_name: str
    old_path: str
    new_path: str
    attrib: bool = False

    @classmethod
    def from_path(cls, old: str, new: str) -> 'MoveAction':
        """
        Construct a MoveAction from two given xpaths

        :param old: old str of the xpath
        :param new: new str of the xpath
        """

        attrib = '@' in old
        if attrib:
            old_path, old_name = split_off_attrib(old)
            new_path, new_name = split_off_attrib(old)
        else:
            old_path, new_path = old, new
            _, old_name = split_off_tag(old_path)
            _, new_name = split_off_tag(new_path)

        return cls(old_name=old_name, new_name=new_name, old_path=old_path, new_path=new_path, attrib=attrib)

    @classmethod
    def from_remove_and_create(cls, remove: 'RemoveAction', create: 'CreateAction') -> 'MoveAction':
        """
        Construct a MoveAction from a remove and create action, merging them together

        :param remove: RemoveAction to merge
        :param create: CreateAction to merge
        """

        if remove.attrib != create.attrib:
            raise ValueError('Inconsistent Remove/Create Actions')

        return cls(old_name=remove.name,
                   new_name=create.name,
                   old_path=remove.path,
                   new_path=create.path,
                   attrib=remove.attrib)


class NormalizedMoveAction(NamedTuple):
    """
    NamedTuple representing the action of moving a tag/attribute to a different place.
    The name of this tag/attribute can also be changed

    This MoveAction holds an additional attribute of an intermediate xpath to use, since the
    tag could not be in the expected starting position if other tags are moved beforehand
    """
    old_name: str
    new_name: str
    old_path: str
    new_path: str
    actual_path: str
    attrib: bool = False

    @classmethod
    def from_move(cls, move_action: MoveAction, actual_path: str) -> 'NormalizedMoveAction':
        """
        Construct a NormalizedMoveAction from a given move and the additional actual xpath to use

        :param move_action: MoveAction to construct the object from
        :param actual_path: str of the intermediate xpath to use as a starting point
        """

        return cls(**move_action._asdict(), actual_path=actual_path)


class AmbiguousAction(NamedTuple):
    """
    NamedTuple representing a change in paths that cannot be resolved automatically
    """
    name: str
    old_paths: Tuple[str]
    new_paths: Tuple[str]
    attrib: bool

    @classmethod
    def from_paths(cls, old: Iterable[str], new: Iterable[str]) -> 'AmbiguousAction':
        """
        Construct AmbiguousAction from given paths

        :param old: Iterable of the paths in the old version
        :param new: Iterable of paths in the new version
        """
        path = list(old)[0]
        attrib = '@' in path
        if attrib:
            _, name = split_off_attrib(path)
        else:
            _, name = split_off_tag(path)

        return cls(name=name, old_paths=tuple(old), new_paths=tuple(new), attrib=attrib)


class RemoveAction(NamedTuple):
    """
    NamedTuple representing the action of removing a tag/attribute from the xml tree
    """
    name: str
    path: str
    attrib: bool = False

    @classmethod
    def from_path(cls, xpath: str) -> 'RemoveAction':
        """
        Construct a RemoveAction from a given xpath

        :param xpath: str of the xpath
        """

        attrib = '@' in xpath
        if attrib:
            path, name = split_off_attrib(xpath)
        else:
            path = xpath
            _, name = split_off_tag(xpath)

        return cls(name=name, path=path, attrib=attrib)


class CreateAction(NamedTuple):
    """
    NamedTuple representing the action of creating a tag/attribute in the xml tree
    """
    name: str
    path: str
    attrib: bool = False
    element: str = None

    @classmethod
    def from_path(cls, xpath: str, element: str = None) -> 'RemoveAction':
        """
        Construct a CreateAction from a given xpath

        :param xpath: str of the xpath
        """

        attrib = '@' in xpath
        if attrib:
            path, name = split_off_attrib(xpath)
        else:
            path = xpath
            _, name = split_off_tag(xpath)

        return cls(name=name, path=path, attrib=attrib, element=element)


def analyse_paths(
    schema_start: 'InputSchemaDict', schema_target: 'InputSchemaDict', path_entries: Union[str, List[str]]
) -> Tuple[List[RemoveAction], List[CreateAction], List[MoveAction], List[AmbiguousAction]]:
    """
    Gather the initial path differences between the two given input schema dictionaries
    fro the given entries. If multiple enetries are given they are first merged together

    :param schema_start: InputSchemaDict to start from
    :param schema_start: InputSchemaDict to end up at
    :param path_entries: which entries of the schema dictionary should be analysed

    :returns: Tuple of List of Actions put into four categories (remove, create, move, ambiguous)
    """

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
        remove.extend(RemoveAction.from_path(path) for path in paths_start[key])

    new_keys = paths_target.keys() - paths_start.keys()
    create = []
    for key in new_keys:
        create.extend(CreateAction.from_path(path) for path in paths_target[key])

    move = []
    ambiguous = []
    possible_change_keys = paths_start.keys() & paths_target.keys()
    for key in possible_change_keys:
        old_paths = paths_start[key]
        new_paths = paths_target[key]

        if old_paths == new_paths:
            continue

        old_paths = set(old_paths)
        new_paths = set(new_paths)

        different_paths = old_paths.symmetric_difference(new_paths)
        if len(different_paths) == 1:
            path = different_paths.pop()
            if path in old_paths:
                remove.append(RemoveAction.from_path(path))
            else:
                create.append(CreateAction.from_path(path))
        elif len(different_paths) == 2:
            if all(path in old_paths for path in different_paths):
                remove.extend(RemoveAction.from_path(path) for path in different_paths)
                continue
            if all(path in new_paths for path in different_paths):
                create.extend(CreateAction.from_path(path) for path in different_paths)
                continue
            first_path = different_paths.pop()
            second_path = different_paths.pop()
            if first_path in old_paths:
                move.append(MoveAction.from_path(old=first_path, new=second_path))
            else:
                move.append(MoveAction.from_path(old=second_path, new=first_path))
        else:
            ambiguous.append(AmbiguousAction.from_paths(old=old_paths, new=new_paths))

    return remove, create, move, ambiguous


def resolve_ambiguouities(ambiguous, remove, create, move, remove_move=False, tag_remove=None, tag_move=None):

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
                        if old_path.replace(action_move.old_path, '') == new_path.replace(action_move.new_path, ''):
                            old_paths.discard(old_path)
                            new_paths.discard(new_path)

        if old_paths == new_paths:
            continue

        different_paths = old_paths.symmetric_difference(new_paths)

        if all(path in new_paths for path in different_paths):
            create.extend(CreateAction.from_path(path) for path in different_paths)
            continue

        if all(path in old_paths for path in different_paths):
            remove.extend(RemoveAction.from_path(path) for path in different_paths)
            continue

        if len(different_paths) == 1:
            path = different_paths.pop()
            if path in old_paths:
                remove.append(RemoveAction.from_path(path))
            else:
                create.append(CreateAction.from_path(path))
        elif len(different_paths) == 2:
            if all(path in old_paths for path in different_paths):
                remove.extend(RemoveAction.from_path(path) for path in different_paths)
                continue
            if all(path in new_paths for path in different_paths):
                create.extend(CreateAction.from_path(path) for path in different_paths)
                continue
            first_path = different_paths.pop()
            second_path = different_paths.pop()
            if first_path in old_paths:
                move.append(MoveAction.from_path(old=first_path, new=second_path))
            else:
                move.append(MoveAction.from_path(old=second_path, new=first_path))
        else:
            ambiguous.append(AmbiguousAction.from_paths(old=old_paths, new=new_paths))


def trim_path_actions(actions):
    pass


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


def _rename_elements(remove: List[RemoveAction], create: List[CreateAction], move: List[MoveAction], from_version: str,
                     to_version: str, name: str) -> None:
    """
    Get user input on tags that were renamed
    """

    remove = sorted(remove, key=lambda x: x.name)
    create = sorted(create, key=lambda x: x.name)

    rename = True
    while remove and create and rename:
        click.echo(f'The following {name} are not found in the target version:')
        click.echo(tabulate.tabulate(remove, showindex=True))
        click.echo(f'The following {name} are not found in the start version:')
        click.echo(tabulate.tabulate(create, showindex=True))

        rename = click.confirm(f'Are there {name} that were renamed?')

        if rename:
            old_name = click.prompt(f'Name in version {from_version}',
                                    type=click.Choice([action.name for action in remove], case_sensitive=False),
                                    show_choices=False)
            new_name = click.prompt(f'Name in version {to_version}',
                                    type=click.Choice([action.name for action in create], case_sensitive=False),
                                    show_choices=False)

            remove_list = remove_action(remove, old_name)
            create_list = remove_action(create, new_name)

            if len(remove_list) != len(create_list):
                raise ValueError('Not supported')
            move.extend(
                MoveAction.from_remove_and_create(remove, create) for remove, create in zip(remove_list, create_list))
            move = trim_move_paths(move)


def _create_tag_elements(create, to_schema):
    """
    Get user input on tags to create
    """
    create_prompt = True
    while create and create_prompt:
        click.echo('The following tags will be created:')
        click.echo(tabulate.tabulate(create, showindex=True))

        create_prompt = click.confirm('Do you want to set an element to create?')

        if create_prompt:
            name = click.prompt('Name of the element',
                                type=click.Choice([action.name for action in create], case_sensitive=False),
                                show_choices=False)
            create_action = remove_action(create, name)

            if len(create_action) != 1:
                raise ValueError('Not implemented')
            create_action = create_action[0]
            allowed_attribs = to_schema['tag_info'][create_action.path]['attribs']

            attribs = {}
            for attrib in allowed_attribs:
                value = click.prompt(f'Value for {attrib}', default=None)
                if value is not None:
                    attribs[attrib] = value

            elem = etree.tostring(etree.Element(create_action.name, **attribs), encoding='unicode', pretty_print=True)
            echo.echo_info(f'The following element will be created: {elem}')

            create.append(create_action._replace(element=elem))
        create = sorted(create, key=lambda x: x.name)
    return create


def _manual_resolution(ambiguous: List[AmbiguousAction], remove: List[RemoveAction], create: List[CreateAction],
                       move: List[MoveAction], name: str):
    """
    Prompt the user for input on actions that cannot be determined automagically
    """

    ambiguous = sorted(ambiguous, key=lambda x: x.name)

    while ambiguous:
        click.echo(f'The following {name} could not be resolved automatically:')
        click.echo(tabulate.tabulate(ambiguous, showindex=True))

        if len(ambiguous) > 1:
            name = click.prompt('Enter the name you want to clarify',
                                type=click.Choice([action.name for action in ambiguous], case_sensitive=False),
                                show_choices=False)

            entry = remove_action(ambiguous, name)

            if len(entry) != 1:
                raise NotImplementedError("It's broken :-(")
            entry = entry[0]
        else:
            entry = ambiguous.pop(0)

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

            action = click.prompt('Which action should be performed',
                                  type=click.Choice(['create', 'remove', 'move'], case_sensitive=False))
            if action == 'remove':
                paths = click.prompt('Enter the row you want to remove from the old paths',
                                     type=ListElement(old_paths, return_list=True))
                for path in paths:
                    remove.append(RemoveAction.from_path(path))
                    old_paths.remove(path)
            elif action == 'create':
                paths = click.prompt('Enter the row you want to create from the new paths',
                                     type=ListElement(new_paths, return_list=True))
                for path in paths:
                    create.append(CreateAction.from_path(path))
                    new_paths.remove(path)
            elif action == 'move':
                old_path_row = click.prompt('Enter the row you want to remove from the old paths', type=int)
                new_path_row = click.prompt('Enter the row you want to remove from the new paths', type=int)
                old_path = old_paths.pop(old_path_row)
                new_path = new_paths.pop(new_path_row)
                move.append(MoveAction.from_path(old=old_path, new=new_path))

        echo.echo_success('Ambiguouity successfully resolved')


def _xml_create_tag_with_parents(xmltree, xpath, node):
    """
    Create a tag at the given xpath together with it's parents if they are missing
    xml_create_tag cannot create subtags, but since we know that we have simple xpaths
    we can do it here

    No tag order is enforced here, since we are in intermediate steps

    :param xmltree: etree ElementTree to operate on
    :param xpath: xpath of the parent node
    :param node: node to create
    """

    parent_nodes = eval_xpath(xmltree, xpath, list_return=True)
    to_create = []
    while not parent_nodes:
        parent_path, parent_name = split_off_tag(xpath)
        to_create.append((parent_path, parent_name))
        parent_nodes = eval_xpath(xmltree, parent_path, list_return=True)

    for parent_path, name in reversed(to_create):
        xml_create_tag(xmltree, parent_path, name)

    xml_create_tag(xmltree, xpath, node)


def _reorder_tree(parent: etree._Element, schema_dict: InputSchemaDict, base_xpath: str = None) -> None:
    """
    Order the elements to be in the correct order for the given schema_dict
    """

    #Check if this is the first call to this routine
    if base_xpath is None:
        base_xpath = f'/{parent.tag}'

    for element in parent:
        new_base_xpath = f'{base_xpath}/{element.tag}'
        _reorder_tree(element, schema_dict, base_xpath=new_base_xpath)

    if base_xpath in schema_dict['tag_info']:
        order = schema_dict['tag_info'][base_xpath]['order']
    else:
        order = []

    if order:
        parent = _reorder_tags(parent, order)


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
            nodes = eval_xpath(xmltree, action.actual_path, list_return=True)
            xml_delete_tag(xmltree, action.actual_path)
        else:
            nodes = eval_xpath(xmltree, action.old_path, list_return=True)
            xml_delete_tag(xmltree, action.old_path)

        for node in nodes:
            path, _ = split_off_tag(action.new_path)
            node.tag = action.new_name
            #Order is not kept here (it is corrected at the end)
            _xml_create_tag_with_parents(xmltree, path, node)

    for action in conversion['tag']['create']:
        action = CreateAction(*action)
        if action.element is not None:
            path, _ = split_off_tag(action.path)
            node = etree.fromstring(action.element)
            _xml_create_tag_with_parents(xmltree, path, node)

    _reorder_tree(xmltree.getroot(), schema_dict_target)

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

    _rename_elements(remove_tags, create_tags, move_tags, from_version, to_version, 'tags')

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

    _manual_resolution(ambiguous_tags, remove_tags, create_tags, move_tags, 'tags')

    #Make move_tags consistent
    for indx, action in enumerate(move_tags):
        #When the tag has been moved all paths afterward have to be adjusted
        if indx == len(move_tags) - 1:
            continue
        for indx_after, action_after in enumerate(move_tags[indx + 1:]):
            if action.old_path in action_after.old_path:
                intermediate_path = action_after.old_path.replace(action.old_path, action.new_path)
                move_tags[indx_after + indx + 1] = NormalizedMoveAction.from_move(action_after,
                                                                                  actual_path=intermediate_path)

    click.echo('The following tags will be moved (Paths normalized):')
    click.echo(tabulate.tabulate(move_tags, showindex=True))

    create_tags = _create_tag_elements(create_tags, to_schema)

    remove_attrib, create_attrib, move_attrib, ambiguous_attrib = analyse_paths(from_schema, to_schema, ATTRIB_ENTRIES)

    remove_attrib = trim_attrib_paths(remove_attrib, remove_tags)
    create_attrib = trim_attrib_paths(create_attrib, create_tags)
    move_attrib = trim_attrib_move_paths(move_attrib, move_tags)

    _rename_elements(remove_attrib, create_attrib, move_attrib, from_version, to_version, 'attributes')

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

    _manual_resolution(ambiguous_attrib, remove_attrib, create_attrib, move_attrib, 'attributes')

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
        json.dump(conversion, f, indent=2, sort_keys=False)
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
