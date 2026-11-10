# ============================================================================
# FFernandes Engenharia e Construção Ltda. — Production Multi-Stage Dockerfile
# Skill: devops-cloud-deploy (Python 3.12 Alpine + Non-Root + Healthcheck)
# ============================================================================

FROM python:3.12-alpine AS runtime

LABEL maintainer="FFernandes Engenharia <contato@ffernandes.eng.br>"
LABEL org.opencontainers.image.title="FFernandes Engenharia — Full-Stack Web & API"
LABEL org.opencontainers.image.description="Portal Institucional, Portfólio Interativo e API REST de Projetos Complementares"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8090 \
    HOST=0.0.0.0

WORKDIR /app

# Criar usuário não-root para segurança de execução em container
RUN addgroup -S ffernandes && adduser -S ffernandes -G ffernandes

# Copiar código de backend, frontend e assets otimizados (.webp/.png/.jpg)
COPY --chown=ffernandes:ffernandes index.html ffernandes_engenharia.html ./
COPY --chown=ffernandes:ffernandes assets/ ./assets/
COPY --chown=ffernandes:ffernandes backend/ ./backend/

# Inicializar banco SQLite com seed determinístico durante o build
RUN python3 backend/seed_data.py && chown -R ffernandes:ffernandes /app/backend

USER ffernandes

EXPOSE 8090

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8090/api/v1/health', timeout=3)" || exit 1

CMD ["python3", "backend/server.py"]
