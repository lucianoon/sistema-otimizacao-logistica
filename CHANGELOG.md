# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e versionamento semântico.

## [Não lançado]

### Adicionado

- `pyproject.toml` + `uv.lock` como fonte única das dependências e da
  configuração de ruff, mypy e pytest. `requirements.txt` passa a ser exportado
  do lock, para o Streamlit Cloud; o CI falha se divergir.
- Job de CI que constrói a imagem Docker, sobe o Streamlit e confirma que o
  processo não é root.
- `SECURITY.md`, `CONTRIBUTING.md` e este CHANGELOG.
- Dependabot para GitHub Actions e dependências Python (mensal, minor/patch
  agrupados). CodeQL habilitado.

### Alterado

- Dockerfile instala pelo lockfile com `uv`, roda como usuário sem privilégios
  e deixa de instalar `build-essential` (todas as dependências têm wheels).
- CI usa `uv sync --locked`; READMEs migram as instruções para `uv`.
- Dependências resolvidas pelo lock nas versões atuais: numpy 1.26 para 2.5,
  pandas 2.1 para 2.3, OR-Tools 9.8 para 9.15, plotly 5 para 6, Streamlit 1.54
  para 1.63, folium 0.15 para 0.20. A suíte de 55 testes passa sem alteração.
- Guias movidos da raiz para `docs/` e indexados nos READMEs.

### Removido

- `ruff.toml`, `mypy.ini` e `pytest.ini`, absorvidos pelo `pyproject.toml`.

## [0.1.0] — 2026-08-27

### Adicionado

- Suíte pytest cobrindo cálculo de custos, manipulação de dados, heurística
  Nearest Neighbor e otimizador OR-Tools, substituindo o script ad hoc.
- CI no GitHub Actions com `pytest`, depois `ruff` e `mypy` como gates (#5).
- README em inglês; README em português volta a ser o principal.
- Dockerfile e `docker-compose.yml` para o app Streamlit.

### Alterado

- Streamlit 1.31 para 1.54 (alertas do Dependabot); numpy deixa de ser preso em 1.x.
- Tipos de `strategy`, `local_search` e `time_limit` declarados para o mypy.
- README enxugado de 19 para 12 seções, com linguagem de impacto baseada em evidência.

### Removido

- Documento de resumo do projeto, redundante com o README (#1).

## Origem — 2025-10-27

- Versão 1.0 do sistema: CVRP com OR-Tools, interface Streamlit, análise de
  custos e entrada manual de localizações.
