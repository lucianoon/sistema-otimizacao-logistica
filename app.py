"""
Sistema de Otimização Logística para o Brasil
Interface Streamlit para otimização de rotas de veículos
"""

import pandas as pd
import streamlit as st
from streamlit_folium import folium_static

from modules.cost_calculator import CostCalculator
from modules.data_handler import DataHandler
from modules.nearest_neighbor import NearestNeighborOptimizer
from modules.optimizer import VRPOptimizer
from modules.visualizer import RouteVisualizer

# Configuração da página
st.set_page_config(
    page_title="Sistema de Otimização Logística",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🚚 Sistema de Otimização Logística")
st.markdown("### Otimização de Rotas para Transporte no Brasil")

# Sidebar para configurações
st.sidebar.header("⚙️ Configurações")

# Seleção do modo de entrada de dados
data_mode = st.sidebar.radio(
    "Modo de Entrada de Dados:",
    ["Dados de Exemplo", "Upload CSV", "Entrada Manual"]
)

# Inicializar session state
if 'solution_calculated' not in st.session_state:
    st.session_state.solution_calculated = False
if 'optimizer' not in st.session_state:
    st.session_state.optimizer = None
if 'metrics' not in st.session_state:
    st.session_state.metrics = None
if 'locations' not in st.session_state:
    st.session_state.locations = None
if 'names' not in st.session_state:
    st.session_state.names = None

# Função para carregar dados
def load_data():
    """Carrega dados baseado no modo selecionado."""
    
    if data_mode == "Dados de Exemplo":
        st.sidebar.subheader("📊 Dados de Exemplo")
        
        num_locations = st.sidebar.slider(
            "Número de Clientes:",
            min_value=5,
            max_value=30,
            value=15
        )
        
        # Selecionar cidade base
        cities = {
            "São Paulo": (-23.5505, -46.6333),
            "Rio de Janeiro": (-22.9068, -43.1729),
            "Belo Horizonte": (-19.9167, -43.9345),
            "Brasília": (-15.7939, -47.8828),
            "Curitiba": (-25.4284, -49.2733),
            "Porto Alegre": (-30.0346, -51.2177)
        }
        
        selected_city = st.sidebar.selectbox(
            "Cidade Base:",
            list(cities.keys())
        )
        
        depot_location = cities[str(selected_city)]
        
        radius_km = st.sidebar.slider(
            "Raio de Distribuição (km):",
            min_value=10,
            max_value=100,
            value=50
        )
        
        include_demands = st.sidebar.checkbox("Incluir Demandas (CVRP)", value=True)
        
        data = DataHandler.create_sample_data(
            num_locations=num_locations,
            depot_location=depot_location,
            radius_km=radius_km,
            include_demands=include_demands
        )
        
        return data
    
    elif data_mode == "Upload CSV":
        st.sidebar.subheader("📁 Upload de Arquivo")
        
        uploaded_file = st.sidebar.file_uploader(
            "Selecione um arquivo CSV:",
            type=['csv']
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                st.sidebar.write("Colunas disponíveis:", df.columns.tolist())
                
                lat_col = st.sidebar.selectbox("Coluna de Latitude:", df.columns, index=0)
                lon_col = st.sidebar.selectbox("Coluna de Longitude:", df.columns, index=1)
                name_col = st.sidebar.selectbox(
                    "Coluna de Nome:",
                    df.columns,
                    index=2 if len(df.columns) > 2 else 0,
                )
                
                demand_col = None
                if st.sidebar.checkbox("Incluir Demandas"):
                    demand_col = st.sidebar.selectbox("Coluna de Demanda:", df.columns)
                
                data = DataHandler.load_locations_from_dataframe(
                    df,
                    lat_column=str(lat_col),
                    lon_column=str(lon_col),
                    name_column=str(name_col),
                    demand_column=demand_col
                )
                
                return data
            
            except Exception as e:
                st.sidebar.error(f"Erro ao carregar arquivo: {str(e)}")
                return None
        else:
            st.sidebar.info("Aguardando upload de arquivo...")
            return None
    
    else:  # Entrada Manual
        st.sidebar.subheader("✏️ Entrada Manual")
        
        # Inicializar session state para entrada manual
        if 'manual_locations' not in st.session_state:
            st.session_state.manual_locations = []
        
        # Depósito
        st.sidebar.markdown("**Depósito (Ponto de Partida)**")
        
        depot_name = st.sidebar.text_input(
            "Nome do Depósito:",
            value="Depósito Central",
            key="depot_name"
        )
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            depot_lat = st.number_input(
                "Latitude:",
                value=-23.5505,
                format="%.6f",
                key="depot_lat"
            )
        with col2:
            depot_lon = st.number_input(
                "Longitude:",
                value=-46.6333,
                format="%.6f",
                key="depot_lon"
            )
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Adicionar Clientes**")
        
        # Formulário para adicionar cliente
        with st.sidebar.form(key="add_location_form", clear_on_submit=True):
            client_name = st.text_input("Nome do Cliente:", value="")
            
            col1, col2 = st.columns(2)
            with col1:
                client_lat = st.number_input("Latitude:", value=-23.5500, format="%.6f")
            with col2:
                client_lon = st.number_input("Longitude:", value=-46.6300, format="%.6f")
            
            client_demand = st.number_input("Demanda (opcional):", value=0, min_value=0)
            
            submit_button = st.form_submit_button("➕ Adicionar Cliente")
            
            if submit_button and client_name:
                st.session_state.manual_locations.append({
                    'nome': client_name,
                    'latitude': client_lat,
                    'longitude': client_lon,
                    'demanda': client_demand
                })
                st.success(f"Cliente '{client_name}' adicionado!")
        
        # Mostrar clientes adicionados
        if st.session_state.manual_locations:
            st.sidebar.markdown(
                f"**Clientes Adicionados: "
                f"{len(st.session_state.manual_locations)}**"
            )
            
            # Botão para limpar todos
            if st.sidebar.button("🗑️ Limpar Todos os Clientes"):
                st.session_state.manual_locations = []
                st.rerun()
            
            # Mostrar lista de clientes com opção de remover
            with st.sidebar.expander("📋 Ver Clientes"):
                for idx, loc in enumerate(st.session_state.manual_locations):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(f"{idx+1}. {loc['nome']}")
                    with col2:
                        if st.button("❌", key=f"remove_{idx}"):
                            st.session_state.manual_locations.pop(idx)
                            st.rerun()
        
        # Preparar dados se houver clientes
        if st.session_state.manual_locations:
            # Criar listas
            all_names = [depot_name] + [loc['nome'] for loc in st.session_state.manual_locations]
            all_locations = [(depot_lat, depot_lon)] + [
                (loc['latitude'], loc['longitude'])
                for loc in st.session_state.manual_locations
            ]
            
            # Verificar se há demandas
            has_demands = any(loc['demanda'] > 0 for loc in st.session_state.manual_locations)
            all_demands = None
            
            if has_demands:
                all_demands = [0] + [loc['demanda'] for loc in st.session_state.manual_locations]
            
            return {
                'locations': all_locations,
                'names': all_names,
                'demands': all_demands
            }
        else:
            st.sidebar.info("📍 Adicione pelo menos 1 cliente para começar.")
            return None

# Carregar dados
data = load_data()

if data is not None:
    locations = data['locations']
    names = data['names']
    demands = data.get('demands', None)
    
    st.session_state.locations = locations
    st.session_state.names = names
    
    # Mostrar dados carregados
    with st.expander("📍 Visualizar Localizações Carregadas", expanded=False):
        df_locations = pd.DataFrame({
            'Nome': names,
            'Latitude': [loc[0] for loc in locations],
            'Longitude': [loc[1] for loc in locations]
        })
        
        if demands:
            df_locations['Demanda'] = demands
        
        st.dataframe(df_locations, use_container_width=True)
    
    # Configurações de otimização
    st.sidebar.header("🚛 Configurações da Frota")
    
    num_vehicles = st.sidebar.number_input(
        "Número de Veículos:",
        min_value=1,
        max_value=10,
        value=4
    )
    
    # Configurações de capacidade
    use_capacity = demands is not None and st.sidebar.checkbox(
        "Usar Restrições de Capacidade", value=bool(demands)
    )
    
    vehicle_capacities = None
    if use_capacity and demands:
        capacity_per_vehicle = st.sidebar.number_input(
            "Capacidade por Veículo:",
            min_value=10,
            max_value=1000,
            value=100
        )
        vehicle_capacities = [int(capacity_per_vehicle)] * int(num_vehicles)
    
    max_distance_km = st.sidebar.number_input(
        "Distância Máxima por Veículo (km):",
        min_value=50,
        max_value=1000,
        value=300
    )
    
    # Seleção de algoritmo
    st.sidebar.header("🧮 Algoritmo de Otimização")
    
    algorithm = st.sidebar.selectbox(
        "Escolha o Algoritmo:",
        [
            "OR-Tools (Recomendado)",
            "Nearest Neighbor (Rápido)"
        ],
        help="OR-Tools: Algoritmo avançado com melhores resultados\n"
             "Nearest Neighbor: Heurística rápida e simples"
    )
    
    # Parâmetros específicos do OR-Tools
    if algorithm == "OR-Tools (Recomendado)":
        with st.sidebar.expander("⚙️ Parâmetros Avançados OR-Tools"):
            strategy = st.selectbox(
                "Estratégia de Primeira Solução:",
                [
                    'PATH_CHEAPEST_ARC',
                    'SAVINGS',
                    'SWEEP',
                    'CHRISTOFIDES',
                    'PARALLEL_CHEAPEST_INSERTION',
                    'LOCAL_CHEAPEST_INSERTION'
                ],
                help="Estratégia para construir a solução inicial"
            )
            
            local_search = st.selectbox(
                "Metaheurística:",
                [
                    'GUIDED_LOCAL_SEARCH',
                    'SIMULATED_ANNEALING',
                    'TABU_SEARCH',
                    'Nenhuma'
                ],
                help="Método de busca local para melhorar a solução"
            )
            
            time_limit = st.slider(
                "Tempo Limite (segundos):",
                min_value=10,
                max_value=300,
                value=30,
                help="Tempo máximo para buscar soluções"
            )
    else:
        strategy = 'PATH_CHEAPEST_ARC'
        local_search = None
        time_limit = 30
    
    # Configurações de custos
    st.sidebar.header("💰 Configurações de Custos")
    
    fuel_price = st.sidebar.number_input(
        "Preço Combustível (R$/L):",
        min_value=3.0,
        max_value=15.0,
        value=6.50,
        step=0.10
    )
    
    fuel_consumption = st.sidebar.number_input(
        "Consumo (km/L):",
        min_value=3.0,
        max_value=20.0,
        value=8.0,
        step=0.5
    )
    
    driver_cost_per_hour = st.sidebar.number_input(
        "Custo Motorista (R$/h):",
        min_value=10.0,
        max_value=100.0,
        value=25.0,
        step=5.0
    )
    
    include_tolls = st.sidebar.checkbox("Incluir Pedágios", value=True)
    
    # Botão para otimizar
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🚀 Otimizar Rotas", type="primary", use_container_width=True):
        with st.spinner(f"Otimizando rotas com {algorithm}... Por favor, aguarde."):
            try:
                # Criar matriz de distâncias
                distance_matrix = DataHandler.create_distance_matrix(
                    locations,
                    method='haversine'
                )
                
                # Criar otimizador baseado no algoritmo selecionado
                optimizer: VRPOptimizer | NearestNeighborOptimizer
                if algorithm == "OR-Tools (Recomendado)":
                    optimizer = VRPOptimizer(
                        distance_matrix=distance_matrix,
                        num_vehicles=int(num_vehicles),
                        depot_index=0,
                        vehicle_capacities=vehicle_capacities if use_capacity else None,
                        demands=demands if use_capacity else None,
                        max_distance_per_vehicle=int(max_distance_km * 1000)
                    )
                    
                    # Resolver com parâmetros configurados
                    success = optimizer.solve(
                        time_limit_seconds=time_limit,
                        strategy=str(strategy),
                        local_search=None if local_search == 'Nenhuma' else local_search
                    )
                    
                else:  # Nearest Neighbor
                    optimizer = NearestNeighborOptimizer(
                        distance_matrix=distance_matrix,
                        num_vehicles=int(num_vehicles),
                        depot_index=0
                    )
                    
                    # Resolver
                    success = optimizer.solve()
                
                if success:
                    st.session_state.optimizer = optimizer
                    st.session_state.metrics = optimizer.get_metrics()
                    st.session_state.solution_calculated = True
                    st.sidebar.success("✅ Otimização concluída!")
                else:
                    st.sidebar.error("❌ Não foi possível encontrar uma solução.")
                    st.session_state.solution_calculated = False
            
            except Exception as e:
                st.sidebar.error(f"❌ Erro na otimização: {str(e)}")
                st.session_state.solution_calculated = False

# Exibir resultados
if st.session_state.solution_calculated and st.session_state.optimizer is not None:
    
    optimizer = st.session_state.optimizer
    metrics = st.session_state.metrics
    locations = st.session_state.locations
    names = st.session_state.names
    routes = metrics['routes']
    route_distances = metrics['route_distances']
    
    # Tabs para organizar informações
    tab1, tab2, tab3, tab4 = st.tabs(["📍 Mapa", "📊 Métricas", "💰 Custos", "📥 Exportar"])
    
    with tab1:
        st.subheader("Mapa de Rotas Otimizadas")
        
        # Criar mapa
        route_map = RouteVisualizer.create_route_map(
            locations=locations,
            routes=routes,
            names=names,
            depot_index=0,
            route_distances=route_distances
        )
        
        # Exibir mapa
        folium_static(route_map, width=1200, height=600)
        
        # Informações das rotas
        st.markdown("### 🚛 Detalhes das Rotas")
        
        for vehicle_id, route in enumerate(routes):
            expander_label = (
                f"Veículo {vehicle_id + 1} - {route_distances[vehicle_id]/1000:.2f} km"
            )
            with st.expander(expander_label):
                route_info = " → ".join([names[idx] for idx in route])
                st.write(f"**Rota:** {route_info}")
                st.write(f"**Distância:** {route_distances[vehicle_id]/1000:.2f} km")
                
                if 'route_loads' in metrics:
                    st.write(f"**Carga:** {metrics['route_loads'][vehicle_id]}")
    
    with tab2:
        st.subheader("Métricas da Solução")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Distância Total",
                f"{metrics['total_distance']/1000:.2f} km"
            )
        
        with col2:
            st.metric(
                "Maior Rota",
                f"{metrics['max_route_distance']/1000:.2f} km"
            )
        
        with col3:
            st.metric(
                "Veículos Usados",
                f"{metrics['num_vehicles_used']}/{num_vehicles}"
            )
        
        with col4:
            st.metric(
                "Clientes Atendidos",
                len(locations) - 1
            )
        
        # Informações do algoritmo usado
        algorithm_used = metrics.get('algorithm', 'OR-Tools')
        execution_time = metrics.get('execution_time', 0)
        
        st.info(
            f"🧮 **Algoritmo Utilizado:** {algorithm_used} | "
            f"⏱️ **Tempo de Execução:** {execution_time:.2f}s"
        )
        
        # Gráficos
        st.markdown("### 📈 Análise Visual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de distâncias
            fig_distance = RouteVisualizer.create_distance_chart(route_distances)
            st.plotly_chart(fig_distance, use_container_width=True)
        
        with col2:
            # Gráfico de carga (se aplicável)
            if 'route_loads' in metrics and vehicle_capacities:
                fig_load = RouteVisualizer.create_load_chart(
                    metrics['route_loads'],
                    vehicle_capacities
                )
                st.plotly_chart(fig_load, use_container_width=True)
    
    with tab3:
        st.subheader("Análise de Custos")
        
        # Calcular custos
        calculator = CostCalculator(
            fuel_price_per_liter=fuel_price,
            fuel_consumption_km_per_liter=fuel_consumption,
            driver_cost_per_hour=driver_cost_per_hour,
            include_tolls=include_tolls
        )
        
        route_distances_km = [d / 1000 for d in route_distances]
        costs = calculator.calculate_route_costs(route_distances_km)
        
        # Métricas de custo
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Custo Total",
                DataHandler.format_currency(costs['total_cost'])
            )
        
        with col2:
            st.metric(
                "Custo Combustível",
                DataHandler.format_currency(costs['total_fuel_cost'])
            )
        
        with col3:
            st.metric(
                "Tempo Total",
                DataHandler.format_time(costs['total_time_hours'])
            )
        
        with col4:
            st.metric(
                "Emissões CO2",
                f"{costs['total_co2_kg']:.2f} kg"
            )
        
        # Breakdown de custos
        st.markdown("### 💵 Detalhamento de Custos")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de pizza
            fig_costs = RouteVisualizer.create_cost_breakdown_chart(costs)
            st.plotly_chart(fig_costs, use_container_width=True)
        
        with col2:
            # Tabela de custos
            st.markdown("#### Resumo")
            cost_data = {
                'Item': [
                    'Combustível', 'Motorista', 'Depreciação',
                    'Pedágios', 'Operacional', 'TOTAL',
                ],
                'Valor (R$)': [
                    f"{costs['total_fuel_cost']:.2f}",
                    f"{costs['total_driver_cost']:.2f}",
                    f"{costs['total_depreciation_cost']:.2f}",
                    f"{costs['total_toll_cost']:.2f}",
                    f"{costs['total_operational_cost']:.2f}",
                    f"{costs['total_cost']:.2f}"
                ]
            }
            st.dataframe(pd.DataFrame(cost_data), use_container_width=True, hide_index=True)
        
        # Emissões de CO2
        st.markdown("### 🌱 Impacto Ambiental")
        fig_co2 = RouteVisualizer.create_co2_chart(costs['total_co2_kg'])
        st.plotly_chart(fig_co2, use_container_width=True)
    
    with tab4:
        st.subheader("Exportar Resultados")
        
        # Criar DataFrame das rotas
        df_routes = DataHandler.create_dataframe_from_routes(
            routes=routes,
            names=names,
            locations=locations,
            route_distances=route_distances
        )
        
        st.markdown("### 📋 Tabela de Rotas")
        st.dataframe(df_routes, use_container_width=True)
        
        # Botões de download
        col1, col2 = st.columns(2)
        
        with col1:
            # Download CSV
            csv = df_routes.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="rotas_otimizadas.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Download Excel
            from io import BytesIO
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_routes.to_excel(writer, sheet_name='Rotas', index=False)
            
            st.download_button(
                label="📥 Download Excel",
                data=buffer.getvalue(),
                file_name="rotas_otimizadas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

else:
    # Mensagem inicial
    st.info(
        "👈 Configure os parâmetros na barra lateral e clique em "
        "'Otimizar Rotas' para começar."
    )
    
    # Informações sobre o sistema
    st.markdown("""
    ## 📖 Sobre o Sistema
    
    Este sistema utiliza algoritmos avançados de otimização para resolver
    problemas de roteamento de veículos (VRP - Vehicle Routing Problem).
    
    ### ✨ Funcionalidades:
    
    - **Otimização de Rotas**: Encontra as rotas mais eficientes para sua frota
    - **Cálculo de Custos**: Estima custos operacionais detalhados
      (combustível, motorista, pedágios, etc.)
    - **Restrições de Capacidade**: Considera a capacidade de carga dos veículos
    - **Visualização Interativa**: Mapas e gráficos para análise das rotas
    - **Análise de Impacto Ambiental**: Calcula emissões de CO2
    - **Exportação de Dados**: Exporte resultados em CSV ou Excel
    
    ### 🚀 Como Usar:
    
    1. Escolha o modo de entrada de dados (Exemplo, CSV ou Manual)
    2. Configure o número de veículos e suas capacidades
    3. Ajuste os parâmetros de custo conforme sua realidade
    4. Clique em "Otimizar Rotas"
    5. Analise os resultados nos diferentes tabs
    6. Exporte os dados se necessário
    
    ### 🇧🇷 Adaptado para o Brasil:
    
    - Valores em Reais (R$)
    - Preços de combustível atualizados
    - Consideração de pedágios
    - Distâncias reais usando coordenadas geográficas
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Sistema de Otimização Logística v1.0 |
        Desenvolvido com ❤️ usando Python, OR-Tools e Streamlit
    </div>
    """,
    unsafe_allow_html=True
)

