FROM archlinux:latest

# Actualizar sistema e instalar paquetes básicos
RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm \
    base-devel \
    python \
    python-pip \
    neovim \
    git \
    nodejs \
    # Limpieza crucial: pacman guarda todos los .tar descargados
    pacman -Scc --noconfirm

# Crear un usuario para no trabajar como root
ARG USERNAME=developer
RUN useradd -m -s /bin/bash $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/$USERNAME

# 3. Variables de entorno de Python y Herramientas
# Arch bloquea instalaciones de pip globales por defecto ahora (PEP 668)
ENV PIP_BREAK_SYSTEM_PACKAGES=1
ENV EDITOR=nvim

USER $USERNAME
WORKDIR /home/$USERNAME/workspace
