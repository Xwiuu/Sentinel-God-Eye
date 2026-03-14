import { createRouter, createWebHistory } from 'vue-router'

import SentinelMap from '../components/SentinelMap.vue'
import TrafficMonitor from '../components/TrafficMonitor.vue'
import SentinelExplorer from '../components/SentinelExplorer.vue'
import SentinelDefense from '../components/SentinelDefense.vue'
import SentinelIntelligence from '../components/SentinelIntelligence.vue'
import sentinelForensics from '../components/SentinelForensics.vue'
import SentinelSettings from '../components/SentinelSettings.vue'
import SentinelShield from '../components/SentinelShield.vue'
const TelaEmConstrucao = { template: '<div class="p-10 flex h-full items-center justify-center w-full"><h1 class="text-3xl text-primary animate-pulse">⚙️ Módulo em Construção...</h1></div>' }

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Dashboard', component: TelaEmConstrucao },
    { path: '/map', name: 'Mapa de Ataques', component: SentinelMap },
    { path: '/traffic', name: 'Monitor de Tráfego', component: TrafficMonitor },
    { path: '/explorer', name: 'Explorer de Requests', component: SentinelExplorer },
    { path: '/intelligence', name: 'Inteligência', component: SentinelIntelligence },
    { path: '/defense', name: 'Defesa e WAF', component: SentinelDefense },
    { path: '/integrations', name: 'Integrações', component: SentinelShield },
    { path: '/forensics', name: 'Forense', component: sentinelForensics },
    { path: '/system', name: 'Sistema', component: SentinelSettings}
  ]
})

export default router