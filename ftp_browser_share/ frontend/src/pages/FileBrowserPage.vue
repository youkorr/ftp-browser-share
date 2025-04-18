<template>
  <v-container>
    <v-card>
      <v-card-title>Navigateur de fichiers FTP</v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item 
            v-for="file in files" 
            :key="file"
          >
            {{ file }}
            <v-btn @click="downloadFile(file)">Télécharger</v-btn>
            <v-btn @click="shareFile(file)">Partager</v-btn>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      files: []
    }
  },
  mounted() {
    this.loadFiles()
  },
  methods: {
    async loadFiles() {
      try {
        const response = await axios.get('/api/files')
        this.files = response.data
      } catch (error) {
        console.error('Erreur de chargement des fichiers', error)
      }
    },
    async downloadFile(filename) {
      try {
        window.location.href = `/api/download/${filename}`
      } catch (error) {
        console.error('Erreur de téléchargement', error)
      }
    },
    async shareFile(filename) {
      try {
        const response = await axios.post('/api/share', { filename })
        alert(`Fichier partagé : ${response.data.shared_url}`)
      } catch (error) {
        console.error('Erreur de partage', error)
      }
    }
  }
}
</script>
