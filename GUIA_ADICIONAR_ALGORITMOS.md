# 📚 Guia Completo: Como Adicionar Novos Algoritmos

Este guia mostra passo a passo como adicionar novos algoritmos de otimização ao sistema.

## 🎯 Exemplo Implementado: Nearest Neighbor

Acabamos de adicionar o algoritmo **Nearest Neighbor** como exemplo. Veja como foi feito:

### Passo 1: Criar o Módulo do Algoritmo

Criamos o arquivo `modules/nearest_neighbor.py` com a seguinte estrutura:

```python
class NearestNeighborOptimizer:
    def __init__(self, distance_matrix, num_vehicles, depot_index=0):
        # Inicialização
        pass
    
    def solve(self, **kwargs) -> bool:
        # Lógica do algoritmo
        return True
    
    def get_routes(self) -> List[List[int]]:
        # Retornar rotas
        return self.solution
    
    def get_metrics(self) -> Dict:
        # Retornar métricas
        return {
            'total_distance': ...,
            'routes': ...,
            'algorithm': 'Nearest Neighbor',
            'execution_time': ...
        }
```

**Pontos Importantes:**
- ✅ Interface comum com OR-Tools (`solve()`, `get_routes()`, `get_metrics()`)
- ✅ Retornar `algorithm` e `execution_time` nas métricas
- ✅ Aceitar `**kwargs` no `solve()` para compatibilidade

### Passo 2: Importar no app.py

```python
from modules.nearest_neighbor import NearestNeighborOptimizer
```

### Passo 3: Adicionar Seletor na Interface

No `app.py`, adicionamos um seletor de algoritmo:

```python
st.sidebar.header("🧮 Algoritmo de Otimização")

algorithm = st.sidebar.selectbox(
    "Escolha o Algoritmo:",
    [
        "OR-Tools (Recomendado)",
        "Nearest Neighbor (Rápido)"
    ],
    help="Descrição dos algoritmos"
)
```

### Passo 4: Adicionar Lógica Condicional

```python
if algorithm == "OR-Tools (Recomendado)":
    optimizer = VRPOptimizer(...)
    success = optimizer.solve(...)
    
elif algorithm == "Nearest Neighbor (Rápido)":
    optimizer = NearestNeighborOptimizer(...)
    success = optimizer.solve()
```

### Passo 5: Exibir Informações do Algoritmo

```python
algorithm_used = metrics.get('algorithm', 'OR-Tools')
execution_time = metrics.get('execution_time', 0)

st.info(f"🧮 **Algoritmo:** {algorithm_used} | ⏱️ **Tempo:** {execution_time:.2f}s")
```

## 🚀 Como Adicionar Seu Próprio Algoritmo

### Template Básico

Crie um arquivo `modules/seu_algoritmo.py`:

