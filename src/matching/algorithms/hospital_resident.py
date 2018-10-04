""" Algorithms for solving instances of the hospital-resident problem. """


def _check_inputs(hospital_prefs, resident_prefs):
    """ Reduce as necessary the preference list of all residents and hospitals
    so that no player ranks another player that they are not also ranked by. """

    for resident in resident_prefs.keys():
        for hospital in resident_prefs[resident]:
            if resident not in hospital_prefs[hospital]:
                raise ValueError(
                    "Hospitals must rank all residents who rank them."
                )


def _get_free_residents(resident_prefs, matching):
    """ Return a list of all residents who are currently unmatched but have a
    non-empty preference list. """

    return [
        resident
        for resident in resident_prefs
        if resident_prefs[resident]
        and not any([resident in match for match in matching.values()])
    ]


def _get_worst_idx(hospital, hospital_prefs, matching):
    """ Find the index of the worst resident currently assigned to `hospital`
    according to their preferences. """

    return max(
        [
            hospital_prefs[hospital].index(resident)
            for resident in hospital_prefs[hospital]
            if resident in matching[hospital]
        ]
    )


def hr_resident_optimal(hospital_prefs, resident_prefs, capacities):
    """ Solve the given instance of HR so that the matching is suitor-optimal.
    The algorithm, set out in [Dubins, Freeman 1981], is as follows:

        1. Assign all hospitals and residents to be unmatched.

        2. Take some unmatched resident, :math:`r`, with a non-empty preference
           list, and consider their most preferred hospital, :math:`h`.

        3. Add :math:`r` to :math:`h`'s matching.

        4. If :math:`h` is over-subscribed:

            - Find :math:`h`'s worst currently matched resident, :math:`r^*`.
            - Remove :math:`r^*` from :math:`h`'s matching and assign them to be
              unmatched.

        5. If :math:`h` is now at capacity:

            - Find :math:`h`'s worst currently matched resident, :math:`r^*`.
            - For each successor, :math:`r'`, to :math:`r^*` in the preference
              list of :math:`h`:

                - Remove :math:`h` from the preference list of :math:`r'`, and
                  vice versa.

        6. Go to 2 until there are no residents left to be considered, then end.

    Parameters
    ----------
    hospital_prefs : dict
        A dictionary with hospitals as keys and their associated preference
        lists as values.
    resident_prefs : dict
        A dictionary with residents as keys and their associated preference
        lists as values.
    capacities : dict
        A dictionary of hospitals and their associated capacities.

    Returns
    -------
    matching : dict
        A stable, resident-optimal matching where each hospital's matches are
        ordered wi h respect to their preference lists.
    """

    matching = {hospital: [] for hospital in hospital_prefs}
    free_residents = _get_free_residents(resident_prefs, matching)

    while free_residents:
        resident = free_residents[0]
        hospital = resident_prefs[resident][0]
        matching[hospital].append(resident)

        if len(matching[hospital]) > capacities[hospital]:
            worst = _get_worst_idx(hospital, hospital_prefs, matching)
            resident = hospital_prefs[hospital][worst]
            matching[hospital].remove(resident)

        if len(matching[hospital]) == capacities[hospital]:
            worst = _get_worst_idx(hospital, hospital_prefs, matching)
            successors = hospital_prefs[hospital][worst + 1 :]

            if successors:
                for resident in successors:
                    hospital_prefs[hospital].remove(resident)
                    if hospital in resident_prefs[resident]:
                        resident_prefs[resident].remove(hospital)

        free_residents = _get_free_residents(resident_prefs, matching)

    for hospital, matches in matching.items():
        sorted_matches = sorted(matches, key=hospital_prefs[hospital].index)
        matching[hospital] = sorted_matches

    return matching


def _get_free_hospitals(hospital_prefs, capacities, matching):

    return [
        hospital
        for hospital in hospital_prefs
        if len(matching[hospital]) < capacities[hospital]
        and any(
            [
                resident
                for resident in hospital_prefs[hospital]
                if resident not in matching[hospital]
            ]
        )
    ]


def hr_hospital_optimal(hospital_prefs, resident_prefs, capacities):
    """ Solve the given instance of HR so that the matching is hospital-optimal.
    The algorithm, set out in [Roth 1984], is as follows:

        1. Assign all hospitals and residents to be unmatched.

        2. Take some hospital, :math:`h`, who is under-subscribed and whose
           preference list contains some resident to whom they are not matched.
           Consider :math:`h`'s most preferred resident, :math:`r`, to whom they
           are not already matched.

        3. If :math:`r` is already assigned to some hospital, :math:`h^*`:

            - Remove :math:`r` from :math:`h^*`'s matching and assign them to be
              unmatched.

        4. Add :math:`r` to`:math:`h`'s matching.

        5. For each successor, :math:`h'`, to :math:`h` in the preference list
           of :math:`r`:

            - Remove :math:`r` from the preference list of :math:`h'`, and vice
              versa.
    """
    matching = {h: [] for h in hospital_prefs}
    free_hospitals = _get_free_hospitals(hospital_prefs, capacities, matching)

    while free_hospitals:
        hospital = free_hospitals[0]
        resident = [
            resident
            for resident in hospital_prefs[hospital]
            if resident not in matching[hospital]
        ][0]

        for hosp, matches in matching.items():
            if resident in matches:
                matching[hosp].remove(resident)

        matching[hospital].append(resident)
        idx = resident_prefs[resident].index(hospital)
        successors = resident_prefs[resident][idx + 1 :]

        if successors:
            for successor in successors:
                hospital_prefs[successor].remove(resident)
                resident_prefs[resident].remove(successor)

        free_hospitals = _get_free_hospitals(
            hospital_prefs, capacities, matching
        )

    return matching


def hospital_resident(
    hospital_prefs, resident_prefs, capacities, optimal="resident"
):
    """ Provide a stable matching for the given instance of HR using one of the
    algorithms set out in [Dubins, Freeman 1981] or [Roth 1984]. Which algorithm
    to be used, and thus the associated party-optimality of the matching, is
    controlled by the :code:`optimal` parameter.

    Parameters
    ----------
    hospital_prefs : dict
        A dictionary with hospitals as keys and their associated preference
        lists as values.
    resident_prefs : dict
        A dictionary with residents as keys and their associated preference
        lists as values.
    capacities : dict
        A dictionary of hospitals and their associated capacities.
    optimal : str
        An indicator for which party the matching should be optimal. Defaults to
        :code:`'resident'` but can also be :code:`'hospital'`.

    Returns
    -------
    matching : dict
        A stable matching with hospitals as keys, and each hospital's matches
        are ordered with respect to their preference lists. The matching itself
        is either resident- or hospital-optimal depending on the :code:`optimal`
        parameter.
    """

    _check_inputs(hospital_prefs, resident_prefs)

    if optimal == "resident":
        matching = hr_resident_optimal(
            hospital_prefs, resident_prefs, capacities
        )
    elif optimal == "hospital":
        matching = hr_hospital_optimal(
            hospital_prefs, resident_prefs, capacities
        )
    else:
        raise ValueError(
            'Optimality option unknown. Should be one of "resident" or '
            f'"hospital". Got {optimal}.'
        )

    return matching
