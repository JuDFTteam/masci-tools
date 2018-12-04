import scipy.constants as constants
import __future__


def constant(keywords):
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
                index = str.index(item, q)
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

            if (len(min_el_inds) > 1):
                raise LookupError(f"Ambiguous result: more than one match for query {keywords}. "
                                  f"Try a more specific query, e.g. more existing keywords, in desired order. "
                                  f"Result matches were: {const_keys_res}."
                                  )

            const_key = const_keys_res[0]
            const_val = [const_vals[ind] for ind in min_el_inds][
                0]  # int, float, or a tuple (val, unit str, uncertainty)

            result = None
            if isinstance(const_val, tuple):
                result = (const_key,) + const_val
            else:
                result = const_key, const_val

            return result


##################################################################
# %% Testing
tau_el_mass_ratio = constant("tau electron ratio")
el_tau_mass_ratio = constant("electron-tau ratio")
print(tau_el_mass_ratio)
print(el_tau_mass_ratio)
# constant("electron tau ratio")
