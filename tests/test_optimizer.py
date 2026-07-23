"""Testes para modules.optimizer.VRPOptimizer (OR-Tools).

Usa instâncias pequenas e determinísticas com local_search=None e
tempo limite curto para execução rápida e reprodutível.
"""

import numpy as np
import pytest

from modules.optimizer import VRPOptimizer


def line_matrix(points_m):
    """Matriz de distâncias (em metros) para pontos em uma linha."""
    n = len(points_m)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i][j] = abs(points_m[i] - points_m[j])
    return matrix


class TestValidation:
    def test_non_square_matrix_raises(self):
        with pytest.raises(ValueError, match='quadrada'):
            VRPOptimizer(
                distance_matrix=np.zeros((3, 4)),
                num_vehicles=1,
            )

    def test_invalid_depot_index_raises(self):
        with pytest.raises(ValueError, match='depósito'):
            VRPOptimizer(
                distance_matrix=np.zeros((3, 3)),
                num_vehicles=1,
                depot_index=5,
            )

    def test_capacity_count_mismatch_raises(self):
        with pytest.raises(ValueError, match='capacidades'):
            VRPOptimizer(
                distance_matrix=np.zeros((3, 3)),
                num_vehicles=2,
                vehicle_capacities=[10],
                demands=[0, 1, 1],
            )

    def test_demand_count_mismatch_raises(self):
        with pytest.raises(ValueError, match='demandas'):
            VRPOptimizer(
                distance_matrix=np.zeros((3, 3)),
                num_vehicles=1,
                vehicle_capacities=[10],
                demands=[0, 1],
            )


class TestSingleVehicleTsp:
    def test_finds_optimal_route_on_line(self):
        # Pontos em linha: depósito em 0, clientes em 1km, 2km e 3km.
        # Rota ótima percorre 6km no total (ida até a ponta e volta).
        matrix = line_matrix([0, 1000, 2000, 3000])
        optimizer = VRPOptimizer(
            distance_matrix=matrix,
            num_vehicles=1,
            depot_index=0,
            max_distance_per_vehicle=100_000,
        )

        assert optimizer.solve(time_limit_seconds=5, local_search=None) is True

        metrics = optimizer.get_metrics()
        assert metrics['total_distance'] == pytest.approx(6000.0)
        assert metrics['num_routes'] == 1

        route = metrics['routes'][0]
        assert route[0] == 0
        assert route[-1] == 0
        assert sorted(route[1:-1]) == [1, 2, 3]


class TestMultiVehicle:
    def test_routes_are_valid(self):
        # 6 localizações: depósito + 5 clientes
        matrix = line_matrix([0, 1000, 2000, 3000, 4000, 5000])
        optimizer = VRPOptimizer(
            distance_matrix=matrix,
            num_vehicles=2,
            depot_index=0,
            max_distance_per_vehicle=100_000,
        )

        assert optimizer.solve(time_limit_seconds=5, local_search=None) is True

        routes = optimizer.get_routes()
        assert len(routes) >= 1

        visited = []
        for route in routes:
            assert route[0] == 0
            assert route[-1] == 0
            visited.extend(node for node in route if node != 0)

        # Cada cliente visitado exatamente uma vez
        assert sorted(visited) == [1, 2, 3, 4, 5]

    def test_metrics_consistency(self):
        matrix = line_matrix([0, 1000, 2000, 3000])
        optimizer = VRPOptimizer(
            distance_matrix=matrix,
            num_vehicles=2,
            depot_index=0,
            max_distance_per_vehicle=100_000,
        )
        optimizer.solve(time_limit_seconds=5, local_search=None)
        metrics = optimizer.get_metrics()

        assert metrics['algorithm'] == 'OR-Tools'
        assert metrics['num_routes'] == len(metrics['routes'])
        assert metrics['total_distance'] == pytest.approx(
            sum(metrics['route_distances'])
        )
        assert metrics['max_route_distance'] == pytest.approx(
            max(metrics['route_distances'])
        )


class TestCapacitatedVrp:
    def test_capacity_constraints_respected(self):
        matrix = line_matrix([0, 1000, 2000, 3000, 4000])
        demands = [0, 4, 4, 4, 4]
        capacities = [8, 8]

        optimizer = VRPOptimizer(
            distance_matrix=matrix,
            num_vehicles=2,
            depot_index=0,
            vehicle_capacities=capacities,
            demands=demands,
            max_distance_per_vehicle=100_000,
        )

        assert optimizer.solve(time_limit_seconds=5, local_search=None) is True

        metrics = optimizer.get_metrics()
        assert 'route_loads' in metrics
        # Demanda total de 16 exige os dois veículos de capacidade 8
        assert len(metrics['routes']) == 2
        for load in metrics['route_loads']:
            assert load <= 8

        visited = [
            node
            for route in metrics['routes']
            for node in route
            if node != 0
        ]
        assert sorted(visited) == [1, 2, 3, 4]


class TestNoSolution:
    def test_returns_empty_when_not_solved(self):
        matrix = line_matrix([0, 1000])
        optimizer = VRPOptimizer(distance_matrix=matrix, num_vehicles=1)
        assert optimizer.get_routes() == []
        assert optimizer.get_metrics() == {}
