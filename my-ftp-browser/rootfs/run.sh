#!/bin/bash
# Script de démarrage principal

# Vérifier et corriger les permissions
chmod 755 /run.sh
chmod 755 /etc/services.d/ftp_browser/run
chmod 755 /etc/cont-init.d/*

# Démarrer les services via S6
echo "Démarrage des services FTP Browser Share..."
exec /init

