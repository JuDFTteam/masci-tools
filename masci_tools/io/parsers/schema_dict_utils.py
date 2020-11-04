
def get_tag_xpath(schema_dict, tag, contains=None):

   if tag not in schema_dict['tag_paths']:
      raise KeyError(f'Unknown tag: {tag}')

   paths = schema_dict['tag_paths'][tag]

   if not isinstance(paths,list):
      paths = [paths]

   if contains is not None:
      paths_copy = paths.copy()
      for xpath in paths_copy:
         if contains not in xpath:
             paths.remove(xpath)

   if len(paths) == 1:
      return paths[0]
   elif len(paths) > 1:
      raise ValueError(f'The tag {tag} has multiple possible paths with the current specification.')
   else:
      raise ValueError(f'The tag {tag} has no path containing the phrase: {contains}.')

def get_attrib_xpath(schema_dict, attrib, contains=None):

   if attrib not in schema_dict['attrib_paths']:
      raise KeyError(f'Unknown attrib: {attrib}')

   paths = schema_dict['attrib_paths'][attrib]

   if not isinstance(paths,list):
      paths = [paths]

   if contains is not None:
      paths_copy = paths.copy()
      for xpath in paths_copy:
         if contains not in xpath:
             paths.remove(xpath)

   if len(paths) == 1:
      return paths[0]
   elif len(paths) > 1:
      raise ValueError(f'The attrib {attrib} has multiple possible paths with the current specification.')
   else:
      raise ValueError(f'The attrib {attrib} has no path containing the phrase: {contains}.')
