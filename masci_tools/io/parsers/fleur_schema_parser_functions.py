"""
functions to extract information about the fleur schema into a python dict
"""
from lxml import etree
from pprint import pprint
import os
import importlib.util
def remove_xsd_namespace(tag,namespaces):
    try:
        return tag.replace(f"{'{'}{namespaces['xsd']}{'}'}","")
    except:
        return None

def get_parent_fleur_type(elem,namespaces,stop_sequence=False):
    """
    Returns the parent simple or complexType to the given element
    If stop_sequence is given and True None is returned when a sequence is encountered
    in the parent chain

    """
    fleur_types = ['simpleType','complexType']
    parent = elem.getparent()
    parent_type = remove_xsd_namespace(parent.tag,namespaces)
    while parent_type not in fleur_types:
        if parent_type == 'sequence' and stop_sequence:
            return None
        parent = parent.getparent()
        parent_type = remove_xsd_namespace(parent.tag,namespaces)
    return parent


def get_xpath(xmlschema,namespaces,tag_name,contains=None,enforce_end_type=None,stop_non_unique=False):
    """
    construct all possible simple xpaths to a given tag
    """

    possible_paths = []

    root_tag = 'fleurInput'
    if tag_name == root_tag:
        return f'/{root_tag}'

    #Get all possible starting points
    if enforce_end_type is None:
        startPoints = xmlschema.xpath(f"//xsd:element[@name='{tag_name}']", namespaces=namespaces)
    else:
        startPoints = xmlschema.xpath(f"//xsd:element[@name='{tag_name}' and @type='{enforce_end_type}']", namespaces=namespaces)
    for elem in startPoints:
        currentelem = elem
        currentTag = tag_name
        parent_type = get_parent_fleur_type(currentelem,namespaces)
        next_type = parent_type.attrib['name']
        if stop_non_unique:
            currentelem = xmlschema.xpath(f"//xsd:element[@type='{next_type}' and @maxOccurs=1] | //xsd:element[@type='{next_type}' and not(@maxOccurs)]", namespaces=namespaces)
        else:
            currentelem = xmlschema.xpath(f"//xsd:element[@type='{next_type}']", namespaces=namespaces)
        
        if len(currentelem) == 0:
            return None
        
        for new_elem in currentelem:
            newTag = new_elem.attrib['name']
            possible_paths_tag = get_xpath(xmlschema,namespaces,newTag,enforce_end_type=next_type)
        if not isinstance(possible_paths_tag,list):
            possible_paths_tag = [possible_paths_tag]
        for tagpath in possible_paths_tag:
            possible_paths.append(f'{tagpath}/{tag_name}')
    
    #Remove paths that do not meet the requirement from contains
    if contains is not None:
        possible_paths_copy = possible_paths.copy()
        for xpath in possible_paths_copy:
            if contains not in xpath:
                possible_paths.remove(xpath)
    
    if len(possible_paths) > 1:
        return possible_paths
    elif len(possible_paths) == 0:
        raise ValueError(f'Found no path to tag {tag_name}')
    else:
        return possible_paths[0]

def get_attrib_xpath(xmlschema,namespaces,attrib_name,stop_non_unique=False):

    possible_paths = []
    attribute_tags = xmlschema.xpath(f"//xsd:attribute[@name='{attrib_name}']", namespaces=namespaces)
    for attrib in attribute_tags:
        attrib_type = get_parent_fleur_type(attrib,namespaces).attrib['name']
        if stop_non_unique:
            element_tags = xmlschema.xpath(f"//xsd:element[@type='{attrib_type}' and @maxOccurs=1]/@name | //xsd:element[@type='{attrib_type}' and not(@maxOccurs)]/@name", namespaces=namespaces)
        else:
            element_tags = xmlschema.xpath(f"//xsd:element[@type='{attrib_type}']/@name", namespaces=namespaces)
        if len(element_tags) == 0:
            continue
        for tag in element_tags:
            tag_paths = get_xpath(xmlschema,namespaces,tag,enforce_end_type=attrib_type,stop_non_unique=stop_non_unique)
            if tag_paths is None:
                continue
            if not isinstance(tag_paths,list):
                tag_paths = [tag_paths]
            for path in tag_paths:
                if f'{path}/@{attrib_name}' not in possible_paths:
                    possible_paths.append(f'{path}/@{attrib_name}')
    if len(possible_paths) == 1:
        return possible_paths[0]
    elif len(possible_paths) == 0:
        return None
    else:
        return possible_paths
  
def get_tags_several(xmlschema,namespaces, **kwargs):
    tags_several = []
    tags = xmlschema.xpath(f"//xsd:element[@maxOccurs!=1]/@name", namespaces=namespaces)
    for tag in tags:
        if tag not in tags_several:
            tags_several.append(tag)
    return tags_several

def get_sequence_order(sequence_elem,namespaces):
    """
    Extract the enforced order of elements in the given sequence element
    """
    elem_order = []
    for child in sequence_elem.getchildren():
        child_type = remove_xsd_namespace(child.tag,namespaces)

        if child_type == 'element':
            elem_order.append(child.attrib['name'])
        elif child_type == 'choice' or child_type == 'sequence':
            elem_order.append(get_sequence_order(child,namespaces))
        elif child_type is None:
            continue # With getchildren sometimes a weird cython function object enters this loop
        else:
            raise KeyError(f'Dont know what to do with {child_type}')
    if len(elem_order) == 1:
        return elem_order[0]
    else:
        return elem_order

