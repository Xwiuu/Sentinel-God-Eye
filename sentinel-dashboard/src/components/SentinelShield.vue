<template>
  <div class="h-full w-full bg-black text-matrix-green font-mono p-6 overflow-y-auto custom-scrollbar flex flex-col gap-8 uppercase">
    
    <div class="border-b border-matrix-green/30 pb-4 flex justify-between items-end">
      <div>
        <h1 class="text-3xl font-black italic tracking-tighter">SENTINEL_ARSENAL</h1>
        <p class="text-[10px] opacity-50 tracking-[0.4em]">Selecione o módulo de implantação do Arcanjo</p>
      </div>
      <div class="text-right">
        <span class="text-[9px] block opacity-40">Versão do Core</span>
        <span class="text-xs font-bold">v4.2.0-STABLE</span>
      </div>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
      <button v-for="cat in categories" :key="cat.id" 
              @click="activeCat = cat.id"
              :class="activeCat === cat.id ? 'bg-matrix-green text-black font-black' : 'border border-matrix-green/30 text-matrix-green opacity-60'"
              class="py-3 text-[10px] transition-all hover:bg-matrix-green/20 hover:opacity-100 flex flex-col items-center gap-1">
        <span class="text-[8px] opacity-50">{{ cat.prefix }}</span>
        {{ cat.label }}
      </button>
    </div>

    <div class="grid grid-cols-12 gap-8">
      
      <div class="col-span-12 lg:col-span-8 flex flex-col gap-4">
        <div class="border border-matrix-green/20 bg-matrix-green/5 p-6">
          <div class="flex justify-between items-start mb-6">
            <div>
              <h2 class="text-lg font-black italic underline">{{ currentContent.title }}</h2>
              <p class="text-[11px] opacity-70 normal-case mt-2 max-w-xl">{{ currentContent.description }}</p>
            </div>
            <div class="bg-matrix-green text-black px-3 py-1 text-[10px] font-black italic">
              {{ currentContent.type }}
            </div>
          </div>

          <div class="relative group mt-4">
            <div class="absolute -top-3 left-4 bg-black px-2 text-[9px] border border-matrix-green/30">SOURCE_CODE</div>
            <button @click="copyCode" class="absolute top-4 right-4 bg-matrix-green text-black px-3 py-1 text-[10px] font-black hover:bg-white transition-all z-10">
              COPY_SNIPPET
            </button>
            <pre class="bg-zinc-950 p-6 pt-10 border border-white/10 text-[12px] text-white overflow-x-auto custom-scrollbar leading-relaxed"><code>{{ currentContent.code }}</code></pre>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-4">
          <div v-for="req in currentContent.requirements" :key="req" 
               class="border border-white/5 p-3 flex flex-col gap-1 bg-white/2">
            <span class="text-[8px] opacity-40 italic">REQUISITO:</span>
            <span class="text-[10px] font-bold">{{ req }}</span>
          </div>
        </div>
      </div>

      <div class="col-span-12 lg:col-span-4 space-y-6">
        <div class="border border-red-600/20 bg-red-950/10 p-6 flex flex-col gap-4">
          <h3 class="text-xs font-black text-red-600">🛡️ ARCANJO_NETWORK_PULSE</h3>
          <div class="space-y-3">
            <div v-for="node in nodes" :key="node.name" class="flex justify-between items-center text-[10px]">
              <span class="opacity-60">{{ node.name }}</span>
              <div class="flex items-center gap-2">
                <span :class="node.status === 'ACTIVE' ? 'text-matrix-green' : 'text-red-600'">{{ node.status }}</span>
                <div class="w-1.5 h-1.5 rounded-full animate-pulse" :class="node.status === 'ACTIVE' ? 'bg-matrix-green' : 'bg-red-600'"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="border border-matrix-green/20 p-6 bg-matrix-green/2">
           <h3 class="text-xs font-black italic mb-4">SEGURANÇA_ATIVA</h3>
           <div class="text-3xl font-black mb-2 tracking-tighter">0.02ms</div>
           <p class="text-[9px] opacity-40 uppercase">Latência média de decisão (Arcanjo Core)</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const activeCat = ref('saas');

const categories = [
  { id: 'saas', label: 'SYNX_FLOW', prefix: 'SAAS_APP' },
  { id: 'lps', label: 'LANDING_PAGES', prefix: 'MARKETING' },
  { id: 'backend', label: 'API_SHIELD', prefix: 'BACKEND' },
  { id: 'infra', label: 'INFRA_EXEC', prefix: 'SYSTEM' }
];

const integrations = {
  saas: {
    title: 'INJETOR_DE_FRONTEND_ARCANJO',
    type: 'JS_DOM_LEVEL_1',
    description: 'Bloqueia o carregamento do seu SaaS se o IP do cliente estiver na Blacklist. Coloque no <head> para máxima prioridade.',
    code: `<script src="http://localhost:8000/shield/protector.js"><\/script>\n<script>\n  SentinelArcanjo.init();\n<\/script>`,
    requirements: ['DOM_ACCESS', 'HTTP_SATELLITE_LINK', 'ASYNC_MODE']
  },
  lps: {
    title: 'ARMADILHA_HONEYPOT_LP',
    type: 'BEHAVIORAL_TRAP',
    description: 'Cria links invisíveis e monitoriza cliques de bots. Se um bot tentar ler o conteúdo oculto, o IP é banido globalmente.',
    code: `<script src="http://localhost:8000/shield/gatekeeper.js"><\/script>`,
    requirements: ['HTML5_REQUIRED', 'NO_INDEX_FOLLOW', 'AUTO_BAN_ENABLED']
  },
  backend: {
    title: 'MIDDLEWARE_DE_ALTA_PERFORMANCE',
    type: 'GO_INTERNAL',
    description: 'Filtro de nível de servidor que consulta a memória RAM local sincronizada pelo Sentinel Brain para descartar pacotes.',
    code: `// Exemplo Middleware Go\nfunc ArcanjoGuard(next http.Handler) {\n  if Arcanjo.IsBlacklisted(r.RemoteAddr) {\n    return 403\n  }\n  next.ServeHTTP(w, r)\n}`,
    requirements: ['GO_COMPILER', 'REDIS_CACHE', 'SUB_MS_LATENCY']
  },
  infra: {
    title: 'EXECUTOR_DE_FIREWALL_OS',
    type: 'PYTHON_SYS_ADMIN',
    description: 'Script que roda no sistema operativo e cria regras de bloqueio permanentes no Windows Defender Firewall.',
    code: `python arcanjo_blocker.py --interface="Ethernet"`,
    requirements: ['ADMIN_PRIVILEGES', 'WIN_DEFENDER_ACTIVE', 'PYTHON_CORE']
  }
};

const currentContent = computed(() => integrations[activeCat.value]);
const nodes = [
  { name: 'SYNX_PROD', status: 'ACTIVE' },
  { name: 'LP_CONVERSAO', status: 'ACTIVE' },
  { name: 'BACKEND_MAIN', status: 'OFFLINE' },
  { name: 'LOCAL_INFRA', status: 'ACTIVE' }
];

const copyCode = () => {
  navigator.clipboard.writeText(currentContent.value.code);
  alert("ALERTA: Snippet copiado para o clipboard operativo.");
};
</script>