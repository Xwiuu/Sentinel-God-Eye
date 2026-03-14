<template>
  <div class="w-full h-full relative bg-black flex items-center justify-center overflow-hidden">
    <div class="absolute top-6 left-6 z-20 font-mono text-[10px] text-matrix-green p-4 border-l-2 border-matrix-green/50 bg-black/80 backdrop-blur-md">
      <div class="flex items-center gap-2 mb-2">
        <div class="w-2 h-2 bg-matrix-green animate-ping"></div>
        <span class="font-black tracking-[0.3em] uppercase">Global_Sentinel_Radar</span>
      </div>
      <div class="space-y-1 opacity-80">
        <p>ORBIT_ALT: <span class="text-white">35,786 KM</span></p>
        <p>SENSORS: <span class="text-white">ACTIVE</span></p>
        <p>MODE: <span class="text-matrix-green font-bold">REAL_TIME_INTERCEPT</span></p>
        <p>LATENCY: <span class="text-white">12ms</span></p>
      </div>
    </div>

    <div class="absolute top-6 right-6 z-20 w-48 font-mono text-[9px] text-matrix-green p-3 border border-matrix-green/30 bg-black/90 shadow-[0_0_20px_rgba(0,255,65,0.1)]">
      <div class="border-b border-matrix-green/30 mb-2 pb-1 font-black italic uppercase italic">High_Threat_Sources</div>
      <div id="blacklist-feed" class="space-y-2 max-h-[200px] overflow-hidden">
        <div class="flex justify-between border-b border-matrix-green/10 pb-1">
          <span>182.XXX.XX</span> <span class="text-emergency-red">99%</span>
        </div>
      </div>
    </div>

    <div ref="globeContainer" class="w-full h-full cursor-grab active:cursor-grabbing"></div>

    <div class="absolute inset-0 pointer-events-none opacity-[0.05] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_2px,3px_100%]"></div>
  </div>
</template>

<script setup>
import { onMounted, ref, onUnmounted } from 'vue';
import Globe from 'globe.gl';

const globeContainer = ref(null);
let myGlobe = null;
let socket = null;

// COORDENADAS DO SEU SERVIDOR (Destino dos ataques)
const SERVER_LOC = { lat: -23.5505, lng: -46.6333 }; // São Paulo

const initGlobe = () => {
  myGlobe = Globe()(globeContainer.value)
    // 1. FUNDO E ATMOSFERA
    .backgroundColor('#000000')
    .showAtmosphere(true)
    .atmosphereColor('#00ff41')
    .atmosphereAltitude(0.2)
    
    // 2. TEXTURAS REAIS (Aqui está o segredo!)
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg') // Terra à noite com luzes
    .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png') // Relevo real dos continentes
    
    // 3. ARCOS DE ATAQUE (Mísseis de luz)
    .arcColor('color')
    .arcDashLength(0.6)
    .arcDashGap(2)
    .arcDashAnimateTime(1500)
    .arcStroke(0.6)
    .arcCurveResolution(64)
    
    // 4. IMPACTOS (Anéis de choque)
    .ringColor(d => d.color)
    .ringMaxRadius(8)
    .ringPropagationSpeed(2)
    .ringRepeatPeriod(1000)
    
    // 5. RÓTULOS (Infos do IP)
    .labelColor(() => '#ffffff')
    .labelSize(0.5)
    .labelDotRadius(0.2);

  // AUTO-ROTATE (Para dar o feeling de satélite)
  myGlobe.controls().autoRotate = true;
  myGlobe.controls().autoRotateSpeed = 0.5;
  myGlobe.pointOfView({ lat: 20, lng: 0, altitude: 2.2 });

  // Customização de Material via Three.js
  const globeMaterial = myGlobe.globeMaterial();
  globeMaterial.color.set('#050505'); 
  globeMaterial.emissive.set('#00ff41');
  globeMaterial.emissiveIntensity = 0.05; // Leve brilho nas bordas
};

const connectToBackend = () => {
  // Conecta no seu Satelite.py (Ajuste o IP se necessário)
  socket = new WebSocket('ws://localhost:8000/ws/threat-stream');

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    // Transforma o evento em um arco no mapa
    const attackArc = {
      startLat: data.geo?.lat || 0,
      startLng: data.geo?.lon || 0,
      endLat: SERVER_LOC.lat,
      endLng: SERVER_LOC.lng,
      color: data.threat_score > 70 ? '#ff0000' : '#00ff41',
      label: `[${data.ip}] - ${data.type || 'REQUEST'}`
    };

    // Adiciona o arco e o anel de impacto se for suspeito
    const currentArcs = myGlobe.arcsData();
    myGlobe.arcsData([...currentArcs, attackArc].slice(-40)); // Mantém os últimos 40 para não pesar

    if (data.threat_score > 40) {
      myGlobe.ringsData([attackArc]);
    }
  };

  socket.onclose = () => setTimeout(connectToBackend, 5000);
};

onMounted(() => {
  initGlobe();
  connectToBackend();
});

onUnmounted(() => {
  if (socket) socket.close();
});
</script>

<style scoped>
/* Estilo tático para o mapa */
canvas { outline: none; }
</style>