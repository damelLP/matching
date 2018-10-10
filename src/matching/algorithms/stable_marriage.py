""" Algorithms for solving instances of the stable marriage problem. """


def stable_marriage(suitor_prefs, reviewer_prefs, optimal="suitor"):
    """ Set out in [Gale, Shapley 1962] and commonly known as the
    Extended Gale-Shapley algorithm, this algorithm is known to provide a
    unique, stable, suitor-optimal matching to any instance of the stable
    marriage problem. If a reviewer-optimal matching is required, then the roles
    of suitors and reviewers should be reversed. The algorithm is as follows:

        1. Assign all suitors and reviewers to be unmatched.

        2. Take any unmatched suitor, :math:`s`, and their most preferred
           reviewer, :math:`r`.

        3. If :math:`r` is matched to some suitor :math:`s^*`:

            - Assign :math:`s^*` to be unmatched.

        4. Assign :math:`s` to be matched to :math:`r`.

        5. For each successor, :math:`s'`, to :math:`s` in the preference list
           of :math:`r`:

            - Remove :math:`r` from the preference list of :math:`s'`, and vice
              versa.

        6. Go to 2 until all suitors are matched, then end.

    Parameters
    ----------
    suitor_prefs : dict
        A dictionary with suitors as keys and their respective preference lists
        as values.
    review_prefs : dict
        A dictionary with reviewers as keys and their respective preference
        lists as values.
    optimal : str
        An indicator for which party the matching should be optimal. Defaults to
        :code:`'suitor'` but can also be :code:`'reviewer'`.

    Returns
    -------
    matching : dict
        The stable matching with the optimal party members as keys and the
        players they are matched with as values.
    """
    if optimal == "reviewer":
        suitor_prefs, reviewer_prefs = reviewer_prefs, suitor_prefs

    suitors = [s for s in suitor_prefs]
    matching = {s: None for s in suitors}

    while suitors:
        suitor = suitors.pop(0)
        reviewer = suitor_prefs[suitor][0]

        if reviewer in matching.values():
            idx = list(matching.values()).index(reviewer)
            current_partner = list(matching.keys())[idx]
            matching[current_partner] = None
            suitors.append(current_partner)

        matching[suitor] = reviewer

        idx = reviewer_prefs[reviewer].index(suitor)
        successors = reviewer_prefs[reviewer][idx + 1 :]

        for successor in successors:
            reviewer_prefs[reviewer].remove(successor)
            suitor_prefs[successor].remove(reviewer)

    return matching
