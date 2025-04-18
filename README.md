# FTP Browser Share Addon

## Configuration

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `ftp_server` | string | Yes | Adresse IP du serveur FTP |
| `ftp_port` | integer | No | Port du serveur FTP (défaut: 21) |
| `ftp_username` | string | Yes | Nom d'utilisateur FTP |
| `ftp_password` | password | Yes | Mot de passe FTP |
| `ftp_root_path` | string | No | Chemin racine sur le serveur FTP |
| `share_duration` | integer | No | Durée de partage en heures (0 = permanent) |

## Installation

1. Ajouter le dépôt de l'addon dans Home Assistant
2. Installer l'addon
3. Configurer les paramètres FTP
4. Démarrer l'addon

## Utilisation

- Accéder à l'interface web sur le port 8099
- Naviguer, télécharger et partager des fichiers
