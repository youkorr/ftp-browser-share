FROM homeassistant/amd64-base-python:3.9-alpine3.13

# Métadonnées
LABEL description="FTP Browser Share Addon"
LABEL maintainer="Votre Nom"

# Installer les dépendances système et Python
RUN apk add --no-cache \
    nginx \
    python3 \
    py3-pip \
    py3-flask \
    nodejs \
    npm \
    && pip3 install --no-cache-dir \
    pyftpdlib \
    flask

# Copier les fichiers de l'application
COPY rootfs /

# Créer le script de démarrage
RUN echo '#!/bin/sh' > /run.sh && \
    echo 'nginx' >> /run.sh && \
    echo 'python3 /usr/share/ftpbrowser/api/server.py' >> /run.sh && \
    chmod +x /run.sh

# Installer les dépendances frontend
WORKDIR /usr/share/ftpbrowser
RUN npm install

# Point d'entrée
CMD ["/run.sh"]
