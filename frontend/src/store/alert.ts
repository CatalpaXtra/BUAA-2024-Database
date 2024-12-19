import { ref } from 'vue'

export interface AlertInfo {
  id: string,
  type: string,
  message: string
}

export const newAlert = ref<AlertInfo>({
  id: 'alert' + 0,
  type: '',
  message: ''
})

export const alert = (message: string, type: string) => {
    newAlert.value.id = Math.random().toString()
    newAlert.value.type = type === null ? 'info' : type
    newAlert.value.message = message
}