<template>
  <div class="layout" :class="{ 'dark': isDark }">
      <side-menu 
        v-if="!isMobile" 
        :active="activeMenu" 
        @update:active="handleMenuChange"
        class="side-menu"
      />
      
      <main class="main-content" :class="{ 'has-bottom-nav': isMobile }">
        <div class="content-wrapper">
          <component :is="currentComponent" />
        </div>
      </main>
      
      <bottom-nav 
        v-if="isMobile" 
        :active="activeMenu"
        @update:active="handleMenuChange"
      />
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, provide, readonly, defineAsyncComponent } from 'vue'
import SideMenu from './SideMenu.vue'
import BottomNav from './BottomNav.vue'
import { componentMap } from '../config/menu.js'
import { isDark } from '../config/theme.js'
import { VCONSOLE_ENABLED_KEY, VCONSOLE_CODE_KEY } from '../config/storage-keys.js'

const isMobile = ref(window.innerWidth < 768)
const activeMenu = ref('nodes')

// 提供主题状态给子组件
provide('isDark', isDark)

// 提供当前菜单状态给 Software 组件
provide('activeMenu', readonly(activeMenu))

const currentComponent = computed(() => {
  return defineAsyncComponent(componentMap[activeMenu.value])
})

const handleMenuChange = (key) => {
  activeMenu.value = key
}

const handleResize = () => {
  isMobile.value = window.innerWidth < 768
}

// 从 localStorage 加载 VConsole
const loadVConsole = () => {
  const vconsoleEnabled = localStorage.getItem(VCONSOLE_ENABLED_KEY)
  if (vconsoleEnabled !== 'true') return
  
  const storedCode = localStorage.getItem(VCONSOLE_CODE_KEY)
  if (!storedCode) return
  
  try {
    const script = document.createElement('script')
    script.textContent = storedCode
    document.body.appendChild(script)
    
    if (window.VConsole) {
      window.vConsole = new window.VConsole()
      console.log('VConsole 已从本地缓存加载')
    }
  } catch (error) {
    console.error('加载 VConsole 失败:', error)
    localStorage.removeItem(VCONSOLE_CODE_KEY)
    localStorage.setItem(VCONSOLE_ENABLED_KEY, 'false')
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  
  // 加载 VConsole（如果之前开启过）
  loadVConsole()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
  background: var(--color-body);
}

.side-menu {
  width: 260px;
  flex-shrink: 0;
  border-right: 1px solid var(--color-outline);
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  z-index: 100;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  margin-left: 260px;
}

.main-content.has-bottom-nav {
  padding-bottom: 64px;
}

.content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

@media (max-width: 768px) {
  .layout {
    flex-direction: column;
  }
  
  .side-menu {
    position: relative;
    width: 100%;
    height: auto;
  }
  
  .main-content {
    width: 100%;
    margin-left: 0;
  }
  
  .content-wrapper {
    overflow-y: visible;
    padding: 0;
  }
}
</style>
