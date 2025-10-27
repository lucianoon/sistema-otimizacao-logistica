# ✏️ Guia de Uso: Entrada Manual

## 📍 Como Adicionar Localizações Manualmente

A funcionalidade de **Entrada Manual** permite que você adicione localizações (depósito e clientes) diretamente na interface, sem precisar de arquivos CSV.

### 🎯 Quando Usar

Use entrada manual quando:
- ✅ Tiver poucas localizações (< 20)
- ✅ Quiser testar rapidamente
- ✅ Não tiver arquivo CSV pronto
- ✅ Precisar de controle total sobre cada ponto

### 📝 Passo a Passo

#### **1. Selecione "Entrada Manual"**

Na barra lateral, escolha:
```
Modo de Entrada de Dados: Entrada Manual
```

#### **2. Configure o Depósito**

O depósito é o ponto de partida e chegada dos veículos.

**Campos:**
- **Nome do Depósito**: Ex: "Centro de Distribuição SP"
- **Latitude**: Coordenada de latitude (ex: -23.5505)
- **Longitude**: Coordenada de longitude (ex: -46.6333)

**Exemplo - São Paulo:**
```
Nome: Depósito Central
Latitude: -23.5505
Longitude: -46.6333
```

#### **3. Adicione Clientes**

Para cada cliente, preencha:

**Campos:**
- **Nome do Cliente**: Ex: "Cliente 1 - Zona Norte"
- **Latitude**: Coordenada de latitude
- **Longitude**: Coordenada de longitude
- **Demanda (opcional)**: Quantidade de carga (0 se não usar)

**Exemplo:**
```
Nome: Cliente 1 - Zona Norte
Latitude: -23.5200
Longitude: -46.6300
Demanda: 15
```

Clique em **"➕ Adicionar Cliente"**

#### **4. Gerencie Clientes**

**Ver clientes adicionados:**
- Clique em "📋 Ver Clientes" para expandir a lista

**Remover cliente:**
- Clique no botão "❌" ao lado do cliente

**Limpar todos:**
- Clique em "🗑️ Limpar Todos os Clientes"

#### **5. Otimize as Rotas**

Quando tiver pelo menos 1 cliente:
1. Configure número de veículos
2. Ajuste custos (opcional)
3. Clique em "🚀 Otimizar Rotas"

### 🗺️ Como Obter Coordenadas

#### **Opção 1: Google Maps**

