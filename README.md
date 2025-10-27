# 🚚 Sistema de Otimização Logística para o Brasil

Sistema completo de otimização de rotas de veículos (VRP - Vehicle Routing Problem) desenvolvido em Python com interface Streamlit, adaptado para resolver problemas reais de logística no Brasil.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)
![OR-Tools](https://img.shields.io/badge/OR--Tools-9.8-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Exemplos](#exemplos)
- [Casos de Uso](#casos-de-uso)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## 🎯 Visão Geral

Este sistema resolve o **Problema de Roteamento de Veículos (VRP)**, um dos problemas mais importantes em logística e otimização combinatória. O objetivo é encontrar as rotas mais eficientes para uma frota de veículos que precisa atender um conjunto de clientes, minimizando custos operacionais e maximizando a eficiência.

### Problema que Resolve

No contexto brasileiro, empresas enfrentam desafios como:
- **Altos custos logísticos**: Brasil tem um dos custos logísticos mais altos do mundo
- **Infraestrutura precária**: Rodovias em más condições aumentam custos de manutenção
- **Grandes distâncias**: País continental com rotas longas de distribuição
- **Custos de combustível elevados**: Preços voláteis e altos
- **Pedágios**: Custos significativos em rotas interestaduais

Este sistema ajuda a:
✅ Reduzir distâncias percorridas em até 30%
✅ Diminuir custos operacionais significativamente
✅ Otimizar uso da frota
✅ Reduzir emissões de CO2
✅ Melhorar tempo de entrega

## ✨ Funcionalidades

### Otimização de Rotas
- Algoritmos avançados do Google OR-Tools
- Suporte a múltiplos veículos
- Restrições de capacidade (CVRP)
- Minimização de distância total ou maior rota
- Múltiplas estratégias de busca

### Cálculo de Custos
- **Combustível**: Baseado em preços brasileiros atuais
- **Motorista**: Custo por hora de trabalho
- **Depreciação**: Desgaste do veículo
- **Pedágios**: Estimativa baseada em distância
- **Operacional**: Custos de manutenção e operação

### Visualizações Interativas
- **Mapas**: Visualização de rotas em mapa interativo
- **Gráficos**: Análise de distâncias, custos e cargas
- **Métricas**: Dashboard com KPIs principais
- **Comparações**: Antes vs depois da otimização

### Análise Ambiental
- Cálculo de emissões de CO2
- Impacto ambiental da operação
- Economia de emissões com otimização

### Exportação de Dados
- Exportar rotas em CSV
- Exportar relatórios em Excel
- Salvar mapas em HTML

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11**: Linguagem principal
- **OR-Tools**: Biblioteca de otimização do Google
- **NumPy**: Computação numérica
- **Pandas**: Manipulação de dados

### Frontend
- **Streamlit**: Framework para interface web
- **Folium**: Mapas interativos
- **Plotly**: Gráficos interativos

### Algoritmos
- **VRP (Vehicle Routing Problem)**: Roteamento básico
- **CVRP (Capacitated VRP)**: Com restrições de capacidade
- **Heurísticas**: PATH_CHEAPEST_ARC, SAVINGS, SWEEP
- **Metaheurísticas**: Guided Local Search, Simulated Annealing

## 📦 Instalação

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/sistema-otimizacao-logistica.git
cd sistema-otimizacao-logistica
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute o sistema**
```bash
streamlit run app.py
```

5. **Acesse no navegador**
```
http://localhost:8501
```

## 🚀 Como Usar

### 1. Entrada de Dados

#### Opção A: Dados de Exemplo
- Selecione "Dados de Exemplo" na barra lateral
- Escolha a cidade base (São Paulo, Rio de Janeiro, etc.)
- Ajuste o número de clientes e raio de distribuição
- Marque "Incluir Demandas" para usar restrições de capacidade

#### Opção B: Upload de CSV
- Prepare um arquivo CSV com as colunas:
  - `latitude`: Latitude do local
  - `longitude`: Longitude do local
  - `nome`: Nome/identificação do local
  - `demanda` (opcional): Demanda do cliente
  
Exemplo de CSV:
```csv
nome,latitude,longitude,demanda
Depósito,-23.5505,-46.6333,0
Cliente 1,-23.5629,-46.6544,15
Cliente 2,-23.5489,-46.6388,20
Cliente 3,-23.5712,-46.6456,10
```

- Selecione "Upload CSV" na barra lateral
- Faça upload do arquivo
- Mapeie as colunas corretamente

### 2. Configuração da Frota

- **Número de Veículos**: Quantos veículos estão disponíveis
- **Capacidade por Veículo**: Capacidade de carga (se aplicável)
- **Distância Máxima**: Limite de km por veículo

### 3. Configuração de Custos

Ajuste os valores conforme sua realidade:
- **Preço Combustível**: R$ por litro (padrão: R$ 6,50)
- **Consumo**: km por litro (padrão: 8 km/L)
- **Custo Motorista**: R$ por hora (padrão: R$ 25/h)
- **Incluir Pedágios**: Marque para considerar custos de pedágio

### 4. Otimizar

- Clique no botão **"🚀 Otimizar Rotas"**
- Aguarde o processamento (geralmente 5-30 segundos)
- Visualize os resultados nas abas

### 5. Analisar Resultados

#### Aba Mapa
- Visualize as rotas otimizadas no mapa
- Cada veículo tem uma cor diferente
- Clique nos marcadores para ver detalhes
- Expanda os detalhes de cada rota

#### Aba Métricas
- Veja métricas principais: distância total, maior rota, veículos usados
- Analise gráficos de distribuição de distâncias
- Verifique utilização de capacidade (se aplicável)

#### Aba Custos
- Veja breakdown completo de custos
- Analise distribuição por categoria
- Verifique impacto ambiental (CO2)
- Compare custo total vs custo por km

#### Aba Exportar
- Visualize tabela completa das rotas
- Baixe em formato CSV ou Excel
- Use os dados em outros sistemas

## 📁 Estrutura do Projeto

```
sistema_otimizacao_logistica/
├── app.py                      # Aplicação principal Streamlit
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
│
├── modules/                    # Módulos do sistema
│   ├── optimizer.py           # Lógica de otimização VRP
│   ├── cost_calculator.py     # Cálculo de custos
│   ├── data_handler.py        # Manipulação de dados
│   └── visualizer.py          # Visualizações e mapas
│
├── data/                       # Dados de exemplo
│   ├── exemplo_clientes.csv
│   └── exemplo_veiculos.csv
│
├── assets/                     # Recursos estáticos
│   └── logo.png
│
└── utils/                      # Utilitários
    └── helpers.py
```

## 💡 Exemplos

### Exemplo 1: Distribuição Urbana em São Paulo

**Cenário**: Empresa de e-commerce precisa entregar 20 pedidos em São Paulo com 4 veículos.

**Configuração**:
- Cidade: São Paulo
- Clientes: 20
- Veículos: 4
- Capacidade: 100 unidades/veículo
- Raio: 30 km

**Resultado**:
- Distância total: 145 km (vs 220 km sem otimização)
- Economia: 34% em distância
- Custo total: R$ 487,50
- Tempo total: 4h 15min
- CO2 economizado: 28 kg

### Exemplo 2: Logística Agrícola

**Cenário**: Distribuição de insumos para fazendas no interior.

**Configuração**:
- Cidade: Brasília
- Fazendas: 15
- Veículos: 3
- Capacidade: 200 unidades/veículo
- Raio: 80 km

**Resultado**:
- Distância total: 385 km
- Custo total: R$ 1.245,00
- Tempo total: 9h 30min
- Veículos utilizados: 3/3

## 🎯 Casos de Uso

### 1. E-commerce e Varejo
- Entregas last-mile
- Distribuição para lojas
- Coleta de produtos

### 2. Logística Agrícola
- Distribuição de insumos
- Coleta de produção
- Transporte de equipamentos

### 3. Indústria
- Distribuição para distribuidores
- Coleta de matéria-prima
- Logística reversa

### 4. Serviços
- Rotas de técnicos
- Coleta de resíduos
- Transporte de pessoal

### 5. Setor Público
- Rotas de ônibus escolares
- Coleta de lixo
- Entregas de correspondência

## 🔧 Configurações Avançadas

### Personalizar Algoritmos

Edite `modules/optimizer.py` para ajustar:
- Estratégias de primeira solução
- Metaheurísticas de busca local
- Tempo limite de otimização
- Parâmetros de busca

### Adicionar Restrições

O sistema suporta:
- **Capacidade**: Já implementado
- **Janelas de Tempo**: Estrutura preparada
- **Múltiplos Depósitos**: Estrutura preparada
- **Pickup & Delivery**: Estrutura preparada

### Integrar APIs de Roteamento

Para distâncias reais de estrada, integre:
- Google Maps Distance Matrix API
- OpenRouteService API
- OSRM (Open Source Routing Machine)

## 📊 Métricas e KPIs

O sistema calcula automaticamente:

### Operacionais
- Distância total (km)
- Distância média por rota
- Maior rota
- Número de veículos utilizados
- Taxa de utilização da frota

### Financeiros
- Custo total (R$)
- Custo por km
- Custo por entrega
- Breakdown por categoria

### Ambientais
- Emissões de CO2 (kg)
- Equivalente em árvores
- Economia vs cenário não otimizado

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Roadmap

- [ ] Adicionar suporte a janelas de tempo (VRPTW)
- [ ] Implementar múltiplos depósitos (MDVRP)
- [ ] Integração com APIs de roteamento real
- [ ] Suporte a pickup and delivery
- [ ] Otimização em tempo real
- [ ] Dashboard gerencial
- [ ] API REST
- [ ] Aplicativo mobile

## 🐛 Problemas Conhecidos

- Grandes instâncias (>50 localizações) podem demorar mais para otimizar
- Mapas podem ficar lentos com muitas rotas
- Exportação de mapas grandes pode consumir memória

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Sistema desenvolvido para resolver problemas reais de logística no Brasil**

## 🙏 Agradecimentos

- Google OR-Tools pela excelente biblioteca de otimização
- Comunidade Streamlit pelo framework incrível
- OpenStreetMap pelos dados de mapas

## 📞 Contato

Para dúvidas, sugestões ou suporte:
- Abra uma issue no GitHub
- Entre em contato via email

---

**Desenvolvido com ❤️ para melhorar a logística no Brasil** 🇧🇷

