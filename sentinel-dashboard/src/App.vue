<template>
  <div class="min-h-screen bg-black text-slate-100 p-6 font-mono scanline">
    <header class="flex justify-between items-center mb-8 border-b border-red-900 pb-4">
      <h1 class="text-3xl font-black text-red-600 tracking-tighter">SENTINEL: GOD EYE v2.0</h1>
      <div class="text-right text-xs">
        <span class="text-emerald-500 animate-pulse">● RADAR ATIVO</span> | TOTAL VISIBILITY MODE
      </div>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      
      <section class="border border-slate-800 bg-slate-900/30 rounded-lg">
        <h2 class="p-4 bg-slate-800 text-slate-300 text-sm font-bold uppercase tracking-widest">
          📡 Live Traffic Feed (Global Entry)
        </h2>
        <div class="overflow-y-auto h-[600px] p-2 space-y-2">
          <div v-for="log in liveTraffic" :key="log.id" 
               class="text-[10px] p-2 border-l-2 border-blue-500 bg-blue-500/5 flex justify-between">
            <span>
              <b class="text-blue-400">[{{ log.method }}]</b> {{ log.ip }} 
              <span class="text-slate-500">→</span> <span class="text-slate-300">{{ log.path }}</span>
            </span>
            <span class="text-slate-600 italic">{{ formatTime(log.timestamp) }}</span>
          </div>
        </div>
      </section>

      <section class="border border-red-900 bg-red-950/10 rounded-lg">
        <h2 class="p-4 bg-red-950/40 text-red-500 text-sm font-bold uppercase tracking-widest">
          💀 Neutralized Threats (Blacklist)
        </h2>
        <div class="overflow-y-auto h-[600px] p-4">
          <div v-for="threat in threats" :key="threat.ip" 
               class="mb-4 p-3 border border-red-900/50 bg-black rounded shadow-lg shadow-red-900/10">
            <div class="flex justify-between font-bold">
              <span class="text-red-400">{{ threat.ip }}</span>
              <span class="text-[10px] text-red-700 uppercase">Status: Terminated</span>
            </div>
            <p class="text-[11px] text-slate-400 mt-1 uppercase">{{ threat.reason }}</p>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const threats = ref([]);
const liveTraffic = ref([]);

const updateData = async () => {
  try {
    // Puxa o Cemitério
    const resBans = await fetch('http://localhost:8081/api/audit/blacklist');
    threats.value = await resBans.json();

    // Puxa o Fluxo Total
    const resLive = await fetch('http://localhost:8081/api/audit/live-traffic');
    liveTraffic.value = await resLive.json();
  } catch (e) { console.error("OFFLINE"); }
};

const formatTime = (ts) => new Date(ts).toLocaleTimeString();

onMounted(() => {
  updateData();
  setInterval(updateData, 2000); // Atualiza a cada 2 segundos pra ser "God Eye" mesmo
});
</script>