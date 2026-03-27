<template>
  <div class="settings-page">
    <!-- 外观设置 -->
    <var-paper class="setting-block" :elevation="1">
      <div class="block-header">
        <var-icon name="palette" size="24" color="var(--color-primary)" />
        <span class="block-title">外观设置</span>
      </div>
      
      <div class="theme-options">
        <div 
          v-for="option in themeOptions" 
          :key="option.value"
          class="theme-option"
          :class="{ active: currentThemeMode === option.value }"
          @click="setThemeMode(option.value)"
        >
          <var-icon :name="option.icon" size="20" />
          <span>{{ option.label }}</span>
        </div>
      </div>
    </var-paper>

    <!-- 开发者选项 -->
    <var-paper class="setting-block" :elevation="1">
      <div class="block-header">
        <var-icon name="code" size="24" color="var(--color-primary)" />
        <span class="block-title">开发者选项</span>
      </div>
      
      <var-cell>
        <template #title>开启 VConsole</template>
        <template #description>用于移动端调试，显示控制台日志</template>
        <template #extra>
          <var-switch v-model="vConsoleEnabled" @change="toggleVConsole" />
        </template>
      </var-cell>
    </var-paper>

    <!-- 网络设置 -->
    <!-- <var-paper class="setting-block" :elevation="1">
      <div class="block-header">
        <var-icon name="globe" size="24" color="var(--color-success)" />
        <span class="block-title">网络加速</span>
      </div>
      
      <var-select v-model="settings.github_mirror" label="GitHub 加速地址">
        <var-option 
          v-for="mirror in githubMirrors" 
          :key="mirror.value"
          :label="mirror.label"
          :value="mirror.value"
        />
      </var-select>
      
      <var-cell class="test-link">
        <template #description>
          <a :href="settings.github_mirror" target="_blank" class="mirror-link">
            测试连接速度 <var-icon name="open-in-new" size="14" />
          </a>
        </template>
      </var-cell>
    </var-paper> -->

    <!-- 关于 -->
    <var-paper class="setting-block" :elevation="1">
      <div class="block-header">
        <var-icon name="information" size="24" color="var(--color-info)" />
        <span class="block-title">关于</span>
      </div>
      
      <var-cell>
        <template #default></template>
        <template #description>
          <div>EasyTier 在飞牛上简化使用的版本，更合适新手简单上手使用，简记：易组网。</div>
          <var-divider />
          <div>
            <p><a href="https://github.com/710850609/fpk-easytier-lite" target="_blank">易组网源码</a></p>
            <p><a href="https://github.com/easyTier/easytier" target="_blank">EasyTier源码</a></p>
            <p><a href="https://easytier.cn/" target="_blank">EasyTier文档</a></p>
          </div>
        </template>
      </var-cell>
    </var-paper>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { themeOptions, setThemeMode, themeMode } from '../config/theme.js'
import { VCONSOLE_ENABLED_KEY, VCONSOLE_CODE_KEY } from '../config/storage-keys.js'
import toast from '../components/toast.js'

const vConsoleEnabled = ref(false)

// 计算当前主题模式（从 theme.js 获取）
const currentThemeMode = computed(() => themeMode.value)
const VCONSOLE_URL = 'https://unpkg.com/vconsole@latest/dist/vconsole.min.js'

// 设置对象（网络加速不存 localStorage）
// const settings = ref({
//   vconsole: false,
//   github_mirror: 'https://ghproxy.com/https://github.com'
// })

const githubMirrors = [
  { label: 'GhProxy', value: 'https://ghproxy.com/https://github.com' },
  { label: 'FastGit', value: 'https://hub.fastgit.xyz' },
  { label: 'GitHub 原始', value: 'https://github.com' },
  { label: 'jsDelivr', value: 'https://cdn.jsdelivr.net/gh' }
]

// 从 localStorage 加载 VConsole 代码
const loadVConsoleFromStorage = () => {
  const storedCode = localStorage.getItem(VCONSOLE_CODE_KEY)
  if (storedCode) {
    try {
      const script = document.createElement('script')
      script.textContent = storedCode
      document.body.appendChild(script)
      
      if (window.VConsole) {
        window.vConsole = new window.VConsole()
        return true
      }
    } catch (error) {
      console.error('加载本地 VConsole 失败:', error)
      localStorage.removeItem(VCONSOLE_CODE_KEY)
    }
  }
  return false
}

// 下载并缓存 VConsole
const downloadAndCacheVConsole = async () => {
  const loading = toast.loading('正在下载 VConsole...')
  try {
    const response = await fetch(VCONSOLE_URL)
    const code = await response.text()
    
    localStorage.setItem(VCONSOLE_CODE_KEY, code)
    
    const script = document.createElement('script')
    script.textContent = code
    document.body.appendChild(script)
    
    if (window.VConsole) {
      window.vConsole = new window.VConsole()
      toast.success('VConsole 已下载并启用')
    } else {      
      toast.error('加载 VConsole 失败，请重试')
    }
  } catch (error) {
    console.error('下载 VConsole 失败:', error)
    toast.error('下载 VConsole 失败，请检查网络连接')
    localStorage.setItem(VCONSOLE_ENABLED_KEY, 'false')
  } finally {
    loading.clear()
  }
}

// 切换 VConsole
const toggleVConsole = async (val) => {
  // 保存开关状态
  localStorage.setItem(VCONSOLE_ENABLED_KEY, val ? 'true' : 'false')  
  if (val) {
    const loaded = loadVConsoleFromStorage()
    if (!loaded) {
      await downloadAndCacheVConsole()
    } else {
      toast.success(`VConsole 已开启`)
    }
  } else {
    if (window.vConsole) {
      window.vConsole.destroy()
      window.vConsole = null
    }
    toast.success('VConsole 已关闭')
  }
}

onMounted(() => {
  // 从 localStorage 加载 VConsole 开关状态
  vConsoleEnabled.value = localStorage.getItem(VCONSOLE_ENABLED_KEY) === 'true'
})
</script>

<style scoped>
.settings-page {
  padding: 16px;
  max-width: 800px;
  margin: 0 auto;
}

.setting-block {
  padding: 20px;
  border-radius: 16px;
  margin-bottom: 16px;
  background: var(--color-surface-container) !important;
}

.block-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.block-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text);
}

.mirror-link, .source-link {
  color: var(--color-primary);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.test-link {
  margin-top: 8px;
}

:deep(.var-cell__description) {
  margin-top: 4px;
}

/* 主题选项样式 */
.theme-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 8px;
  border-radius: 12px;
  border: 2px solid var(--color-outline);
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.theme-option:hover {
  border-color: var(--color-primary);
  background: var(--color-surface-container);
}

.theme-option.active {
  border-color: var(--color-primary);
  background: var(--color-primary-container);
  color: var(--color-on-primary-container);
}

.theme-option span {
  font-size: 14px;
  font-weight: 500;
}
</style>
