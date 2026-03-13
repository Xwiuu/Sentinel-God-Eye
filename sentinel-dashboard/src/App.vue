<script setup>
import { useRoute } from 'vue-router';

// A lista do seu menu lateral baseado no seu planejamento
const menuItems = [
  { name: 'Dashboard', path: '/', icon: '🏠' },
  { name: 'Mapa de Ataques', path: '/map', icon: '🌍' },
  { name: 'Monitor de Tráfego', path: '/traffic', icon: '📡' },
  { name: 'Explorer de Requests', path: '/explorer', icon: '🔎' },
  { name: 'Inteligência (AI)', path: '/intelligence', icon: '🧠' },
  { name: 'Defesa & WAF', path: '/defense', icon: '🛡️' },
  { name: 'Integrações', path: '/integrations', icon: '🔌' },
  { name: 'Analytics', path: '/analytics', icon: '📊' },
  { name: 'Forense', path: '/forensics', icon: '🎥' },
  { name: 'Sistema', path: '/system', icon: '⚙️' }
];

const route = useRoute();
</script>

<template>
  <div class="flex h-screen w-screen bg-dark">
    
    <aside class="w-64 bg-panel border-r border-slate-800 flex flex-col">
      
      <div class="h-16 flex items-center px-6 border-b border-slate-800">
        <span class="text-xl font-bold tracking-widest text-white drop-shadow-[0_0_8px_rgba(0,255,204,0.8)]">
          👁️ SENTINEL
        </span>
      </div>

      <nav class="flex-1 overflow-y-auto py-4">
        <ul class="space-y-1">
          <li v-for="item in menuItems" :key="item.name">
            <router-link 
              :to="item.path"
              class="flex items-center px-6 py-3 text-sm text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
              :class="{ 'bg-slate-800 border-r-4 border-primary text-primary font-bold': route.path === item.path }"
            >
              <span class="mr-3 text-lg">{{ item.icon }}</span>
              {{ item.name }}
            </router-link>
          </li>
        </ul>
      </nav>

      <div class="p-4 border-t border-slate-800">
        <div class="flex items-center">
          <div class="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold border border-primary/50">
            AD
          </div>
          <div class="ml-3">
            <p class="text-xs font-bold text-white">Admin Global</p>
            <p class="text-[10px] text-primary">Nível Militar Ativo</p>
          </div>
        </div>
      </div>
    </aside>

    <main class="flex-1 relative overflow-hidden">
      <router-view></router-view>
    </main>

  </div>
</template>