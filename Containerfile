# ══════════════════════════════════════════════════════════════════════════════
# STAGE 1 — base
# Imagen mínima compartida: sistema + usuario no-root + Python limpio.
# Ni herramientas de desarrollo ni dependencias de la app.
# ══════════════════════════════════════════════════════════════════════════════
FROM archlinux:latest AS base

ARG USERNAME=developer
ARG UID=1000
ARG GID=1000

# Sistema base: solo Python y lo estrictamente necesario para compilar wheels
RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm \
        base-devel \
        python \
        python-pip && \
    pacman -Scc --noconfirm && \
    rm -rf /var/cache/pacman/pkg/*

# Usuario no-root con UID/GID del host para evitar problemas de permisos
RUN groupadd --gid "$GID" "$USERNAME" && \
    useradd  --uid "$UID" --gid "$GID" -m -s /bin/bash "$USERNAME"

# Variables de entorno comunes a ambos stages hijos
# el entorno vitual se encuentra en /opt/venv
RUN mkdir -p /opt/venv && chown "$UID:$GID" /opt/venv

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# ══════════════════════════════════════════════════════════════════════════════
# STAGE 2 — development
# Imagen completa: herramientas de edición + venv con extras [dev] + bash.
# El código NO se copia aquí; se monta como volumen desde el host.
# ══════════════════════════════════════════════════════════════════════════════
FROM base AS development

# Herramientas exclusivas del entorno de desarrollo
RUN pacman -S --noconfirm \
        python-virtualenv \
        neovim \
        git \
        nodejs \
        npm && \
    pacman -Scc --noconfirm && \
    rm -rf /var/cache/pacman/pkg/*

ENV EDITOR=nvim

USER $USERNAME
WORKDIR /home/$USERNAME/workspace

# 1. Instalar dependencias (incluye grupo [dev]: pytest, linters, type-checkers…)
COPY --chown=$USERNAME:$USERNAME pyproject.toml README.md ./
RUN mkdir -p src && \
    python -m venv "$VIRTUAL_ENV" && \
    pip install --upgrade pip --quiet && \
    pip install -e ".[dev]" --quiet   # editable + extras de desarrollo

# El código se monta en tiempo de ejecución vía compose → no se copia aquí
CMD ["/bin/bash"]

# ══════════════════════════════════════════════════════════════════════════════
# STAGE 3 — production
# Imagen final ligera: solo dependencias de runtime + código fuente copiado.
# Sin Neovim, sin git, sin npm, sin paquetes [dev].
# ══════════════════════════════════════════════════════════════════════════════
FROM base AS production

USER $USERNAME
WORKDIR /home/$USERNAME/workspace

# 1. Instalar dependencias (capa cacheada independiente del código)
COPY --chown=$USERNAME:$USERNAME pyproject.toml README.md ./
RUN mkdir -p src && \
    python -m venv "$VIRTUAL_ENV" && \
    pip install --upgrade pip --quiet && \
    pip install . --quiet          # solo dependencias de producción (sin [dev])

# 2. Copiar el código fuente (capa separada para cache eficiente)
COPY --chown=$USERNAME:$USERNAME src/       ./src/
COPY --chown=$USERNAME:$USERNAME resources/ ./resources/

# Ajusta este CMD al entry-point real de tu aplicación
ENTRYPOINT ["python", "-m", "src"]
CMD ["--help"]