```python
"""
Seu Algoritmo Customizado
Descrição do que ele faz
"""

import numpy as np
from typing import List, Dict
import time


class SeuAlgoritmoOptimizer:
    """
    Implementação do seu algoritmo para VRP.
    """
    
    def __init__(
        self,
        distance_matrix: np.ndarray,
        num_vehicles: int,
        depot_index: int = 0,
        # Adicione seus parâmetros específicos aqui
        parametro_customizado: int = 100
    ):
        """
        Inicializa o otimizador.
        
        Args:
            distance_matrix: Matriz de distâncias
            num_vehicles: Número de veículos
            depot_index: Índice do depósito
            parametro_customizado: Seu parâmetro específico
        """
        self.distance_matrix = distance_matrix
        self.num_vehicles = num_vehicles
        self.depot_index = depot_index
        self.parametro_customizado = parametro_customizado
        self.num_locations = len(distance_matrix)
        
        self.solution = None
        self.execution_time = 0
    
    def solve(self, **kwargs) -> bool:
        """
        Resolve o problema usando seu algoritmo.
        
        Returns:
            True se encontrou solução, False caso contrário
        """
        start_time = time.time()
        
        # ========================================
        # IMPLEMENTE SEU ALGORITMO AQUI
        # ========================================
        
        # Exemplo: criar rotas vazias
        routes = []
        
        # Sua lógica de otimização...
        # 1. Inicialização
        # 2. Loop principal
        # 3. Critério de parada
        
        # ========================================
        
        self.solution = routes
        self.execution_time = time.time() - start_time
        
        return True
    
    def get_routes(self) -> List[List[int]]:
        """Retorna as rotas da solução."""
        return self.solution if self.solution else []
    
    def get_route_distance(self, route: List[int]) -> float:
        """Calcula distância de uma rota."""
        distance = 0
        for i in range(len(route) - 1):
            distance += self.distance_matrix[route[i]][route[i + 1]]
        return distance
    
    def get_metrics(self) -> Dict:
        """
        Calcula métricas da solução.
        
        IMPORTANTE: Manter mesma estrutura de retorno!
        """
        if not self.solution:
            return {}
        
        routes = self.solution
        route_distances = [self.get_route_distance(r) for r in routes]
        total_distance = sum(route_distances)
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
            'algorithm': 'Seu Algoritmo'  # Nome do seu algoritmo
        }
    
    def print_solution(self):
        """Imprime solução formatada (opcional)."""
        if not self.solution:
            print("Nenhuma solução encontrada!")
            return
        
        metrics = self.get_metrics()
        print(f"Algoritmo: {metrics['algorithm']}")
        print(f"Distância Total: {metrics['total_distance']/1000:.2f} km")
        print(f"Tempo: {metrics['execution_time']:.3f}s")
```

### Integrar na Interface

**1. Importar no `app.py`:**

```python
from modules.seu_algoritmo import SeuAlgoritmoOptimizer
```

**2. Adicionar no seletor:**

```python
algorithm = st.sidebar.selectbox(
    "Escolha o Algoritmo:",
    [
        "OR-Tools (Recomendado)",
        "Nearest Neighbor (Rápido)",
        "Seu Algoritmo (Customizado)"  # ADICIONE AQUI
    ]
)
```

**3. Adicionar parâmetros específicos (opcional):**

```python
if algorithm == "Seu Algoritmo (Customizado)":
    with st.sidebar.expander("⚙️ Parâmetros do Seu Algoritmo"):
        parametro_customizado = st.slider(
            "Seu Parâmetro:",
            min_value=10,
            max_value=500,
            value=100
        )
```

**4. Adicionar na lógica de otimização:**

```python
elif algorithm == "Seu Algoritmo (Customizado)":
    optimizer = SeuAlgoritmoOptimizer(
        distance_matrix=distance_matrix,
        num_vehicles=num_vehicles,
        depot_index=0,
        parametro_customizado=parametro_customizado
    )
    success = optimizer.solve()
```

## 📋 Checklist de Implementação

Ao adicionar um novo algoritmo, verifique:

- [ ] **Classe criada** com nome descritivo
- [ ] **Método `__init__`** com parâmetros necessários
- [ ] **Método `solve()`** que retorna `bool`
- [ ] **Método `get_routes()`** que retorna `List[List[int]]`
- [ ] **Método `get_metrics()`** com estrutura padrão
- [ ] **Atributo `execution_time`** calculado
- [ ] **Atributo `algorithm`** nas métricas
- [ ] **Importado no `app.py`**
- [ ] **Adicionado no seletor** da interface
- [ ] **Lógica condicional** implementada
- [ ] **Testado** com dados de exemplo
- [ ] **Documentado** com docstrings

## 🧪 Testar Seu Algoritmo

Crie um arquivo de teste `test_seu_algoritmo.py`:

