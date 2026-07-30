"""
Script para Comparar Algoritmos de Otimização
Compara OR-Tools vs Nearest Neighbor
"""

import time

import pandas as pd

from modules.data_handler import DataHandler
from modules.nearest_neighbor import NearestNeighborOptimizer
from modules.optimizer import VRPOptimizer


def compare_algorithms():
    """Compara diferentes algoritmos de otimização."""
    
    print("\n" + "="*70)
    print("COMPARAÇÃO DE ALGORITMOS DE OTIMIZAÇÃO")
    print("="*70)
    
    # Criar dados de teste
    print("\n📊 Criando dados de teste...")
    data = DataHandler.create_sample_data(
        num_locations=10,
        depot_location=(-23.5505, -46.6333),  # São Paulo
        radius_km=30,
        include_demands=False
    )
    
    locations = data['locations']
    
    print(f"✓ {len(locations)} localizações criadas")
    
    # Criar matriz de distâncias
    distance_matrix = DataHandler.create_distance_matrix(locations, method='haversine')
    print("✓ Matriz de distâncias criada")
    
    num_vehicles = 3
    
    # Resultados
    results = {}
    
    # ========================================
    # TESTE 1: Nearest Neighbor
    # ========================================
    print("\n" + "-"*70)
    print("🔍 Testando: Nearest Neighbor")
    print("-"*70)
    
    optimizer_nn = NearestNeighborOptimizer(
        distance_matrix=distance_matrix,
        num_vehicles=num_vehicles,
        depot_index=0
    )
    
    start = time.time()
    success_nn = optimizer_nn.solve()
    time_nn = time.time() - start
    
    if success_nn:
        metrics_nn = optimizer_nn.get_metrics()
        results['Nearest Neighbor'] = metrics_nn
        
        print("✅ Solução encontrada!")
        print(f"   Distância Total: {metrics_nn['total_distance']/1000:.2f} km")
        print(f"   Maior Rota: {metrics_nn['max_route_distance']/1000:.2f} km")
        print(f"   Veículos Usados: {metrics_nn['num_vehicles_used']}")
        print(f"   Tempo: {time_nn:.3f}s")
    else:
        print("❌ Falhou")
    
    # ========================================
    # TESTE 2: OR-Tools (PATH_CHEAPEST_ARC)
    # ========================================
    print("\n" + "-"*70)
    print("🔍 Testando: OR-Tools (PATH_CHEAPEST_ARC)")
    print("-"*70)
    
    optimizer_or1 = VRPOptimizer(
        distance_matrix=distance_matrix,
        num_vehicles=num_vehicles,
        depot_index=0,
        max_distance_per_vehicle=100000
    )
    
    start = time.time()
    success_or1 = optimizer_or1.solve(
        time_limit_seconds=30,
        strategy='PATH_CHEAPEST_ARC',
        local_search=None
    )
    time_or1 = time.time() - start
    
    if success_or1:
        metrics_or1 = optimizer_or1.get_metrics()
        results['OR-Tools (PATH_CHEAPEST_ARC)'] = metrics_or1
        
        print("✅ Solução encontrada!")
        print(f"   Distância Total: {metrics_or1['total_distance']/1000:.2f} km")
        print(f"   Maior Rota: {metrics_or1['max_route_distance']/1000:.2f} km")
        print(f"   Veículos Usados: {metrics_or1['num_vehicles_used']}")
        print(f"   Tempo: {time_or1:.3f}s")
    else:
        print("❌ Falhou")
    
    # ========================================
    # TESTE 3: OR-Tools (SAVINGS)
    # ========================================
    print("\n" + "-"*70)
    print("🔍 Testando: OR-Tools (SAVINGS)")
    print("-"*70)
    
    optimizer_or2 = VRPOptimizer(
        distance_matrix=distance_matrix,
        num_vehicles=num_vehicles,
        depot_index=0,
        max_distance_per_vehicle=100000
    )
    
    start = time.time()
    success_or2 = optimizer_or2.solve(
        time_limit_seconds=30,
        strategy='SAVINGS',
        local_search=None
    )
    time_or2 = time.time() - start
    
    if success_or2:
        metrics_or2 = optimizer_or2.get_metrics()
        results['OR-Tools (SAVINGS)'] = metrics_or2
        
        print("✅ Solução encontrada!")
        print(f"   Distância Total: {metrics_or2['total_distance']/1000:.2f} km")
        print(f"   Maior Rota: {metrics_or2['max_route_distance']/1000:.2f} km")
        print(f"   Veículos Usados: {metrics_or2['num_vehicles_used']}")
        print(f"   Tempo: {time_or2:.3f}s")
    else:
        print("❌ Falhou")
    
    # ========================================
    # COMPARAÇÃO FINAL
    # ========================================
    print("\n" + "="*70)
    print("📊 COMPARAÇÃO FINAL")
    print("="*70)
    
    if results:
        # Criar tabela comparativa
        comparison_data = []
        
        for algo_name, metrics in results.items():
            comparison_data.append({
                'Algoritmo': algo_name,
                'Distância Total (km)': f"{metrics['total_distance']/1000:.2f}",
                'Maior Rota (km)': f"{metrics['max_route_distance']/1000:.2f}",
                'Veículos Usados': metrics['num_vehicles_used'],
                'Tempo (s)': f"{metrics['execution_time']:.3f}"
            })
        
        df = pd.DataFrame(comparison_data)
        print("\n" + df.to_string(index=False))
        
        # Encontrar melhor solução
        best_algo = min(results.items(), key=lambda x: x[1]['total_distance'])
        fastest_algo = min(results.items(), key=lambda x: x[1]['execution_time'])
        
        print("\n" + "-"*70)
        print(f"🏆 Melhor Distância: {best_algo[0]}")
        print(f"   {best_algo[1]['total_distance']/1000:.2f} km")
        
        print(f"\n⚡ Mais Rápido: {fastest_algo[0]}")
        print(f"   {fastest_algo[1]['execution_time']:.3f}s")
        
        # Calcular economia
        if len(results) > 1:
            distances = [m['total_distance'] for m in results.values()]
            worst_distance = max(distances)
            best_distance = min(distances)
            savings_km = (worst_distance - best_distance) / 1000
            savings_percent = ((worst_distance - best_distance) / worst_distance) * 100
            
            print("\n💰 Economia Potencial:")
            print(f"   {savings_km:.2f} km ({savings_percent:.1f}%)")
        
        print("="*70 + "\n")
        
        return df
    else:
        print("❌ Nenhum algoritmo conseguiu resolver o problema")
        return None

if __name__ == "__main__":
    compare_algorithms()

