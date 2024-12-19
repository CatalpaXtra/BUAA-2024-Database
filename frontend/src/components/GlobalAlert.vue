<script setup lang="ts">
import { ref, watch } from 'vue';
import { type AlertInfo, newAlert } from '@/store/alert';

// 使用 Map 存储 Alert 信息，方便管理和删除
const alertMap = ref<Map<string, AlertInfo>>(new Map());

// 监听新 Alert 创建事件，将其加入 alertMap，并设置定时删除
watch(newAlert.value, () => {
  if (newAlert.value.id) {
    // 克隆新 Alert 信息并存入 Map
    alertMap.value.set(newAlert.value.id, { ...newAlert.value });

    // 自动删除当前 Alert
    scheduleAlertDeletion(newAlert.value.id);
  }
});

// 定时删除 Alert
const scheduleAlertDeletion = (id: string) => {
  setTimeout(() => {
    if (alertMap.value.has(id)) {
      alertMap.value.delete(id);
      console.log('Alert deleted:', id); // 调试用，可移除
    }
  }, 3000);
};
</script>

<template>
  <div class="alert-container">
    <!-- 遍历 alertMap 中的 Alert 并渲染 -->
    <v-alert
      class="v-alert"
      v-for="(alert, index) in Array.from(alertMap.values())"
      :key="index"
      :type="alert.type"
      border="start"
      variant="tonal"
      close-label="关闭提示"
      closable
      :text="alert.message"
    >
    </v-alert>
  </div>
</template>

<style scoped>
/* Alert 容器样式 */
.alert-container {
  position: absolute;
  top: 8%;
  right: 5%;
  z-index: 9999;
}

/* 单个 Alert 的样式 */
.v-alert {
  margin-top: 0.2rem !important;
}
</style>
