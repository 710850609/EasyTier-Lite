<template>
  <div class="side-menu">
    <div class="logo">
      <var-icon name="network-wired" :size="32" />
      <span class="logo-text">易组网 . EasyTier</span>
    </div>
    
    <div class="menu-list">
      <template v-for="menu in menuTree" :key="menu.key">
        <!-- 有子菜单的项 -->
        <div v-if="menu.children" class="menu-group">
          <div 
            class="menu-item"
            :class="{ active: active?.startsWith(menu.key) }"
            @click="toggleExpand(menu.key)"
          >
            <var-icon :name="menu.icon" class="menu-icon" />
            <span class="menu-title">{{ menu.label }}</span>
            <var-icon 
              name="chevron-down" 
              class="expand-icon"
              :class="{ expanded: expandedKeys.includes(menu.key) }"
            />
          </div>
          
          <div class="sub-menu-list" v-show="expandedKeys.includes(menu.key)">
            <div 
              v-for="child in menu.children"
              :key="child.key"
              class="sub-menu-item"
              :class="{ active: active === child.key }"
              @click="handleClick(child.key)"
            >
              <var-icon :name="child.icon" size="18" />
              <span>{{ child.label }}</span>
            </div>
          </div>
        </div>
        
        <!-- 无子菜单的项 -->
        <div 
          v-else
          class="menu-item"
          :class="{ active: active === menu.key }"
          @click="handleClick(menu.key)"
        >
          <var-icon :name="menu.icon" class="menu-icon" />
          <span class="menu-title">{{ menu.label }}</span>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { menuTree } from '../config/menu.js'

const props = defineProps({
  active: String
})

const emit = defineEmits(['update:active'])

const expandedKeys = ref([])

// 监听 active 变化，自动展开父菜单
watch(() => props.active, (val) => {
  if (val?.startsWith('software-') && !expandedKeys.value.includes('software')) {
    expandedKeys.value.push('software')
  }
}, { immediate: true })

const toggleExpand = (key) => {
  const index = expandedKeys.value.indexOf(key)
  if (index > -1) {
    expandedKeys.value.splice(index, 1)
  } else {
    expandedKeys.value.push(key)
  }
}

const handleClick = (key) => {
  emit('update:active', key)
}
</script>

<style scoped>
.side-menu {
  height: 100vh;
  background: var(--color-surface);
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--color-outline);
}

.logo {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--color-outline);
}

.logo-text {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-primary);
}

.menu-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 4px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--color-on-surface);
}

.menu-item:hover {
  background: var(--color-surface-container-highest);
}

.menu-item.active {
  background: var(--color-primary-container);
  color: var(--color-on-primary-container);
}

.menu-icon {
  margin-right: 12px;
  color: var(--color-on-surface-variant);
}

.menu-item.active .menu-icon {
  color: var(--color-on-primary-container);
}

.menu-title {
  flex: 1;
  font-size: 14px;
}

.expand-icon {
  transition: transform 0.2s;
  color: var(--color-on-surface-variant);
}

.expand-icon.expanded {
  transform: rotate(180deg);
}

.menu-group {
  margin-bottom: 4px;
}

.sub-menu-list {
  padding-left: 8px;
}

.sub-menu-item {
  display: flex;
  align-items: center;
  padding: 10px 16px 10px 40px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--color-on-surface-variant);
  font-size: 13px;
  gap: 8px;
}

.sub-menu-item:hover {
  background: var(--color-surface-container-highest);
}

.sub-menu-item.active {
  background: var(--color-primary-container);
  color: var(--color-on-primary-container);
}
</style>
