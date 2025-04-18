import { createRouter, createWebHistory } from 'vue-router'
import ConfigPage from './pages/ConfigPage.vue'
import FileBrowserPage from './pages/FileBrowserPage.vue'
import SharedFilesPage from './pages/SharedFilesPage.vue'

const routes = [
  { path: '/config', component: ConfigPage },
  { path: '/files', component: FileBrowserPage },
  { path: '/shared', component: SharedFilesPage },
  { path: '/', redirect: '/config' }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
