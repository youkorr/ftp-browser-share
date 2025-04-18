FROM homeassistant/amd64-base-python:3.9-alpine3.13

# Métadonnées
LABEL description="FTP Browser Share Addon"
LABEL maintainer="Votre Nom"

# Installer les dépendances système
RUN apk add --no-cache \
    nginx \
    python3 \
    py3-pip \
    nodejs \
    npm

# Copier les fichiers de l'application
COPY rootfs /

# Installer les dépendances Python
RUN pip3 install --no-cache-dir \
    flask \
    python-ftplib

# Installer les dépendances frontend
WORKDIR /usr/share/ftpbrowser
RUN npm install

# Permissions
RUN chmod a+x /run.sh

# Point d'entrée
CMD [ "/run.sh" ]
