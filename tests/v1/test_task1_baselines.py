import pytest
from mock import patch

from loggibud.v1.baselines.shared import ortools
from loggibud.v1.baselines.task1 import lkh_3
from loggibud.v1.distances import (
    calculate_distance_matrix_great_circle_m,
    calculate_route_distance_great_circle_m,
)
from loggibud.v1.eval.task1 import evaluate_solution


@pytest.fixture
def mocked_ortools_osrm_distance_matrix():
    """Monkey-patch the OR-Tools OSRM distance matrix with the Great Circle"""

    with patch(
        "loggibud.v1.baselines.shared.ortools.calculate_distance_matrix_m",
        new=calculate_distance_matrix_great_circle_m,
    ) as mock_osrm:
        yield mock_osrm


@pytest.fixture
def mocked_lkh_osrm_distance_matrix():
    """Monkey-patch the LKH OSRM distance matrix with the Great Circle"""

    with patch(
        "loggibud.v1.data_conversion.calculate_distance_matrix_m",
        new=calculate_distance_matrix_great_circle_m,
    ) as mock_osrm:
        yield mock_osrm


@pytest.fixture
def mocked_osrm_route_distance():
    """Monkey-patch the OSRM route distance with the Great Circle"""

    with patch(
        "loggibud.v1.eval.task1.calculate_route_distance_m",
        new=calculate_route_distance_great_circle_m,
    ) as mock_osrm:
        yield mock_osrm


def test_ortools_solver(
    toy_cvrp_instance,
    mocked_ortools_osrm_distance_matrix,
    mocked_osrm_route_distance,
):
    result = ortools.solve(toy_cvrp_instance)

    total_distance = evaluate_solution(toy_cvrp_instance, result)

    assert total_distance


def test_lkh_solver(
    toy_cvrp_instance,
    mocked_lkh_osrm_distance_matrix,
    mocked_osrm_route_distance,
):
    result = lkh_3.solve(toy_cvrp_instance)

    total_distance = evaluate_solution(toy_cvrp_instance, result)

    assert total_distance
