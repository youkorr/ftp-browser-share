FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    lftp \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-cors pyftpdlib

# Create app directory
WORKDIR /app

# Install frontend dependencies
COPY package*.json ./
RUN npm install

# Copy all files
COPY . .

# Build frontend
RUN npm run build

# Make scripts executable
RUN chmod +x /app/run.sh
RUN chmod +x /app/api/start_api.sh

EXPOSE 3000

CMD [ "/app/run.sh" ]
