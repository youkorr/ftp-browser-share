FROM homeassistant/amd64-base-python:3.9-alpine3.13

# Métadonnées
LABEL description="FTP Browser Share Addon"
LABEL maintainer="Votre Nom"

# Installer les dépendances système
RUN apk add --no-cache \
    nginx \
    python3 \
    py3-pip \
    py3-flask \
    nodejs \
    npm \
    bash

# Installer les dépendances Python
RUN pip3 install --no-cache-dir \
    flask \
    pyftpdlib

# Créer les répertoires nécessaires avec les bonnes permissions
RUN mkdir -p \
    /run/s6/services/nginx \
    /run/s6/services/ftp-server \
    /usr/share/ftpbrowser \
    /config/www/partage/shared \
    /etc/services.d/nginx \
    /etc/services.d/ftp-server \
    /etc/cont-init.d

# Copier les fichiers de configuration
COPY rootfs /

# Définir les permissions de manière explicite
RUN set -x \
    && chmod 755 /run.sh \
    && find /etc/services.d -type f -name "run" -exec chmod 755 {} \; \
    && find /etc/cont-init.d -type f -exec chmod 755 {} \; \
    && chown -R root:root /etc/services.d \
    && chown -R root:root /etc/cont-init.d \
    && chown -R root:root /run.sh

# Installer les dépendances frontend
WORKDIR /usr/share/ftpbrowser
RUN npm install

# Nettoyer et préparer
RUN chown -R root:root /usr/share/ftpbrowser \
    && chmod -R 755 /usr/share/ftpbrowser

# Point d'entrée par défaut de Home Assistant
ENTRYPOINT ["/init"]


