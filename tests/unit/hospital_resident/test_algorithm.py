import itertools

import pytest
import numpy as np

from hypothesis import given, settings
from hypothesis.strategies import (
    dictionaries,
    integers,
    permutations,
    sampled_from,
)

from matching.algorithms import hospital_resident
from .util import HOSPITAL_RESIDENT, make_hospital_prefs


@HOSPITAL_RESIDENT
def test_resident_optimal(resident_preferences, capacities, seed):
    """ Verify that the hospital-resident algorithm produces a valid,
    resident-optimal matching for an instance of HR. """

    resident_preferences = dict(sorted(resident_preferences.items()))

    if all(resident_preferences.values()):
        np.random.seed(seed)

        hospital_preferences = make_hospital_prefs(resident_preferences)
        matching = hospital_resident(
            hospital_preferences,
            resident_preferences,
            capacities,
            optimal="resident",
        )

        assert set(hospital_preferences.keys()) == set(matching.keys())

        for hospital, matches in matching.items():
            old_idx = -np.infty
            for resident in matches:
                idx = hospital_preferences[hospital].index(resident)
                assert idx >= old_idx
                old_idx = idx
    else:
        assert 2 + 2 == 4


@HOSPITAL_RESIDENT
def test_hospital_optimal(resident_preferences, capacities, seed):
    """ Verify that the hospital-resident algorithm produces a valid,
    hospital-optimal matching for an instance of HR. """

    resident_preferences = dict(sorted(resident_preferences.items()))

    if all(resident_preferences.values()):
        np.random.seed(seed)

        hospital_preferences = make_hospital_prefs(resident_preferences)
        matching = hospital_resident(
            hospital_preferences,
            resident_preferences,
            capacities,
            optimal="hospital",
        )

        assert set(hospital_preferences.keys()) == set(matching.keys())

        for hospital, matches in matching.items():
            old_idx = -np.infty
            for resident in matches:
                idx = hospital_preferences[hospital].index(resident)
                assert idx >= old_idx
                old_idx = idx
    else:
        assert 2 + 2 == 4


def test_raises_missing_rank_error():
    """ Verify that a ValueError is raised when a hospital does not rank all the
    residents that rank it. """

    resident_preferences = {
        "A": ["Y"],
        "B": ["Y", "X"],
        "C": ["Y", "Z", "X"],
        "D": ["X", "Y", "Z"],
    }

    hospital_preferences = {
        "X": ["C"],  # X should rank B and D as well.
        "Y": ["A", "B", "D", "C"],
        "Z": ["C", "D"],
    }

    capacities = {hospital: 2 for hospital in hospital_preferences}

    with pytest.raises(ValueError):
        hospital_resident(
            hospital_preferences, resident_preferences, capacities
        )

def test_raises_extra_rank_error():
    """ Verify that a ValueError is raised when a hospital ranks a resident that
    has not also ranked it. """

    resident_preferences = {
        "A": ["Y"],
        "B": ["Y", "X"],
        "C": ["Y", "Z", "X"],
        "D": ["X", "Y", "Z"],
    }

    hospital_preferences = {
        "X": ["C", "B", "D"],
        "Y": ["A", "B", "D", "C"],
        "Z": ["C", "D", "A"],  # Z has ranked A but A has no preference for Z.
    }

    capacities = {hospital: 2 for hospital in hospital_preferences}

    with pytest.raises(ValueError):
        hospital_resident(
            hospital_preferences, resident_preferences, capacities
        )
