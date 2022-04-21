"""
This module implements a commandline tool available with ``masci-tools inpxml`` to
convert inp.xml files between different file versions
"""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable, NamedTuple, Sequence, TypeVar, cast
try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict
import json
from pathlib import Path
import os

from lxml import etree
import click
import tabulate

from masci_tools.io.parsers.fleur_schema import InputSchemaDict
from masci_tools.io.fleur_xml import load_inpxml
from masci_tools.util.schema_dict_util import evaluate_attribute, tag_exists
from masci_tools.util.typing import XMLLike, FileLike
from masci_tools.util.xml.xml_setters_basic import xml_delete_tag, xml_delete_att, xml_create_tag, _reorder_tags, xml_set_attrib_value_no_create
from masci_tools.util.xml.xml_setters_names import set_attrib_value
from masci_tools.util.xml.common_functions import split_off_attrib, split_off_tag, eval_xpath
from masci_tools.cmdline.parameters.slice import ListElement
from masci_tools.cmdline.utils import echo

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
    def from_path(cls, old: str, new: str) -> MoveAction:
        """
        Construct a MoveAction from two given xpaths

        :param old: old str of the xpath
        :param new: new str of the xpath
        """

        attrib = '@' in old
        if attrib:
            old_path, old_name = split_off_attrib(old)
            new_path, new_name = split_off_attrib(new)
        else:
            old_path, new_path = old, new
            _, old_name = split_off_tag(old_path)
            _, new_name = split_off_tag(new_path)

        return cls(old_name=old_name, new_name=new_name, old_path=old_path, new_path=new_path, attrib=attrib)

    @classmethod
    def from_remove_and_create(cls, remove: RemoveAction, create: CreateAction) -> MoveAction:
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
    def from_move(cls, move_action: MoveAction, actual_path: str) -> NormalizedMoveAction:
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
    old_paths: tuple[str, ...]
    new_paths: tuple[str, ...]
    attrib: bool

    @classmethod
    def from_paths(cls, old: Iterable[str], new: Iterable[str]) -> AmbiguousAction:
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
    warning: str = ''
    attrib: bool = False

    @classmethod
    def from_path(cls, xpath: str) -> RemoveAction:
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
    element: str | None = None

    @classmethod
    def from_path(cls, xpath: str, element: str | None = None) -> CreateAction:
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


SimpleAction = TypeVar('SimpleAction', CreateAction, RemoveAction)
NamedAction = TypeVar('NamedAction', CreateAction, RemoveAction, AmbiguousAction)


class Actions(TypedDict):
    remove: list[RemoveAction]
    create: list[CreateAction]
    move: list[MoveAction | NormalizedMoveAction]


class FileConversion(TypedDict, total=False):
    from_version: str
    to_version: str
    tag: Actions
    attrib: Actions


