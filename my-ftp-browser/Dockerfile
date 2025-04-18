FROM alpine:3.18

# Métadonnées
LABEL description="FTP Browser Share Addon"
LABEL maintainer="Votre Nom"

# Installer Python et autres dépendances système
RUN apk add --no-cache \
    python3 \
    py3-pip \
    nginx \
    nodejs \
    npm \
    bash \
    curl

# Installer les dépendances Python
RUN pip3 install --no-cache-dir \
    flask \
    pyftpdlib

# Créer les répertoires nécessaires
RUN mkdir -p \
    /usr/share/ftpbrowser \
    /config/www/partage/shared

# Copier les fichiers de configuration
COPY rootfs/ /

# Définir les permissions explicitement - IMPORTANT pour run.sh
RUN chmod +x /run.sh && \
    ls -la /run.sh && \
    chmod -R +x /etc/services.d/*/run 2>/dev/null || true && \
    chmod -R +x /etc/cont-init.d/* 2>/dev/null || true

# Installer les dépendances frontend
WORKDIR /usr/share/ftpbrowser
RUN npm install

# Nettoyer et préparer
RUN chown -R root:root /usr/share/ftpbrowser \
    && chmod -R 755 /usr/share/ftpbrowser

# Utiliser un script shell comme point d'entrée
CMD ["/bin/sh", "/run.sh"]


