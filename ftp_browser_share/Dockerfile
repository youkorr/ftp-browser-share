ARG BUILD_FROM
FROM $BUILD_FROM

# Update package index and install requirements separately for better debugging
RUN apk update

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    nodejs \
    npm

# Install Python dependencies separately
RUN pip3 install --no-cache-dir \
    flask \
    flask-cors \
    pyftpdlib 

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
