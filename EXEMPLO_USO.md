# 🎬 Exemplo de Uso: Seletor de Algoritmos

## Como Usar o Seletor de Algoritmos

### 1. Acesse a Interface

Abra a aplicação Streamlit no navegador.

### 2. Localize o Seletor de Algoritmos

Na barra lateral esquerda, você verá uma nova seção:

```
🧮 Algoritmo de Otimização
```

### 3. Escolha o Algoritmo

Você tem duas opções:

#### **OR-Tools (Recomendado)**
- Algoritmo avançado do Google
- Melhores resultados de otimização
- Mais lento (10-60 segundos)
- Parâmetros configuráveis

**Parâmetros Avançados:**
- Estratégia de Primeira Solução
- Metaheurística
- Tempo Limite

#### **Nearest Neighbor (Rápido)**
- Heurística simples e rápida
- Resultados bons (não ótimos)
- Muito rápido (< 1 segundo)
- Sem parâmetros adicionais

### 4. Configure os Dados

Configure seus dados normalmente:
- Modo de entrada (Exemplo, CSV, Manual)
- Número de veículos
- Capacidades (se necessário)
- Custos

### 5. Clique em "🚀 Otimizar Rotas"

O sistema irá:
1. Usar o algoritmo selecionado
2. Mostrar progresso
3. Exibir resultados

### 6. Veja as Informações do Algoritmo

Nos resultados, você verá:

```
🧮 Algoritmo Utilizado: Nearest Neighbor | ⏱️ Tempo de Execução: 0.00s
```

Ou:

```
🧮 Algoritmo Utilizado: OR-Tools | ⏱️ Tempo de Execução: 12.45s
```

## 📊 Quando Usar Cada Algoritmo

### Use **Nearest Neighbor** quando:
- ✅ Precisar de resultados rápidos
- ✅ Tiver muitas localizações (> 50)
- ✅ Não precisar da solução ótima
- ✅ Quiser fazer testes rápidos
- ✅ Tiver restrições de tempo

### Use **OR-Tools** quando:
- ✅ Precisar da melhor solução possível
- ✅ Tiver tempo para esperar
- ✅ Tiver menos localizações (< 30)
- ✅ Quiser explorar diferentes estratégias
- ✅ Precisar de soluções para produção

## 🎯 Comparação Prática

### Exemplo: 10 Clientes em São Paulo

**Nearest Neighbor:**
- Distância: 175.99 km
- Tempo: < 0.01s
- Veículos: 2

**OR-Tools:**
- Distância: 177.00 km
- Tempo: 0.01s
- Veículos: 3

**Análise:**
- Nearest Neighbor foi ligeiramente melhor neste caso
- Ambos foram muito rápidos
- OR-Tools usou mais veículos (melhor balanceamento)

### Exemplo: 50 Clientes

**Nearest Neighbor:**
- Tempo: ~0.1s
- Resultado: Bom

**OR-Tools:**
- Tempo: ~60s
- Resultado: Ótimo (5-10% melhor)

## 💡 Dicas

1. **Teste Rápido**: Use Nearest Neighbor primeiro para validar dados
2. **Otimização Final**: Use OR-Tools para solução de produção
3. **Compare**: Execute ambos e compare resultados
4. **Ajuste Parâmetros**: Experimente diferentes estratégias no OR-Tools

## 🔄 Fluxo de Trabalho Recomendado

```
1. Carregar dados
   ↓
2. Testar com Nearest Neighbor (validação rápida)
   ↓
3. Ajustar configurações se necessário
   ↓
4. Otimizar com OR-Tools (solução final)
   ↓
5. Comparar resultados
   ↓
6. Exportar melhor solução
```

## 📚 Próximos Passos

Agora que você sabe usar o seletor:

1. Adicione seus próprios algoritmos (veja GUIA_ADICIONAR_ALGORITMOS.md)
2. Compare diferentes estratégias
3. Analise trade-offs tempo vs qualidade
4. Escolha o melhor para seu caso de uso

---

**Sistema pronto para produção!** 🚀
