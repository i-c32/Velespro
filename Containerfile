FROM archlinux:latest

# ── 1. Sistema base ────────────────────────────────────────────────────────────
# Se actualiza e instalan paquetes en una sola capa para evitar cache stale.
# Al final se limpia la caché de pacman para reducir el tamaño de la imagen.
RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm \
    base-devel \
    python \
    python-pip \
    python-virtualenv \
    neovim \
    git \
    nodejs \
    npm && \
    pacman -Scc --noconfirm && \
    rm -rf /var/cache/pacman/pkg/*

# ── 2. Usuario no-root ─────────────────────────────────────────────────────────
ARG USERNAME=developer
ARG UID=1000
ARG GID=1000

RUN groupadd --gid $GID $USERNAME && \
    useradd --uid $UID --gid $GID -m -s /bin/bash $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# ── 3. Variables de entorno ────────────────────────────────────────────────────
ENV EDITOR=nvim \
    VIRTUAL_ENV=/home/$USERNAME/.venv \
    PATH="/home/$USERNAME/.venv/bin:$PATH"

# ── 4. Entorno virtual + dependencias del pyproject.toml ──────────────────────
# Copiamos primero solo el pyproject.toml para aprovechar el cache de capas:
# si el código cambia pero las deps no, esta capa no se reconstruye.
USER $USERNAME
WORKDIR /home/$USERNAME/workspace

COPY --chown=$USERNAME:$USERNAME pyproject.toml README.md ./
RUN mkdir -p src

RUN python -m venv $VIRTUAL_ENV && \
    pip install --upgrade pip && \
    pip install -e ".[dev]"

# ── 5. Código fuente (capa separada para cache eficiente) ──────────────────────
#COPY --chown=$USERNAME:$USERNAME . /home/$USERNAME/workspace/

CMD ["/bin/bash"]
