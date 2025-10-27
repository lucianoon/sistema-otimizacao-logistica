"""
Módulo de Manipulação de Dados
Processamento de endereços, coordenadas e dados de entrada
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Optional
from math import radians, cos, sin, asin, sqrt


class DataHandler:
    """
    Classe para manipular dados de entrada do sistema de otimização.
    """
    
    @staticmethod
    def haversine_distance(
        lat1: float, lon1: float, 
        lat2: float, lon2: float
    ) -> float:
        """
        Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine.
        
        Args:
            lat1, lon1: Latitude e longitude do ponto 1
            lat2, lon2: Latitude e longitude do ponto 2
            
        Returns:
            Distância em metros
        """
        # Converter para radianos
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        # Fórmula de Haversine
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Raio da Terra em metros
        r = 6371000
        
        return c * r
    
    @staticmethod
    def euclidean_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """
        Calcula a distância euclidiana entre dois pontos.
        
        Args:
            x1, y1: Coordenadas do ponto 1
            x2, y2: Coordenadas do ponto 2
            
        Returns:
            Distância euclidiana
        """
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    @staticmethod
    def create_distance_matrix(
        locations: List[Tuple[float, float]],
        method: str = 'haversine'
    ) -> np.ndarray:
        """
        Cria uma matriz de distâncias entre localizações.
        
        Args:
            locations: Lista de tuplas (latitude, longitude) ou (x, y)
            method: Método de cálculo ('haversine' ou 'euclidean')
            
        Returns:
            Matriz de distâncias numpy array
        """
        n = len(locations)
        distance_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    distance_matrix[i][j] = 0
                else:
                    if method == 'haversine':
                        distance_matrix[i][j] = DataHandler.haversine_distance(
                            locations[i][0], locations[i][1],
                            locations[j][0], locations[j][1]
                        )
                    elif method == 'euclidean':
                        distance_matrix[i][j] = DataHandler.euclidean_distance(
                            locations[i][0], locations[i][1],
                            locations[j][0], locations[j][1]
                        )
                    else:
                        raise ValueError(f"Método '{method}' não suportado")
        
        return distance_matrix
    
    @staticmethod
    def load_locations_from_csv(
        filepath: str,
        lat_column: str = 'latitude',
        lon_column: str = 'longitude',
        name_column: str = 'nome',
        demand_column: Optional[str] = None
    ) -> Dict:
        """
        Carrega localizações de um arquivo CSV.
        
        Args:
            filepath: Caminho do arquivo CSV
            lat_column: Nome da coluna de latitude
            lon_column: Nome da coluna de longitude
            name_column: Nome da coluna de identificação
            demand_column: Nome da coluna de demanda (opcional)
            
        Returns:
            Dicionário com dados processados
        """
        df = pd.read_csv(filepath)
        
        # Validar colunas
        required_columns = [lat_column, lon_column, name_column]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Coluna '{col}' não encontrada no CSV")
        
        locations = list(zip(df[lat_column], df[lon_column]))
        names = df[name_column].tolist()
        
        result = {
            'locations': locations,
            'names': names,
            'dataframe': df
        }
        
        if demand_column and demand_column in df.columns:
            result['demands'] = df[demand_column].tolist()
        
        return result
    
    @staticmethod
    def load_locations_from_dataframe(
        df: pd.DataFrame,
        lat_column: str = 'latitude',
        lon_column: str = 'longitude',
        name_column: str = 'nome',
        demand_column: Optional[str] = None
    ) -> Dict:
        """
        Carrega localizações de um DataFrame pandas.
        
        Args:
            df: DataFrame com dados
            lat_column: Nome da coluna de latitude
            lon_column: Nome da coluna de longitude
            name_column: Nome da coluna de identificação
            demand_column: Nome da coluna de demanda (opcional)
            
        Returns:
            Dicionário com dados processados
        """
        # Validar colunas
        required_columns = [lat_column, lon_column, name_column]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Coluna '{col}' não encontrada no DataFrame")
        
        locations = list(zip(df[lat_column], df[lon_column]))
        names = df[name_column].tolist()
        
        result = {
            'locations': locations,
            'names': names,
            'dataframe': df
        }
        
        if demand_column and demand_column in df.columns:
            result['demands'] = df[demand_column].tolist()
        
        return result
    
    @staticmethod
    def create_sample_data(
        num_locations: int = 15,
        depot_location: Tuple[float, float] = (-23.5505, -46.6333),  # São Paulo
        radius_km: float = 50,
        include_demands: bool = False
    ) -> Dict:
        """
        Cria dados de exemplo para testes.
        
        Args:
            num_locations: Número de localizações (incluindo depósito)
            depot_location: Coordenadas do depósito (lat, lon)
            radius_km: Raio em km para gerar localizações
            include_demands: Se deve incluir demandas aleatórias
            
        Returns:
            Dicionário com dados de exemplo
        """
        np.random.seed(42)
        
        # Converter raio para graus (aproximadamente)
        radius_deg = radius_km / 111.0  # 1 grau ≈ 111 km
        
        locations = [depot_location]
        names = ['Depósito']
        
        # Gerar localizações aleatórias ao redor do depósito
        for i in range(1, num_locations):
            # Gerar ângulo e raio aleatórios
            angle = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(0, radius_deg)
            
            # Calcular nova posição
            lat = depot_location[0] + r * np.cos(angle)
            lon = depot_location[1] + r * np.sin(angle)
            
            locations.append((lat, lon))
            names.append(f'Cliente {i}')
        
        result = {
            'locations': locations,
            'names': names
        }
        
        if include_demands:
            # Depósito tem demanda 0, clientes têm demandas aleatórias
            demands = [0] + list(np.random.randint(1, 20, num_locations - 1))
            result['demands'] = demands
        
        return result
    
    @staticmethod
    def validate_locations(locations: List[Tuple[float, float]]) -> bool:
        """
        Valida se as coordenadas são válidas.
        
        Args:
            locations: Lista de tuplas (latitude, longitude)
            
        Returns:
            True se válido, False caso contrário
        """
        for lat, lon in locations:
            if not (-90 <= lat <= 90):
                return False
            if not (-180 <= lon <= 180):
                return False
        return True
    
    @staticmethod
    def create_dataframe_from_routes(
        routes: List[List[int]],
        names: List[str],
        locations: List[Tuple[float, float]],
        route_distances: Optional[List[float]] = None
    ) -> pd.DataFrame:
        """
        Cria um DataFrame com informações das rotas.
        
        Args:
            routes: Lista de rotas
            names: Lista de nomes das localizações
            locations: Lista de coordenadas
            route_distances: Lista de distâncias das rotas (opcional)
            
        Returns:
            DataFrame com informações das rotas
        """
        data = []
        
        for vehicle_id, route in enumerate(routes):
            for seq, location_idx in enumerate(route):
                row = {
                    'veiculo': vehicle_id + 1,
                    'sequencia': seq,
                    'localizacao_id': location_idx,
                    'nome': names[location_idx] if location_idx < len(names) else f'Local {location_idx}',
                    'latitude': locations[location_idx][0],
                    'longitude': locations[location_idx][1]
                }
                
                if route_distances:
                    row['distancia_rota_km'] = route_distances[vehicle_id] / 1000
                
                data.append(row)
        
        return pd.DataFrame(data)
    
    @staticmethod
    def export_routes_to_csv(
        routes: List[List[int]],
        names: List[str],
        locations: List[Tuple[float, float]],
        filepath: str,
        route_distances: Optional[List[float]] = None
    ):
        """
        Exporta rotas para um arquivo CSV.
        
        Args:
            routes: Lista de rotas
            names: Lista de nomes das localizações
            locations: Lista de coordenadas
            filepath: Caminho do arquivo de saída
            route_distances: Lista de distâncias das rotas (opcional)
        """
        df = DataHandler.create_dataframe_from_routes(
            routes, names, locations, route_distances
        )
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
    
    @staticmethod
    def format_distance(distance_meters: float) -> str:
        """
        Formata distância para exibição.
        
        Args:
            distance_meters: Distância em metros
            
        Returns:
            String formatada
        """
        if distance_meters < 1000:
            return f"{distance_meters:.0f} m"
        else:
            return f"{distance_meters/1000:.2f} km"
    
    @staticmethod
    def format_time(time_hours: float) -> str:
        """
        Formata tempo para exibição.
        
        Args:
            time_hours: Tempo em horas
            
        Returns:
            String formatada
        """
        hours = int(time_hours)
        minutes = int((time_hours - hours) * 60)
        
        if hours > 0:
            return f"{hours}h {minutes}min"
        else:
            return f"{minutes}min"
    
    @staticmethod
    def format_currency(value: float) -> str:
        """
        Formata valor monetário em reais.
        
        Args:
            value: Valor em reais
            
        Returns:
            String formatada
        """
        return f"R$ {value:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')

