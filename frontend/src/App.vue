<template>
  <div class="app-container">
    <!-- 内容区域 -->
    <div class="content-wrapper">
      <component :is="currentComponent" />
    </div>

    <!-- 标签页 - 固定在底部 -->
    <div class="tabs-wrapper">
       <var-bottom-navigation v-model:active="activeTab" active-color="var(--color-primary)">
        <var-bottom-navigation-item name="nodes" label="节点" icon="format-list-checkbox" />
        <var-bottom-navigation-item name="config" label="配置" icon="bookmark" />
        <var-bottom-navigation-item name="download" label="下载" icon="download" />
        <var-bottom-navigation-item name="setting" label="设置" icon="cog" />
      </var-bottom-navigation>
    </div>
    
  </div>
</template>

<script setup>
import { shallowRef, onMounted, onUnmounted, watch } from 'vue'
import { Snackbar, Dialog, StyleProvider, Themes } from '@varlet/ui'
import { getAppMessage } from './assets/fnapp.js'

// 允许同时显示多个消息条
Snackbar.allowMultiple(true)
const activeTab = shallowRef('nodes')
// const isDark = shallowRef(false)
const isMobile = shallowRef(false)
const currentComponent = shallowRef(null)
const switchVconsole = shallowRef(false)
let vconsoleInstance = null

// 动态导入组件
const loadComponent = async (tab) => {
  switch (tab) {
    case 'nodes':
      const { default: NodesTab } = await import('./components/NodesTab.vue')
      currentComponent.value = NodesTab
      break
    case 'config':
      const { default: ConfigTab } = await import('./components/ConfigTab.vue')
      currentComponent.value = ConfigTab
      break
    case 'download':
      const { default: DownloadTab } = await import('./components/DownloadTab.vue')
      currentComponent.value = DownloadTab
      break
    case 'setting':
      const { default: SettingTab } = await import('./components/SettingTab.vue')
      currentComponent.value = SettingTab
      break
    default:
      currentComponent.value = null
  }
}

// 监听标签页变化
watch(activeTab, (newTab) => {
  loadComponent(newTab)
})

const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

const changeTheme = (theme) => {
  if (theme === 'dark') {
    // isDark.value = true
    console.log('md3Dark')
    StyleProvider(Themes.md3Dark)
    // StyleProvider(Themes.dark)
  } else {
    // isDark.value = false
    // console.log('md3Light')
    StyleProvider(Themes.md3Light)
    // StyleProvider(null)
  }
}

const checkSystemTheme = async () => {
  const fnTheme = localStorage.getItem('fnos-theme-mode')  
  // const appTheme = document.body.getAttribute('theme-mode')
  const appInfo = await getAppMessage();
  console.log(appInfo)
  const appTheme = (appInfo || {})?.nightMode;
  console.log('appTheme', appTheme)
  
  if (fnTheme === '10' || appTheme === 'light') {
    // isDark.value = false
    console.log('light', fnTheme, appTheme)
    changeTheme('light')
  } else if (fnTheme === '20' || appTheme === 'dark') {
    // isDark.value = true
    console.log('dark', fnTheme, appTheme) 
    changeTheme('dark')
  } else {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      // isDark.value = true
      console.log('system-dark', fnTheme, appTheme) 
      changeTheme('dark')
    } else {
      // isDark.value = false
      console.log('system-light', fnTheme, appTheme) 
      changeTheme('light')
    }
  }
}

// 切换 VConsole 状态
const toggleVconsole = () => {
  if (switchVconsole.value && vconsoleInstance) {
    vconsoleInstance.destroy()
    switchVconsole.value = false
    vconsoleInstance = null
    return
  }
  import('vconsole').then(({ default: VConsole }) => {
    vconsoleInstance = new VConsole()
    switchVconsole.value = true
  })
}

onMounted(() => {
  toggleVconsole()
  setInterval(() => {
    checkSystemTheme()
  }, 1000)
  //  ()
  checkMobile()
  // 初始加载第一个组件
  loadComponent(activeTab.value)
  
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    checkSystemTheme()
    // isDark.value = e.matches
    // if (isDark.value) {
    //   changeTheme('dark')
    // } else {
    //   changeTheme('light')
    // }
  })
  
  window.addEventListener('storage', (e) => {
    if (e.key === 'fnos-theme-mode') {
      checkSystemTheme()
    }
  })
  
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style scoped>
  .app-container {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    height: 96vh;
  }

  .content-wrapper {
    flex: 1;
    overflow: auto;
    padding: 0 0px;
  }

  .tabs-wrapper {
    flex-shrink: 0;
    padding: 12px;
    border-top: 1px solid var(--color-outline);
    background: var(--color-body);
  }

  @media (max-width: 767px) {
    .app-container {
      height: 100vh;
    }

    .tabs-wrapper {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      width: 100%;
      background: var(--color-body);
      border-top: 1px solid var(--color-outline);
    }

    .content-wrapper {
      padding-bottom: 80px;
    }
  }
</style>
