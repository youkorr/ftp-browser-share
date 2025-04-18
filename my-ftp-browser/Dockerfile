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

# Créer les répertoires nécessaires
RUN mkdir -p \
    /usr/share/ftpbrowser \
    /config/www/partage/shared \
    /run/nginx

# Copier et préparer les fichiers
COPY rootfs/usr/share/ftpbrowser /usr/share/ftpbrowser
COPY rootfs/run.sh /
RUN chmod a+x /run.sh

# Installer les dépendances frontend
WORKDIR /usr/share/ftpbrowser
RUN npm install

# Permissions et préparation
RUN chown -R root:root /usr/share/ftpbrowser \
    && chmod -R 755 /usr/share/ftpbrowser \
    && chmod -R 755 /config

# Point d'entrée par défaut de Home Assistant
ENTRYPOINT ["/init"]

# Commande à exécuter
CMD ["/run.sh"]
