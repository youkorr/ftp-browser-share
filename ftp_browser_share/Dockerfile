ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements
RUN apk add --no-cache \
    py3-pip \
    nodejs \
    npm \
    && pip3 install --no-cache-dir \
    flask \
    flask-cors \
    pyftpdlib \
    lftp

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
