"""Testes unitários para modules.cost_calculator.CostCalculator."""

import pytest

from modules.cost_calculator import CostCalculator


@pytest.fixture
def calculator():
    """Calculadora com valores fixos para resultados determinísticos."""
    return CostCalculator(
        fuel_price_per_liter=6.50,
        fuel_consumption_km_per_liter=8.0,
        cost_per_km=2.50,
        driver_cost_per_hour=25.00,
        vehicle_depreciation_per_km=0.50,
        toll_cost_per_100km=15.00,
        average_speed_kmh=60.0,
        include_tolls=True,
    )


class TestComponentCosts:
    def test_fuel_cost(self, calculator):
        # 80 km / 8 km/L = 10 L * R$ 6,50 = R$ 65,00
        assert calculator.calculate_fuel_cost(80.0) == pytest.approx(65.0)

    def test_fuel_cost_zero_distance(self, calculator):
        assert calculator.calculate_fuel_cost(0.0) == 0.0

    def test_time_hours(self, calculator):
        # 120 km a 60 km/h = 2 horas
        assert calculator.calculate_time_hours(120.0) == pytest.approx(2.0)

    def test_driver_cost(self, calculator):
        # 60 km a 60 km/h = 1 hora * R$ 25 = R$ 25
        assert calculator.calculate_driver_cost(60.0) == pytest.approx(25.0)

    def test_depreciation_cost(self, calculator):
        assert calculator.calculate_depreciation_cost(100.0) == pytest.approx(50.0)

    def test_toll_cost(self, calculator):
        assert calculator.calculate_toll_cost(100.0) == pytest.approx(15.0)

    def test_toll_cost_disabled(self):
        calculator = CostCalculator(include_tolls=False)
        assert calculator.calculate_toll_cost(100.0) == 0.0

    def test_operational_cost(self, calculator):
        assert calculator.calculate_operational_cost(10.0) == pytest.approx(25.0)

    def test_co2_emissions(self, calculator):
        # 8 km = 1 litro * 2,68 kg CO2/L
        assert calculator.calculate_co2_emissions(8.0) == pytest.approx(2.68)


class TestTotalCost:
    def test_total_is_sum_of_components(self, calculator):
        distance = 100.0
        costs = calculator.calculate_total_cost(distance)

        expected_total = (
            costs['fuel_cost']
            + costs['driver_cost']
            + costs['depreciation_cost']
            + costs['toll_cost']
            + costs['operational_cost']
        )
        assert costs['total_cost'] == pytest.approx(expected_total)
        assert costs['distance_km'] == distance

    def test_total_cost_known_value(self, calculator):
        # 100 km: combustível 81,25 + motorista 41,67 + depreciação 50
        # + pedágio 15 + operacional 250 = 437,92 (aprox)
        costs = calculator.calculate_total_cost(100.0)
        assert costs['fuel_cost'] == pytest.approx(81.25)
        assert costs['driver_cost'] == pytest.approx(100.0 / 60.0 * 25.0)
        assert costs['depreciation_cost'] == pytest.approx(50.0)
        assert costs['toll_cost'] == pytest.approx(15.0)
        assert costs['operational_cost'] == pytest.approx(250.0)
        assert costs['time_hours'] == pytest.approx(100.0 / 60.0)


class TestRouteCosts:
    def test_aggregates_multiple_routes(self, calculator):
        distances = [85.5, 92.3, 78.8]
        costs = calculator.calculate_route_costs(distances)

        assert costs['num_routes'] == 3
        assert costs['total_distance_km'] == pytest.approx(sum(distances))
        assert costs['total_cost'] == pytest.approx(
            sum(rc['total_cost'] for rc in costs['route_costs'])
        )
        assert costs['average_cost_per_route'] == pytest.approx(costs['total_cost'] / 3)
        assert costs['cost_per_km'] == pytest.approx(
            costs['total_cost'] / sum(distances)
        )
        assert costs['total_co2_kg'] > 0

    def test_empty_route_list(self, calculator):
        costs = calculator.calculate_route_costs([])
        assert costs['num_routes'] == 0
        assert costs['total_distance_km'] == 0
        assert costs['total_cost'] == 0
        assert costs['average_cost_per_route'] == 0
        assert costs['cost_per_km'] == 0


class TestCompareScenarios:
    def test_savings_between_scenarios(self, calculator):
        comparison = calculator.compare_scenarios(
            scenario1_distances=[100.0],
            scenario2_distances=[80.0],
            scenario1_name='Antes',
            scenario2_name='Depois',
        )

        savings = comparison['savings']
        assert savings['distance_saved_km'] == pytest.approx(20.0)
        assert savings['cost_saved'] > 0
        assert savings['co2_saved_kg'] > 0
        assert 0 < savings['cost_reduction_percent'] < 100
        assert 'Antes' in comparison
        assert 'Depois' in comparison

    def test_identical_scenarios_have_zero_savings(self, calculator):
        comparison = calculator.compare_scenarios([50.0], [50.0])
        savings = comparison['savings']
        assert savings['distance_saved_km'] == pytest.approx(0.0)
        assert savings['cost_saved'] == pytest.approx(0.0)
        assert savings['cost_reduction_percent'] == pytest.approx(0.0)
