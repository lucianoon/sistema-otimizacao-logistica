"""
Algoritmo Nearest Neighbor (Vizinho Mais Próximo)
Heurística simples e rápida para VRP
"""

import numpy as np
from typing import List, Dict


class NearestNeighborOptimizer:
    """
    Implementação do algoritmo Nearest Neighbor para VRP.
    
    Este é um algoritmo guloso que constrói rotas escolhendo sempre
    o cliente mais próximo não visitado.
    """
    
    def __init__(
        self,
        distance_matrix: np.ndarray,
        num_vehicles: int,
        depot_index: int = 0,
        max_customers_per_route: int = None
    ):
        """
        Inicializa o otimizador Nearest Neighbor.
        
        Args:
            distance_matrix: Matriz de distâncias entre localizações
            num_vehicles: Número de veículos disponíveis
            depot_index: Índice do depósito
            max_customers_per_route: Máximo de clientes por rota (opcional)
        """
        self.distance_matrix = distance_matrix
        self.num_vehicles = num_vehicles
        self.depot_index = depot_index
        self.num_locations = len(distance_matrix)
        self.max_customers_per_route = max_customers_per_route
        
        if self.max_customers_per_route is None:
            # Distribuir clientes igualmente entre veículos
            num_customers = self.num_locations - 1
            self.max_customers_per_route = (num_customers // num_vehicles) + 2
        
        self.solution = None
        self.execution_time = 0
    
    def solve(self, **kwargs) -> bool:
        """
        Resolve o problema usando o algoritmo Nearest Neighbor.
        
        Returns:
            True se encontrou solução, False caso contrário
        """
        import time
        start_time = time.time()
        
        # Conjunto de clientes não visitados
        unvisited = set(range(self.num_locations))
        unvisited.remove(self.depot_index)
        
        routes = []
        
        # Construir rota para cada veículo
        for vehicle_id in range(self.num_vehicles):
            if not unvisited:
                break
            
            route = [self.depot_index]
            current_location = self.depot_index
            customers_in_route = 0
            
            # Construir rota escolhendo sempre o mais próximo
            while unvisited and customers_in_route < self.max_customers_per_route:
                # Encontrar cliente mais próximo não visitado
                nearest_customer = min(
                    unvisited,
                    key=lambda x: self.distance_matrix[current_location][x]
                )
                
                # Adicionar à rota
                route.append(nearest_customer)
                unvisited.remove(nearest_customer)
                current_location = nearest_customer
                customers_in_route += 1
            
            # Retornar ao depósito
            route.append(self.depot_index)
            
            # Adicionar rota apenas se tiver clientes
            if len(route) > 2:
                routes.append(route)
        
        self.solution = routes
        self.execution_time = time.time() - start_time
        
        return True
    
    def get_routes(self) -> List[List[int]]:
        """
        Retorna as rotas da solução.
        
        Returns:
            Lista de rotas
        """
        return self.solution if self.solution else []
    
    def get_route_distance(self, route: List[int]) -> float:
        """
        Calcula a distância de uma rota.
        
        Args:
            route: Lista de índices da rota
            
        Returns:
            Distância total da rota
        """
        distance = 0
        for i in range(len(route) - 1):
            distance += self.distance_matrix[route[i]][route[i + 1]]
        return distance
    
    def get_metrics(self) -> Dict:
        """
        Calcula métricas da solução.
        
        Returns:
            Dicionário com métricas
        """
        if not self.solution:
            return {}
        
        routes = self.solution
        route_distances = []
        total_distance = 0
        
        for route in routes:
            distance = self.get_route_distance(route)
            route_distances.append(distance)
            total_distance += distance
        
        max_route_distance = max(route_distances) if route_distances else 0
        
        return {
            'objective_value': total_distance,
            'total_distance': total_distance,
            'max_route_distance': max_route_distance,
            'num_routes': len(routes),
            'num_vehicles_used': len(routes),
            'route_distances': route_distances,
            'routes': routes,
            'execution_time': self.execution_time,
            'algorithm': 'Nearest Neighbor'
        }
    
    def print_solution(self):
        """Imprime a solução de forma formatada."""
        if not self.solution:
            print("Nenhuma solução encontrada!")
            return
        
        metrics = self.get_metrics()
        routes = metrics['routes']
        
        print(f"\n{'='*60}")
        print(f"SOLUÇÃO - NEAREST NEIGHBOR")
        print(f"{'='*60}")
        print(f"Distância Total: {metrics['total_distance']/1000:.2f} km")
        print(f"Maior Rota: {metrics['max_route_distance']/1000:.2f} km")
        print(f"Veículos Utilizados: {metrics['num_vehicles_used']}/{self.num_vehicles}")
        print(f"Tempo de Execução: {metrics['execution_time']:.3f} segundos")
        print(f"{'='*60}\n")
        
        for vehicle_id, route in enumerate(routes):
            distance = metrics['route_distances'][vehicle_id]
            print(f"Veículo {vehicle_id + 1}:")
            print(f"  Rota: {' -> '.join(map(str, route))}")
            print(f"  Distância: {distance/1000:.2f} km")
            print()

