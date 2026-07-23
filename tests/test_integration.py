"""Teste de integração do pipeline completo (migrado de test_system.py).

Dados de exemplo -> matriz de distâncias -> otimização -> custos.
Sem UI Streamlit, sem rede e sem chaves de API.
"""

from pathlib import Path

import pytest

from modules.cost_calculator import CostCalculator
from modules.data_handler import DataHandler
from modules.optimizer import VRPOptimizer

EXAMPLE_CSV = Path(__file__).resolve().parent.parent / 'data' / 'exemplo_clientes.csv'


def test_full_pipeline_with_sample_data():
    """VRP básico com dados sintéticos determinísticos (seed fixa)."""
    data = DataHandler.create_sample_data(
        num_locations=8,
        depot_location=(-23.5505, -46.6333),  # São Paulo
        radius_km=30,
        include_demands=False,
    )
    locations = data['locations']
    assert DataHandler.validate_locations(locations)

    distance_matrix = DataHandler.create_distance_matrix(locations, method='haversine')
    assert distance_matrix.shape == (8, 8)

    optimizer = VRPOptimizer(
        distance_matrix=distance_matrix,
        num_vehicles=2,
        depot_index=0,
        max_distance_per_vehicle=200_000,
    )
    assert optimizer.solve(time_limit_seconds=10, local_search=None) is True

    metrics = optimizer.get_metrics()
    assert metrics['total_distance'] > 0

    visited = [
        node
        for route in metrics['routes']
        for node in route
        if node != 0
    ]
    assert sorted(visited) == list(range(1, 8))

    # Custos a partir das distâncias das rotas
    calculator = CostCalculator()
    route_distances_km = [d / 1000 for d in metrics['route_distances']]
    costs = calculator.calculate_route_costs(route_distances_km)

    assert costs['total_distance_km'] == pytest.approx(metrics['total_distance'] / 1000)
    assert costs['total_cost'] > 0
    assert costs['total_co2_kg'] > 0


def test_cvrp_pipeline_with_example_csv():
    """CVRP usando o CSV de exemplo do repositório."""
    data = DataHandler.load_locations_from_csv(
        str(EXAMPLE_CSV),
        lat_column='latitude',
        lon_column='longitude',
        name_column='nome',
        demand_column='demanda',
    )
    locations = data['locations']
    demands = data['demands']

    distance_matrix = DataHandler.create_distance_matrix(locations, method='haversine')

    total_demand = sum(demands)
    capacities = [total_demand, total_demand]  # capacidade folgada

    optimizer = VRPOptimizer(
        distance_matrix=distance_matrix,
        num_vehicles=2,
        depot_index=0,
        vehicle_capacities=capacities,
        demands=demands,
        max_distance_per_vehicle=200_000,
    )
    assert optimizer.solve(time_limit_seconds=10, local_search=None) is True

    metrics = optimizer.get_metrics()
    visited = [
        node
        for route in metrics['routes']
        for node in route
        if node != 0
    ]
    assert sorted(visited) == list(range(1, len(locations)))

    for load, capacity in zip(metrics['route_loads'], capacities):
        assert load <= capacity
