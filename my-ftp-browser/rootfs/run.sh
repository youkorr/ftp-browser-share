#!/usr/bin/with-contenv bashio
# Démarrer les services via S6
/etc/services.d/nginx/run &
/etc/services.d/ftp-server/run &

# Attendre la fin des processus
wait
