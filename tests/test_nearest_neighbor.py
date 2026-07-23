"""Testes unitários para modules.nearest_neighbor.NearestNeighborOptimizer."""

import numpy as np
import pytest

from modules.nearest_neighbor import NearestNeighborOptimizer


@pytest.fixture
def line_matrix():
    """Matriz de distâncias para 4 pontos em linha: 0km, 1km, 2km, 3km.

    Índice 0 é o depósito. Distâncias em metros.
    """
    points = [0, 1000, 2000, 3000]
    n = len(points)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i][j] = abs(points[i] - points[j])
    return matrix


class TestSolve:
    def test_single_vehicle_visits_all_in_order(self, line_matrix):
        optimizer = NearestNeighborOptimizer(
            distance_matrix=line_matrix,
            num_vehicles=1,
            depot_index=0,
        )
        assert optimizer.solve() is True

        routes = optimizer.get_routes()
        # Guloso em pontos numa linha: 0 -> 1 -> 2 -> 3 -> 0
        assert routes == [[0, 1, 2, 3, 0]]
        # 1km + 1km + 1km + 3km de volta = 6km
        assert optimizer.get_route_distance(routes[0]) == pytest.approx(6000.0)

    def test_routes_start_and_end_at_depot(self, line_matrix):
        optimizer = NearestNeighborOptimizer(
            distance_matrix=line_matrix,
            num_vehicles=2,
            depot_index=0,
        )
        optimizer.solve()
        for route in optimizer.get_routes():
            assert route[0] == 0
            assert route[-1] == 0

    def test_all_customers_visited_exactly_once(self, line_matrix):
        optimizer = NearestNeighborOptimizer(
            distance_matrix=line_matrix,
            num_vehicles=2,
            depot_index=0,
        )
        optimizer.solve()

        visited = [
            node
            for route in optimizer.get_routes()
            for node in route
            if node != 0
        ]
        assert sorted(visited) == [1, 2, 3]

    def test_max_customers_per_route_is_respected(self, line_matrix):
        optimizer = NearestNeighborOptimizer(
            distance_matrix=line_matrix,
            num_vehicles=2,
            depot_index=0,
            max_customers_per_route=2,
        )
        optimizer.solve()

        routes = optimizer.get_routes()
        assert routes == [[0, 1, 2, 0], [0, 3, 0]]
        for route in routes:
            assert len(route) - 2 <= 2


class TestMetrics:
    def test_metrics_content(self, line_matrix):
        optimizer = NearestNeighborOptimizer(
            distance_matrix=line_matrix,
            num_vehicles=1,
            depot_index=0,
        )
        optimizer.solve()
        metrics = optimizer.get_metrics()

        assert metrics['algorithm'] == 'Nearest Neighbor'
        assert metrics['num_routes'] == 1
        assert metrics['num_vehicles_used'] == 1
        assert metrics['total_distance'] == pytest.approx(6000.0)
        assert metrics['max_route_distance'] == pytest.approx(6000.0)
        assert metrics['route_distances'] == [pytest.approx(6000.0)]

    def test_metrics_empty_before_solve(self, line_matrix):
        optimizer = NearestNeighborOptimizer(
            distance_matrix=line_matrix,
            num_vehicles=1,
            depot_index=0,
        )
        assert optimizer.get_metrics() == {}
        assert optimizer.get_routes() == []
