#!/usr/bin/with-contenv bashio
# Démarrer Nginx
nginx

# Démarrer l'API Python
python3 /usr/share/ftpbrowser/api/server.py &

# Attendre que les processus se terminent
wait
