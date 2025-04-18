FROM python:3.9-alpine

# Installer les dépendances système
RUN apk add --no-cache \
    build-base \
    linux-headers \
    nginx \
    nodejs \
    npm

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du backend
COPY backend/ ./backend/
COPY requirements.txt .

# Copier les fichiers frontend
COPY frontend/ ./frontend/

# Copier la configuration Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Installer les dépendances frontend
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Revenir au répertoire principal
WORKDIR /app

# Copier le script de démarrage
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exposer les ports
EXPOSE 80 8099

# Point d'entrée
CMD ["/entrypoint.sh"]

