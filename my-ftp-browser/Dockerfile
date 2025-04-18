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
    tini

# Installer les dépendances Python
RUN pip3 install --no-cache-dir \
    flask \
    pyftpdlib

# Créer les répertoires nécessaires
RUN mkdir -p \
    /run/s6/services/nginx \
    /run/s6/services/ftp-server \
    /usr/share/ftpbrowser \
    /config/www/partage/shared

# Copier les fichiers de configuration
COPY rootfs /

# Définir les permissions de manière explicite
RUN set -x \
    && find /etc/services.d -type f -name "run" -exec chmod 0755 {} \; \
    && find /etc/cont-init.d -type f -exec chmod 0755 {} \; \
    && chmod 0755 /run.sh

# Installer les dépendances frontend
WORKDIR /usr/share/ftpbrowser
RUN npm install

# Nettoyer et préparer
RUN chown -R root:root /usr/share/ftpbrowser \
    && chmod -R 755 /usr/share/ftpbrowser

# Make sure /init script exists and is executable
RUN if [ -f "/init" ]; then chmod 755 /init; fi

# Use tini as an init system
ENTRYPOINT ["/sbin/tini", "--"]

# Define your command to start your services
CMD ["/run.sh"]


