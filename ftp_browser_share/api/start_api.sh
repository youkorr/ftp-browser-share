#!/bin/sh
export HOST=$(jq --raw-output '.host' /data/options.json)
export USERNAME=$(jq --raw-output '.username' /data/options.json)
export PASSWORD=$(jq --raw-output '.password' /data/options.json)
export PORT=$(jq --raw-output '.port' /data/options.json)
export ROOT_PATH=$(jq --raw-output '.root_path' /data/options.json)

python3 /app/api/api.py
