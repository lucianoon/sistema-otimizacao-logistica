"""
Módulo de Cálculo de Custos Logísticos
Adaptado para a realidade brasileira
"""

from typing import Dict, List
import numpy as np


class CostCalculator:
    """
    Classe para calcular custos logísticos no contexto brasileiro.
    """
    
    # Valores médios brasileiros (2025)
    DEFAULT_FUEL_PRICE_PER_LITER = 6.50  # R$ por litro (gasolina/diesel)
    DEFAULT_FUEL_CONSUMPTION = 8.0  # km por litro (média caminhões)
    DEFAULT_COST_PER_KM = 2.50  # R$ por km (inclui manutenção, pneus, etc)
    DEFAULT_DRIVER_COST_PER_HOUR = 25.00  # R$ por hora
    DEFAULT_VEHICLE_DEPRECIATION_PER_KM = 0.50  # R$ por km
    DEFAULT_TOLL_COST_PER_100KM = 15.00  # R$ por 100km (média)
    DEFAULT_AVERAGE_SPEED = 60.0  # km/h (velocidade média em rotas)
    
    # Emissões de CO2
    CO2_EMISSION_PER_LITER = 2.68  # kg de CO2 por litro de diesel
    
    def __init__(
        self,
        fuel_price_per_liter: float = DEFAULT_FUEL_PRICE_PER_LITER,
        fuel_consumption_km_per_liter: float = DEFAULT_FUEL_CONSUMPTION,
        cost_per_km: float = DEFAULT_COST_PER_KM,
        driver_cost_per_hour: float = DEFAULT_DRIVER_COST_PER_HOUR,
        vehicle_depreciation_per_km: float = DEFAULT_VEHICLE_DEPRECIATION_PER_KM,
        toll_cost_per_100km: float = DEFAULT_TOLL_COST_PER_100KM,
        average_speed_kmh: float = DEFAULT_AVERAGE_SPEED,
        include_tolls: bool = True
    ):
        """
        Inicializa o calculador de custos.
        
        Args:
            fuel_price_per_liter: Preço do combustível em R$ por litro
            fuel_consumption_km_per_liter: Consumo em km por litro
            cost_per_km: Custo operacional adicional por km (R$)
            driver_cost_per_hour: Custo do motorista por hora (R$)
            vehicle_depreciation_per_km: Depreciação do veículo por km (R$)
            toll_cost_per_100km: Custo médio de pedágios por 100km (R$)
            average_speed_kmh: Velocidade média em km/h
            include_tolls: Se deve incluir custos de pedágios
        """
        self.fuel_price_per_liter = fuel_price_per_liter
        self.fuel_consumption_km_per_liter = fuel_consumption_km_per_liter
        self.cost_per_km = cost_per_km
        self.driver_cost_per_hour = driver_cost_per_hour
        self.vehicle_depreciation_per_km = vehicle_depreciation_per_km
        self.toll_cost_per_100km = toll_cost_per_100km
        self.average_speed_kmh = average_speed_kmh
        self.include_tolls = include_tolls
    
    def calculate_fuel_cost(self, distance_km: float) -> float:
        """
        Calcula o custo de combustível.
        
        Args:
            distance_km: Distância em quilômetros
            
        Returns:
            Custo de combustível em R$
        """
        liters_consumed = distance_km / self.fuel_consumption_km_per_liter
        return liters_consumed * self.fuel_price_per_liter
    
    def calculate_time_hours(self, distance_km: float) -> float:
        """
        Calcula o tempo de viagem em horas.
        
        Args:
            distance_km: Distância em quilômetros
            
        Returns:
            Tempo em horas
        """
        return distance_km / self.average_speed_kmh
    
    def calculate_driver_cost(self, distance_km: float) -> float:
        """
        Calcula o custo do motorista.
        
        Args:
            distance_km: Distância em quilômetros
            
        Returns:
            Custo do motorista em R$
        """
        time_hours = self.calculate_time_hours(distance_km)
        return time_hours * self.driver_cost_per_hour
    
    def calculate_depreciation_cost(self, distance_km: float) -> float:
        """
        Calcula o custo de depreciação do veículo.
        
        Args:
            distance_km: Distância em quilômetros
            
        Returns:
            Custo de depreciação em R$
        """
        return distance_km * self.vehicle_depreciation_per_km
    
    def calculate_toll_cost(self, distance_km: float) -> float:
        """
        Calcula o custo estimado de pedágios.
        
        Args:
            distance_km: Distância em quilômetros
            
        Returns:
            Custo de pedágios em R$
        """
        if not self.include_tolls:
            return 0.0
        return (distance_km / 100.0) * self.toll_cost_per_100km
    
    def calculate_operational_cost(self, distance_km: float) -> float:
        """
        Calcula o custo operacional adicional.
        
        Args:
            distance_km: Distância em quilômetros
            
        Returns:
            Custo operacional em R$
        """
        return distance_km * self.cost_per_km
    
    def calculate_total_cost(self, distance_km: float) -> Dict[str, float]:
        """
        Calcula o custo total detalhado.
        
        Args:
            distance_km: Distância em quilômetros
            
        Returns:
            Dicionário com breakdown de custos
        """
        fuel_cost = self.calculate_fuel_cost(distance_km)
        driver_cost = self.calculate_driver_cost(distance_km)
        depreciation_cost = self.calculate_depreciation_cost(distance_km)
        toll_cost = self.calculate_toll_cost(distance_km)
        operational_cost = self.calculate_operational_cost(distance_km)
        
        total_cost = (
            fuel_cost + 
            driver_cost + 
            depreciation_cost + 
            toll_cost + 
            operational_cost
        )
        
        return {
            'distance_km': distance_km,
            'fuel_cost': fuel_cost,
            'driver_cost': driver_cost,
            'depreciation_cost': depreciation_cost,
            'toll_cost': toll_cost,
            'operational_cost': operational_cost,
            'total_cost': total_cost,
            'time_hours': self.calculate_time_hours(distance_km)
        }
    
    def calculate_co2_emissions(self, distance_km: float) -> float:
        """
        Calcula as emissões de CO2.
        
        Args:
            distance_km: Distância em quilômetros
            
        Returns:
            Emissões de CO2 em kg
        """
        liters_consumed = distance_km / self.fuel_consumption_km_per_liter
        return liters_consumed * self.CO2_EMISSION_PER_LITER
    
    def calculate_route_costs(self, route_distances_km: List[float]) -> Dict:
        """
        Calcula custos para múltiplas rotas.
        
        Args:
            route_distances_km: Lista de distâncias de rotas em km
            
        Returns:
            Dicionário com custos agregados
        """
        total_distance = sum(route_distances_km)
        route_costs = [self.calculate_total_cost(dist) for dist in route_distances_km]
        
        total_fuel_cost = sum(rc['fuel_cost'] for rc in route_costs)
        total_driver_cost = sum(rc['driver_cost'] for rc in route_costs)
        total_depreciation = sum(rc['depreciation_cost'] for rc in route_costs)
        total_toll_cost = sum(rc['toll_cost'] for rc in route_costs)
        total_operational = sum(rc['operational_cost'] for rc in route_costs)
        total_cost = sum(rc['total_cost'] for rc in route_costs)
        total_time = sum(rc['time_hours'] for rc in route_costs)
        total_co2 = self.calculate_co2_emissions(total_distance)
        
        return {
            'total_distance_km': total_distance,
            'total_fuel_cost': total_fuel_cost,
            'total_driver_cost': total_driver_cost,
            'total_depreciation_cost': total_depreciation,
            'total_toll_cost': total_toll_cost,
            'total_operational_cost': total_operational,
            'total_cost': total_cost,
            'total_time_hours': total_time,
            'total_co2_kg': total_co2,
            'num_routes': len(route_distances_km),
            'route_costs': route_costs,
            'average_cost_per_route': total_cost / len(route_distances_km) if route_distances_km else 0,
            'cost_per_km': total_cost / total_distance if total_distance > 0 else 0
        }
    
    def compare_scenarios(
        self, 
        scenario1_distances: List[float],
        scenario2_distances: List[float],
        scenario1_name: str = "Cenário 1",
        scenario2_name: str = "Cenário 2"
    ) -> Dict:
        """
        Compara dois cenários de roteamento.
        
        Args:
            scenario1_distances: Distâncias do cenário 1
            scenario2_distances: Distâncias do cenário 2
            scenario1_name: Nome do cenário 1
            scenario2_name: Nome do cenário 2
            
        Returns:
            Dicionário com comparação detalhada
        """
        costs1 = self.calculate_route_costs(scenario1_distances)
        costs2 = self.calculate_route_costs(scenario2_distances)
        
        savings = {
            'distance_saved_km': costs1['total_distance_km'] - costs2['total_distance_km'],
            'cost_saved': costs1['total_cost'] - costs2['total_cost'],
            'time_saved_hours': costs1['total_time_hours'] - costs2['total_time_hours'],
            'co2_saved_kg': costs1['total_co2_kg'] - costs2['total_co2_kg'],
            'fuel_cost_saved': costs1['total_fuel_cost'] - costs2['total_fuel_cost'],
        }
        
        if costs1['total_cost'] > 0:
            savings['cost_reduction_percent'] = (savings['cost_saved'] / costs1['total_cost']) * 100
        else:
            savings['cost_reduction_percent'] = 0
        
        return {
            scenario1_name: costs1,
            scenario2_name: costs2,
            'savings': savings
        }
    
    def print_cost_breakdown(self, costs: Dict):
        """
        Imprime breakdown de custos formatado.
        
        Args:
            costs: Dicionário de custos retornado por calculate_route_costs
        """
        print(f"\n{'='*60}")
        print(f"ANÁLISE DE CUSTOS LOGÍSTICOS")
        print(f"{'='*60}")
        print(f"Distância Total: {costs['total_distance_km']:.2f} km")
        print(f"Tempo Total: {costs['total_time_hours']:.2f} horas")
        print(f"Número de Rotas: {costs['num_routes']}")
        print(f"\n{'CUSTOS DETALHADOS':^60}")
        print(f"{'-'*60}")
        print(f"Combustível:        R$ {costs['total_fuel_cost']:>10,.2f}")
        print(f"Motorista:          R$ {costs['total_driver_cost']:>10,.2f}")
        print(f"Depreciação:        R$ {costs['total_depreciation_cost']:>10,.2f}")
        print(f"Pedágios:           R$ {costs['total_toll_cost']:>10,.2f}")
        print(f"Operacional:        R$ {costs['total_operational_cost']:>10,.2f}")
        print(f"{'-'*60}")
        print(f"CUSTO TOTAL:        R$ {costs['total_cost']:>10,.2f}")
        print(f"{'-'*60}")
        print(f"Custo por km:       R$ {costs['cost_per_km']:>10,.2f}")
        print(f"Custo por rota:     R$ {costs['average_cost_per_route']:>10,.2f}")
        print(f"\n{'IMPACTO AMBIENTAL':^60}")
        print(f"{'-'*60}")
        print(f"Emissões CO2:       {costs['total_co2_kg']:>10,.2f} kg")
        print(f"{'='*60}\n")

