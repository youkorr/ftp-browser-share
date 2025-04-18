ARG BUILD_FROM=ghcr.io/hassio-addons/base:13.0.0
FROM ${BUILD_FROM}

# Définir la version du build
ARG BUILD_VERSION=dev

# Installation des dépendances système
RUN apk add --no-cache \
    python3 \
    python3-dev \
    py3-pip \
    py3-wheel \
    py3-setuptools \
    build-base \
    nginx \
    curl \
    tzdata \
    nodejs \
    npm \
    libffi-dev \
    openssl-dev

# Installation des dépendances Python
# Création d'un environnement virtuel Python pour éviter les conflits
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Installation des dépendances Python dans l'environnement virtuel
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    Flask==2.0.1 \
    Werkzeug==2.0.3 \
    requests==2.26.0 \
    PyJWT==2.1.0 \
    python-dateutil==2.8.2 \
    pyftpdlib

# Copie des fichiers de configuration, scripts et frontend
COPY rootfs/ /

# Installer le frontend
WORKDIR /usr/share/ftpbrowser
RUN npm install

# Rendre les scripts exécutables
RUN chmod a+x /run.sh && \
    find /etc/cont-init.d/ -type f -exec chmod +x {} \; && \
    find /etc/services.d/ -type f -name run -exec chmod a+x {} \;

# Ports exposés
EXPOSE 8099

# Point d'entrée supervisé par S6
ENTRYPOINT ["/init"]

# Métadonnées
LABEL \
    io.hass.name="FTP Browser & Media Share" \
    io.hass.description="Access FTP servers with a user-friendly web interface, share files, and stream media" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Votre Nom <votre.email@example.com>"


