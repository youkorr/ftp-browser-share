from flask import Flask, jsonify, request
import os
import logging
from datetime import datetime, timedelta
from .ftp_client import FTPClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ftp_client = FTPClient()

@app.route('/api/files', methods=['GET'])
def list_files():
    try:
        if not ftp_client.connect(os.getenv('HOST'), int(os.getenv('PORT'))):
            return jsonify({"error": "FTP connection failed"}), 500
            
        if not ftp_client.login(os.getenv('USERNAME'), os.getenv('PASSWORD'))):
            return jsonify({"error": "FTP login failed"}), 500

        files = ftp_client.list_files(os.getenv('ROOT_PATH'))
        return jsonify({
            'files': [f.split()[-1] for f in files if not f.startswith('d')]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        ftp_client.disconnect()

@app.route('/api/share', methods=['POST'])
def share_file():
    try:
        data = request.json
        filename = data['filename']
        remote_path = f"{os.getenv('ROOT_PATH')}/{filename}" if os.getenv('ROOT_PATH') else filename
        local_path = f"/share/ftp_shared/{filename}"

        if not ftp_client.connect(os.getenv('HOST'), int(os.getenv('PORT'))):
            return jsonify({"error": "FTP connection failed"}), 500
            
        if not ftp_client.login(os.getenv('USERNAME'), os.getenv('PASSWORD'))):
            return jsonify({"error": "FTP login failed"}), 500

        if not ftp_client.download_file(remote_path, local_path):
            return jsonify({"error": "File download failed"}), 500

        return jsonify({
            'status': 'success',
            'url': f"/local/ftp_shared/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        ftp_client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
