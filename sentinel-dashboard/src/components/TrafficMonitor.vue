<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const logs = ref([]);
const selectedLog = ref(null);
let socket = null;

const loadHistory = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/history');
    const data = await res.json();
    console.log("📜 Histórico recebido:", data);
    logs.value = data;
  } catch (e) {
    console.error("Erro ao carregar histórico");
  }
};

const connectToStream = () => {
  socket = new WebSocket('ws://localhost:8000/ws/threat-stream');
  
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("📥 Novo pacote via WS:", data);
    // Unshift adiciona no topo da lista
    logs.value.unshift(data);
    if (logs.value.length > 100) logs.value.pop();
  };

  socket.onclose = () => setTimeout(connectToStream, 3000);
};

onMounted(() => {
  loadHistory();
  connectToStream();
});

onUnmounted(() => { if (socket) socket.close(); });
</script>

<template>
  <div v-for="(log, index) in logs" :key="index" @click="selectedLog = log"
       class="grid grid-cols-12 gap-2 p-2 border-b border-matrix-green/10 hover:bg-white/5 cursor-pointer">
    <div class="col-span-2">{{ log.ip || 'N/A' }}</div>
    <div class="col-span-1">{{ log.method || '???' }}</div>
    <div class="col-span-5 truncate text-white/70">{{ log.path || '/' }}</div>
    <div class="col-span-2">{{ log.geo?.country || 'Local' }}</div>
    <div class="col-span-2 text-right font-bold" :class="log.threat_score > 40 ? 'text-red-500' : ''">
      {{ log.threat_score }}%
    </div>
  </div>
</template>