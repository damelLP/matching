""" Useful functions and decorators for the HR tests. """

import itertools
import numpy as np

from hypothesis import given
from hypothesis.strategies import (
    dictionaries,
    integers,
    sampled_from,
)


def get_inputs(values):
    """ Generate the list of all possible ordered subsets of values. """

    power_set = set(
        [
            tuple(set(prod))
            for prod in itertools.product(values, repeat=len(values))
        ]
    )
    power_perms = [itertools.permutations(comb) for comb in power_set]

    ordered_power_set = []
    for perm in power_perms:
        for item in perm:
            ordered_power_set.append(list(item))

    return ordered_power_set


def make_hospital_prefs(resident_prefs):
    """ Given some resident preferences, make a valid set of hospital
    preferences. """

    hospitals = []
    for val in resident_prefs.values():
        for item in val:
            if item not in hospitals:
                hospitals.append(item)

    hospital_prefs = {
        h: np.random.permutation(
            [r for r in resident_prefs if h in resident_prefs[r]]
        ).tolist()
        for h in hospitals
    }

    return dict(sorted(hospital_prefs.items()))


HOSPITAL_RESIDENT = given(
    resident_preferences=dictionaries(
        keys=sampled_from(["A", "B", "C", "D"]),
        values=sampled_from(get_inputs(["X", "Y", "Z"])),
        min_size=4,
        max_size=4,
    ),
    capacities=dictionaries(
        keys=sampled_from(["X", "Y", "Z"]),
        values=integers(min_value=1),
        min_size=3,
        max_size=3,
    ),
    seed=integers(min_value=0),
)
