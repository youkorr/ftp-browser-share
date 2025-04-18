<template>
  <v-container>
    <v-card>
      <v-card-title>Configuration du serveur FTP</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="saveConfig">
          <v-text-field 
            v-model="config.ftp_server" 
            label="Adresse du serveur FTP" 
            required
          ></v-text-field>
          
          <v-text-field 
            v-model.number="config.ftp_port" 
            label="Port" 
            type="number"
          ></v-text-field>
          
          <v-text-field 
            v-model="config.ftp_username" 
            label="Nom d'utilisateur" 
            required
          ></v-text-field>
          
          <v-text-field 
            v-model="config.ftp_password" 
            label="Mot de passe" 
            type="password" 
            required
          ></v-text-field>
          
          <v-text-field 
            v-model="config.ftp_root_path" 
            label="Chemin racine"
          ></v-text-field>
          
          <v-text-field 
            v-model.number="config.share_duration" 
            label="Durée de partage (heures)" 
            type="number"
          ></v-text-field>
          
          <v-btn type="submit" color="primary">Sauvegarder</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      config: {
        ftp_server: '',
        ftp_port: 21,
        ftp_username: '',
        ftp_password: '',
        ftp_root_path: '',
        share_duration: 0
      }
    }
  },
  mounted() {
    this.loadConfig()
  },
  methods: {
    async loadConfig() {
      try {
        const response = await axios.get('/api/config')
        this.config = response.data
      } catch (error) {
        console.error('Erreur de chargement de la configuration', error)
      }
    },
    async saveConfig() {
      try {
        await axios.post('/api/config', this.config)
        alert('Configuration sauvegardée avec succès')
      } catch (error) {
        console.error('Erreur de sauvegarde de la configuration', error)
      }
    }
  }
}
</script>
