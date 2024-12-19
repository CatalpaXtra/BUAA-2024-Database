<template>
  <v-app :theme="theme">
    <Layout/> 
  </v-app>

</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Layout from './components/Layout.vue'
import { theme } from '@/composables/theme'

export default defineComponent({
  name: 'App',
  setup() {
    return {
      theme,
    };
  },
  components: {
    Layout,
  },
  data () {
    return {
      //
    }
  },
})
</script>