def analyse_paths(
    schema_start: InputSchemaDict, schema_target: InputSchemaDict, path_entries: str | list[str]
) -> tuple[list[RemoveAction], list[CreateAction], list[MoveAction], list[AmbiguousAction]]:
    """
    Gather the initial path differences between the two given input schema dictionaries
    for the given entries. If multiple enetries are given they are first merged together

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
    remove: list[RemoveAction] = []
    for key in removed_keys:
        remove.extend(RemoveAction.from_path(path) for path in paths_start[key])

    new_keys = paths_target.keys() - paths_start.keys()
    create: list[CreateAction] = []
    for key in new_keys:
        create.extend(CreateAction.from_path(path) for path in paths_target[key])

    move = []
    ambiguous = []
    possible_change_keys = paths_start.keys() & paths_target.keys()
    for key in possible_change_keys:
        if paths_start[key] == paths_target[key]:
            continue

        old_paths = set(paths_start[key])
        new_paths = set(paths_target[key])

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


def resolve_ambiguouities(ambiguous: list[AmbiguousAction],
                          remove: list[RemoveAction],
                          create: list[CreateAction],
                          move: list[MoveAction],
                          remove_move: bool = False,
                          tag_remove: list[RemoveAction] | None = None,
                          tag_move: list[MoveAction] | None = None) -> None:
    """
    Try to resolve ambuouities by using additional information from moved/created removed tags/attributes
    """

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


def trim_paths(paths: list[SimpleAction]) -> list[SimpleAction]:

    path_copy = paths.copy()
    for action in path_copy:
        for action2 in path_copy:
            if action == action2:
                continue
            if action.path in action2.path:
                if action2 in paths:
                    paths.remove(action2)

    return paths


def trim_attrib_paths(paths: list[SimpleAction], tag_paths: list[SimpleAction]) -> list[SimpleAction]:

    path_copy = paths.copy()
    for tag_action in tag_paths:
        for attrib_action in path_copy:
            if tag_action.path in attrib_action.path:
                if attrib_action in paths:
                    paths.remove(attrib_action)

    return paths


def trim_move_paths(paths: list[MoveAction]) -> list[MoveAction]:

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


def trim_attrib_move_paths(paths: list[MoveAction], tag_paths: list[MoveAction]) -> list[MoveAction]:

    path_copy = paths.copy()
    for action in tag_paths:
        for action2 in path_copy:
            if action.old_path in action2.old_path:
                if action2.old_path.replace(action.old_path, '') == action2.new_path.replace(action.new_path, ''):
                    if action2 in paths:
                        paths.remove(action2)

    return paths


def remove_action(actions: list[NamedAction], name: str) -> list[NamedAction]:
    """
    Find all the occurrences of actions with a given name and return them and remove them from the list

    :param actions: List of actions
    :param name: str name to find

    :returns: List of actions matching the given name
    """

    matching = [action for action in actions if action.name == name]
    for action in matching:
        actions.remove(action)

    if not matching:
        raise ValueError(f'Action {name} not found')

    return matching


def echo_actions(actions: Sequence[NamedTuple], ignore: Iterable[str] | None = None, header: str = '') -> None:
    """
    Echo a list of actions in a nicely formatted list

    :param actions: list of actions to show
    :param ignore: Iterable of str with attributes to ignore in the table
    :param header: str optional Title for the table
    """

    if ignore is None:
        ignore = {'attrib'}

    actions_dict = [action._asdict() for action in actions]

    if ignore:
        for action in actions_dict:
            for key in ignore:
                action.pop(key, None)

    click.echo(header)
    if any(isinstance(action, AmbiguousAction) for action in actions):
        first = True
        for action in actions_dict:
            old_length = len(action['old_paths'])
            new_length = len(action['new_paths'])
            if old_length < new_length:
                action['old_paths'] += (None,) * (new_length - old_length)
            elif new_length < old_length:
                action['new_paths'] += (None,) * (old_length - new_length)
            if 'name' in action:
                action['name'] = [action['name']] + [None] * max(new_length, old_length)
            if first:
                click.echo(tabulate.tabulate(action, headers=['Name', 'Old paths', 'New paths']))
                first = False
            else:
                click.echo(tabulate.tabulate(action))
    else:
        click.echo(tabulate.tabulate(actions_dict, showindex=True, headers='keys'))
    click.echo()


def load_conversion(from_version: str, to_version: str) -> FileConversion:
    """
    Load the conversion between the given versions from a stored json file

    :param from_version: str of the initial version
    :param to_version: str of the final version

    :returns: a dict with the actions to perform
    """
    filepath = FILE_DIRECTORY / 'conversions' / f"conversion_{from_version.replace('.','')}_to_{to_version.replace('.','')}.json"

    with open(filepath, encoding='utf-8') as f:
        conversion: FileConversion = json.load(f)

    #convert back to the namedtuples
    conversion['tag']['create'] = [CreateAction(*action) for action in conversion['tag']['create']]
    conversion['tag']['remove'] = [RemoveAction(*action) for action in conversion['tag']['remove']]
    move: list[MoveAction | NormalizedMoveAction] = []
    for action in conversion['tag']['move']:
        if len(action) == 6:
            move.append(NormalizedMoveAction(*action))
        else:
            move.append(MoveAction(*action))
    conversion['tag']['move'] = move

    conversion['attrib']['create'] = [CreateAction(*action) for action in conversion['attrib']['create']]
    conversion['attrib']['remove'] = [RemoveAction(*action) for action in conversion['attrib']['remove']]
    move = []
    for action in conversion['attrib']['move']:
        if len(action) == 6:
            move.append(NormalizedMoveAction(*action))
        else:
            move.append(MoveAction(*action))
    conversion['attrib']['move'] = move

    return conversion


def dump_conversion(conversion: FileConversion) -> None:
    """
    Save the given conversion as a json file in the conversions subfolder

    :param conversion: dict representing the conversion
    """

    filepath = FILE_DIRECTORY / 'conversions' / f"conversion_{conversion['from_version'].replace('.','')}_to_{conversion['to_version'].replace('.','')}.json"
    os.makedirs(filepath.parent, exist_ok=True)

    #Drop all create actions, which have no element set
    conversion['tag']['create'] = [action for action in conversion['tag']['create'] if action.element is not None]
    conversion['attrib']['create'] = [action for action in conversion['attrib']['create'] if action.element is not None]

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(conversion, f, indent=2, sort_keys=False)


def _rename_elements(remove: list[RemoveAction], create: list[CreateAction], move: list[MoveAction], from_version: str,
                     to_version: str, name: str) -> tuple[list[RemoveAction], list[CreateAction], list[MoveAction]]:
    """
    Get user input on tags that were renamed
    """

    remove = sorted(remove, key=lambda x: x.name)
    create = sorted(create, key=lambda x: x.name)

    rename = True
    while remove and create and rename:
        echo_actions(remove,
                     header=f'The following {name} are not found in the target version:',
                     ignore={'attrib', 'warning'})
        echo_actions(create,
                     header=f'The following {name} are not found in the start version:',
                     ignore={'attrib', 'element'})

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
    return remove, create, move


def _create_tag_elements(create: list[CreateAction], to_schema: InputSchemaDict) -> list[CreateAction]:
    """
    Get user input on tags to create
    """
    create_prompt = True
    while create and create_prompt:
        echo_actions(create, header='The following tags will be created:')

        create_prompt = click.confirm('Do you want to set an element to create?')

        if create_prompt:
            name = click.prompt('Name of the element',
                                type=click.Choice([action.name for action in create], case_sensitive=False),
                                show_choices=False)
            create_actions = remove_action(create, name)

            if len(create_actions) != 1:
                raise ValueError('Not implemented')
            create_action = create_actions[0]
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


def _add_warnings_on_remove(remove: list[RemoveAction], name: str) -> list[RemoveAction]:
    """
    Get user input on warnings to show
    """
    warning_prompt = True
    while remove and warning_prompt:
        echo_actions(remove, header=f'The following {name} will be removed:')

        warning_prompt = click.confirm(f'Do you want to add a warning if a {name} is removed?')

        if warning_prompt:
            elem_name = click.prompt('Name of the element',
                                     type=click.Choice([action.name for action in remove], case_sensitive=False),
                                     show_choices=False)
            remove_list = remove_action(remove, elem_name)
            while click.confirm('Do you want to enter another element?', default=False):
                elem_name = click.prompt('Name of the element',
                                         type=click.Choice([action.name for action in remove], case_sensitive=False),
                                         show_choices=False)
                remove_list += remove_action(remove, elem_name)

            warning = click.prompt('Enter the warning message', type=click.types.StringParamType())
            remove.extend(action._replace(warning=warning) for action in remove_list)
        remove = sorted(remove, key=lambda x: x.name)
    return remove


def _create_attrib_elements(create: list[CreateAction], to_schema: InputSchemaDict) -> list[CreateAction]:
    """
    Get user input on attributes to create
    """
    create_prompt = True
    while create and create_prompt:
        echo_actions(create, header='The following attributes will be created:')

        create_prompt = click.confirm('Do you want to set a value for a given attribute?')

        if create_prompt:
            name = click.prompt('Name of the attribute',
                                type=click.Choice([action.name for action in create], case_sensitive=False),
                                show_choices=False)
            create_actions = remove_action(create, name)

            if len(create_actions) != 1:
                raise ValueError('Not implemented')
            create_action = create_actions[0]
            default = to_schema['tag_info'][create_action.path]['optional_attribs'].get(create_action.name)
            if default is not None:
                default = str(default)

            value = click.prompt(f'Value for {create_action.name}', default=default)
            if value is not None:
                create.append(create_action._replace(element=value))
        create = sorted(create, key=lambda x: x.name)
    return create


def _manual_resolution(ambiguous: list[AmbiguousAction], remove: list[RemoveAction], create: list[CreateAction],
                       move: list[MoveAction],
                       name: str) -> tuple[list[RemoveAction], list[CreateAction], list[MoveAction]]:
    """
    Prompt the user for input on actions that cannot be determined automagically
    """

    ambiguous = sorted(ambiguous, key=lambda x: x.name)

    while ambiguous:
        echo_actions(ambiguous, header=f'The following {name} could not be resolved automatically:')

        if len(ambiguous) > 1:
            name = click.prompt('Enter the name you want to clarify',
                                type=click.Choice([action.name for action in ambiguous], case_sensitive=False),
                                show_choices=False)

            entries = remove_action(ambiguous, name)

            if len(entries) != 1:
                raise NotImplementedError("It's broken :-(")
            entry = entries[0]
        else:
            entry = ambiguous.pop(0)

        click.echo(f'Entry {entry.name}:')

        old_paths = sorted(entry.old_paths)
        new_paths = sorted(entry.new_paths)

        while (new_paths or old_paths) and new_paths != old_paths:
            old_paths_display, new_paths_display = old_paths.copy(), new_paths.copy()
            if len(old_paths) < len(new_paths):
                old_paths_display += [None] * (len(new_paths) - len(old_paths))  #type:ignore
            elif len(new_paths) < len(old_paths):
                new_paths_display += [None] * (len(old_paths) - len(new_paths))  #type:ignore

            click.echo(
                tabulate.tabulate(list(zip(old_paths_display, new_paths_display)),
                                  showindex=True,
                                  headers=['Old Paths', 'New Paths']))

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
                old_path_row = click.prompt('Enter the row you want to remove from the old paths',
                                            type=click.types.IntParamType())
                new_path_row = click.prompt('Enter the row you want to remove from the new paths',
                                            type=click.types.IntParamType())
                old_path = old_paths.pop(old_path_row)
                new_path = new_paths.pop(new_path_row)
                move.append(MoveAction.from_path(old=old_path, new=new_path))

        echo.echo_success('Ambiguouity successfully resolved')
    return remove, create, move


def _xml_create_tag_with_parents(xmltree: XMLLike, xpath: str, node: etree._Element) -> None:
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


def _xml_delete_attribute_with_warnings(xmltree: XMLLike, xpath: str, name: str, warning: str = '') -> None:
    """
    Delete the attribute at the given xpath with the given name and show a warning if one is given

    :param xmltree: etree ElementTree to operate on
    :param xpath: xpath of the parent node
    :param name: name of the attribute
    :param warning: str of the warning to show in case there are nodes that are removed
    """
    values = eval_xpath(xmltree, f'{xpath}/@{name}', list_return=True)
    if values:
        if warning:
            echo.echo_warning(warning)
        xml_delete_att(xmltree, xpath, name)


def _xml_delete_tag_with_warnings(xmltree: XMLLike, xpath: str, warning: str = '') -> None:
    """
    Delete the tag at the given xpath and show a warning if one is given

    :param xmltree: etree ElementTree to operate on
    :param xpath: xpath of the node
    :param warning: str of the warning to show in case there are nodes that are removed
    """
    nodes = eval_xpath(xmltree, xpath, list_return=True)
    if nodes:
        if warning:
            echo.echo_warning(warning)
        xml_delete_tag(xmltree, xpath)


def _reorder_tree(parent: etree._Element, schema_dict: InputSchemaDict, base_xpath: str | None = None) -> None:
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


def convert_inpxml(xmltree: etree._ElementTree, schema_dict: InputSchemaDict, to_version: str) -> etree._ElementTree:
    """
    Convert the given xmltree to the given file version

    :param xmltree: XML tree to convert
    :param schema_dict: SchemaDict corresponding to the original file version
    :param to_version: file version to which to convert

    :returns: the XML tree converted to the given file version
    """
    schema_dict_target = InputSchemaDict.fromVersion(to_version)

    #We want to leave comments in so we cannot use clear_xml for the xinclude feature
    #Here we just include and write out the complete xml file
    xmltree.xinclude()
    from_version = evaluate_attribute(xmltree, schema_dict, 'fleurInputVersion')

    conversion = load_conversion(from_version, to_version)

    set_attrib_value(xmltree, schema_dict_target, 'fleurInputVersion', to_version)

    action: MoveAction | RemoveAction | CreateAction | NormalizedMoveAction
    #Collect the nodes to be moved
    move_tags: list[list[etree._Element]] = []
    for action in conversion['tag']['move']:
        move_tags.append(eval_xpath(xmltree, action.old_path, list_return=True))  #type: ignore

    #Collect the attributes to be moved
    move_attribs = []
    for action in conversion['attrib']['move']:
        move_attribs.append(eval_xpath(xmltree, f'{action.old_path}/@{action.old_name}', list_return=True))

    for action in conversion['tag']['remove']:
        _xml_delete_tag_with_warnings(xmltree, action.path, warning=action.warning)

    for action in conversion['attrib']['remove']:
        _xml_delete_attribute_with_warnings(xmltree, action.path, action.name, warning=action.warning)

    for action, nodes in zip(conversion['tag']['move'], move_tags):
        if isinstance(action, NormalizedMoveAction):
            path = action.actual_path
        else:
            path = action.old_path

        if eval_xpath(xmltree, path, list_return=True):
            xml_delete_tag(xmltree, path)

        for node in nodes:
            path, _ = split_off_tag(action.new_path)
            node.tag = action.new_name
            #Order is not kept here (it is corrected at the end)
            _xml_create_tag_with_parents(xmltree, path, node)

    for action in conversion['tag']['create']:
        if action.element is not None:
            path, _ = split_off_tag(action.path)
            node = etree.fromstring(action.element)
            _xml_create_tag_with_parents(xmltree, path, node)

    for action, values in zip(conversion['attrib']['move'], move_attribs):
        if isinstance(action, NormalizedMoveAction):
            path = action.actual_path
        else:
            path = action.old_path

        if eval_xpath(xmltree, f'{path}/@{action.old_name}', list_return=True):
            xml_delete_att(xmltree, path, action.old_name)
        if values:
            nodes: list[etree._Element] = eval_xpath(xmltree, action.new_path, list_return=True)  #type: ignore
            if nodes:
                xml_set_attrib_value_no_create(xmltree, action.new_path, action.new_name, values)

    for action in conversion['attrib']['create']:
        if action.element is not None:
            nodes: list[etree._Element] = eval_xpath(xmltree, action.path, list_return=True)  #type: ignore
            if nodes:
                xml_set_attrib_value_no_create(xmltree, action.path, action.name, action.element)

    _reorder_tree(xmltree.getroot(), schema_dict_target)
    schema_dict_target.validate(xmltree)

    #If there was no relax.xml included we need to rewrite the xinclude tag for it
    INCLUDE_NSMAP = {'xi': 'http://www.w3.org/2001/XInclude'}
    INCLUDE_TAG = etree.QName(INCLUDE_NSMAP['xi'], 'include')
    FALLBACK_TAG = etree.QName(INCLUDE_NSMAP['xi'], 'fallback')
    if not tag_exists(xmltree, schema_dict_target, 'relaxation'):
        xinclude_elem = etree.Element(INCLUDE_TAG, href='relax.xml', nsmap=INCLUDE_NSMAP)
        xinclude_elem.append(etree.Element(FALLBACK_TAG))
        xmltree.getroot().append(xinclude_elem)

    etree.indent(xmltree)
    return xmltree


@click.group('inpxml')
def inpxml():
    """
    Tool for converting inp.xml files to different versions
    """


@inpxml.command('convert')
@click.argument('xml-file', type=click.Path(exists=True))
@click.argument('to_version', type=str)
@click.option('--output-file', '-o', type=str, default='inp.xml', help='Name of the output file')
@click.option('--overwrite', is_flag=True, help='If the flag is given and the file already exists it is overwritten')
@click.pass_context
def cmd_convert_inpxml(ctx: click.Context, xml_file: FileLike, to_version: str, output_file: str,
                       overwrite: bool) -> None:
    """
    Convert the given XML_FILE file to version TO_VERSION

    XML_FILE is the file to convert
    TO_VERSION is the file version of the finale input file
    """
    xmltree, schema_dict = load_inpxml(xml_file)
    from_version = evaluate_attribute(xmltree, schema_dict, 'fleurInputVersion')

    try:
        load_conversion(from_version, to_version)
    except FileNotFoundError:
        echo.echo_warning(f'No conversion available between versions {from_version} to {to_version}')
        if click.confirm('Do you want to generate this conversion now'):
            ctx.invoke(generate_inp_conversion, from_version=from_version, to_version=to_version)
        else:
            echo.echo_critical('Cannot convert')

    if Path(output_file).is_file():
        if not overwrite:
            echo.echo_critical(f'The output file {output_file} already exists. Use the overwrite flag to ignore')
        echo.echo_warning(f'The output file {output_file} already exists. Will be overwritten')

    try:
        convert_inpxml(xmltree, schema_dict, to_version)
        echo.echo_success('The conversion was successful')
        echo.echo_info(
            'It is not guaranteed that a FLEUR calculation will behave in the exact same way as the old input file\n'
            'Please check the file for correctness beforehand')
    except etree.DocumentInvalid as err:
        echo.echo_critical(
            f'inp.xml conversion did not finish successfully. The resulting file violates the XML schema with:\n {err}')

    xmltree.write(output_file, encoding='utf-8', pretty_print=True)
    echo.echo_success(f'Converted file written to {output_file}')


@inpxml.command('generate-conversion')
@click.argument('from_version', type=str)
@click.argument('to_version', type=str)
@click.option('--show/--no-show', default=True, help='Show a summary of the conversion at the end')
@click.pass_context
def generate_inp_conversion(ctx: click.Context, from_version: str, to_version: str, show: bool) -> FileConversion:
    """
    Generate the conversions from FROM_VERSION to TO_VERSION

    FROM_VERSION is the file version of the initial input file
    TO_VERSION is the file version of the finale input file
    """
    TAG_ENTRY = 'tag_paths'
    ATTRIB_ENTRIES = ['unique_attribs', 'unique_path_attribs', 'other_attribs']

    from_schema = InputSchemaDict.fromVersion(from_version)
    to_schema = InputSchemaDict.fromVersion(to_version)

    remove_tags, create_tags, move_tags, ambiguous_tags = analyse_paths(from_schema, to_schema, TAG_ENTRY)

    remove_tags = trim_paths(remove_tags)
    create_tags = trim_paths(create_tags)
    move_tags = trim_move_paths(move_tags)

    remove_tags, create_tags, move_tags = _rename_elements(remove_tags, create_tags, move_tags, from_version,
                                                           to_version, 'tags')

    #Check again if we can now resolve ambiguouities
    resolve_ambiguouities(ambiguous_tags, remove_tags, create_tags, move_tags)
    remove_tags = trim_paths(remove_tags)
    create_tags = trim_paths(create_tags)
    move_tags = trim_move_paths(move_tags)

    remove_tags = sorted(remove_tags, key=lambda x: x.name)
    create_tags = sorted(create_tags, key=lambda x: x.name)
    move_tags = sorted(move_tags, key=lambda x: x.new_name)

    remove_tags, create_tags, move_tags = _manual_resolution(ambiguous_tags, remove_tags, create_tags, move_tags,
                                                             'tags')

    remove_tags = sorted(remove_tags, key=lambda x: x.name)
    create_tags = sorted(create_tags, key=lambda x: x.name)
    move_tags = sorted(move_tags, key=lambda x: x.new_name)

    #Make move_tags consistent
    for indx, action in enumerate(move_tags):
        #When the tag has been moved all paths afterward have to be adjusted
        if indx == len(move_tags) - 1:
            continue
        for indx_after, action_after in enumerate(move_tags[indx + 1:]):
            if action.old_path in action_after.old_path:
                intermediate_path = action_after.old_path.replace(action.old_path, action.new_path)
                #yapf:disable
                move_tags[indx_after + indx + 1] = NormalizedMoveAction.from_move(action_after, actual_path=intermediate_path)  #type:ignore
                #yapf:enable

    create_tags = _create_tag_elements(create_tags, to_schema)
    remove_tags = _add_warnings_on_remove(remove_tags, 'tags')

    remove_attrib, create_attrib, move_attrib, ambiguous_attrib = analyse_paths(from_schema, to_schema, ATTRIB_ENTRIES)

    remove_attrib = trim_attrib_paths(remove_attrib, remove_tags)
    create_attrib = trim_attrib_paths(create_attrib, create_tags)
    move_attrib = trim_attrib_move_paths(move_attrib, move_tags)

    remove_attrib = sorted(remove_attrib, key=lambda x: x.name)
    create_attrib = sorted(create_attrib, key=lambda x: x.name)
    move_attrib = sorted(move_attrib, key=lambda x: x.new_name)

    remove_attrib, create_attrib, move_attrib = _rename_elements(remove_attrib, create_attrib, move_attrib,
                                                                 from_version, to_version, 'attributes')

    remove_attrib = sorted(remove_attrib, key=lambda x: x.name)
    create_attrib = sorted(create_attrib, key=lambda x: x.name)
    move_attrib = sorted(move_attrib, key=lambda x: x.new_name)

    #Check again if we can now resolve ambiguouities
    resolve_ambiguouities(ambiguous_attrib,
                          remove_attrib,
                          create_attrib,
                          move_attrib,
                          remove_move=True,
                          tag_remove=remove_tags,
                          tag_move=move_tags)

    remove_attrib, create_attrib, move_attrib = _manual_resolution(ambiguous_attrib, remove_attrib, create_attrib,
                                                                   move_attrib, 'attributes')

    create_attrib = _create_attrib_elements(create_attrib, to_schema)
    remove_attrib = _add_warnings_on_remove(remove_attrib, 'attributes')

    conversion = FileConversion({
        'from_version': from_version,
        'to_version': to_version,
        'tag': {
            'remove': remove_tags,
            'create': create_tags,
            'move': cast('list[MoveAction| NormalizedMoveAction]', move_tags)
        },
        'attrib': {
            'remove': remove_attrib,
            'create': create_attrib,
            'move': cast('list[MoveAction| NormalizedMoveAction]', move_attrib)
        }
    })

    dump_conversion(conversion)

    if show:
        ctx.invoke(show_inp_conversion, from_version=from_version, to_version=to_version)

    return conversion


@inpxml.command('show-conversion')
@click.argument('from_version', type=str)
@click.argument('to_version', type=str)
def show_inp_conversion(from_version: str, to_version: str) -> None:
    """
    Show the actions for an already created conversion from FROM_VERSION to TO_VERSION

    FROM_VERSION is the file version of the initial input file
    TO_VERSION is the file version of the finale input file
    """
    try:
        conversion = load_conversion(from_version, to_version)
    except FileNotFoundError:
        echo.echo_critical(f'No conversion available between versions {from_version} to {to_version}')

    echo.echo_info(f'Actions performed for transforming from version {from_version} to {to_version}')
    echo_actions(conversion['tag']['remove'], header='The following tags are removed:')
    echo_actions(conversion['tag']['create'], header='The following tags are created:')
    echo_actions(conversion['tag']['move'], header='The following tags are moved:', ignore={'attrib', 'actual_path'})
    echo_actions(conversion['attrib']['remove'], header='The following attributes are removed:')
    echo_actions(conversion['attrib']['create'], header='The following attributes are created:')
    echo_actions(conversion['attrib']['move'],
                 header='The following attributes are moved:',
                 ignore={'attrib', 'actual_path'})
