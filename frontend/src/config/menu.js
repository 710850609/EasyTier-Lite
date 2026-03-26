/**
 * 菜单配置
 * 统一维护应用的所有菜单项
 */

// 使用 import.meta.glob 预加载所有视图组件
const viewModules = import.meta.glob('../views/*.vue')

// 菜单树结构（每个节点单行）
export const menuTree = [
  { key: 'nodes', label: '节点', icon: 'format-list-checkbox', title: '节点管理', component: 'Nodes' },
  { key: 'config', label: '配置', icon: 'bookmark-outline', title: '配置管理', component: 'Config' },
  { key: 'software', label: '应用', icon: 'shopping-outline', title: '软件下载', component: 'Software',
    children: [
      { key: 'software-windows', label: 'Windows', icon: 'menu-right', component: 'Software' },
      { key: 'software-macos', label: 'macOS', icon: 'menu-right', component: 'Software' },
      { key: 'software-ios', label: 'iOS', icon: 'menu-right', component: 'Software' },
      { key: 'software-linux', label: 'Linux', icon: 'menu-right', component: 'Software' },
      { key: 'software-android', label: 'Android', icon: 'menu-right', component: 'Software' },
      { key: 'software-harmonyos', label: '鸿蒙', icon: 'menu-right', component: 'Software' }
    ]
  },
  { key: 'settings', label: '设置', icon: 'cog-outline', title: '系统设置', component: 'Settings' }
]

// 扁平化菜单树
const flattenMenuTree = (items) => {
  const result = []
  items.forEach(item => {
    result.push(item)
    if (item.children) {
      result.push(...flattenMenuTree(item.children))
    }
  })
  return result
}

// 组件映射表（从菜单树构建）
const buildComponentMap = () => {
  const map = {}
  const flatMenus = flattenMenuTree(menuTree)
  flatMenus.forEach(item => {
    if (item.component) {
      const modulePath = `../views/${item.component}.vue`
      if (viewModules[modulePath]) {
        map[item.key] = viewModules[modulePath]
      }
    }
  })
  return map
}

export const componentMap = buildComponentMap()

export default menuTree
