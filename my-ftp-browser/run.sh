#!/usr/bin/with-contenv bashio
# Script de démarrage principal

# Démarrer Nginx
nginx &

# Démarrer l'API Python
python3 /usr/share/ftpbrowser/api/server.py &

# Attendre la fin des processus
wait
