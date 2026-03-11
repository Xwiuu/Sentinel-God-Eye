<template>
  <div ref="chartRef" class="map-canvas"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import 'echarts-gl'

const props = defineProps(['lastEvent'])
const chartRef = ref(null)
let chart = null

onMounted(() => {
  chart = echarts.init(chartRef.value)
  
  const option = {
    backgroundColor: 'transparent',
    globe: {
      // Textura de alta resolução do planeta
      baseTexture: 'https://echarts.apache.org/examples/data-gl/asset/world.topo.bathy.200401.jpg',
      heightTexture: 'https://echarts.apache.org/examples/data-gl/asset/world.topo.bathy.200401.jpg',
      displacementScale: 0.04,
      shading: 'realistic',
      environment: 'none',
      realisticMaterial: { roughness: 0.9 },
      postEffect: { enable: true, bloom: { enable: true, bloomIntensity: 0.1 } },
      viewControl: { autoRotate: true, autoRotateSpeed: 3, distance: 220 }
    },
    series: [{
      type: 'scatter3D',
      coordinateSystem: 'globe',
      symbolSize: 12,
      itemStyle: { color: '#00ff41', opacity: 1, shadowBlur: 10, shadowColor: '#00ff41' },
      data: []
    }]
  }
  chart.setOption(option)
})

// Monitora novos eventos para "pinar" no mapa
watch(() => props.lastEvent, (newEvent) => {
  if (newEvent && newEvent.geo && chart) {
    chart.setOption({
      series: [{
        data: [[newEvent.geo.lon, newEvent.geo.lat, 0]]
      }]
    })
  }
})
</script>

<style scoped>
.map-canvas { width: 100%; height: 500px; filter: drop-shadow(0 0 20px rgba(0, 255, 65, 0.2)); }
</style>