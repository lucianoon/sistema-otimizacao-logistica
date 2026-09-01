# Como contribuir

## Ambiente

```bash
uv sync --locked              # mesmas versões do CI e da imagem Docker
uv run streamlit run app.py
```

Sem `uv`, `pip install -r requirements.txt` funciona: o arquivo é exportado do
`uv.lock` e existe para o Streamlit Cloud, que não lê o lockfile.

## Antes de abrir o PR

```bash
uv run ruff check .
uv run mypy
uv run pytest -q
```

Os três comandos são exatamente os que o CI executa. A suíte não faz chamada
de rede; a geocodificação e os mapas são exercitados com dados locais.

## Dependências

Adicione ao `pyproject.toml`, rode `uv lock` e regenere o arquivo derivado:

```bash
uv export --no-dev --no-hashes --no-annotate --no-header -o requirements.txt
```

Faça commit de `pyproject.toml`, `uv.lock` e `requirements.txt` juntos. O CI
falha se o lock estiver desatualizado ou se o `requirements.txt` divergir.

## Novos algoritmos

Veja `docs/GUIA_ADICIONAR_ALGORITMOS.md` para a interface que um otimizador
precisa implementar e como registrá-lo no seletor.

## Registro de mudanças

Descreva a mudança em `CHANGELOG.md`, na seção **Não lançado**.
