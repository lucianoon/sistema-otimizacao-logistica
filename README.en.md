# 🚚 Logistics Optimization System for Brazil

*[Versão em português](README.md)*

A complete vehicle routing (VRP — Vehicle Routing Problem) optimization system
built in Python with a Streamlit interface, adapted to real logistics problems
in Brazil.

[![CI](https://github.com/lucianoon/sistema-otimizacao-logistica/actions/workflows/ci.yml/badge.svg)](https://github.com/lucianoon/sistema-otimizacao-logistica/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)
![OR-Tools](https://img.shields.io/badge/OR--Tools-9.8-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Overview

This system solves the **Vehicle Routing Problem (VRP)**, one of the most
important problems in logistics and combinatorial optimization. The goal is to
find the most efficient routes for a fleet that has to serve a set of
customers, minimizing operating cost and maximizing efficiency.

### The problem it addresses

In the Brazilian context, companies face challenges such as:

- **High logistics costs**: Brazil has some of the highest logistics costs in the world
- **Poor infrastructure**: roads in bad condition drive maintenance costs up
- **Long distances**: a continental country with long distribution routes
- **High fuel costs**: volatile and expensive
- **Tolls**: a significant cost on interstate routes

The system lets users:

- compare routes and search for a lower-distance solution for the given scenario;
- estimate operating costs from explicit parameters;
- improve fleet utilization while respecting capacity and maximum distance;
- analyze distance, load, cost and emissions.

How much it helps depends entirely on the instance. Run
[`compare_algorithms.py`](compare_algorithms.py) to measure the gain on your own
data instead of trusting a headline percentage.

## ✨ Features

### Route optimization
- Advanced algorithms from Google OR-Tools
- Multiple vehicles
- Capacity constraints (CVRP)
- Minimize total distance or the longest single route
- Multiple search strategies

### Cost calculation
- **Fuel**: based on current Brazilian prices
- **Driver**: cost per working hour
- **Depreciation**: vehicle wear
- **Tolls**: estimated from distance
- **Operational**: maintenance and operating costs

### Interactive visualizations
- **Maps**: routes drawn on an interactive map
- **Charts**: distance, cost and load analysis
- **Metrics**: dashboard with the main KPIs
- **Comparisons**: before vs. after optimization

### Environmental analysis
- CO2 emission calculation
- Environmental impact of the operation
- Emissions saved through optimization

### Data export
- Export routes to CSV
- Export reports to Excel
- Save maps as HTML

## 🛠️ Tech stack

### Backend
- **Python 3.11**: main language
- **OR-Tools**: Google's optimization library
- **NumPy**: numerical computing
- **Pandas**: data manipulation

### Frontend
- **Streamlit**: web interface framework
- **Folium**: interactive maps
- **Plotly**: interactive charts

### Algorithms
- **VRP (Vehicle Routing Problem)**: basic routing
- **CVRP (Capacitated VRP)**: with capacity constraints
- **Heuristics**: PATH_CHEAPEST_ARC, SAVINGS, SWEEP
- **Metaheuristics**: Guided Local Search, Simulated Annealing
- **Nearest Neighbor**: a simple baseline, kept so OR-Tools can be measured
  against something

## 📦 Installation

### Prerequisites
- Python 3.11 or newer
- pip

### Step by step

1. **Clone the repository**
```bash
git clone https://github.com/lucianoon/sistema-otimizacao-logistica.git
cd sistema-otimizacao-logistica
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install the dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the system**
```bash
streamlit run app.py
```

5. **Open it in the browser**
```
http://localhost:8501
```

## 🚀 How to use

### 1. Data input

#### Option A: sample data
- Select "Dados de Exemplo" (sample data) in the sidebar
- Choose the base city (São Paulo, Rio de Janeiro, etc.)
- Adjust the number of customers and the distribution radius
- Check "Incluir Demandas" (include demands) to use capacity constraints

#### Option B: CSV upload
- Prepare a CSV file with these columns:
  - `latitude`: location latitude
  - `longitude`: location longitude
  - `nome`: location name/identifier
  - `demanda` (optional): customer demand

Example CSV:
```csv
nome,latitude,longitude,demanda
Depósito,-23.5505,-46.6333,0
Cliente 1,-23.5629,-46.6544,15
Cliente 2,-23.5489,-46.6388,20
Cliente 3,-23.5712,-46.6456,10
```

- Select "Upload CSV" in the sidebar
- Upload the file
- Map the columns correctly

> The interface labels and the sample CSV headers are in Portuguese, as shown
> above. The column names (`nome`, `latitude`, `longitude`, `demanda`) are what
> the parser expects.

### 2. Fleet configuration

- **Number of vehicles**: how many vehicles are available
- **Capacity per vehicle**: load capacity (where applicable)
- **Maximum distance**: km limit per vehicle

### 3. Cost configuration

Adjust the values to match your reality:
- **Fuel price**: R$ per litre (default: R$ 6.50)
- **Consumption**: km per litre (default: 8 km/L)
- **Driver cost**: R$ per hour (default: R$ 25/h)
- **Include tolls**: check to account for toll costs

### 4. Optimize

- Click **"🚀 Otimizar Rotas"** (optimize routes)
- Wait for processing (usually 5–30 seconds)
- Review the results in the tabs

### 5. Analyze the results

#### Map tab
- See the optimized routes on the map
- Each vehicle gets its own color
- Click the markers for details
- Expand each route for a breakdown

#### Metrics tab
- Main metrics: total distance, longest route, vehicles used
- Distance distribution charts
- Capacity utilization (where applicable)

#### Costs tab
- Full cost breakdown
- Distribution by category
- Environmental impact (CO2)
- Total cost vs. cost per km

#### Export tab
- Full route table
- Download as CSV or Excel
- Feed the data into other systems

## 🧪 Tests

The project has an automated **pytest** suite in `tests/` covering cost
calculation, data handling, the Nearest Neighbor heuristic, the OR-Tools
optimizer and an end-to-end integration path. The tests run automatically on
GitHub Actions on every push and pull request.

To run them locally:

```bash
pip install -r requirements.txt pytest ruff mypy
ruff check .    # lint
mypy            # type check
pytest
```

## 💡 Worked examples

> **These are illustrative scenarios, not measured benchmark results.** The
> numbers below show the shape of the output the system produces for a given
> configuration — they were not recorded from a reproducible run and should not
> be cited as performance figures. For real measurements on your own instance,
> run `python compare_algorithms.py`, which benchmarks OR-Tools against the
> Nearest Neighbor baseline and prints distance, longest route, vehicles used
> and solve time for each.

### Example 1: urban distribution in São Paulo

**Scenario**: an e-commerce company needs to deliver 20 orders in São Paulo with
4 vehicles.

**Configuration**:
- City: São Paulo
- Customers: 20
- Vehicles: 4
- Capacity: 100 units/vehicle
- Radius: 30 km

**Output shape**: total distance, distance saved against the unoptimized route,
total cost in R$, total time, and CO2 saved.

### Example 2: agricultural logistics

**Scenario**: distributing inputs to farms in the countryside.

**Configuration**:
- City: Brasília
- Farms: 15
- Vehicles: 3
- Capacity: 200 units/vehicle
- Radius: 80 km

**Output shape**: total distance, total cost in R$, total time, and vehicles
used out of vehicles available.

## Use cases

The same CVRP model covers e-commerce last-mile, agricultural distribution and
collection, industrial and reverse logistics, field-technician routing and
public-sector routes (school transport, waste collection).

## 🔧 Advanced configuration

### Customizing the algorithms

Edit `modules/optimizer.py` to adjust:
- First-solution strategies
- Local-search metaheuristics
- Optimization time limit
- Search parameters

See [`GUIA_ADICIONAR_ALGORITMOS.md`](docs/GUIA_ADICIONAR_ALGORITMOS.md) (in
Portuguese) for the interface a new algorithm must implement.

### Adding constraints

- **Capacity**: implemented
- **Time windows**: not implemented — structure prepared
- **Multiple depots**: not implemented — structure prepared
- **Pickup & delivery**: not implemented — structure prepared

### Integrating routing APIs

For real road distances, integrate:
- Google Maps Distance Matrix API
- OpenRouteService API
- OSRM (Open Source Routing Machine)

Distances are currently computed geometrically, not over the road network.

## 📊 Metrics and KPIs

The system computes automatically:

### Operational
- Total distance (km)
- Average distance per route
- Longest route
- Number of vehicles used
- Fleet utilization rate

### Financial
- Total cost (R$)
- Cost per km
- Cost per delivery
- Breakdown by category

### Environmental
- CO2 emissions (kg)
- Tree equivalent
- Savings vs. the unoptimized scenario

## Known limitations

- Large instances (>50 locations) take longer to optimize
- Maps can get slow with many routes
- Exporting large maps can consume a lot of memory
- Distances are geometric, not road-network distances

## 📚 Documentation

Detailed guides (in Portuguese) live in [`docs/`](docs/):

- [`QUICKSTART.md`](docs/QUICKSTART.md): from clone to first optimization in minutes
- [`EXEMPLO_USO.md`](docs/EXEMPLO_USO.md): how to pick and compare the algorithms in the selector
- [`ENTRADA_MANUAL.md`](docs/ENTRADA_MANUAL.md): how to add locations manually in the UI
- [`GUIA_ADICIONAR_ALGORITMOS.md`](docs/GUIA_ADICIONAR_ALGORITMOS.md): interface a new algorithm must implement
- [`DEPLOY.md`](docs/DEPLOY.md): permanent deployment options and required settings

## 📄 License

This project is under the MIT license. See the `LICENSE` file for details.

---

**Built to improve logistics in Brazil** 🇧🇷
