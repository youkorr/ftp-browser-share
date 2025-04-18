ARG BUILD_FROM=ghcr.io/hassio-addons/base:13.0.0
FROM ${BUILD_FROM}

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

# Approche alternative pour Python - utiliser les packages apk lorsque disponibles
RUN apk add --no-cache \
    py3-flask \
    py3-requests \
    py3-jwt \
    py3-dateutil \
    py3-werkzeug

# Pour pyftpdlib qui n'a peut-être pas de package Alpine, on utilisera pip 
# mais d'une manière plus sûre
RUN python3 -m pip install --no-cache-dir pyftpdlib --break-system-packages

# Copie des fichiers de configuration et scripts
COPY rootfs/ /

# Copier le script d'exécution principal
COPY run.sh /
RUN chmod +x /run.sh && \
    find /etc/services.d -type f -name run -exec chmod +x {} \;

# Préparer le frontend
WORKDIR /usr/share/ftpbrowser
COPY rootfs/usr/share/ftpbrowser/package.json ./
RUN npm install

# Port exposé pour l'interface web
EXPOSE 8099

# Point d'entrée supervisé par S6
RUN chmod +x /etc/cont-init.d/*

# Métadonnées
LABEL \
    io.hass.name="FTP Browser & Media Share" \
    io.hass.description="Naviguer et partager des fichiers via FTP" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Votre Nom <votre.email@example.com>"


