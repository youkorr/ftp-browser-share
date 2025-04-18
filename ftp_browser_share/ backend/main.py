import os
import ftplib
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import shutil
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Charger la configuration
def load_config():
    with open('/data/options.json', 'r') as f:
        return json.load(f)

# Connexion FTP
def connect_ftp():
    config = load_config()
    ftp = ftplib.FTP()
    ftp.connect(config['ftp_server'], config['ftp_port'])
    ftp.login(user=config['ftp_username'], passwd=config['ftp_password'])
    if config['ftp_root_path']:
        ftp.cwd(config['ftp_root_path'])
    return ftp

# API - Liste des fichiers FTP
@app.route('/api/files', methods=['GET'])
def list_files():
    try:
        ftp = connect_ftp()
        files = ftp.nlst()
        ftp.quit()
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Télécharger un fichier
@app.route('/api/download/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        ftp = connect_ftp()
        local_path = f"/config/www/partage/{filename}"
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        with open(local_path, 'wb') as local_file:
            ftp.retrbinary(f'RETR {filename}', local_file.write)
        
        ftp.quit()
        return send_from_directory('/config/www/partage', filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Partager un fichier
@app.route('/api/share', methods=['POST'])
def share_file():
    config = load_config()
    filename = request.json.get('filename')
    duration = config.get('share_duration', 0)
    
    try:
        source_path = f"/config/www/partage/{filename}"
        share_path = f"/config/www/partage/shared/{filename}"
        
        os.makedirs(os.path.dirname(share_path), exist_ok=True)
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
    for filename in os.listdir(shared_dir):
        if filename.endswith('.expiry'):
            with open(os.path.join(shared_dir, filename), 'r') as f:
                expiry_time = datetime.fromisoformat(f.read().strip())
                if datetime.now() > expiry_time:
                    base_filename = filename.replace('.expiry', '')
                    os.remove(os.path.join(shared_dir, base_filename))
                    os.remove(os.path.join(shared_dir, filename))

if __name__ == '__main__':
    os.makedirs("/config/www/partage", exist_ok=True)
    os.makedirs("/config/www/partage/shared", exist_ok=True)
    cleanup_shared_files()
    app.run(host='0.0.0.0', port=8099)
