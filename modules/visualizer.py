"""
Módulo de Visualização
Criação de mapas e gráficos para análise de rotas
"""

import folium
from folium import plugins
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Tuple, Dict, Optional
import pandas as pd
import numpy as np


class RouteVisualizer:
    """
    Classe para visualizar rotas em mapas e gráficos.
    """
    
    # Cores para diferentes veículos
    VEHICLE_COLORS = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', 
        '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2',
        '#F8B739', '#52B788', '#E76F51', '#2A9D8F'
    ]
    
    @staticmethod
    def create_route_map(
        locations: List[Tuple[float, float]],
        routes: List[List[int]],
        names: List[str],
        depot_index: int = 0,
        route_distances: Optional[List[float]] = None,
        zoom_start: int = 11
    ) -> folium.Map:
        """
        Cria um mapa interativo com as rotas otimizadas.
        
        Args:
            locations: Lista de coordenadas (latitude, longitude)
            routes: Lista de rotas (cada rota é uma lista de índices)
            names: Lista de nomes das localizações
            depot_index: Índice do depósito
            route_distances: Distâncias das rotas em metros (opcional)
            zoom_start: Nível de zoom inicial
            
        Returns:
            Objeto folium.Map
        """
        # Calcular centro do mapa
        lats = [loc[0] for loc in locations]
        lons = [loc[1] for loc in locations]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        
        # Criar mapa
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            tiles='OpenStreetMap'
        )
        
        # Adicionar depósito
        depot_lat, depot_lon = locations[depot_index]
        folium.Marker(
            location=[depot_lat, depot_lon],
            popup=f"<b>{names[depot_index]}</b><br>Depósito",
            tooltip=names[depot_index],
            icon=folium.Icon(color='red', icon='home', prefix='fa')
        ).add_to(m)
        
        # Adicionar rotas
        for vehicle_id, route in enumerate(routes):
            color = RouteVisualizer.VEHICLE_COLORS[vehicle_id % len(RouteVisualizer.VEHICLE_COLORS)]
            
            # Criar linha da rota
            route_coords = [locations[idx] for idx in route]
            
            # Informações da rota
            distance_info = ""
            if route_distances and vehicle_id < len(route_distances):
                distance_km = route_distances[vehicle_id] / 1000
                distance_info = f"<br>Distância: {distance_km:.2f} km"
            
            folium.PolyLine(
                locations=route_coords,
                color=color,
                weight=3,
                opacity=0.7,
                popup=f"<b>Veículo {vehicle_id + 1}</b>{distance_info}",
                tooltip=f"Veículo {vehicle_id + 1}"
            ).add_to(m)
            
            # Adicionar marcadores dos clientes
            for seq, idx in enumerate(route):
                if idx == depot_index:
                    continue  # Pular depósito
                
                lat, lon = locations[idx]
                
                # Criar popup com informações
                popup_html = f"""
                <div style="font-family: Arial; font-size: 12px;">
                    <b>{names[idx]}</b><br>
                    Veículo: {vehicle_id + 1}<br>
                    Sequência: {seq}<br>
                    Coordenadas: {lat:.4f}, {lon:.4f}
                </div>
                """
                
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=f"{names[idx]} (V{vehicle_id + 1})",
                    icon=folium.Icon(
                        color='blue',
                        icon='info-sign',
                        prefix='glyphicon'
                    )
                ).add_to(m)
                
                # Adicionar número de sequência
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=8,
                    popup=f"Sequência: {seq}",
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.6,
                    weight=2
                ).add_to(m)
        
        # Adicionar controle de camadas
        folium.LayerControl().add_to(m)
        
        # Adicionar plugin de fullscreen
        plugins.Fullscreen().add_to(m)
        
        # Adicionar medidor de distância
        plugins.MeasureControl(position='topleft').add_to(m)
        
        return m
    
    @staticmethod
    def create_distance_chart(
        route_distances: List[float],
        route_labels: Optional[List[str]] = None
    ) -> go.Figure:
        """
        Cria gráfico de barras com distâncias das rotas.
        
        Args:
            route_distances: Lista de distâncias em metros
            route_labels: Labels das rotas (opcional)
            
        Returns:
            Figura plotly
        """
        if not route_labels:
            route_labels = [f"Veículo {i+1}" for i in range(len(route_distances))]
        
        distances_km = [d / 1000 for d in route_distances]
        
        fig = go.Figure(data=[
            go.Bar(
                x=route_labels,
                y=distances_km,
                text=[f"{d:.2f} km" for d in distances_km],
                textposition='auto',
                marker_color=RouteVisualizer.VEHICLE_COLORS[:len(route_distances)]
            )
        ])
        
        fig.update_layout(
            title="Distância por Rota",
            xaxis_title="Veículo",
            yaxis_title="Distância (km)",
            template="plotly_white",
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_cost_breakdown_chart(costs: Dict) -> go.Figure:
        """
        Cria gráfico de pizza com breakdown de custos.
        
        Args:
            costs: Dicionário de custos
            
        Returns:
            Figura plotly
        """
        labels = ['Combustível', 'Motorista', 'Depreciação', 'Pedágios', 'Operacional']
        values = [
            costs['total_fuel_cost'],
            costs['total_driver_cost'],
            costs['total_depreciation_cost'],
            costs['total_toll_cost'],
            costs['total_operational_cost']
        ]
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
            )
        ])
        
        fig.update_layout(
            title="Distribuição de Custos",
            template="plotly_white",
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_route_comparison_chart(
        scenario1_distances: List[float],
        scenario2_distances: List[float],
        scenario1_name: str = "Sem Otimização",
        scenario2_name: str = "Com Otimização"
    ) -> go.Figure:
        """
        Cria gráfico comparando dois cenários.
        
        Args:
            scenario1_distances: Distâncias do cenário 1 em metros
            scenario2_distances: Distâncias do cenário 2 em metros
            scenario1_name: Nome do cenário 1
            scenario2_name: Nome do cenário 2
            
        Returns:
            Figura plotly
        """
        total1 = sum(scenario1_distances) / 1000
        total2 = sum(scenario2_distances) / 1000
        
        fig = go.Figure(data=[
            go.Bar(
                name=scenario1_name,
                x=['Distância Total'],
                y=[total1],
                text=[f"{total1:.2f} km"],
                textposition='auto',
                marker_color='#FF6B6B'
            ),
            go.Bar(
                name=scenario2_name,
                x=['Distância Total'],
                y=[total2],
                text=[f"{total2:.2f} km"],
                textposition='auto',
                marker_color='#4ECDC4'
            )
        ])
        
        fig.update_layout(
            title="Comparação de Cenários",
            yaxis_title="Distância (km)",
            template="plotly_white",
            barmode='group',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_metrics_table(metrics: Dict) -> pd.DataFrame:
        """
        Cria tabela com métricas da solução.
        
        Args:
            metrics: Dicionário de métricas
            
        Returns:
            DataFrame pandas
        """
        data = {
            'Métrica': [
                'Distância Total',
                'Maior Rota',
                'Número de Rotas',
                'Veículos Utilizados'
            ],
            'Valor': [
                f"{metrics['total_distance']/1000:.2f} km",
                f"{metrics['max_route_distance']/1000:.2f} km",
                metrics['num_routes'],
                metrics['num_vehicles_used']
            ]
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def create_load_chart(
        route_loads: List[int],
        vehicle_capacities: List[int]
    ) -> go.Figure:
        """
        Cria gráfico de carga por veículo.
        
        Args:
            route_loads: Lista de cargas por rota
            vehicle_capacities: Lista de capacidades dos veículos
            
        Returns:
            Figura plotly
        """
        vehicle_labels = [f"Veículo {i+1}" for i in range(len(route_loads))]
        
        fig = go.Figure()
        
        # Adicionar barras de carga
        fig.add_trace(go.Bar(
            name='Carga',
            x=vehicle_labels,
            y=route_loads,
            text=route_loads,
            textposition='auto',
            marker_color='#4ECDC4'
        ))
        
        # Adicionar linha de capacidade
        fig.add_trace(go.Scatter(
            name='Capacidade',
            x=vehicle_labels,
            y=vehicle_capacities[:len(route_loads)],
            mode='lines+markers',
            line=dict(color='#FF6B6B', width=2, dash='dash'),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Utilização de Capacidade por Veículo",
            xaxis_title="Veículo",
            yaxis_title="Carga",
            template="plotly_white",
            height=400,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_co2_chart(co2_kg: float) -> go.Figure:
        """
        Cria gráfico de emissões de CO2.
        
        Args:
            co2_kg: Emissões em kg
            
        Returns:
            Figura plotly
        """
        # Converter para toneladas se necessário
        if co2_kg > 1000:
            value = co2_kg / 1000
            unit = "toneladas"
        else:
            value = co2_kg
            unit = "kg"
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': f"Emissões de CO2 ({unit})"},
            gauge={
                'axis': {'range': [None, value * 1.5]},
                'bar': {'color': "#FF6B6B"},
                'steps': [
                    {'range': [0, value * 0.5], 'color': "#98D8C8"},
                    {'range': [value * 0.5, value], 'color': "#FFA07A"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': value * 0.9
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            template="plotly_white"
        )
        
        return fig
    
    @staticmethod
    def save_map_html(
        map_obj: folium.Map,
        filepath: str
    ):
        """
        Salva mapa em arquivo HTML.
        
        Args:
            map_obj: Objeto folium.Map
            filepath: Caminho do arquivo de saída
        """
        map_obj.save(filepath)