def extract_attribute_types(xmlschema,namespaces, **kwargs):
    """
    Determine the required type of all attributes
    TODO: Inspect custom types to determine which category they should be
    """
    possible_attrib = xmlschema.xpath("//xsd:attribute", namespaces=namespaces)
    
    bool_types = ['FleurBool']
    int_types = ['xsd:nonNegativeInteger','xsd:positiveInteger','xsd:integer',
                 'SpinNumberType','AngularMomentumNumberType','MainQuantumNumberType']
    float_types = ['xsd:double','ZeroToOneNumberType','FleurDouble'] 
    string_types = ['BZIntegrationModeEnum','XCFunctionalEnum','xsd:string','EParamSelectionEnum',
                    'MixingEnum','ForceMixEnum','RDMFTFunctionalEnum','KPointListPurposeEnum','CoreSpecEdgeEnum',
                    'ElectronStateEnum','FleurVersionType','ManualCutoffType','ManualKKintgrCutoffType','ManualCutoffType',
                   'NumBandsType','kPointListTypeEnum','TripleFleurBool']
    
    types_dict = {}
    types_dict['switch'] = []
    types_dict['int'] = []
    types_dict['float'] = []
    types_dict['string'] = []
    types_dict['other'] = []
    for attrib in possible_attrib:
        name_attrib = attrib.attrib['name']
        type_attrib = attrib.attrib['type']
        if type_attrib in bool_types:
            if name_attrib not in types_dict['switch']:
                types_dict['switch'].append(name_attrib)
        elif type_attrib in int_types:
            if name_attrib not in types_dict['int']:
                types_dict['int'].append(name_attrib)
        elif type_attrib in float_types:
            if name_attrib not in types_dict['float']:
                types_dict['float'].append(name_attrib)
        elif type_attrib in string_types:
            if name_attrib not in types_dict['string']:
                types_dict['string'].append(name_attrib)
        else:
            if name_attrib not in types_dict['other']:
                types_dict['other'].append(name_attrib)
                print(f'Unsorted type:{type_attrib}')
    return types_dict

def get_tag_paths(xmlschema,namespaces, **kwargs):
    possible_tags = xmlschema.xpath("//xsd:element/@name", namespaces=namespaces)
    tag_paths = {}
    for tag in possible_tags:
        tag_paths[tag] = get_xpath(xmlschema,namespaces,tag)
    return tag_paths

def get_attrib_paths(xmlschema,namespaces, **kwargs):
    attrib_paths = {}
    possible_attrib = xmlschema.xpath("//xsd:attribute/@name", namespaces=namespaces)
    for attrib in possible_attrib:
        attrib_paths[attrib] = get_attrib_xpath(xmlschema,namespaces,attrib)
    return attrib_paths

def get_tags_order(xmlschema,namespaces, **kwargs):
    tag_order = {}
    sequences = xmlschema.xpath("//xsd:sequence", namespaces=namespaces)

    for sequence in sequences:
        parent = get_parent_fleur_type(sequence,namespaces,stop_sequence=True)
        if parent is None:
            continue
        parent_type = parent.attrib['name']
        tag_name = xmlschema.xpath(f"//xsd:element[@type='{parent_type}']/@name", namespaces=namespaces)
        if tag_name:
            tag_name = tag_name[0]
        else:
            continue
        tag_order[tag_name] = get_sequence_order(sequence,namespaces)
    return tag_order
   
def get_settable_attributes(xmlschema,namespaces, **kwargs):
    
    settable = {}
    for attrib, path in kwargs['attrib_paths'].items():
        if isinstance(path,list):
            continue #Already multiple possible paths
        path = get_attrib_xpath(xmlschema,namespaces,attrib,stop_non_unique=True)
        if path is not None:
            settable[attrib] = path

    return settable


def create_schema_dict(path):

    schema_actions = {'tag_paths': get_tag_paths,
                      'attrib_paths': get_attrib_paths,
                      'tags_several': get_tags_several,
                      'tag_order': get_tags_order,
                      'attrib_types': extract_attribute_types,
                      'settable_attribs': get_settable_attributes
                      }

    print(f'processing: {path}/FleurInputSchema.xsd')
    xmlschema = etree.parse(f'{path}/FleurInputSchema.xsd')

    namespaces = {"xsd": "http://www.w3.org/2001/XMLSchema"}
    inp_version = xmlschema.xpath("/xsd:schema/@version", namespaces=namespaces)[0]
    schema_dict = {}
    for key, action in schema_actions.items():
        schema_dict[key] = action(xmlschema,namespaces,**schema_dict)

    with open(f'{path}/schema_dict.py','w') as f:
        f.write(f"__inp_version__ = '{inp_version}'\n")
        f.write('schema_dict = ')
        pprint(schema_dict, f)


def load_schema_dict(path):
    """
    load the Fleurschema dict from the specified path
    """

    schema_file_path = os.path.join(path,'FleurInputSchema.xsd')
    schema_dict_path = os.path.join(path,'schema_dict.py')
    if not os.path.isfile(schema_file_path):
        raise ValueError(f'No input schema found at {path}')

    if not os.path.isfile(schema_dict_path):
        print(f'Generating schema_dict file for given input schema: {schema_file_path}')
        create_schema_dict(path)

    #import schema_dict
    spec = importlib.util.spec_from_file_location("schema", schema_dict_path)
    schema = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(schema)
    print(f'Loaded schema_dict input version {schema.__inp_version__}')
    return schema.schema_dict

