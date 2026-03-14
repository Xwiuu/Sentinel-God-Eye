<template>
  <div class="h-full w-full bg-black flex flex-col p-6 font-mono border-t border-matrix-green/20">
    
    <div class="flex justify-between items-center mb-6 border-b border-matrix-green/30 pb-4">
      <div>
        <h1 class="text-xl font-black text-matrix-green tracking-tighter uppercase italic">
          Database_Explorer_v1.0
        </h1>
        <p class="text-[9px] text-matrix-green/60 uppercase tracking-[0.3em]">
          Node: DC-SAO-PAULO-01 | Source: ClickHouse_Logs
        </p>
      </div>
      <div class="text-right">
        <div class="text-[10px] text-matrix-green/50 uppercase">Search_Filters_Active</div>
        <div class="text-white font-bold text-xs uppercase italic">Query_Mode: Deep_Scan</div>
      </div>
    </div>

    <div class="flex gap-4 mb-6 p-4 bg-matrix-green/5 border border-matrix-green/20">
      <div class="flex flex-col gap-1">
        <span class="text-[9px] text-matrix-green/50 uppercase font-bold ml-1">IP_Target</span>
        <input v-model="filters.ip" @keyup.enter="runSearch" placeholder="0.0.0.0" 
               class="bg-black border border-matrix-green/30 p-2 text-xs text-matrix-green outline-none focus:border-matrix-green w-64 transition-all" />
      </div>
      <button @click="runSearch" class="self-end bg-matrix-green text-black font-black text-xs px-8 py-2.5 hover:bg-white transition-all uppercase italic">
        Execute_Query
      </button>
    </div>

    <div class="flex-1 overflow-hidden border border-matrix-green/10 bg-black/40">
      <div class="overflow-y-auto h-full custom-scrollbar">
        <table class="w-full text-left border-collapse">
          <thead class="sticky top-0 bg-matrix-green/10 backdrop-blur-md text-[10px] uppercase text-matrix-green border-b border-matrix-green/30">
            <tr>
              <th class="p-4">Timestamp</th>
              <th class="p-4">Source_IP</th>
              <th class="p-4">Path_Target</th>
              <th class="p-4">Threat_Score</th>
              <th class="p-4 text-right">Details</th>
            </tr>
          </thead>
          <tbody class="text-[11px] text-matrix-green/80">
            <tr v-if="results.length === 0">
              <td colspan="5" class="p-10 text-center opacity-30 italic uppercase">
                [ No_Data_Found_In_Vault ]
              </td>
            </tr>
            <tr v-for="res in results" :key="res.timestamp" 
                class="border-b border-matrix-green/5 hover:bg-white/5 transition-colors group">
              <td class="p-4 opacity-50">{{ res.timestamp.replace('T', ' ').slice(0, 19) }}</td>
              <td class="p-4 font-bold text-white tracking-widest">{{ res.ip }}</td>
              <td class="p-4 truncate max-w-xs group-hover:text-matrix-green transition-colors">{{ res.path }}</td>
              <td class="p-4">
                <span :class="res.threat_score > 70 ? 'text-red-500 font-black' : 'text-matrix-green'" 
                      class="px-2 py-0.5 border border-current text-[10px]">
                  {{ res.threat_score }}%
                </span>
              </td>
              <td class="p-4 text-right">
                <button class="text-[9px] border border-matrix-green/40 px-3 py-1 hover:bg-matrix-green hover:text-black uppercase font-bold">Inspect</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<<script setup>
import { ref, onMounted } from 'vue';

const results = ref([]);
const filters = ref({ ip: '' });
const loading = ref(false);

const runSearch = async () => {
  loading.value = true;
  console.log("🔍 Iniciando busca no Vault...");
  
  try {
    // Monta a URL. Se o IP estiver vazio, ele traz tudo (conforme seu JSON mostrou)
    const url = `http://localhost:8000/api/explorer?ip=${filters.value.ip}`;
    
    const res = await fetch(url, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!res.ok) throw new Error(`Erro HTTP: ${res.status}`);

    const data = await res.json();
    
    // DEBUG NO CONSOLE DO NAVEGADOR
    console.log("📦 Dados brutos recebidos:", data);

    // Garante que é um array antes de atribuir
    results.value = Array.isArray(data) ? data : [];
    
    console.log("✅ Resultados processados:", results.value.length);
  } catch (e) {
    console.error("❌ Falha na Query do Explorer:", e);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  runSearch(); // Carrega automaticamente ao abrir
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 5px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0, 255, 65, 0.2); }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(0, 255, 65, 0.5); }
</style>