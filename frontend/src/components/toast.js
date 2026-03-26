import { Snackbar } from '@varlet/ui'
import { h } from 'vue'
import { Icon } from '@varlet/ui'

// 类型映射
const typeMap = {
  'default': '',
  'success': 'success',
  'warning': 'warning',
  'error': 'error',
  'info': 'primary',
  'loading': 'loading'
}

// 全局配置：允许多个 Snackbar 同时显示，最多3个
Snackbar.allowMultiple(true)
// Snackbar.setMaxCount(3)

// 创建 Toast（clear 方法幂等）
function createToast(message, type = 'default', duration = 3000) {
  let cleared = false

  const snackbar = Snackbar({
    content: message,
    type: typeMap[type] || '',
    position: 'top',
    duration: duration,
    icon: () => type === 'loading' ? 'loading' : '',
    action: () =>
      h(Icon, {
        name: 'window-close',
        size: '20',
        style: { cursor: 'pointer', marginLeft: '8px' },
        onClick: () => {
            snackbar.clear()
          }
      })
  })

  return snackbar
}

// 导出直接可用的函数
export const toast = {
  success(message, duration = 3000) {
    return createToast(message, 'success', duration)
  },

  error(message, duration = 5000) {
    return createToast(message, 'error', duration)
  },

  warning(message, duration = 3000) {
    return createToast(message, 'warning', duration)
  },

  info(message, duration = 3000) {
    return createToast(message, 'info', duration)
  },

  loading(message = '加载中...', duration = 0) {
    return createToast(message, 'loading', duration)
  }
}

export default toast
