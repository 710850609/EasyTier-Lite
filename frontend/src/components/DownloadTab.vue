<template>
  <var-tabs
    elevation
    sticky
    sticky-z-index="999"
    v-model:active="downloadActive"
  >
  <var-tab>软件</var-tab>
    <var-tab>配置文件</var-tab>
  </var-tabs>

  <var-tabs-items v-model:active="downloadActive">
    <var-tab-item>
      <div class="tab-content">
      <h3>下载筛选</h3>
        <var-divider />
        <div>
          <h3>系统</h3>
          <var-cell>
            <template #default>
              <var-space :size="[10, 10]"> 
                <var-button 
                  :type="system === item ? 'success' : 'default'" 
                  v-for="item in systemList" 
                  :key="item" 
                  @click="handleSystemChange(item)"
                >
                  {{ item }}
                </var-button>
              </var-space>
            </template>
          </var-cell>
          <var-divider />
        </div>
        <div v-if="!['windows', 'harmonyos', 'ios'].includes(system)">
          <h3>EasyTier版本</h3>
          <var-cell>
            <template #default>
              <var-space :size="[20, 20]"> 
                <var-button 
                  :type="version === item ? 'success' : 'default'" 
                  v-for="item in versionList" 
                  :key="item" 
                  @click="handleVersionChange(item)"
                >
                  {{ item }}
                </var-button>
              </var-space>
            </template>
          </var-cell>
          <var-divider />
        </div>
        <div v-if="['macos', 'linux'].includes(system)">
          <h3>CPU架构</h3>
          <var-cell>
            <template #default>
              <var-space :size="[20, 20]"> 
                <var-button 
                  :type="arch === item ? 'success' : 'default'" 
                  v-for="item in archList" 
                  :key="item"                
                  @click="handleArchChange(item)"
                i>
                  {{ item }}
                </var-button>
              </var-space>
            </template>
          </var-cell>
          <var-divider />
        </div>        
        <div v-if="!['windows', 'harmonyos', 'ios'].includes(system)">
          <h3>Github加速</h3>
          <var-cell>
            <template #default>
              <var-space :size="[20, 20]"> 
                <var-button 
                  :type="githubProxy === item ? 'success' : 'default'" 
                  v-for="item in githubProxyList" 
                  :key="item" 
                
                  @click="handleGithubProxyChange(item)"
                i>
                  {{ item }}
                </var-button>
              </var-space>
            </template>
          </var-cell>
          <var-divider />
        </div>
        <h3>下载链接</h3>
        <var-cell icon="shopping"  v-if="downloadUrl !== ''">
          <template #description>
            {{downloadName}}
          </template>
          <template #extra>
            <var-space :size="[20, 20]">
              <var-button type="primary" @click="download" v-if="!['harmonyos', 'ios'].includes(system)">下载</var-button>
              <var-button type="primary" @click="copyDownloadUrl" v-if="['harmonyos', 'ios'].includes(system)">复制下载链接</var-button>
            </var-space>
          </template>
        </var-cell>
    </div>
    </var-tab-item>
    <var-tab-item>
      <var-cell icon="file-document-outline" description="下载配置文件，可用于导入软件运行">
        <template #extra>
          <var-button type="primary" @click="downloadConfig">下载</var-button>
        </template>
      </var-cell>
    </var-tab-item>
  </var-tabs-items>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { Snackbar, Dialog } from '@varlet/ui'

  const downloadActive = ref(0)  
  const show = ref(true)
  const systemList = ref(['windows', 'macos', 'linux', 'android', 'harmonyos', 'ios'])
  const archList = ref(['x86_64', 'arm64'])
  const versionList = ref(['2.4.5', '2.5.0'])
  const githubProxyList = ref(['https://ghfast.top', 'https://gh.llkk.cc', 'https://hk.gh-proxy.org', 'https://gh-proxy.org', 'https://cdn.gh-proxy.org', 'https://edgeone.gh-proxy.org'])
  
  const system = ref('windows')
  const arch = ref('x86_64')
  const version = ref('2.5.0')
  const githubProxy = ref('https://ghfast.top')
  const downloadName = ref('')
  const downloadUrl = ref('')

  function handleVersionChange(item) {
    version.value = item
    getDownloadUrl()
  }

  function handleSystemChange(item) {
    system.value = item
    getDownloadUrl()
  }

  function handleArchChange(item) {
    arch.value = item
    getDownloadUrl()
  }
  
  function handleGithubProxyChange(item) {
    githubProxy.value = item
    getDownloadUrl()
  }

  function getDownloadUrl() {
    if (!version.value) {
        Snackbar.error('请选择 EasyTier 版本');
        return
    }
    if (!system.value) {
        Snackbar.error('请选择系统');
        return
    }
    
    if (system.value === 'android') {
      // downloadName.value = `app-universal-release.apk`
      downloadName.value = `安装软件后，下载配置文件，并导入配置文件`;
      downloadUrl.value = `${githubProxy.value}/https://github.com/EasyTier/EasyTier/releases/download/v2.5.0/app-universal-release.apk`;
    } else {
      if (!arch.value) {
        Snackbar.error('请选择 CPU 架构');
        return
      }
      
      if (system.value == 'windows') {
        // downloadName.value = `easytier-manager-pro.zip`
        downloadName.value = `下载解压后，选择内置配置，直接启动(组网)`
        downloadUrl.value = `/cgi/ThirdParty/EasyTier-Lite/api.cgi/windows/download`;
      } else {
        // downloadName.value = `easytier-${system.value}-${arch.value}-v${version.value}.zip"
        downloadName.value = `安装软件后，下载配置文件，并导入配置文件`;
        downloadUrl.value = `${githubProxy.value}/https://github.com+/EasyTier/EasyTier/releases/download/v${version.value}/${downloadName.value}`;
        if (['harmonyos', 'ios'].includes(system.value)) {
          downloadName.value = `浏览器打开链接，下载EasyTier`
        }
      }
    }    
    // console.log('Download URL:', downloadUrl.value)
    // console.log('Download Name:', downloadName.value)
  }

  function download() {
    if (downloadUrl.value) {
      window.open(downloadUrl.value, '_blank')
    } else {
      getDownloadUrl()
    }
  }

  function downloadConfig() {
    window.open('/cgi/ThirdParty/EasyTier-Lite/api.cgi/configs/download', '_blank')
  }

  getDownloadUrl()
</script>

<style scoped>
/* .main-content {
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  overflow: hidden;
}

.tab-content {
  padding: 24px;
}

.tab-content h2 {
  color: var(--text-primary);
  margin-bottom: 16px;
}

.tab-content p {
  color: var(--text-secondary);
} */
</style>
