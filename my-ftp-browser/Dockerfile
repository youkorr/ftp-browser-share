FROM homeassistant/amd64-base-python:3.9-alpine3.13

# Métadonnées
LABEL description="FTP Browser Share Addon"
LABEL maintainer="Votre Nom"

# Installer les dépendances système et s6-overlay
RUN apk add --no-cache \
    nginx \
    python3 \
    py3-pip \
    py3-flask \
    nodejs \
    npm \
    bash

# Télécharger et installer l'overlay S6 (version stable)
ARG S6_OVERLAY_VERSION=3.1.5.0
RUN wget -O /tmp/s6-overlay-noarch.tar.xz https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz && \
    wget -O /tmp/s6-overlay-x86_64.tar.xz https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz && \
    rm -f /tmp/s6-overlay-noarch.tar.xz /tmp/s6-overlay-x86_64.tar.xz

# Installer les dépendances Python
RUN pip3 install --no-cache-dir \
    flask \
    pyftpdlib

# Créer les répertoires nécessaires
RUN mkdir -p \
    /etc/services.d/nginx \
    /etc/services.d/ftp-server \
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

# S'assurer que l'init script a les bonnes permissions
RUN chmod 755 /init || true

# Point d'entrée pour S6
ENTRYPOINT ["/bin/sh", "-c"]
CMD ["/run.sh"]


