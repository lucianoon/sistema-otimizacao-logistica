"""
Script de Teste do Sistema de Otimização Logística
Testa todas as funcionalidades principais
"""

import sys
import numpy as np
from modules.optimizer import VRPOptimizer
from modules.cost_calculator import CostCalculator
from modules.data_handler import DataHandler
from modules.visualizer import RouteVisualizer

def test_basic_vrp():
    """Testa otimização VRP básica."""
    print("\n" + "="*60)
    print("TESTE 1: VRP Básico (São Paulo)")
    print("="*60)
    
    # Criar dados de exemplo
    data = DataHandler.create_sample_data(
        num_locations=10,
        depot_location=(-23.5505, -46.6333),  # São Paulo
        radius_km=30,
        include_demands=False
    )
    
    locations = data['locations']
    names = data['names']
    
    print(f"✓ {len(locations)} localizações carregadas")
    
    # Criar matriz de distâncias
    distance_matrix = DataHandler.create_distance_matrix(locations, method='haversine')
    print(f"✓ Matriz de distâncias criada: {distance_matrix.shape}")
    
    # Criar otimizador
    optimizer = VRPOptimizer(
        distance_matrix=distance_matrix,
        num_vehicles=4,
        depot_index=0,
        max_distance_per_vehicle=100000
    )
    
    print("✓ Otimizador criado")
    
    # Resolver
    print("⏳ Resolvendo problema...")
    success = optimizer.solve(time_limit_seconds=60, local_search=None)
    
    if success:
        print("✅ Solução encontrada!")
        
        # Obter métricas
        metrics = optimizer.get_metrics()
        
        print(f"\nRESULTADOS:")
        print(f"  Distância Total: {metrics['total_distance']/1000:.2f} km")
        print(f"  Maior Rota: {metrics['max_route_distance']/1000:.2f} km")
        print(f"  Veículos Utilizados: {metrics['num_vehicles_used']}/4")
        print(f"  Número de Rotas: {metrics['num_routes']}")
        
        # Imprimir rotas
        print(f"\nROTAS:")
        routes = metrics['routes']
        for i, route in enumerate(routes):
            distance = metrics['route_distances'][i]
            route_names = " → ".join([names[idx] for idx in route])
            print(f"  Veículo {i+1}: {route_names}")
            print(f"    Distância: {distance/1000:.2f} km")
        
        return True
    else:
        print("❌ Não foi possível encontrar solução")
        return False

def test_cvrp():
    """Testa VRP com restrições de capacidade."""
    print("\n" + "="*60)
    print("TESTE 2: CVRP (Capacitated VRP)")
    print("="*60)
    
    # Criar dados com demandas
    data = DataHandler.create_sample_data(
        num_locations=8,
        depot_location=(-22.9068, -43.1729),  # Rio de Janeiro
        radius_km=30,
        include_demands=True
    )
    
    locations = data['locations']
    names = data['names']
    demands = data['demands']
    
    print(f"✓ {len(locations)} localizações com demandas carregadas")
    print(f"  Demanda total: {sum(demands[1:])} unidades")
    
    # Criar matriz de distâncias
    distance_matrix = DataHandler.create_distance_matrix(locations, method='haversine')
    
    # Configurar veículos
    num_vehicles = 2
    vehicle_capacities = [150, 150]
    
    # Criar otimizador
    optimizer = VRPOptimizer(
        distance_matrix=distance_matrix,
        num_vehicles=num_vehicles,
        depot_index=0,
        vehicle_capacities=vehicle_capacities,
        demands=demands,
        max_distance_per_vehicle=80000
    )
    
    print("✓ Otimizador CVRP criado")
    
    # Resolver
    print("⏳ Resolvendo problema...")
    success = optimizer.solve(time_limit_seconds=60, local_search=None)
    
    if success:
        print("✅ Solução encontrada!")
        
        metrics = optimizer.get_metrics()
        
        print(f"\nRESULTADOS:")
        print(f"  Distância Total: {metrics['total_distance']/1000:.2f} km")
        print(f"  Veículos Utilizados: {metrics['num_vehicles_used']}/{num_vehicles}")
        
        # Imprimir rotas com cargas
        print(f"\nROTAS E CARGAS:")
        routes = metrics['routes']
        route_loads = metrics['route_loads']
        
        for i, route in enumerate(routes):
            distance = metrics['route_distances'][i]
            load = route_loads[i]
            capacity = vehicle_capacities[i]
            utilization = (load / capacity) * 100
            
            route_names = " → ".join([names[idx] for idx in route])
            print(f"  Veículo {i+1}:")
            print(f"    Rota: {route_names}")
            print(f"    Distância: {distance/1000:.2f} km")
            print(f"    Carga: {load}/{capacity} ({utilization:.1f}% utilização)")
        
        return True
    else:
        print("❌ Não foi possível encontrar solução")
        return False

