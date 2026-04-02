<script setup lang="ts">
import { ref } from 'vue'
import { executeButtonAction } from '../services/actionExecutor'
import { callBackendMethod } from '../services/backendMethods'
import { useButtonStore } from '../state/buttonStore'
import type { ButtonConfig } from '../types/button'
import { httpRequest } from '../utils/http'

const { sortedButtons } = useButtonStore()
const message = ref('')
const pendingId = ref<string | null>(null)

function showMessage(text: string): void {
  message.value = text
  window.setTimeout(() => {
    if (message.value === text) {
      message.value = ''
    }
  }, 2200)
}

async function handleExecute(button: ButtonConfig): Promise<void> {
  try {
    pendingId.value = button.id
    await executeButtonAction({
      button,
      httpRequest,
      callBackendMethod,
      showMessage,
    })
  } catch (error) {
    const text = error instanceof Error ? error.message : '执行失败'
    showMessage(text)
  } finally {
    pendingId.value = null
  }
}
</script>

<template>
  <section class="page">
    <header class="page-header">
      <h2>按钮展示页</h2>
      <p class="tip">根据配置顺序展示并执行动作</p>
    </header>

    <div v-if="message" class="message">{{ message }}</div>

    <div v-if="!sortedButtons.length" class="panel empty">暂无按钮，请先去配置页面新增</div>

    <div v-else class="display-grid">
      <button
        v-for="item in sortedButtons"
        :key="item.id"
        :disabled="pendingId === item.id"
        :style="{
          color: item.style.textColor,
          backgroundColor: item.style.backgroundColor,
          borderColor: item.style.borderColor,
          borderRadius: `${item.style.borderRadius}px`,
          padding: `${item.style.paddingY}px ${item.style.paddingX}px`,
          fontSize: `${item.style.fontSize}px`,
          borderStyle: 'solid',
          borderWidth: '1px',
          opacity: pendingId === item.id ? 0.6 : 1,
          cursor: pendingId === item.id ? 'wait' : 'pointer',
        }"
        @click="handleExecute(item)"
      >
        {{ pendingId === item.id ? '执行中...' : item.text }}
      </button>
    </div>
  </section>
</template>
