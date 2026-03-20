import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'

export default defineConfig({
  base: './',
  plugins: [
    vue(),
    Components({
      dirs: ['src/components'],
      extensions: ['vue'],
      deep: true,
      dts: true,
      directoryAsNamespace: true,
      globalNamespaces: ['components'],
      include: [/\.vue$/, /\.vue\?vue/],
      exclude: [/[\\/]node_modules[\\/]/, /[\\/]\.git[\\/]/, /[\\/]\.vscode[\\/]/],
    }),
    AutoImport({
      imports: [
        'vue',
        {
          '@varlet/ui': [
            'Snackbar',
            'Dialog',
            'StyleProvider',
            'Themes',
            'Button',
            'Cell',
            'Tabs',
            'Tab',
            'BottomNavigation',
            'BottomNavigationItem',
            'MenuSelect',
            'Select',
            'TextField',
            'Switch',
            'Slider',
            'Rate',
            'ColorPicker',
            'DatePicker',
            'TimePicker',
            'Upload',
            'ImagePreview',
            'Image',
            'Avatar',
            'Badge',
            'Chip',
            'Progress',
            'Skeleton',
            'Loading',
            'Toast',
            'Popup',
            'Dialog',
            'Snackbar',
            'PullRefresh',
            'Swipe',
            'SwipeItem',
            'Stepper',
            'NumberKeyboard',
            'Stepper',
            'Steps',
            'Card',
            'List',
            'Cell',
            'Icon',
            'App',
          ],
        },
      ],
      dts: true,
      dirs: ['src'],
      include: [/\.vue$/, /\.vue\?vue/],
      exclude: [/[\\/]node_modules[\\/]/, /[\\/]\.git[\\/]/, /[\\/]\.vscode[\\/]/],
    }),
  ],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/cgi': {
        target: 'https://192.168.220.3:5667',
        changeOrigin: true,
        secure: false,
        configure: (proxy, options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Proxying to:', options.target + req.url)
          })
          proxy.on('error', (err, req, res) => {
            console.log('Proxy error:', err)
          })
        },
      },
    },
  },
})
