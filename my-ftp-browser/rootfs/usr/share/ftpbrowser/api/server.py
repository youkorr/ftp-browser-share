import os
import json
from flask import Flask, request, jsonify, send_from_directory
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
import shutil
from datetime import datetime, timedelta

app = Flask(__name__)

# Charger la configuration
def load_config():
    with open('/data/options.json', 'r') as f:
        return json.load(f)

# Connexion FTP (utilisation de pyftpdlib)
def connect_ftp():
    config = load_config()
    authorizer = DummyAuthorizer()
    authorizer.add_user(
        config['ftp_username'], 
        config['ftp_password'], 
        config['ftp_root_path'] or '/config', 
        perm='elradfmwMT'
    )
    
    handler = FTPHandler
    handler.authorizer = authorizer
    return handler, authorizer

# API - Liste des fichiers FTP
@app.route('/api/files', methods=['GET'])
def list_files():
    try:
        config = load_config()
        root_path = config['ftp_root_path'] or '/config'
        files = os.listdir(root_path)
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Télécharger un fichier
@app.route('/api/download/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        config = load_config()
        root_path = config['ftp_root_path'] or '/config'
        local_path = os.path.join(root_path, filename)
        
        return send_from_directory(root_path, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Partager un fichier
@app.route('/api/share', methods=['POST'])
def share_file():
    config = load_config()
    filename = request.json.get('filename')
    duration = config.get('share_duration', 0)
    
    try:
        root_path = config['ftp_root_path'] or '/config'
        source_path = os.path.join(root_path, filename)
        share_dir = "/config/www/partage/shared"
        share_path = os.path.join(share_dir, filename)
        
        os.makedirs(share_dir, exist_ok=True)
        shutil.copy(source_path, share_path)
        
        if duration > 0:
            expiry_time = datetime.now() + timedelta(hours=duration)
            with open(f"{share_path}.expiry", 'w') as f:
                f.write(str(expiry_time))
        
        return jsonify({
            "status": "success", 
            "shared_url": f"/local/partage/shared/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Configuration
@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    if request.method == 'GET':
        try:
            with open('/data/options.json', 'r') as f:
                return jsonify(json.load(f))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    elif request.method == 'POST':
        try:
            config = request.json
            with open('/data/options.json', 'w') as f:
                json.dump(config, f)
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Nettoyage des fichiers expirés
def cleanup_shared_files():
    shared_dir = "/config/www/partage/shared"
    os.makedirs(shared_dir, exist_ok=True)
    
    for filename in os.listdir(shared_dir):
        if filename.endswith('.expiry'):
            with open(os.path.join(shared_dir, filename), 'r') as f:
                expiry_time = datetime.fromisoformat(f.read().strip())
                if datetime.now() > expiry_time:
                    base_filename = filename.replace('.expiry', '')
                    os.remove(os.path.join(shared_dir, base_filename))
                    os.remove(os.path.join(shared_dir, filename))

if __name__ == '__main__':
    cleanup_shared_files()
    app.run(host='0.0.0.0', port=8099)
