"""Holds utility functions for the HDF file Reader module.

"""
import __future__
import inspect
from collections import namedtuple

import scipy.constants as constants


def get_class(method):
    """py3-compatible version of getting a method's type.
    :return:
    """
    if inspect.ismethod(method):
        for cls in inspect.getmro(method.__self__.__class__):
            if cls.__dict__.get(method.__name__) is method:
                return cls
        method = method.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(method):
        cls = getattr(inspect.getmodule(method),
                      method.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return getattr(method, '__objclass__', None)  # handle special descriptor objects


def constant(keywords, printAlternatives=True):
    """Semi-intelligent scipy.constants finder.

    Notes
    =====
    Recognized keywords separators: whitespace, comma, (under)score, (semi)colon.
    Order of keywords influences result (closest match).

    Raises
    ======
      LookupError
         If no match or ambiguous matches

    Examples
    ========
    >>> angstrom = constant("Angstrom")
    >>> print(angstrom)
    Constant(name='angstrom', value=1e-10)
    >>> pi = constant("pi")
    >>> print(pi)
    Constant(name='pi', value=3.141592653589793)
    >>> tau_el_mass_ratio = constant("tau electron ratio")
    >>> print(tau_el_mass_ratio)
    Constant(name='tau-electron mass ratio', value=3477.15, unit='', uncertainty=0.31)
    >>> el_tau_mass_ratio = constant("ratio electron-tau")  # order does matter to a degree
    >>> el_tau_mass_ratio = constant("electron tau mass")  # same result
    >>> print(el_tau_mass_ratio)
    Constant(name='electron-tau mass ratio', value=0.000287592, unit='', uncertainty=2.6e-08)
    >>> bohr_rad = constant("bohr atom radius")
    >>> bohr_rad = constant("bohr radius")  # same result
    >>> print(bohr_rad)
    Constant(name='Bohr radius', value=5.2917721067e-11, unit='m', uncertainty=1.2e-20)
    >>> light_speed = constant("light of-speed")
    Function constant(keywords=['light', 'of', 'speed']): selected constant 'speed_of_light'.
    Chosen from available alternatives: ['speed_of_light', 'speed of light in vacuum'].
    >>> light_speed = constant("speed light")  # same result
    Function constant(keywords=['speed', 'light']): selected constant 'speed_of_light'.
    Chosen from available alternatives: ['speed_of_light', 'speed of light in vacuum'].
    >>> print(light_speed)
    Constant(name='speed_of_light', value=299792458.0)

    TODO
    ====
       Cleanup code.

    :param keywords: one or more keywords
    :type keywords: string
    :param printAlternatives: if more than match
    :return: tuple (name,value) or (name,value,unit,uncertainty) if physical constant
    """
    assert (isinstance(keywords, str))

    # prepare the query
    queries_orig_len = len(keywords)
    replacements = ["-", "_", ",", ";"]
    for replacement in replacements:
        keywords = str.replace(keywords, replacement, " ")
    keywords = str.split(keywords)
    # print(keywords)

    # gather non-physical constants
    mask = [not attr.startswith("__")
            and not callable(getattr(constants, attr))  # like e.g. find()
            and not isinstance(getattr(constants, attr), dict)  # like e.g. physical_constants
            and not isinstance(getattr(constants, attr), __future__._Feature)
            for attr in dir(constants)]
    const_keys = [item for (item, accept) in zip(dir(constants), mask) if accept]
    const_vals = [getattr(constants, attr) for attr in const_keys]
    # the remaining constants are either float or int

    # now extend by physical constants
    const_keys.extend(list(constants.physical_constants.keys()))
    const_vals.extend(list(constants.physical_constants.values()))
    #     print(const_keys)

    # result placeholder:
    const_key = None
    const_val = None

    # first handle the most simple case: there is only one keyword, and it
    # matches a constant name exactly.
    if (len(keywords) == 1 and keywords[0].lower() in [name.lower() for name in const_keys]):
        ind = [name.lower() for name in const_keys].index(keywords[0].lower())
        const_key = const_keys[ind]
        const_val = const_vals[ind]
    else:

        # now search:
        # first try a simple approach. If that returns [], then do it incrementally.
        #     matches = [item for item in const_keys if all(query.lower() in item.lower() for query in queries)]
        #     print(matches)
        #     if not matches:

        # have to select a careful approach.
        # firstly we want to incrementally shorten the matches list:
        # [q3 in [q2 in [q1 in list]]], for example, where queries = [q1, q2, q3].
        # 2ndly we want to reflect match index order. Meaning:
        # If q1 and q2 in item1 and item2, then the item were q1 occurrs 'earlier' is preferred.
        # Example: q1='tau', q2='electron', item1='electron-tau-mass', item2='tau-electron-mass'
        # Now
        #     print(f"list: {lst}, queries: {qs}")
        not_found_marker = 100003  # prime number
        match_indss = []
        for item in const_keys:
            match_inds = []
            not_found_factor = 1
            not_one_match = True
            for q in keywords:
                #             print(f"\titem {item}\t, query {q}")
                try:
                    index = str.index(item.lower(), q.lower())
                    not_one_match = False
                    match_inds.append(index)
                except ValueError:
                    match_inds.append(not_found_factor * not_found_marker)
                    not_found_factor += 1
            if not_one_match:
                match_inds = [-1 * not_found_marker]
            match_indss.append(match_inds)
        #         if match_inds:
        #             match_indss.append(match_inds)

        if not match_indss:
            raise LookupError(f"Not found any matches for query {keywords}.")
        else:

            # now we got a list of lists. for each item of the original list,
            # it contains a list of the indices where the respective query word
            # q1, q2, ... in queries was found in that item.
            # Now we could get the index of the item with the lowest indss score,
            # that is, items where lower query words come before higher query words get preferred.
            # example: lst=['A B','B A'],qs=['b','a'] -> [[2,0],[0,2]] -> lst[1] < lst[0].
            # But have to normalize first.
            # example: lst=['A B','xxxB A'], as before -> [[2,0],[3,5]] -> lst[0] < lst[1]: Wrong!
            #                               normalized -> [[2,0],[0,2]] -> lst[1] < lst[0]: correct
            #         print(match_indss)
            offsets = [min(match_inds) for match_inds in match_indss]
            match_indss[:] = [[ind - min(match_inds)
                               if (ind % not_found_marker)
                               else ind
                               for ind in match_inds]
                              if len(match_inds) > 1
                              else match_inds
                              for match_inds in match_indss]
            #         print(match_indss)

            #     min_el = min([[abs(ind) for ind in match_inds] for match_inds in match_indss])
            #     print(f"min_el: {min_el}")
            #     # min_el_ind = match_indss.index(min_el) #only finds first occurrence
            #     min_el_inds = [ind for ind, item in enumerate(match_indss) if item == min_el]

            # first make a preselection among match_indss items:
            # find the ones with the largest matches count, then only compare them in the next step
            matches_countss = [0 * i for i in range(len(match_indss))]
            for i, match_inds in enumerate(match_indss):
                #             print(f"i = {i}:")
                # match_ind's that are negative are skipped altogether
                if any(ind < 0 for ind in match_inds):
                    continue
                for j, ind in enumerate(match_inds):
                    #                 print(f"\tj={j}:")
                    if (ind % not_found_marker):  # marker doesn't divide ind
                        matches_countss[i] += 1
            match_indss_mask = [matches_count == max(matches_countss) for matches_count in matches_countss]
            #         print(matches_countss)
            #         print(match_indss_mask)

            if not any(matches_countss):
                raise LookupError(f"Not found any matches for query {keywords}.")
            else:

                min_el_inds = []
                min_el = match_indss[matches_countss.index(max(matches_countss))]
                first = True
                for i, match_inds in enumerate(match_indss):
                    if not match_indss_mask[i]:
                        continue
                    #                 print(f"i = {i}: min_el_inds = {min_el_inds}")
                    # compare current item with current minimal item
                    # inds that are markers are ignored.
                    comparator = 0
                    for j, ind in enumerate(match_inds):
                        #                     print(f"\tj={j}:")
                        if (ind < min_el[j]):
                            #                         print(f"\t\t ind < min")
                            comparator = -1
                            min_el = match_inds
                            min_el_inds = [i]
                            break
                        elif (ind > min_el[j]):
                            #                         print(f"\t\t ind > min")
                            comparator = 1
                            break
                        #                     print(f"\t\t ind == min")
                        comparator = 0
                    #                 print(f"\tcompararor={comparator}")
                    if (comparator == 0):
                        min_el_inds.append(i)

                const_keys_res = [const_keys[ind] for ind in min_el_inds]
                const_vals_res = [const_vals[ind] for ind in
                                  min_el_inds]  # int, float, or a tuple (val, unit str, uncertainty)
                # print(f"const_keys_res: {const_keys_res}")

                alternatives = f"Chosen from available alternatives: {const_keys_res}." if len(
                    const_keys_res) > 1 else ""

                if (len(min_el_inds) > 1):
                    # choose the one with the closest length to the query length
                    len_query = len(' '.join(word for word in keywords))
                    len_keys = [abs(len(key) - len_query) for key in const_keys_res]
                    min_len = min(len_keys)
                    min_keys_inds = [ind for ind, item in enumerate(len_keys) if min_len == item]
                    # print(f"len_keys: {len_keys}, min_keys_inds: {min_keys_inds}")
                    const_keys_res = [const_keys_res[ind] for ind in min_keys_inds]
                    const_vals_res = [const_vals_res[ind] for ind in min_keys_inds]

                    if (len(min_keys_inds) > 1):
                        raise LookupError(f"Ambiguous result: more than one match for query {keywords}. "
                                          f"Try a more specific query, e.g. more existing keywords, in desired order. "
                                          f"Result matches were: {const_keys_res}."
                                          )

            const_key = const_keys_res[0]
            const_val = const_vals_res[0]

            if printAlternatives and alternatives:
                print(f"Function constant(keywords={keywords}): selected constant '{const_key}'.\n" + alternatives)

    result = None
    if isinstance(const_val, tuple):
        Constant = namedtuple('Constant', ['name', 'value', 'unit', 'uncertainty'])
        result = Constant(*((const_key,) + const_val))
        # result = (const_key,) + const_val
    else:
        Constant = namedtuple('Constant', ['name', 'value'])
        result = Constant(*(const_key, const_val))
        # result = const_key, const_val

    return result
