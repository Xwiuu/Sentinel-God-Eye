<template>
  <div
    class="h-full w-full bg-black text-matrix-green font-mono p-4 flex flex-col gap-4 overflow-hidden uppercase"
  >
    <div
      class="flex justify-between border border-matrix-green/30 bg-matrix-green/5 p-2 px-6 items-center"
    >
      <div class="flex gap-8">
        <div class="flex flex-col">
          <span class="text-[8px] opacity-50">Neural_Link_Status</span>
          <span class="text-xs font-black animate-pulse"
            >UPLINK_ESTABLISHED</span
          >
        </div>
        <div class="flex flex-col">
          <span class="text-[8px] opacity-50">Heuristic_Engine</span>
          <span class="text-xs font-black text-white">LEARNING_MODE</span>
        </div>
      </div>
      <div class="text-xl font-black italic tracking-tighter text-white">
        SENTINEL_INTEL_CORE_v4
      </div>
      <div class="flex gap-4 items-center">
        <span class="text-[10px] border border-matrix-green px-2 italic"
          >Node: 01_SP_BRAZIL</span
        >
        <div
          class="w-3 h-3 bg-matrix-green rounded-full shadow-[0_0_10px_#00ff41]"
        ></div>
      </div>
    </div>

    <div class="flex-1 grid grid-cols-12 gap-4 overflow-hidden">
      <div class="col-span-4 flex flex-col gap-4">
        <div
          class="flex-1 border border-matrix-green/20 p-4 bg-black/40 flex flex-col items-center justify-center relative overflow-hidden"
        >
          <div
            class="absolute inset-0 opacity-10 pointer-events-none bg-[radial-gradient(circle,rgba(0,255,65,1)_0%,transparent_70%)]"
          ></div>
          <span class="absolute top-2 left-2 text-[9px] font-bold underline"
            >Spatial_Threat_Radar</span
          >
          <svg viewBox="0 0 100 100" class="w-48 h-48 opacity-80">
            <circle
              cx="50"
              cy="50"
              r="48"
              fill="none"
              stroke="#00ff41"
              stroke-width="0.5"
              stroke-dasharray="2"
            />
            <circle
              cx="50"
              cy="50"
              r="30"
              fill="none"
              stroke="#00ff41"
              stroke-width="0.5"
              opacity="0.5"
            />
            <line
              x1="50"
              y1="50"
              x2="50"
              y2="2"
              stroke="#00ff41"
              stroke-width="1"
            >
              <animateTransform
                attributeName="transform"
                type="rotate"
                from="0 50 50"
                to="360 50 50"
                dur="4s"
                repeatCount="indefinite"
              />
            </line>
          </svg>
        </div>

        <div class="h-1/3 border border-matrix-green/20 p-4 bg-matrix-green/5">
          <span class="text-[9px] font-bold block mb-4 italic"
            >High_Priority_Targets</span
          >
          <div
            v-for="(item, i) in stats.top_ips"
            :key="i"
            class="flex justify-between text-[10px] mb-1.5 hover:bg-white/5 p-1 transition-all"
          >
            <span class="text-white">{{ item.ip }}</span>
            <span class="font-black text-matrix-green"
              >{{ item.total }}
              <span class="opacity-50 text-[8px]">HITS</span></span
            >
          </div>
        </div>
      </div>

      <div class="col-span-5 flex flex-col gap-4">
        <div
          class="flex-1 border border-matrix-green/20 bg-black/60 p-6 flex flex-col"
        >
          <div class="flex justify-between items-end mb-6">
            <div>
              <h2 class="text-lg font-black italic">Threat_Pulse_Monitor</h2>
              <p class="text-[8px] opacity-40">
                Real-time packet frequency across all ingestion nodes
              </p>
            </div>
            <span class="text-2xl font-black text-white italic"
              >0.024<span class="text-[10px] opacity-50 font-normal"
                >ms_lat</span
              ></span
            >
          </div>

          <div
            class="flex-1 flex items-end gap-1 px-2 border-b border-l border-matrix-green/20"
          >
            <div
              v-for="(v, i) in stats.pulse_data"
              :key="i"
              :style="{ height: v * 10 + 10 + '%' }"
              class="flex-1 bg-gradient-to-t from-matrix-green/40 to-white/80 animate-pulse"
            ></div>
          </div>

          <div class="grid grid-cols-3 gap-4 mt-6">
            <div class="text-center">
              <p class="text-[8px] opacity-50">Peak_Score</p>
              <p class="text-xl font-bold">100%</p>
            </div>
            <div class="text-center border-x border-matrix-green/10">
              <p class="text-[8px] opacity-50">Filter_Efficiency</p>
              <p class="text-xl font-bold text-white">99.2%</p>
            </div>
            <div class="text-center">
              <p class="text-[8px] opacity-50">AI_Precision</p>
              <p class="text-xl font-bold">88.4%</p>
            </div>
          </div>
        </div>
      </div>

      <div class="col-span-3 flex flex-col gap-4">
        <div
          class="h-1/2 border border-emergency-red/40 bg-emergency-red/10 p-6 flex flex-col items-center justify-center text-center"
        >
          <div
            class="w-full text-left mb-auto text-[8px] text-emergency-red font-bold"
          >
            Priority_Zero_Alert
          </div>
          <h3
            class="text-xs text-emergency-red tracking-widest mb-2 font-bold italic"
          >
            Threat_Level
          </h3>
          <h2
            class="text-6xl font-black text-emergency-red animate-pulse italic drop-shadow-[0_0_15px_rgba(255,0,0,0.5)]"
          >
            D-2
          </h2>
          <p
            class="mt-4 text-[9px] font-bold text-white bg-emergency-red px-2 py-1"
          >
            RETALIATION_ON
          </p>
        </div>

        <div
          class="flex-1 border border-matrix-green/20 bg-os-gray p-4 font-mono text-[9px] space-y-2 overflow-hidden"
        >
          <p class="text-white font-bold italic opacity-60 underline">
            Neural_Reasoning_Log:
          </p>
          <div class="space-y-1 opacity-80">
            <p>> Mapping 127.0.0.1 to known botnet signatures...</p>
            <p class="text-white">> [MATCH] SQL_INJECTION protocol detected.</p>
            <p>> Executing Tier 3 mitigation on ingestor-01.</p>
            <p>> SOC Orchestrator: Wireshark capture started.</p>
            <p>> Correlation engine linking ID: 0a93fea0...</p>
            <p class="text-white">
              > Predictive: 89% chance of multi-IP rotation.
            </p>
            <p class="animate-pulse">_</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const stats = ref({
  top_ips: [],
  pulse_data: [1, 5, 2, 8, 4, 3, 9, 2, 5, 1, 7, 4, 8, 3, 6],
});

const fetchStats = async () => {
  try {
    const res = await fetch("http://localhost:8000/api/intelligence/stats");
    const data = await res.json();
    stats.value = data;
  } catch (e) {
    console.error("Intelligence offline");
  }
};

onMounted(() => {
  fetchStats();
  setInterval(fetchStats, 5000); // Atualiza mais rápido (5s)
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #00ff41;
}
@keyframes scan {
  from {
    transform: translateY(-100%);
  }
  to {
    transform: translateY(100%);
  }
}
</style>
