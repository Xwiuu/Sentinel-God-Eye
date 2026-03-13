import { createRouter, createWebHistory } from 'vue-router'

const TelaEmConstrucao = { template: '<div class="p-10 flex h-full items-center justify-center w-full"><h1 class="text-3xl text-primary animate-pulse">⚙️ Módulo em Construção...</h1></div>' }

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Dashboard', component: TelaEmConstrucao },
    { path: '/map', name: 'Mapa de Ataques', component: TelaEmConstrucao },
    { path: '/traffic', name: 'Monitor de Tráfego', component: TelaEmConstrucao },
    { path: '/explorer', name: 'Explorer de Requests', component: TelaEmConstrucao },
    { path: '/intelligence', name: 'Inteligência', component: TelaEmConstrucao },
    { path: '/defense', name: 'Defesa e WAF', component: TelaEmConstrucao },
    { path: '/integrations', name: 'Integrações', component: TelaEmConstrucao },
    { path: '/analytics', name: 'Analytics', component: TelaEmConstrucao },
    { path: '/forensics', name: 'Forense', component: TelaEmConstrucao },
    { path: '/system', name: 'Sistema', component: TelaEmConstrucao },
  ]
})

export default router