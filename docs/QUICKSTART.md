# 🚀 Guia de Início Rápido

## Instalação Rápida

```bash
# 1. Clone ou baixe o projeto
cd sistema_otimizacao_logistica

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o sistema
streamlit run app.py
```

## Primeiro Uso - Passo a Passo

### 1. Acesse a Interface

Após executar o comando acima, abra seu navegador em:
```
http://localhost:8501
```

### 2. Configure os Dados

Na barra lateral esquerda, você tem 3 opções:

#### Opção A: Dados de Exemplo (Recomendado para começar)
- Selecione "Dados de Exemplo"
- Escolha uma cidade base (ex: São Paulo)
- Ajuste o número de clientes (5-30)
- Defina o raio de distribuição (10-100 km)
- Marque "Incluir Demandas" se quiser usar restrições de capacidade

#### Opção B: Upload de CSV
- Prepare um arquivo CSV com as colunas:
  - `nome`: Nome do local
  - `latitude`: Latitude
  - `longitude`: Longitude
  - `demanda` (opcional): Demanda do cliente

Exemplo de CSV:
```csv
nome,latitude,longitude,demanda
Depósito,-23.5505,-46.6333,0
Cliente 1,-23.5629,-46.6544,15
Cliente 2,-23.5489,-46.6388,20
```

### 3. Configure a Frota

- **Número de Veículos**: Quantos veículos você tem disponíveis
- **Capacidade por Veículo**: Capacidade de carga (se usar demandas)
- **Distância Máxima**: Limite de km que cada veículo pode rodar

### 4. Configure os Custos

Ajuste os valores para sua realidade:
- **Preço Combustível**: R$ por litro (padrão: R$ 6,50)
- **Consumo**: km por litro (padrão: 8 km/L)
- **Custo Motorista**: R$ por hora (padrão: R$ 25/h)
- **Incluir Pedágios**: Marque para considerar custos de pedágio

### 5. Otimize!

Clique no botão **"🚀 Otimizar Rotas"** e aguarde alguns segundos.

### 6. Analise os Resultados

Navegue pelas abas:

- **📍 Mapa**: Veja as rotas otimizadas no mapa interativo
- **📊 Métricas**: Analise distâncias e utilização da frota
- **💰 Custos**: Veja breakdown completo de custos
- **📥 Exportar**: Baixe os resultados em CSV ou Excel

## Exemplos Práticos

### Exemplo 1: Entregas Urbanas em São Paulo

**Configuração:**
```
Modo: Dados de Exemplo
Cidade: São Paulo
Clientes: 15
Veículos: 4
Raio: 30 km
Incluir Demandas: Sim
Capacidade: 100 unidades
```

**Resultado Esperado:**
- Distância total: ~150-200 km
- Custo total: ~R$ 500-700
- Tempo total: ~4-6 horas

### Exemplo 2: Distribuição Regional

**Configuração:**
```
Modo: Dados de Exemplo
Cidade: Brasília
Clientes: 10
Veículos: 3
Raio: 80 km
Distância Máxima: 300 km
```

**Resultado Esperado:**
- Distância total: ~300-400 km
- Custo total: ~R$ 1.000-1.500
- Tempo total: ~8-10 horas

## Dicas de Uso

### ✅ Boas Práticas

1. **Comece Pequeno**: Teste primeiro com 5-10 clientes
2. **Ajuste Gradualmente**: Aumente a complexidade aos poucos
3. **Valide os Dados**: Verifique se as coordenadas estão corretas
4. **Experimente Configurações**: Teste diferentes números de veículos
5. **Analise os Custos**: Compare cenários diferentes

### ⚠️ Problemas Comuns

**Problema**: "Não foi possível encontrar solução"
- **Solução**: Reduza o número de clientes ou aumente o número de veículos
- **Solução**: Aumente a distância máxima por veículo
- **Solução**: Aumente a capacidade dos veículos (se usar demandas)

**Problema**: Otimização muito lenta
- **Solução**: Reduza o número de localizações
- **Solução**: Use menos veículos
- **Solução**: Simplifique as restrições

**Problema**: Rotas muito longas
- **Solução**: Aumente o número de veículos
- **Solução**: Reduza o raio de distribuição
- **Solução**: Ajuste a distância máxima por veículo

## Próximos Passos

Depois de dominar o básico:

1. **Use Seus Dados Reais**: Prepare um CSV com seus clientes
2. **Ajuste os Custos**: Configure valores precisos da sua operação
3. **Compare Cenários**: Teste diferentes configurações de frota
4. **Exporte Resultados**: Use os dados exportados no seu planejamento
5. **Automatize**: Integre o sistema no seu fluxo de trabalho

## Suporte

Para dúvidas ou problemas:
- Consulte o README.md completo
- Verifique os exemplos na pasta `data/`
- Execute os testes: `python test_system.py`

## Recursos Adicionais

- **Documentação Completa**: `README.md`
- **Código Fonte**: Pasta `modules/`
- **Exemplos**: Pasta `data/`
- **Testes**: `test_system.py`

---

**Desenvolvido para resolver problemas reais de logística no Brasil** 🇧🇷

