import os
import ftplib
import json
from flask import Flask, render_template, request, send_file, jsonify
import shutil
from datetime import datetime, timedelta

app = Flask(__name__)

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

# Liste des fichiers FTP
@app.route('/list_files')
def list_files():
    try:
        ftp = connect_ftp()
        files = ftp.nlst()
        ftp.quit()
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)})

# Télécharger un fichier
@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        ftp = connect_ftp()
        local_path = f"/config/www/partage/{filename}"
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        with open(local_path, 'wb') as local_file:
            ftp.retrbinary(f'RETR {filename}', local_file.write)
        
        ftp.quit()
        return send_file(local_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)})

# Partager un fichier
@app.route('/share', methods=['POST'])
def share_file():
    config = load_config()
    filename = request.form.get('filename')
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
        
        return jsonify({"status": "success", "shared_url": f"/local/partage/shared/{filename}"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Page principale
@app.route('/')
def index():
    return render_template('index.html')

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