```python
from modules.seu_algoritmo import SeuAlgoritmoOptimizer
from modules.data_handler import DataHandler

# Criar dados de teste
data = DataHandler.create_sample_data(num_locations=10)
locations = data['locations']
distance_matrix = DataHandler.create_distance_matrix(locations)

# Criar otimizador
optimizer = SeuAlgoritmoOptimizer(
    distance_matrix=distance_matrix,
    num_vehicles=3
)

# Resolver
print("Testando seu algoritmo...")
success = optimizer.solve()

if success:
    print("✅ Sucesso!")
    metrics = optimizer.get_metrics()
    print(f"Distância: {metrics['total_distance']/1000:.2f} km")
    print(f"Tempo: {metrics['execution_time']:.3f}s")
else:
    print("❌ Falhou")
```

Execute:
```bash
python test_seu_algoritmo.py
```

## 💡 Exemplos de Algoritmos para Implementar

### 1. Algoritmo Genético

```python
class GeneticVRPOptimizer:
    def __init__(self, ..., population_size=100, generations=500):
        # População inicial
        # Operadores: seleção, crossover, mutação
        pass
```

### 2. Ant Colony Optimization

```python
class AntColonyOptimizer:
    def __init__(self, ..., num_ants=50, evaporation_rate=0.5):
        # Feromônios
        # Regras de construção de soluções
        pass
```

### 3. Simulated Annealing

```python
class SimulatedAnnealingOptimizer:
    def __init__(self, ..., initial_temp=1000, cooling_rate=0.95):
        # Temperatura inicial
        # Função de resfriamento
        pass
```

### 4. Tabu Search

```python
class TabuSearchOptimizer:
    def __init__(self, ..., tabu_tenure=10, max_iterations=1000):
        # Lista tabu
        # Critério de aspiração
        pass
```

### 5. Savings Algorithm (Clarke-Wright)

```python
class SavingsAlgorithmOptimizer:
    def __init__(self, ...):
        # Calcular savings
        # Ordenar e mesclar rotas
        pass
```

## 🎨 Personalizar Visualizações

Se seu algoritmo gera informações adicionais, você pode exibir:

```python
# No app.py, após exibir métricas
if algorithm == "Seu Algoritmo (Customizado)":
    st.markdown("### 📊 Informações Adicionais")
    
    # Exemplo: convergência
    if 'convergence_history' in metrics:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=metrics['convergence_history'],
            mode='lines',
            name='Convergência'
        ))
        st.plotly_chart(fig)
```

## 🔧 Dicas Avançadas

### 1. Suporte a Restrições de Capacidade

```python
def __init__(self, ..., vehicle_capacities=None, demands=None):
    self.vehicle_capacities = vehicle_capacities
    self.demands = demands

def solve(self):
    # Verificar capacidade ao construir rotas
    if self.vehicle_capacities and self.demands:
        current_load = sum(self.demands[i] for i in route)
        if current_load > self.vehicle_capacities[vehicle_id]:
            # Não adicionar cliente
            pass
```

### 2. Logging e Debug

```python
import logging

def solve(self, verbose=False):
    if verbose:
        logging.info(f"Iniciando otimização...")
        logging.info(f"Iteração {i}: melhor = {best_distance}")
```

### 3. Paralelização

```python
from multiprocessing import Pool

def solve(self, num_processes=4):
    with Pool(num_processes) as pool:
        results = pool.map(self.evaluate_solution, population)
```

## 📚 Recursos Úteis

- **OR-Tools Docs**: https://developers.google.com/optimization
- **VRP Algorithms**: https://neo.lcc.uma.es/vrp/
- **Heuristics**: https://www.sciencedirect.com/topics/computer-science/vehicle-routing-problem

## 🎓 Conclusão

Agora você tem tudo para adicionar seus próprios algoritmos! O sistema foi projetado para ser extensível e fácil de customizar.

**Próximos passos:**
1. Escolha um algoritmo para implementar
2. Crie o módulo seguindo o template
3. Teste isoladamente
4. Integre na interface
5. Compare com OR-Tools

Boa sorte! 🚀

