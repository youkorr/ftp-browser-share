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
    npm

# Installer les dépendances Python
RUN pip3 install --no-cache-dir \
    flask \
    pyftpdlib

# Copier les fichiers de configuration
COPY rootfs /

# Créer les répertoires nécessaires
RUN mkdir -p \
    /usr/share/ftpbrowser \
    /config/www/partage/shared

# Copier les fichiers de l'application
COPY rootfs/usr/share/ftpbrowser /usr/share/ftpbrowser

# Donner les permissions d'exécution
RUN chmod a+x /run.sh \
    && chmod a+x /etc/services.d/nginx/run \
    && chmod a+x /etc/services.d/ftp-server/run

# Installer les dépendances frontend
WORKDIR /usr/share/ftpbrowser
RUN npm install

# Nettoyer et préparer
RUN chown -R root:root /usr/share/ftpbrowser \
    && chmod -R 755 /usr/share/ftpbrowser

# Point d'entrée par défaut de Home Assistant
ENTRYPOINT ["/init"]

# Commande à exécuter
CMD ["/run.sh"]

