<template>
  <div class="h-full w-full bg-black text-matrix-green font-mono p-6 flex flex-col gap-6 overflow-hidden">
    
    <div class="grid grid-cols-4 gap-4">
      <div class="border border-matrix-green/20 bg-matrix-green/5 p-4 relative">
        <p class="text-[9px] uppercase opacity-50">Global_Defense_State</p>
        <p class="text-xl font-black text-white italic tracking-tighter">ACTIVE_ARMED</p>
        <div class="absolute top-2 right-2 w-2 h-2 bg-matrix-green animate-ping"></div>
      </div>
      <div class="border border-emergency-red/20 bg-emergency-red/5 p-4">
        <p class="text-[9px] uppercase opacity-50 text-emergency-red">Hostiles_Neutralized</p>
        <p class="text-xl font-black text-emergency-red italic tracking-tighter">{{ blacklist.length }}</p>
      </div>
      <div class="border border-matrix-green/20 bg-matrix-green/5 p-4 col-span-2 flex items-center justify-between">
        <div>
          <p class="text-[9px] uppercase opacity-50">Auto_Mitigation_Tier</p>
          <p class="text-lg font-bold text-white uppercase italic">Level_3: Total_Lockdown</p>
        </div>
        <div class="flex gap-2">
          <div v-for="i in 3" :key="i" class="w-6 h-1 bg-matrix-green"></div>
          <div class="w-6 h-1 bg-matrix-green/20"></div>
        </div>
      </div>
    </div>

    <div class="flex-1 border border-emergency-red/30 bg-black/40 flex flex-col overflow-hidden shadow-[0_0_50px_rgba(255,0,0,0.05)]">
      <div class="p-3 bg-emergency-red/10 border-b border-emergency-red/30 flex justify-between items-center">
        <span class="text-[10px] font-black uppercase text-emergency-red tracking-[0.2em] animate-pulse">
          ⚠️ Blacklist_Vault: High_Threat_Origins
        </span>
        <button @click="fetchBlacklist" class="text-[9px] bg-emergency-red text-white px-3 py-1 hover:bg-white hover:text-black transition-all">REFRESH_VAULT</button>
      </div>

      <div class="flex-1 overflow-y-auto custom-scrollbar">
        <table class="w-full text-left">
          <thead class="bg-black text-[9px] uppercase text-emergency-red border-b border-emergency-red/20">
            <tr>
              <th class="p-4">Neutralized_At</th>
              <th class="p-4">Hostile_IP</th>
              <th class="p-4">Violation_Protocol</th>
              <th class="p-4 text-right">Counter_Measure</th>
            </tr>
          </thead>
          <tbody class="text-[11px]">
            <tr v-for="ip in blacklist" :key="ip.ip" class="border-b border-white/5 hover:bg-emergency-red/5 transition-all group">
              <td class="p-4 opacity-50">{{ formatTime(ip.banned_at) }}</td>
              <td class="p-4 text-white font-bold tracking-widest">{{ ip.ip }}</td>
              <td class="p-4 text-emergency-red italic font-bold opacity-80 uppercase">{{ ip.reason }}</td>
              <td class="p-4 text-right">
                <button class="text-[9px] border border-matrix-green/30 text-matrix-green px-3 py-1 hover:bg-matrix-green hover:text-black uppercase">Authorize_Pardon</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const blacklist = ref([]);

const fetchBlacklist = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/blacklist');
    blacklist.value = await res.json();
  } catch (e) {
    console.error("Failed to load death row.");
  }
};

const formatTime = (ts) => {
  return ts.replace('T', ' ').slice(0, 19);
};

onMounted(fetchBlacklist);
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #ff0000; }
</style>