# Étape 1: Build du frontend avec Node.js
FROM node:18 as build-frontend

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build || (echo "Build failed" && cat package.json && ls -la && exit 1)

# Étape 2: Image finale avec Python
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    lftp \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-cors pyftpdlib

# Create app directory
WORKDIR /app

# Copier les fichiers backend
COPY ./api ./api
COPY ./run.sh ./run.sh

# Copier les fichiers frontend construits de l'étape précédente
COPY --from=build-frontend /app/build ./build

# Make scripts executable
RUN chmod +x /app/run.sh
RUN chmod +x /app/api/start_api.sh

EXPOSE 3000

CMD [ "/app/run.sh" ]
