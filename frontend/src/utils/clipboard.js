/**
 * 剪贴板工具函数
 * 支持复制文本到剪贴板，兼容 HTTP/HTTPS 环境
 */

/**
 * 降级复制方案（使用 document.execCommand）
 * @param {string} text - 要复制的文本
 * @returns {boolean} - 是否复制成功
 */
const fallbackCopy = (text) => {
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.style.position = 'fixed'
  textarea.style.left = '-9999px'
  textarea.style.top = '0'
  textarea.setAttribute('readonly', '')
  document.body.appendChild(textarea)
  textarea.select()
  textarea.setSelectionRange(0, text.length)
  
  try {
    const result = document.execCommand('copy')
    document.body.removeChild(textarea)
    return result
  } catch (e) {
    document.body.removeChild(textarea)
    return false
  }
}

/**
 * 复制文本到剪贴板
 * @param {string} text - 要复制的文本
 * @returns {Promise<boolean>} - 是否复制成功
 */
export const copyToClipboard = async (text) => {
  if (!text) return false
  
  // 尝试使用现代 API（仅在 HTTPS 下可用）
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(text)
      return true
    } catch (err) {
      return fallbackCopy(text)
    }
  }
  
  // 使用降级方案
  return fallbackCopy(text)
}


export default {
  copyToClipboard
}
