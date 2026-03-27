import { createApp } from 'vue'
import App from './App.vue'
import Varlet from '@varlet/ui'
import '@varlet/ui/es/style'
import '@varlet/touch-emulator'

const app = createApp(App)
app.use(Varlet)
app.mount('#app')
