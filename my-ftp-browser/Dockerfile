FROM alpine:3.19

# Ajouter les dépôts nécessaires
RUN echo "http://dl-cdn.alpinelinux.org/alpine/latest-stable/main" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/latest-stable/community" >> /etc/apk/repositories && \
    apk update

# Installer les dépendances système
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-setuptools \
    gcc \
    g++ \
    musl-dev \
    make \
    binutils \
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

# Script principal
COPY run.sh /
RUN chmod +x /run.sh && \
    find /etc/services.d -type f -name run -exec chmod +x {} \;

# Préparer le frontend
WORKDIR /usr/share/ftpbrowser
COPY rootfs/usr/share/ftpbrowser/package.json ./
RUN npm install || true

# Port exposé pour l'interface web
EXPOSE 8099

# Point d’entrée supervisé par S6
ENTRYPOINT ["/init"]

# Métadonnées
LABEL \
    io.hass.name="FTP Browser & Media Share" \
    io.hass.description="Access FTP servers with a user-friendly web interface, share files, and stream media" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Votre Nom <votre.email@example.com"]






