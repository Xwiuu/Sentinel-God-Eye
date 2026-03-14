<template>
  <div
    class="h-screen w-screen bg-[#020202] text-[#00ff41] font-mono overflow-hidden p-1 flex flex-col relative select-none"
  >
    <div
      class="absolute inset-0 pointer-events-none z-50 opacity-[0.08] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_2px,3px_100%]"
    ></div>

    <div
      class="flex-1 border-[3px] border-double border-[#00ff41]/30 flex flex-col relative"
    >
      <header
        class="h-16 border-b-[3px] border-double border-[#00ff41]/30 bg-[#0a0a0a] flex items-center justify-between px-4"
      >
        <div class="flex items-center gap-4">
          <div
            class="bg-[#00ff41] text-black px-3 py-1 font-black text-2xl tracking-tighter italic"
          >
            SENTINEL_GOD_EYE
          </div>
          <div class="hidden md:block text-[10px] leading-none opacity-60">
            STRATEGIC DEFENSE INTERFACE<br />
            VERSION: 4.0.0-PROXIMA<br />
            NODE: DC-SAO-PAULO-01
          </div>
        </div>

        <div class="flex gap-8 items-center font-bold text-xs uppercase">
          <div class="flex flex-col items-end">
            <span class="text-[9px] opacity-40">Packet_Loss</span>
            <span class="text-white">0.000%</span>
          </div>
          <div class="flex flex-col items-end">
            <span class="text-[9px] opacity-40">Threat_Level</span>
            <span class="text-red-600 animate-pulse">DEFCON 2</span>
          </div>
          <div class="border-2 border-[#00ff41] p-2 bg-[#00ff41]/10">
            {{ currentTime }}
          </div>
        </div>
      </header>

      <div class="flex flex-1 overflow-hidden relative">
        <aside
          class="w-16 border-r-[3px] border-double border-[#00ff41]/30 flex flex-col bg-[#050505] z-20"
        >
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="h-20 border-b border-[#00ff41]/20 flex flex-col items-center justify-center hover:bg-[#00ff41]/10 transition-all relative group"
            active-class="bg-[#00ff41]/20 text-white"
          >
            <div
              class="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-[#00ff41] opacity-0 group-hover:opacity-100"
            ></div>
            <span
              class="text-[10px] font-bold opacity-40 group-hover:opacity-100"
              >{{ item.short }}</span
            >
            <span class="text-xl mt-1">{{ item.icon }}</span>
          </router-link>
        </aside>

        <main
          class="flex-1 relative overflow-hidden bg-[url('https://www.transparenttextures.com/patterns/asfalt-dark.png')]"
        >
          <div
            class="absolute inset-0 opacity-10 pointer-events-none"
            style="
              background-image: radial-gradient(#00ff41 1px, transparent 1px);
              background-size: 30px 30px;
            "
          ></div>

          <div
            class="absolute top-4 right-4 w-48 border border-[#00ff41]/40 bg-black/80 p-2 text-[9px] z-10 font-bold"
          >
            <div class="border-b border-[#00ff41]/20 mb-1">
              LOCAL_RADAR_SCAN
            </div>
            <div class="flex justify-between">
              <span>X-POS:</span> <span class="text-white">44.092</span>
            </div>
            <div class="flex justify-between">
              <span>Y-POS:</span> <span class="text-white">12.881</span>
            </div>
            <div class="mt-2 text-yellow-500 underline uppercase">
              Targeting_Active
            </div>
          </div>

          <div class="absolute inset-0 p-4">
            <router-view />
          </div>

          <footer
            class="absolute bottom-0 left-0 right-0 h-40 bg-black/90 border-t-[3px] border-double border-[#00ff41]/30 p-3 font-mono text-[10px] z-30"
          >
            <div
              class="flex justify-between items-center mb-2 border-b border-[#00ff41]/20 pb-1"
            >
              <span class="font-black"
                >CORE_INTERCEPTOR_STREAM [SENSORS: 42]</span
              >
              <span class="animate-pulse">● RECORDING_PCAP</span>
            </div>
            <div
              class="overflow-y-auto h-28 space-y-1 scrollbar-hide text-[#00ff41]/80"
            >
              <p v-for="n in 10" :key="n">
                <span class="text-white">[{{ new Date().toISOString() }}]</span>
                <span class="text-red-500 font-bold ml-2">ALERT:</span>
                INBOUND_TCP_FLOOD from
                <span class="underline">192.168.{{ n }}.254</span> targeting
                PORT 80 [BLOCK_ACTION_EXECUTED]
              </p>
            </div>
          </footer>
        </main>
      </div>

      <div
        class="absolute bottom-4 right-4 w-12 h-12 border-b-2 border-r-2 border-[#00ff41]/40 pointer-events-none"
      ></div>
      <div
        class="absolute top-20 right-4 w-12 h-12 border-t-2 border-r-2 border-[#00ff41]/40 pointer-events-none text-[8px] flex items-start justify-end pr-1 pt-1 opacity-20 uppercase font-black"
      >
        Secure_Link
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const currentTime = ref("");
const menuItems = [
  { short: "DSH", icon: "📡", path: "/" },
  { short: "MAP", icon: "🌍", path: "/map" },
  { short: "TRF", icon: "📊", path: "/traffic" },
  { short: "EXP", icon: "🔎", path: "/explorer" },
  { short: "DEF", icon: "🛡️", path: "/defense" },
  { short: "INT", icon: "🧠", path: "/intelligence" },
  { short: "FOR", icon: "🔍", path: "/forensics" }, // O novo monstro
  { short: "ITG", icon: "🔌", path: "/integrations" },
  { short: "SYS", icon: "⚙️", path: "/system" },
];

onMounted(() => {
  setInterval(() => {
    currentTime.value =
      new Date().toLocaleTimeString("pt-BR", { hour12: false }) +
      ":" +
      new Date().getMilliseconds();
  }, 50);
});
</script>

<style>
/* Reset de scrollbar para manter o look de terminal */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* Animação de Flicker de monitor velho */
@keyframes flicker {
  0% {
    opacity: 0.98;
  }
  5% {
    opacity: 0.95;
  }
  10% {
    opacity: 0.99;
  }
  100% {
    opacity: 1;
  }
}
body {
  animation: flicker 0.15s infinite;
}

/* Tipografia de radar */
.font-mono {
  font-family: "JetBrains Mono", "Courier New", monospace;
  letter-spacing: -0.5px;
}
</style>
