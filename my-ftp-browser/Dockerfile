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
    openssl-dev \
    py3-flask \
    py3-requests \
    py3-jwt \
    py3-dateutil \
    py3-werkzeug

# Installation de pyftpdlib via pip
RUN python3 -m pip install --no-cache-dir pyftpdlib --break-system-packages

# Copie des fichiers de configuration, scripts et frontend
COPY rootfs/ /

# Installer les dépendances Python en séparant chaque commande pour une meilleure visibilité des erreurs
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir Flask==2.0.1 && \
    pip3 install --no-cache-dir Werkzeug==2.0.3 && \
    pip3 install --no-cache-dir requests==2.26.0 && \
    pip3 install --no-cache-dir PyJWT==2.1.0 && \
    pip3 install --no-cache-dir python-dateutil==2.8.2
# Permissions pour les scripts cont-init.d et services.d
RUN chmod +x /run.sh \
    && find /etc/cont-init.d/ -type f -exec chmod +x {} \; \
    && find /etc/services.d/ -type f -name run -exec chmod +x {} \;

# Installer le frontend (si package.json existe)
WORKDIR /usr/share/ftpbrowser
COPY rootfs/usr/share/ftpbrowser/package.json ./
RUN npm install

# Rendre les scripts exécutables
RUN chmod a+x /run.sh && \
    find /etc/services.d -type f -name run -exec chmod a+x {} \;
# Ports exposés
EXPOSE 8099

# Point d’entrée supervisé par S6
ENTRYPOINT [ "/init" ]

# Métadonnées
LABEL \
    io.hass.name="FTP Browser & Media Share" \
    io.hass.description="Access FTP servers with a user-friendly web interface, share files, and stream media" \
    io.hass.description="Naviguer et partager des fichiers via FTP" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Votre Nom <votre.email@example.com>"



