import { ref } from 'vue';
import type { Ref } from 'vue';

// 从 localStorage 初始化主题
const savedTheme = localStorage.getItem('theme') || 'light';
export const theme: Ref<string> = ref(savedTheme);

// 切换主题并保存到 localStorage
export function toggleTheme(): void {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
  localStorage.setItem('theme', theme.value); // 保存到 localStorage
}