1. Abra [Google Maps](https://maps.google.com)
2. Clique com botão direito no local desejado
3. Clique no primeiro item (coordenadas)
4. As coordenadas serão copiadas

**Formato:** `-23.5505, -46.6333`
- Primeiro número = Latitude
- Segundo número = Longitude

#### **Opção 2: Buscar Endereço**

1. Digite o endereço no Google Maps
2. Clique com botão direito no marcador
3. Copie as coordenadas

#### **Opção 3: Usar Ferramenta Online**

- [LatLong.net](https://www.latlong.net/)
- [GPS Coordinates](https://gps-coordinates.org/)

### 📊 Exemplo Completo

**Cenário:** Entregas em São Paulo

**Depósito:**
```
Nome: CD São Paulo
Latitude: -23.5505
Longitude: -46.6333
```

**Clientes:**

1. **Cliente 1 - Zona Norte**
   - Latitude: -23.5200
   - Longitude: -46.6300
   - Demanda: 15

2. **Cliente 2 - Zona Sul**
   - Latitude: -23.6100
   - Longitude: -46.6500
   - Demanda: 20

3. **Cliente 3 - Zona Leste**
   - Latitude: -23.5500
   - Longitude: -46.5800
   - Demanda: 18

4. **Cliente 4 - Zona Oeste**
   - Latitude: -23.5400
   - Longitude: -46.7000
   - Demanda: 12

**Configuração:**
- Veículos: 2
- Capacidade: 50 unidades cada
- Algoritmo: OR-Tools

**Resultado Esperado:**
- Distância total: ~40-50 km
- 2 rotas otimizadas
- Todos os clientes atendidos

### 💡 Dicas

#### **Coordenadas Válidas no Brasil**

**Latitude:**
- Norte: ~5° (positivo)
- Sul: ~-34° (negativo)
- **Formato:** -23.5505 (6 casas decimais)

**Longitude:**
- Leste: ~-34° (negativo)
- Oeste: ~-74° (negativo)
- **Formato:** -46.6333 (6 casas decimais)

#### **Precisão**

- 4 casas decimais: ~11 metros
- 5 casas decimais: ~1 metro
- 6 casas decimais: ~0.1 metro (recomendado)

#### **Validação**

O sistema valida automaticamente:
- ✅ Coordenadas dentro dos limites válidos
- ✅ Formato numérico correto
- ✅ Pelo menos 1 cliente adicionado

### ⚠️ Problemas Comuns

#### **"Adicione pelo menos 1 cliente"**

**Causa:** Nenhum cliente foi adicionado ainda

**Solução:** Preencha o formulário e clique em "➕ Adicionar Cliente"

#### **Coordenadas invertidas**

**Sintoma:** Pontos aparecem fora do Brasil no mapa

**Solução:** Verifique se:
- Latitude vem primeiro (ex: -23.5505)
- Longitude vem depois (ex: -46.6333)
- Ambos são negativos no Brasil

#### **Cliente não aparece na lista**

**Causa:** Nome do cliente vazio

**Solução:** Preencha o campo "Nome do Cliente" antes de adicionar

### 🔄 Fluxo de Trabalho

```
1. Selecionar "Entrada Manual"
   ↓
2. Configurar Depósito
   ↓
3. Adicionar Cliente 1
   ↓
4. Adicionar Cliente 2
   ↓
5. Adicionar Cliente 3...
   ↓
6. Verificar lista de clientes
   ↓
7. Configurar veículos e custos
   ↓
8. Otimizar rotas
   ↓
9. Analisar resultados
   ↓
10. Exportar (opcional)
```

### 📍 Principais Cidades do Brasil

Use estas coordenadas como referência:

| Cidade | Latitude | Longitude |
|--------|----------|-----------|
| São Paulo | -23.5505 | -46.6333 |
| Rio de Janeiro | -22.9068 | -43.1729 |
| Belo Horizonte | -19.9167 | -43.9345 |
| Brasília | -15.7939 | -47.8828 |
| Curitiba | -25.4284 | -49.2733 |
| Porto Alegre | -30.0346 | -51.2177 |
| Salvador | -12.9714 | -38.5014 |
| Fortaleza | -3.7172 | -38.5433 |
| Recife | -8.0476 | -34.8770 |
| Manaus | -3.1190 | -60.0217 |

### 🎓 Exemplo de Uso Real

**Empresa:** Distribuidora de Bebidas em SP

**Depósito:**
```
Nome: CD Guarulhos
Latitude: -23.4538
Longitude: -46.5333
```

**Clientes (Supermercados):**
```
1. Extra Tatuapé: -23.5400, -46.5750, Demanda: 30
2. Carrefour Mooca: -23.5650, -46.5950, Demanda: 25
3. Pão de Açúcar Vila Mariana: -23.5880, -46.6350, Demanda: 20
4. Extra Pinheiros: -23.5670, -46.6820, Demanda: 35
5. Carrefour Santana: -23.5050, -46.6290, Demanda: 28
```

**Configuração:**
- 2 caminhões
- Capacidade: 80 caixas cada
- Custo combustível: R$ 6,50/L
- Consumo: 6 km/L (caminhão carregado)

**Resultado:**
- Distância total: 68 km
- Custo total: R$ 285
- Tempo: 3h 20min
- Economia vs rotas manuais: 23%

### ✨ Vantagens da Entrada Manual

- ✅ **Flexibilidade**: Adicione pontos conforme necessário
- ✅ **Controle**: Veja exatamente o que está sendo adicionado
- ✅ **Rapidez**: Para poucos pontos, mais rápido que CSV
- ✅ **Teste**: Ideal para validar o sistema
- ✅ **Aprendizado**: Entenda melhor como funciona

### 📚 Próximos Passos

Depois de dominar a entrada manual:

1. **Exporte para CSV**: Salve seus dados para reutilizar
2. **Use Upload CSV**: Para lotes maiores
3. **Automatize**: Integre com seu sistema
4. **Otimize**: Teste diferentes configurações

---

**Entrada manual agora totalmente funcional!** ✏️✨

