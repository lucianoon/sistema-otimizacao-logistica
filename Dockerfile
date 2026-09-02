FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/usr/local \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true

WORKDIR /app

# Camada de dependências: só invalida quando o lockfile muda. As versões são
# exatamente as que o CI testou (`uv sync --locked`). Todas têm wheels para
# 3.12, então build-essential deixou de ser necessário (o packages.txt segue
# existindo só para o Streamlit Cloud).
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY app.py compare_algorithms.py ./
COPY modules ./modules
COPY data ./data

# Processo sem root. O Streamlit escreve em ~/.streamlit, por isso HOME gravável.
RUN useradd --create-home --uid 1000 app && chown -R app:app /app
USER app

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

CMD ["streamlit", "run", "app.py"]
