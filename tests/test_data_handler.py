"""Testes unitários para modules.data_handler.DataHandler."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from modules.data_handler import DataHandler

EXAMPLE_CSV = Path(__file__).resolve().parent.parent / 'data' / 'exemplo_clientes.csv'

SAO_PAULO = (-23.5505, -46.6333)
RIO_DE_JANEIRO = (-22.9068, -43.1729)


class TestDistances:
    def test_haversine_sp_to_rj(self):
        # Distância em linha reta SP -> RJ é de aproximadamente 357 km
        distance = DataHandler.haversine_distance(
            SAO_PAULO[0], SAO_PAULO[1], RIO_DE_JANEIRO[0], RIO_DE_JANEIRO[1]
        )
        assert distance == pytest.approx(357_000, rel=0.02)

    def test_haversine_same_point_is_zero(self):
        distance = DataHandler.haversine_distance(
            SAO_PAULO[0], SAO_PAULO[1], SAO_PAULO[0], SAO_PAULO[1]
        )
        assert distance == pytest.approx(0.0)

    def test_haversine_is_symmetric(self):
        d1 = DataHandler.haversine_distance(
            SAO_PAULO[0], SAO_PAULO[1], RIO_DE_JANEIRO[0], RIO_DE_JANEIRO[1]
        )
        d2 = DataHandler.haversine_distance(
            RIO_DE_JANEIRO[0], RIO_DE_JANEIRO[1], SAO_PAULO[0], SAO_PAULO[1]
        )
        assert d1 == pytest.approx(d2)

    def test_euclidean_distance(self):
        assert DataHandler.euclidean_distance(0, 0, 3, 4) == pytest.approx(5.0)


class TestDistanceMatrix:
    def test_matrix_shape_and_diagonal(self):
        locations = [SAO_PAULO, RIO_DE_JANEIRO, (-19.9167, -43.9345)]
        matrix = DataHandler.create_distance_matrix(locations, method='haversine')

        assert matrix.shape == (3, 3)
        assert np.allclose(np.diag(matrix), 0.0)
        # Haversine é simétrica
        assert np.allclose(matrix, matrix.T)
        # Elementos fora da diagonal são positivos
        off_diagonal = matrix[~np.eye(3, dtype=bool)]
        assert (off_diagonal > 0).all()

    def test_euclidean_method(self):
        locations = [(0, 0), (3, 4)]
        matrix = DataHandler.create_distance_matrix(locations, method='euclidean')
        assert matrix[0][1] == pytest.approx(5.0)

    def test_invalid_method_raises(self):
        with pytest.raises(ValueError):
            DataHandler.create_distance_matrix([(0, 0), (1, 1)], method='manhattan')


class TestCsvLoading:
    def test_load_example_csv(self):
        data = DataHandler.load_locations_from_csv(
            str(EXAMPLE_CSV),
            lat_column='latitude',
            lon_column='longitude',
            name_column='nome',
            demand_column='demanda',
        )

        assert len(data['locations']) == 16
        assert len(data['names']) == 16
        assert data['names'][0] == 'Depósito Central'
        assert data['locations'][0] == (-23.5505, -46.6333)
        # Depósito tem demanda 0; demanda total dos clientes é 257
        assert data['demands'][0] == 0
        assert sum(data['demands'][1:]) == 257
        assert DataHandler.validate_locations(data['locations'])

    def test_load_csv_missing_column_raises(self):
        with pytest.raises(ValueError, match='inexistente'):
            DataHandler.load_locations_from_csv(
                str(EXAMPLE_CSV),
                lat_column='latitude',
                lon_column='longitude',
                name_column='inexistente',
            )

    def test_load_from_dataframe(self):
        df = pd.DataFrame({
            'nome': ['Depósito', 'Cliente A'],
            'latitude': [-23.55, -23.52],
            'longitude': [-46.63, -46.60],
            'demanda': [0, 10],
        })
        data = DataHandler.load_locations_from_dataframe(df, demand_column='demanda')
        assert data['locations'] == [(-23.55, -46.63), (-23.52, -46.60)]
        assert data['names'] == ['Depósito', 'Cliente A']
        assert data['demands'] == [0, 10]

    def test_load_from_dataframe_missing_column_raises(self):
        df = pd.DataFrame({'nome': ['A'], 'latitude': [0.0]})
        with pytest.raises(ValueError):
            DataHandler.load_locations_from_dataframe(df)


class TestValidation:
    def test_valid_locations(self):
        assert DataHandler.validate_locations([SAO_PAULO, RIO_DE_JANEIRO]) is True

    def test_invalid_latitude(self):
        assert DataHandler.validate_locations([(100.0, 0.0)]) is False

    def test_invalid_longitude(self):
        assert DataHandler.validate_locations([(0.0, 200.0)]) is False

    def test_boundary_values_are_valid(self):
        assert DataHandler.validate_locations([(90.0, 180.0), (-90.0, -180.0)]) is True


class TestSampleData:
    def test_sample_data_is_deterministic(self):
        data1 = DataHandler.create_sample_data(num_locations=10)
        data2 = DataHandler.create_sample_data(num_locations=10)
        assert data1['locations'] == data2['locations']

    def test_sample_data_structure(self):
        data = DataHandler.create_sample_data(
            num_locations=8, include_demands=True
        )
        assert len(data['locations']) == 8
        assert len(data['names']) == 8
        assert data['names'][0] == 'Depósito'
        assert data['demands'][0] == 0
        assert all(d > 0 for d in data['demands'][1:])
        assert DataHandler.validate_locations(data['locations'])


class TestRoutesDataframe:
    def test_create_dataframe_from_routes(self):
        routes = [[0, 1, 0], [0, 2, 0]]
        names = ['Depósito', 'Cliente 1', 'Cliente 2']
        locations = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
        route_distances = [5000.0, 8000.0]

        df = DataHandler.create_dataframe_from_routes(
            routes, names, locations, route_distances
        )

        assert len(df) == 6  # 3 paradas por rota, 2 rotas
        assert set(df['veiculo'].unique()) == {1, 2}
        assert df.iloc[0]['nome'] == 'Depósito'
        assert df.iloc[1]['nome'] == 'Cliente 1'
        assert df.iloc[0]['distancia_rota_km'] == pytest.approx(5.0)


class TestFormatting:
    def test_format_distance_meters(self):
        assert DataHandler.format_distance(500) == '500 m'

    def test_format_distance_kilometers(self):
        assert DataHandler.format_distance(45678) == '45.68 km'

    def test_format_time_with_hours(self):
        assert DataHandler.format_time(3.75) == '3h 45min'

    def test_format_time_minutes_only(self):
        assert DataHandler.format_time(0.5) == '30min'

    def test_format_currency_brazilian(self):
        assert DataHandler.format_currency(1234.56) == 'R$ 1.234,56'
