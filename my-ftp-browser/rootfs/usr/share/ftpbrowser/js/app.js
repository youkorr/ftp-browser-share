document.addEventListener('DOMContentLoaded', () => {
    const configForm = document.getElementById('config-form');
    const fileList = document.getElementById('file-list');

    // Charger la configuration
    async function loadConfig() {
        try {
            const response = await fetch('/api/config');
            const config = await response.json();
            Object.keys(config).forEach(key => {
                const input = configForm.elements[key];
                if (input) input.value = config[key];
            });
        } catch (error) {
            console.error('Erreur de chargement de la configuration', error);
        }
    }

    // Sauvegarder la configuration
    configForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(configForm);
        const config = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/api/config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(config)
            });
            const result = await response.json();
            alert('Configuration sauvegardée');
        } catch (error) {
            console.error('Erreur de sauvegarde', error);
        }
    });

    // Charger les fichiers
    async function loadFiles() {
        try {
            const response = await fetch('/api/files');
            const files = await response.json();
            fileList.innerHTML = files.map(file => `
                <li>
                    ${file}
                    <div class="actions">
                        <button onclick="downloadFile('${file}')">Télécharger</button>
                        <button onclick="shareFile('${file}')">Partager</button>
                    </div>
                </li>
            `).join('');
        } catch (error) {
            console.error('Erreur de chargement des fichiers', error);
        }
    }

    // Télécharger un fichier
    window.downloadFile = async (filename) => {
        window.location.href = `/api/download/${filename}`;
    }

    // Partager un fichier
    window.shareFile = async (filename) => {
        try {
            const response = await fetch('/api/share', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ filename })
            });
            const result = await response.json();
            alert(`Fichier partagé : ${result.shared_url}`);
        } catch (error) {
            console.error('Erreur de partage', error);
        }
    }

    // Initialisation
    loadConfig();
    loadFiles();
});
