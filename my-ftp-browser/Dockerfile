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
    npm

# Mise à jour de pip et installation des dépendances Python
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir \
        flask \
        requests \
        PyJWT \
        python-dateutil \
        werkzeug \
        pyftpdlib

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
ENTRYPOINT ["/init"]

# Métadonnées
LABEL \
    io.hass.name="FTP Browser & Media Share" \
    io.hass.description="Naviguer et partager des fichiers via FTP" \
    io.hass.description="Access FTP servers with a user-friendly web interface, share files, and stream media" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Votre Nom <votre.email@example.com>"