def test_cost_calculator():
    """Testa calculadora de custos."""
    print("\n" + "="*60)
    print("TESTE 3: Calculadora de Custos")
    print("="*60)
    
    # Criar calculadora com valores brasileiros
    calculator = CostCalculator(
        fuel_price_per_liter=6.50,
        fuel_consumption_km_per_liter=8.0,
        driver_cost_per_hour=25.0,
        include_tolls=True
    )
    
    print("✓ Calculadora criada com valores brasileiros")
    print(f"  Combustível: R$ 6,50/L")
    print(f"  Consumo: 8 km/L")
    print(f"  Motorista: R$ 25/h")
    
    # Simular rotas
    route_distances_km = [85.5, 92.3, 78.8]  # 3 rotas
    
    print(f"\n⏳ Calculando custos para {len(route_distances_km)} rotas...")
    
    costs = calculator.calculate_route_costs(route_distances_km)
    
    print("✅ Custos calculados!")
    
    print(f"\nRESULTADOS:")
    print(f"  Distância Total: {costs['total_distance_km']:.2f} km")
    print(f"  Tempo Total: {costs['total_time_hours']:.2f} horas")
    print(f"  Custo Total: R$ {costs['total_cost']:.2f}")
    print(f"\nDETALHAMENTO:")
    print(f"  Combustível: R$ {costs['total_fuel_cost']:.2f}")
    print(f"  Motorista: R$ {costs['total_driver_cost']:.2f}")
    print(f"  Depreciação: R$ {costs['total_depreciation_cost']:.2f}")
    print(f"  Pedágios: R$ {costs['total_toll_cost']:.2f}")
    print(f"  Operacional: R$ {costs['total_operational_cost']:.2f}")
    print(f"\nIMPACTO AMBIENTAL:")
    print(f"  Emissões CO2: {costs['total_co2_kg']:.2f} kg")
    
    return True

def test_data_handler():
    """Testa manipulação de dados."""
    print("\n" + "="*60)
    print("TESTE 4: Manipulação de Dados")
    print("="*60)
    
    # Testar cálculo de distâncias
    print("✓ Testando cálculo de distâncias...")
    
    # São Paulo para Rio de Janeiro
    sp = (-23.5505, -46.6333)
    rj = (-22.9068, -43.1729)
    
    distance = DataHandler.haversine_distance(sp[0], sp[1], rj[0], rj[1])
    print(f"  São Paulo → Rio de Janeiro: {distance/1000:.2f} km")
    
    # Testar validação
    print("✓ Testando validação de coordenadas...")
    
    valid_locations = [(-23.5505, -46.6333), (-22.9068, -43.1729)]
    invalid_locations = [(100, 200), (-22.9068, -43.1729)]
    
    is_valid = DataHandler.validate_locations(valid_locations)
    print(f"  Coordenadas válidas: {is_valid}")
    
    is_invalid = DataHandler.validate_locations(invalid_locations)
    print(f"  Coordenadas inválidas detectadas: {not is_invalid}")
    
    # Testar formatação
    print("✓ Testando formatação...")
    print(f"  Distância: {DataHandler.format_distance(45678)}")
    print(f"  Tempo: {DataHandler.format_time(3.75)}")
    print(f"  Moeda: {DataHandler.format_currency(1234.56)}")
    
    return True

def test_csv_loading():
    """Testa carregamento de CSV."""
    print("\n" + "="*60)
    print("TESTE 5: Carregamento de CSV")
    print("="*60)
    
    csv_path = "/home/ubuntu/sistema_otimizacao_logistica/data/exemplo_clientes.csv"
    
    try:
        print(f"⏳ Carregando {csv_path}...")
        
        data = DataHandler.load_locations_from_csv(
            csv_path,
            lat_column='latitude',
            lon_column='longitude',
            name_column='nome',
            demand_column='demanda'
        )
        
        print("✅ CSV carregado com sucesso!")
        
        locations = data['locations']
        names = data['names']
        demands = data['demands']
        
        print(f"\nDADOS CARREGADOS:")
        print(f"  Localizações: {len(locations)}")
        print(f"  Primeira localização: {names[0]} {locations[0]}")
        print(f"  Demanda total: {sum(demands[1:])} unidades")
        
        # Criar matriz de distâncias
        distance_matrix = DataHandler.create_distance_matrix(locations, method='haversine')
        
        print(f"  Matriz de distâncias: {distance_matrix.shape}")
        
        return True
    
    except Exception as e:
        print(f"❌ Erro ao carregar CSV: {str(e)}")
        return False

def run_all_tests():
    """Executa todos os testes."""
    print("\n" + "="*60)
    print("SISTEMA DE OTIMIZAÇÃO LOGÍSTICA - SUITE DE TESTES")
    print("="*60)
    
    results = []
    
    # Executar testes
    results.append(("VRP Básico", test_basic_vrp()))
    results.append(("CVRP", test_cvrp()))
    results.append(("Calculadora de Custos", test_cost_calculator()))
    results.append(("Manipulação de Dados", test_data_handler()))
    results.append(("Carregamento CSV", test_csv_loading()))
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {test_name}: {status}")
    
    print(f"\n{passed}/{total} testes passaram ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! Sistema funcionando corretamente.")
        return True
    else:
        print(f"\n⚠️ {total - passed} teste(s) falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

