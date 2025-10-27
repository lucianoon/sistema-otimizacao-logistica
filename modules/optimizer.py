"""
Módulo de Otimização de Rotas usando OR-Tools
Sistema de Otimização Logística para o Brasil
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
from typing import Dict, List, Tuple, Optional


class VRPOptimizer:
    """
    Classe para resolver problemas de roteamento de veículos (VRP)
    usando Google OR-Tools.
    """
    
    def __init__(
        self,
        distance_matrix: np.ndarray,
        num_vehicles: int,
        depot_index: int = 0,
        vehicle_capacities: Optional[List[int]] = None,
        demands: Optional[List[int]] = None,
        time_windows: Optional[List[Tuple[int, int]]] = None,
        max_distance_per_vehicle: int = 100000
    ):
        """
        Inicializa o otimizador VRP.
        
        Args:
            distance_matrix: Matriz de distâncias entre localizações (em metros)
            num_vehicles: Número de veículos disponíveis
            depot_index: Índice do depósito (ponto de partida/chegada)
            vehicle_capacities: Lista com capacidade de cada veículo (opcional)
            demands: Lista com demanda de cada localização (opcional)
            time_windows: Lista de tuplas (início, fim) para janelas de tempo (opcional)
            max_distance_per_vehicle: Distância máxima por veículo em metros
        """
        self.distance_matrix = distance_matrix
        self.num_vehicles = num_vehicles
        self.depot_index = depot_index
        self.vehicle_capacities = vehicle_capacities
        self.demands = demands
        self.time_windows = time_windows
        self.max_distance_per_vehicle = max_distance_per_vehicle
        self.num_locations = len(distance_matrix)
        
        # Validações
        self._validate_inputs()
        
        # Objetos do OR-Tools
        self.manager = None
        self.routing = None
        self.solution = None
        
    def _validate_inputs(self):
        """Valida os dados de entrada."""
        if self.distance_matrix.shape[0] != self.distance_matrix.shape[1]:
            raise ValueError("A matriz de distâncias deve ser quadrada")
        
        if self.depot_index >= self.num_locations:
            raise ValueError("Índice do depósito inválido")
        
        if self.vehicle_capacities and len(self.vehicle_capacities) != self.num_vehicles:
            raise ValueError("Número de capacidades deve corresponder ao número de veículos")
        
        if self.demands and len(self.demands) != self.num_locations:
            raise ValueError("Número de demandas deve corresponder ao número de localizações")
    
    def _create_data_model(self) -> Dict:
        """Cria o modelo de dados para o OR-Tools."""
        data = {
            'distance_matrix': self.distance_matrix.tolist(),
            'num_vehicles': self.num_vehicles,
            'depot': self.depot_index
        }
        
        if self.vehicle_capacities:
            data['vehicle_capacities'] = self.vehicle_capacities
        
        if self.demands:
            data['demands'] = self.demands
        
        if self.time_windows:
            data['time_windows'] = self.time_windows
        
        return data
    
    def _distance_callback(self, from_index: int, to_index: int) -> int:
        """
        Retorna a distância entre dois nós.
        
        Args:
            from_index: Índice de origem
            to_index: Índice de destino
            
        Returns:
            Distância entre os nós
        """
        from_node = self.manager.IndexToNode(from_index)
        to_node = self.manager.IndexToNode(to_index)
        return int(self.distance_matrix[from_node][to_node])
    
    def _demand_callback(self, from_index: int) -> int:
        """
        Retorna a demanda de um nó.
        
        Args:
            from_index: Índice do nó
            
        Returns:
            Demanda do nó
        """
        from_node = self.manager.IndexToNode(from_index)
        return self.demands[from_node]
    
    def solve(
        self,
        time_limit_seconds: int = 30,
        strategy: str = 'PATH_CHEAPEST_ARC',
        local_search: Optional[str] = 'GUIDED_LOCAL_SEARCH'
    ) -> bool:
        import time
        start_time = time.time()
        """
        Resolve o problema de roteamento.
        
        Args:
            time_limit_seconds: Tempo limite para busca em segundos
            strategy: Estratégia de primeira solução
            local_search: Metaheurística de busca local
            
        Returns:
            True se encontrou solução, False caso contrário
        """
        data = self._create_data_model()
        
        # Criar o index manager
        self.manager = pywrapcp.RoutingIndexManager(
            len(data['distance_matrix']),
            data['num_vehicles'],
            data['depot']
        )
        
        # Criar o modelo de roteamento
        self.routing = pywrapcp.RoutingModel(self.manager)
        
        # Registrar callback de distância
        transit_callback_index = self.routing.RegisterTransitCallback(
            lambda from_index, to_index: self._distance_callback(from_index, to_index)
        )
        
        # Definir custo de arco
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        # Adicionar dimensão de distância
        dimension_name = 'Distance'
        self.routing.AddDimension(
            transit_callback_index,
            0,  # sem folga
            self.max_distance_per_vehicle,  # distância máxima por veículo
            True,  # começar acumulado em zero
            dimension_name
        )
        distance_dimension = self.routing.GetDimensionOrDie(dimension_name)
        # Definir custo para minimizar a maior rota
        distance_dimension.SetGlobalSpanCostCoefficient(100)
        
        # Adicionar restrições de capacidade se fornecidas
        if self.vehicle_capacities and self.demands:
            demand_callback_index = self.routing.RegisterUnaryTransitCallback(
                lambda from_index: self._demand_callback(from_index)
            )
            self.routing.AddDimensionWithVehicleCapacity(
                demand_callback_index,
                0,  # sem folga de capacidade
                self.vehicle_capacities,  # capacidades dos veículos
                True,  # começar acumulado em zero
                'Capacity'
            )
        
        # Configurar parâmetros de busca
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        
        # Estratégia de primeira solução
        strategy_map = {
            'PATH_CHEAPEST_ARC': routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC,
            'PATH_MOST_CONSTRAINED_ARC': routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC,
            'SAVINGS': routing_enums_pb2.FirstSolutionStrategy.SAVINGS,
            'SWEEP': routing_enums_pb2.FirstSolutionStrategy.SWEEP,
            'CHRISTOFIDES': routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES,
            'PARALLEL_CHEAPEST_INSERTION': routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION,
            'LOCAL_CHEAPEST_INSERTION': routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_INSERTION,
        }
        search_parameters.first_solution_strategy = strategy_map.get(
            strategy, 
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        
        # Metaheurística de busca local
        if local_search:
            local_search_map = {
                'GUIDED_LOCAL_SEARCH': routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH,
                'SIMULATED_ANNEALING': routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING,
                'TABU_SEARCH': routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH,
                'GENERIC_TABU_SEARCH': routing_enums_pb2.LocalSearchMetaheuristic.GENERIC_TABU_SEARCH,
            }
            search_parameters.local_search_metaheuristic = local_search_map.get(
                local_search,
                routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
            )
        
        # Tempo limite
        search_parameters.time_limit.seconds = time_limit_seconds
        
        # Configurações adicionais para melhorar a busca
        search_parameters.log_search = False
        
        # Resolver o problema
        self.solution = self.routing.SolveWithParameters(search_parameters)
        
        # Armazenar tempo de execução
        self.execution_time = time.time() - start_time
        
        # Retornar se encontrou solução
        return self.solution is not None
    
    def get_routes(self) -> List[List[int]]:
        """
        Extrai as rotas da solução.
        
        Returns:
            Lista de rotas, onde cada rota é uma lista de índices de localizações
        """
        if not self.solution:
            return []
        
        routes = []
        for vehicle_id in range(self.num_vehicles):
            index = self.routing.Start(vehicle_id)
            route = []
            
            while not self.routing.IsEnd(index):
                node_index = self.manager.IndexToNode(index)
                route.append(node_index)
                index = self.solution.Value(self.routing.NextVar(index))
            
            # Adicionar o depósito final
            route.append(self.manager.IndexToNode(index))
            
            # Só adicionar rotas que visitam pelo menos um cliente
            if len(route) > 2:  # Mais que depósito inicial e final
                routes.append(route)
        
        return routes
    
    def get_route_distance(self, route: List[int]) -> float:
        """
        Calcula a distância total de uma rota.
        
        Args:
            route: Lista de índices de localizações
            
        Returns:
            Distância total em metros
        """
        distance = 0
        for i in range(len(route) - 1):
            distance += self.distance_matrix[route[i]][route[i + 1]]
        return distance
    
    def get_metrics(self) -> Dict:
        """
        Calcula métricas da solução.
        
        Returns:
            Dicionário com métricas da solução
        """
        if not self.solution:
            return {}
        
        routes = self.get_routes()
        total_distance = 0
        max_route_distance = 0
        route_distances = []
        
        for route in routes:
            distance = self.get_route_distance(route)
            route_distances.append(distance)
            total_distance += distance
            max_route_distance = max(max_route_distance, distance)
        
        metrics = {
            'objective_value': self.solution.ObjectiveValue(),
            'total_distance': total_distance,
            'max_route_distance': max_route_distance,
            'num_routes': len(routes),
            'num_vehicles_used': len(routes),
            'route_distances': route_distances,
            'routes': routes,
            'execution_time': getattr(self, 'execution_time', 0),
            'algorithm': 'OR-Tools'
        }
        
        # Adicionar métricas de capacidade se disponíveis
        if self.vehicle_capacities and self.demands:
            route_loads = []
            for route in routes:
                load = sum(self.demands[node] for node in route if node != self.depot_index)
                route_loads.append(load)
            metrics['route_loads'] = route_loads
        
        return metrics
    
    def print_solution(self):
        """Imprime a solução de forma formatada."""
        if not self.solution:
            print("Nenhuma solução encontrada!")
            return
        
        metrics = self.get_metrics()
        routes = metrics['routes']
        
        print(f"\n{'='*60}")
        print(f"SOLUÇÃO DE ROTEAMENTO")
        print(f"{'='*60}")
        print(f"Valor Objetivo: {metrics['objective_value']}")
        print(f"Distância Total: {metrics['total_distance']/1000:.2f} km")
        print(f"Maior Rota: {metrics['max_route_distance']/1000:.2f} km")
        print(f"Veículos Utilizados: {metrics['num_vehicles_used']}/{self.num_vehicles}")
        print(f"{'='*60}\n")
        
        for vehicle_id, route in enumerate(routes):
            distance = metrics['route_distances'][vehicle_id]
            print(f"Veículo {vehicle_id + 1}:")
            print(f"  Rota: {' -> '.join(map(str, route))}")
            print(f"  Distância: {distance/1000:.2f} km")
            
            if 'route_loads' in metrics:
                load = metrics['route_loads'][vehicle_id]
                capacity = self.vehicle_capacities[vehicle_id] if vehicle_id < len(self.vehicle_capacities) else 'N/A'
                print(f"  Carga: {load}/{capacity}")
            
            print()

