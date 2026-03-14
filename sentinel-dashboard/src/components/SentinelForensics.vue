<template>
  <div class="h-full w-full bg-black text-matrix-green font-mono p-4 overflow-y-auto custom-scrollbar flex flex-col gap-4">
    
    <div class="border-2 border-matrix-green/30 bg-matrix-green/5 p-6 shadow-[0_0_30px_rgba(0,255,65,0.05)]">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-3 h-3 bg-matrix-green animate-ping rounded-full"></div>
        <h1 class="text-xl font-black italic tracking-widest uppercase">Sentinel_Deep_Forensics_v4.2</h1>
      </div>
      <div class="flex gap-4">
        <input v-model="targetIp" @keyup.enter="runInvestigation" placeholder="ENTER_HOSTILE_IP_ADDRESS_FOR_DEEP_TRACE..." 
               class="flex-1 bg-black border-b border-matrix-green/50 p-3 text-white outline-none focus:border-white transition-all uppercase tracking-widest text-sm">
        <button @click="runInvestigation" :disabled="loading" 
                class="bg-matrix-green text-black font-black px-10 hover:bg-white transition-all disabled:opacity-30 flex items-center gap-2">
          <span v-if="loading" class="animate-spin">🌀</span>
          <span>{{ loading ? 'EXTRACTING...' : 'EXECUTE_DEEP_SCAN' }}</span>
        </button>
      </div>
    </div>

    <div v-if="report && !loading" class="grid grid-cols-12 gap-4 animate-in fade-in zoom-in duration-500">
      
      <div class="col-span-4 flex flex-col gap-4">
        <div class="border border-matrix-green/20 bg-os-gray p-5 text-center">
          <p class="text-[9px] opacity-40 mb-2 italic uppercase">Criminal_Confidence_Score</p>
          <h2 class="text-6xl font-black leading-none" :class="report.score > 50 ? 'text-emergency-red' : 'text-matrix-green'">
            {{ report.score }}<span class="text-xl">%</span>
          </h2>
          <p class="text-[8px] mt-2 text-white/50">DATABASE: ABUSE_IPDB_GLOBAL</p>
        </div>

        <div class="border border-matrix-green/20 bg-os-gray p-5 flex-1">
          <span class="text-[9px] font-black text-white bg-matrix-green px-2 py-0.5 uppercase">Hardware_Recon</span>
          <div class="mt-4 space-y-4">
            <div class="border-l-2 border-matrix-green/30 pl-3">
              <p class="text-[8px] opacity-50 uppercase">Operating_System</p>
              <p class="text-sm text-white font-bold">{{ report.shodan?.os || 'Undetected' }}</p>
            </div>
            <div class="border-l-2 border-matrix-green/30 pl-3">
              <p class="text-[8px] opacity-50 uppercase">Identified_Services</p>
              <div class="flex flex-wrap gap-1 mt-1">
                <span v-for="svc in report.shodan?.services" :key="svc" class="text-[9px] bg-matrix-green/10 border border-matrix-green/30 px-1 text-matrix-green italic">
                  {{ svc }}
                </span>
              </div>
            </div>
            <div class="border-l-2 border-matrix-green/30 pl-3">
              <p class="text-[8px] opacity-50 uppercase">Open_Ports</p>
              <div class="flex flex-wrap gap-2 mt-1">
                <span v-for="p in report.shodan?.ports" :key="p" class="text-xs font-black text-white bg-white/10 px-2">{{ p }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-span-8 flex flex-col gap-4">
        <div class="grid grid-cols-2 gap-4 h-full">
          
          <div class="border border-matrix-green/20 bg-black/40 p-5 flex flex-col justify-between">
            <span class="text-[9px] font-black text-white bg-blue-600 px-2 py-0.5 w-max uppercase italic">Identity_Match</span>
            <div class="space-y-3 my-4">
              <div class="flex justify-between border-b border-white/5 pb-1">
                <span class="text-[10px] opacity-50">HOSTNAME:</span>
                <span class="text-[10px] text-blue-400 font-bold">{{ report.shodan?.hostnames[0] || 'N/A' }}</span>
              </div>
              <div class="flex justify-between border-b border-white/5 pb-1">
                <span class="text-[10px] opacity-50">CITY/REGION:</span>
                <span class="text-[10px] text-white">{{ report.geo.city }}, {{ report.geo.regionName }}</span>
              </div>
              <div class="flex justify-between border-b border-white/5 pb-1">
                <span class="text-[10px] opacity-50">ISP_PROVIDER:</span>
                <span class="text-[10px] text-white">{{ report.geo.isp }}</span>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2 mt-auto">
              <button @click="openGoogleMaps" class="bg-blue-600/20 border border-blue-500 text-blue-400 text-[10px] py-2 font-black hover:bg-blue-600 hover:text-white transition-all uppercase">
                Satellite_View
              </button>
              <button @click="openStreetView" class="bg-orange-600/20 border border-orange-500 text-orange-400 text-[10px] py-2 font-black hover:bg-orange-600 hover:text-white transition-all uppercase">
                Street_Viewer
              </button>
            </div>
          </div>

          <div class="border border-matrix-green/20 bg-black relative overflow-hidden">
             <div class="absolute inset-0 opacity-40 pointer-events-none z-10 bg-[radial-gradient(circle,transparent_50%,black_100%)]"></div>
             <iframe 
                width="100%" height="100%" 
                frameborder="0" style="border:0; filter: grayscale(1) invert(1) contrast(1.5);" 
                :src="`https://maps.google.com/maps?q=${report.geo.lat},${report.geo.lon}&t=k&z=17&ie=UTF8&iwloc=&output=embed`" 
                allowfullscreen>
             </iframe>
          </div>

        </div>

        <div class="border border-red-900/50 bg-red-900/5 p-4 flex flex-col gap-2">
           <p class="text-[9px] text-emergency-red font-black flex items-center gap-2">
             <span class="w-2 h-2 bg-emergency-red rounded-full animate-pulse"></span> 
             DETECTION_ENGINE: EXPLOITABLE_VULNERABILITIES_FOUND
           </p>
           <div class="flex flex-wrap gap-2 max-h-24 overflow-y-auto custom-scrollbar">
             <div v-for="vuln in report.shodan?.vulns" :key="vuln" class="text-[10px] bg-red-600 text-white px-2 font-bold py-0.5">
               {{ vuln }}
             </div>
             <p v-if="!report.shodan?.vulns?.length" class="text-xs opacity-30 italic">No public CVEs found for this node.</p>
           </div>
        </div>
      </div>

    </div>

    <div v-if="!report && !loading" class="flex-1 border border-white/5 flex items-center justify-center">
       <p class="text-xs opacity-20 italic uppercase tracking-[0.5em]">Awaiting_Hostile_Signature_Input</p>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';

const targetIp = ref('');
const report = ref(null);
const loading = ref(false);

const runInvestigation = async () => {
  if (!targetIp.value) return;
  loading.value = true;
  report.value = null;
  try {
    const res = await fetch(`http://localhost:8000/api/forensics/investigate/${targetIp.value}`);
    const data = await res.json();
    report.value = data;
    console.log("🕵️ Forensics Report Generated:", data);
  } catch (e) {
    console.error("Forensics link failed.");
  } finally {
    loading.value = false;
  }
};

const openGoogleMaps = () => {
  if (report.value?.geo) {
    const { lat, lon } = report.value.geo;
    window.open(`https://www.google.com/maps/search/?api=1&query=${lat},${lon}`, '_blank');
  }
};

const openStreetView = () => {
  if (report.value?.geo) {
    const { lat, lon } = report.value.geo;
    window.open(`https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${lat},${lon}`, '_blank');
  }
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 3px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #00ff41; }
.bg-os-gray { background-color: rgba(20, 20, 20, 0.8); }
.text-emergency-red { color: #ff003c; }
</style>