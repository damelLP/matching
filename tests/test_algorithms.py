""" Tests for each algorithm on small example cases. """

from hypothesis import given
from hypothesis.strategies import (
    dictionaries,
    permutations,
    sampled_from,
)

from matching.algorithms import stable_marriage


STABLE_MARRIAGE = given(
    suitor_preferences=dictionaries(
        keys=sampled_from(["A", "B", "C"]),
        values=permutations(["D", "E", "F"]),
        min_size=3,
        max_size=3,
    ),
    reviewer_preferences=dictionaries(
        keys=sampled_from(["D", "E", "F"]),
        values=permutations(["A", "B", "C"]),
        min_size=3,
        max_size=3,
    ),
)


@STABLE_MARRIAGE
def test_stable_marriage_suitor(suitor_preferences, reviewer_preferences):
    """ Assert that the Gale-Shapley algorithm produces a valid, suitor-optimal
    solution to an instance of SM. """

    matching = stable_marriage(
        suitor_preferences, reviewer_preferences, optimal="suitor"
    )

    assert set(suitor_preferences.keys()) == set(matching.keys())
    assert set(reviewer_preferences.keys()) == set(matching.values())

    for player, partner in matching.items():
        assert player and partner


@STABLE_MARRIAGE
def test_stable_marriage_reviewer(suitor_preferences, reviewer_preferences):
    """ Assert that the Gale-Shapley algorithm produces a valid,
    reviewer-optimal solution to an instance of SM. """

    matching = stable_marriage(
        suitor_preferences, reviewer_preferences, optimal="reviewer"
    )

    assert set(suitor_preferences.keys()) == set(matching.values())
    assert set(reviewer_preferences.keys()) == set(matching.keys())

    for player, partner in matching.items():
        assert player and partner
