// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'dark', // 默认主题为浅色模式
    themes: {
      light: {
        // 浅色模式的主题配置
        dark: false, // 浅色模式
      },
      dark: {
        // 暗黑模式的主题配置
        dark: true, // 暗黑模式
      },
    },
  },
})
