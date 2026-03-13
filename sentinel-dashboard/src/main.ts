import { createApp } from 'vue'
import './style.css' 
import App from './App.vue'
import router from './router' // <--- Deixe só assim!

createApp(App).use(router).mount('#app')