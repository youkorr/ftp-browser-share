ARG BUILD_FROM
FROM $BUILD_FROM

# Update package index and install requirements separately for better debugging
RUN apk update

# Install system dependencies with necessary build tools
RUN apk add --no-cache \
    python3 \
    py3-pip \
    nodejs \
    npm \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    make

# Upgrade pip first
RUN pip3 install --upgrade pip setuptools wheel

# Install Python dependencies separately
RUN pip3 install --no-cache-dir flask
RUN pip3 install --no-cache-dir flask-cors
RUN pip3 install --no-cache-dir pyftpdlib

# Install lftp separately
RUN apk add --no-cache lftp

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
