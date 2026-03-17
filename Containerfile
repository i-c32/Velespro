# ══════════════════════════════════════════════════════════════════════════════
# STAGE 1 — base
# Imagen mínima compartida: sistema + usuario no-root + Python limpio.
# Ni herramientas de desarrollo ni dependencias de la app.
# ══════════════════════════════════════════════════════════════════════════════
FROM fedora:latest AS base

ARG USERNAME=developer
ARG UID=1000
ARG GID=1000

# Sistema base: solo Python y lo estrictamente necesario para compilar wheels
RUN dnf upgrade -y && \
    dnf install -y \
        python3 \
        python3-pip && \
    dnf clean all && \
    rm -rf /var/cache/dnf*

# Usuario no-root con UID/GID del host para evitar problemas de permisos
RUN groupadd --gid "$GID" "$USERNAME" && \
    useradd  --uid "$UID" --gid "$GID" -m -s /bin/bash "$USERNAME"

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# ══════════════════════════════════════════════════════════════════════════════
# STAGE 2 — development
# Imagen completa: herramientas de edición + venv con extras [dev] + bash.
# El código NO se copia aquí; se monta como volumen desde el host.
# ══════════════════════════════════════════════════════════════════════════════
FROM base AS development

# Herramientas exclusivas del entorno de desarrollo
RUN dnf install -y \
        neovim \
        man-db \
        git \
        nodejs \
        scdoc \
        npm && \
    dnf clean all && \
    rm -rf /var/cache/dnf*

ENV EDITOR=nvim

# Compilar el .scd y dejarlo en la estructura correcta
COPY --chown=root:root .config/man/nvim_cheat.1.scd /tmp/nvim_cheat.scd
RUN mkdir -p /usr/local/share/man/man1 && \
    scdoc < /tmp/nvim_cheat.scd > /usr/local/share/man/man1/nvim_cheat.1 && \
    rm /tmp/nvim_cheat.scd && \
    mandb --quiet

# [FIX] Crear el venvs y fijar permisos ANTES de cambiar de usuario,
# así los RUN posteriores (como pip install) pueden correr como $USERNAME.
RUN python3 -m venv "$VIRTUAL_ENV"  && chown -R "$UID:$GID" "$VIRTUAL_ENV"

# WORKDIR definido antes del primer COPY
WORKDIR /home/$USERNAME/workspace

# Todos los pasos siguientes corren como el usuario no-root
USER $USERNAME

# 1. Instalar dependencias (incluye grupo [dev]: pytest, linters, type-checkers…)
COPY --chown=$USERNAME:$USERNAME pyproject.toml README.md ./
RUN mkdir -p src && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e ".[dev]" && \
    pip install --no-cache-dir yamllint

# El código se monta en tiempo de ejecución vía compose → no se copia aquí
CMD ["/bin/bash"]

# ══════════════════════════════════════════════════════════════════════════════
# STAGE 3 — production
# Imagen final ligera: solo dependencias de runtime + código fuente copiado.
# Sin Neovim, sin git, sin npm, sin paquetes [dev].
# ══════════════════════════════════════════════════════════════════════════════
FROM python:3.14-slim AS production

ARG USERNAME=developer
ARG UID=1000
ARG GID=1000

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgomp1 \
        libgfortran5 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --gid "$GID" "$USERNAME" && \
    useradd  --uid "$UID" --gid "$GID" -m -s /bin/bash "$USERNAME"

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/home/developer/workspace/src"

RUN python -m venv "$VIRTUAL_ENV" && chown -R "$UID:$GID" "$VIRTUAL_ENV"

WORKDIR /home/$USERNAME/workspace
USER $USERNAME

# 1. Instalar dependencias (capa cacheada independiente del código)
COPY --chown=$USERNAME:$USERNAME pyproject.toml README.md ./

RUN mkdir -p src && \
    pip install --no-cache-dir --upgrade pip  && \
    pip install --no-cache-dir .           # solo dependencias de producción (sin [dev])

# 2. Copiar el código fuente (capa separada para cache eficiente)
COPY --chown=$USERNAME:$USERNAME src/       ./src/
COPY --chown=$USERNAME:$USERNAME resources/ ./resources/

# Ajusta este CMD al entry-point real de tu aplicación
ENTRYPOINT ["python", "-m", "src.velespro"]
CMD ["--help"]
