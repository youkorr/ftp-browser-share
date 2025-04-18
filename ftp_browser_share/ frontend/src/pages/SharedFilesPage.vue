<template>
  <v-container>
    <v-card>
      <v-card-title>Fichiers partagés</v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item 
            v-for="file in sharedFiles" 
            :key="file"
          >
            {{ file }}
            <v-btn @click="viewFile(file)">Voir</v-btn>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      sharedFiles: []
    }
  },
  mounted() {
    this.loadSharedFiles()
  },
  methods: {
    loadSharedFiles() {
      // Logique pour charger les fichiers partagés
      // Peut nécessiter une API supplémentaire côté backend
    },
    viewFile(filename) {
      window.open(`/local/partage/shared/${filename}`, '_blank')
    }
  }
}
</script>
