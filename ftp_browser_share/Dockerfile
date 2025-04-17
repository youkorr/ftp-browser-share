FROM python:3.9-slim

# Install system dependencies with a more recent Node.js version
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lftp \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-cors pyftpdlib

# Create app directory
WORKDIR /app

# Copy all files first so package.json and build scripts are available
COPY . .

# Install frontend dependencies with detailed error logging
RUN npm install

# Debug the build environment
RUN node --version && npm --version

# Build frontend with more detailed output
RUN npm run build || (echo "Build failed - showing package.json contents:" && cat package.json && exit 1)

# Make scripts executable
RUN chmod +x /app/run.sh
RUN chmod +x /app/api/start_api.sh

EXPOSE 3000

CMD [ "/app/run.sh" ]
