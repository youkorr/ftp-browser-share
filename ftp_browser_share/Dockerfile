FROM python:3.9-slim

# Install Node.js 18.x
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

# Copy all files
COPY . .

# Debug information
RUN echo "Node version:" && node --version
RUN echo "NPM version:" && npm --version
RUN echo "Package.json content:" && cat package.json
RUN echo "Directory structure:" && ls -la

# Install packages with detailed logs
RUN npm install --verbose

# Try to run the build with debugging
RUN npm run build --verbose || (echo "BUILD FAILED - Debug info:" && \
    npm list && \
    echo "LOGS:" && \
    cat npm-debug.log* 2>/dev/null || echo "No npm debug log found" && \
    exit 1)

# Make scripts executable
RUN chmod +x /app/run.sh
RUN chmod +x /app/api/start_api.sh

EXPOSE 3000

CMD [ "/app/run.sh" ]
