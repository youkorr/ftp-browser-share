<template>
  <v-app>
    <v-navigation-drawer permanent>
      <v-list>
        <v-list-item 
          v-for="item in menuItems" 
          :key="item.title"
          :to="item.path"
        >
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      menuItems: [
        { title: 'Configuration', path: '/config' },
        { title: 'Navigateur de fichiers', path: '/files' },
        { title: 'Fichiers partagés', path: '/shared' }
      ]
    }
  }
}
</script>
