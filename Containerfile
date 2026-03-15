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
        python \
        python-pip && \
    pacman -Scc --noconfirm && \
    rm -rf /var/cache/pacman/pkg/*

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
RUN pacman -S --noconfirm \
        python-virtualenv \
        neovim \
        man-db \
        git \
        nodejs \
        scdoc \
        taplo-cli \
        yaml-language-server \
        vscode-json-languageserver \
        ruff && \
    pacman -Scc --noconfirm && \
    rm -rf /var/cache/pacman/pkg/*

ENV VIRTUAL_ENV_LSP=/opt/venv_lsp \
    PATH="/opt/venv/bin:/opt/venv_lsp/bin:$PATH" \
    EDITOR=nvim

# Compilar el .scd y dejarlo en la estructura correcta
COPY --chown=root:root .config/man/nvim_cheat.1.scd /tmp/nvim_cheat.scd
RUN mkdir -p /usr/local/share/man/man1 && \
    scdoc < /tmp/nvim_cheat.scd > /usr/local/share/man/man1/nvim_cheat.1 && \
    rm /tmp/nvim_cheat.scd && \
    mandb --quiet

# [FIX] Crear ambos venvs y fijar permisos ANTES de cambiar de usuario,
# así los RUN posteriores (como pip install) pueden correr como $USERNAME.
RUN python -m venv "$VIRTUAL_ENV"  && chown -R "$UID:$GID" "$VIRTUAL_ENV" && \
    python -m venv "$VIRTUAL_ENV_LSP" && chown -R "$UID:$GID" "$VIRTUAL_ENV_LSP"

# WORKDIR definido antes del primer COPY
WORKDIR /home/$USERNAME/workspace

# Todos los pasos siguientes corren como el usuario no-root
USER $USERNAME

# 1. Instalar dependencias (incluye grupo [dev]: pytest, linters, type-checkers…)
COPY --chown=$USERNAME:$USERNAME pyproject.toml README.md ./
RUN mkdir -p src && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e ".[dev]"   # editable + extras de desarrollo

# Creamos un entorno virtual para los lsp
# Dependencias LSP en su propio venv aislado
RUN /opt/venv_lsp/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv_lsp/bin/pip install --no-cache-dir \
        basedpyright \
        yamllint

# El código se monta en tiempo de ejecución vía compose → no se copia aquí
CMD ["/bin/bash"]

# ══════════════════════════════════════════════════════════════════════════════
# STAGE 3 — production
# Imagen final ligera: solo dependencias de runtime + código fuente copiado.
# Sin Neovim, sin git, sin npm, sin paquetes [dev].
# ══════════════════════════════════════════════════════════════════════════════
FROM base AS production

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
ENTRYPOINT ["python", "-m", "src"]
CMD ["--help"]
