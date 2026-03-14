<template>
  <div
    class="h-full w-full bg-black text-matrix-green font-mono p-4 flex flex-col gap-4 overflow-hidden uppercase relative"
  >
    <div
      class="absolute inset-0 opacity-5 pointer-events-none bg-[linear-gradient(rgba(0,255,65,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,65,0.1)_1px,transparent_1px)] bg-[size:40px_40px]"
    ></div>

    <div
      class="z-10 flex justify-between items-center border border-matrix-green/30 bg-matrix-green/5 p-4 shadow-[0_0_20px_rgba(0,255,65,0.05)]"
    >
      <div>
        <h1 class="text-2xl font-black italic tracking-widest text-white">
          CORE_SYSTEM_DIRECTIVES
        </h1>
        <p class="text-[9px] opacity-40 tracking-[0.5em]">
          Sentinel_OS Kernel v4.2.0-Proxima
        </p>
      </div>
      <div class="flex gap-6 items-center">
        <div class="text-right">
          <p class="text-[8px] opacity-50">System_Uptime</p>
          <p class="text-xs font-bold text-white">14:02:33:09</p>
        </div>
        <div class="h-8 w-[1px] bg-matrix-green/30"></div>
        <div class="flex flex-col items-center">
          <div
            class="w-3 h-3 bg-matrix-green rounded-full shadow-[0_0_10px_#00ff41] animate-pulse"
          ></div>
          <span class="text-[8px] mt-1">SEC_LINK</span>
        </div>
      </div>
    </div>

    <div class="z-10 flex-1 grid grid-cols-12 gap-4 overflow-hidden">
      <div class="col-span-4 flex flex-col gap-4">
        <div class="border border-matrix-green/20 bg-black/60 p-4 space-y-4">
          <span
            class="text-[10px] font-black border-b border-matrix-green/30 block pb-1"
            >Hardware_Telemetria</span
          >
          <div v-for="(val, label) in health" :key="label" class="space-y-1">
            <div class="flex justify-between text-[9px]">
              <span>{{ label }}</span>
              <span class="text-white">{{ val }}%</span>
            </div>
            <div class="h-1 w-full bg-matrix-green/10">
              <div
                class="h-full bg-matrix-green shadow-[0_0_5px_#00ff41]"
                :style="{ width: val + '%' }"
              ></div>
            </div>
          </div>
        </div>

        <div
          class="flex-1 border border-matrix-green/20 bg-matrix-green/5 p-4 space-y-3 overflow-y-auto custom-scrollbar"
        >
          <span
            class="text-[10px] font-black border-b border-matrix-green/30 block pb-1 italic"
            >Active_Modules</span
          >
          <div
            v-for="(label, key) in switches"
            :key="key"
            @click="configs[key] = !configs[key]"
            :class="
              configs[key]
                ? 'border-matrix-green bg-matrix-green/10'
                : 'border-white/10 bg-transparent opacity-40'
            "
            class="p-3 border cursor-pointer transition-all flex justify-between items-center group"
          >
            <div class="flex flex-col">
              <span class="text-[10px] font-bold tracking-tighter">{{
                label
              }}</span>
              <span class="text-[8px] italic">{{
                configs[key] ? "Status: ONLINE" : "Status: STANDBY"
              }}</span>
            </div>
            <div
              :class="
                configs[key]
                  ? 'bg-matrix-green shadow-[0_0_10px_#00ff41]'
                  : 'bg-white/20'
              "
              class="w-2 h-2 rounded-full"
            ></div>
          </div>
        </div>
      </div>

      <div class="col-span-8 flex flex-col gap-4">
        <div
          class="flex-1 border border-matrix-green/20 bg-black/60 p-6 flex flex-col gap-8 relative overflow-hidden"
        >
          <div
            class="absolute top-0 right-0 p-2 opacity-5 text-[40px] font-black italic select-none"
          >
            TUNING
          </div>

          <h2
            class="text-sm font-black italic border-l-4 border-matrix-green pl-3"
          >
            Mitigation_Threshold_Calibration
          </h2>

          <div class="space-y-6 relative">
            <div class="flex justify-between items-end">
              <div>
                <p class="text-[10px] font-black text-white">
                  Tier_3: Lethal_Mitigation
                </p>
                <p class="text-[8px] opacity-40 normal-case">
                  Minimum score for automated PostgreSQL/Firewall drop
                </p>
              </div>
              <p class="text-4xl font-black text-white tracking-tighter">
                {{ configs.ban_threshold
                }}<span class="text-lg opacity-40">%</span>
              </p>
            </div>
            <div class="relative flex items-center group">
              <div class="absolute -top-4 left-0 text-[7px] opacity-30">
                50%_MIN
              </div>
              <div class="absolute -top-4 right-0 text-[7px] opacity-30">
                100%_MAX
              </div>
              <input
                type="range"
                v-model="configs.ban_threshold"
                min="50"
                max="100"
                class="sentinel-range"
              />
            </div>
          </div>

          <div class="space-y-6 relative">
            <div class="flex justify-between items-end">
              <div>
                <p class="text-[10px] font-black text-white">
                  Tier_2: Intercept_Challenge
                </p>
                <p class="text-[8px] opacity-40 normal-case">
                  Threshold for JavaScript bot-trapping mechanisms
                </p>
              </div>
              <p class="text-4xl font-black text-white tracking-tighter">
                {{ configs.challenge_threshold
                }}<span class="text-lg opacity-40">%</span>
              </p>
            </div>
            <input
              type="range"
              v-model="configs.challenge_threshold"
              min="10"
              max="50"
              class="sentinel-range"
            />
          </div>
        </div>

        <div
          class="border border-emergency-red/30 bg-emergency-red/5 p-4 flex justify-between items-center gap-6"
        >
          <div class="flex gap-4 items-center">
            <div
              class="w-10 h-10 border border-emergency-red flex items-center justify-center text-emergency-red font-black text-xl animate-pulse"
            >
              !
            </div>
            <div>
              <p class="text-[10px] font-black text-emergency-red">
                Emergency_Erase_Protocol
              </p>
              <p class="text-[8px] opacity-50 text-white normal-case">
                Warning: This action will purge the entire ClickHouse log vault
                and Blacklist DB.
              </p>
            </div>
          </div>
          <button
            class="bg-emergency-red text-black font-black px-6 py-3 text-[10px] hover:bg-white transition-all uppercase italic shadow-[0_0_15px_rgba(255,0,0,0.3)]"
          >
            Purge_All_Evidence
          </button>
        </div>

        <button
          @click="saveConfigs"
          :disabled="saving"
          class="bg-matrix-green text-black font-black py-4 text-sm tracking-[0.3em] italic hover:bg-white hover:shadow-[0_0_30px_#00ff41] transition-all disabled:opacity-30"
        >
          {{
            saving ? "> TRANSMITTING_CHANGES..." : "> APPLY_SYSTEM_DIRECTIVES"
          }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const health = ref({ CPU: 0, RAM: 0, GPU: 0, DISK: 0 });
const configs = ref({
  ban_threshold: 90,
  challenge_threshold: 40,
  auto_mitigation: true,
  debug_mode: false,
  soc_active: true,
});
const switches = {
  auto_mitigation: "Global_Firewall_Sync",
  debug_mode: "Kernel_Deep_Logs",
  soc_active: "Autonomous_OSINT_Scans",
};
const saving = ref(false);

const updateHealth = () => {
  health.value = {
    CPU: (Math.random() * 20 + 30).toFixed(1),
    RAM: (Math.random() * 10 + 60).toFixed(1),
    GPU: (Math.random() * 15 + 10).toFixed(1),
    DISK: 44.2,
  };
};

const saveConfigs = async () => {
  saving.value = true;
  try {
    await fetch("http://localhost:8000/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(configs.value),
    });
    setTimeout(() => {
      saving.value = false;
    }, 1000);
  } catch (e) {
    saving.value = false;
  }
};

onMounted(() => {
  setInterval(updateHealth, 2000);
  updateHealth();
});
</script>

<style scoped>
.sentinel-range {
  -webkit-appearance: none;
  width: 100%;
  height: 2px;
  background: rgba(0, 255, 65, 0.1);
  outline: none;
  border: 1px solid rgba(0, 255, 65, 0.2);
}
.sentinel-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 15px;
  height: 15px;
  background: #fff;
  border: 2px solid #00ff41;
  box-shadow: 0 0 10px #00ff41;
  cursor: pointer;
}
.custom-scrollbar::-webkit-scrollbar {
  width: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #00ff41;
}
</style>
