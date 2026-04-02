<script setup lang="ts">
import { ref } from 'vue'
import { executeButtonAction } from '../services/actionExecutor'
import { callBackendMethod } from '../services/backendMethods'
import { parseButtonsFromSchemaText } from '../services/buttonSchema'
import type { ButtonConfig } from '../types/button'
import { httpRequest } from '../utils/http'

const rawSchemaText = ref('')
const importedButtons = ref<ButtonConfig[]>([])
const errorMessage = ref('')
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

function handleImportFromText(): void {
  if (!rawSchemaText.value.trim()) {
    errorMessage.value = '请先粘贴 JSON Schema 内容'
    importedButtons.value = []
    return
  }

  try {
    importedButtons.value = parseButtonsFromSchemaText(rawSchemaText.value)
    errorMessage.value = ''
    showMessage('Schema 导入成功')
  } catch (error) {
    importedButtons.value = []
    errorMessage.value = error instanceof Error ? error.message : '导入失败，请检查 JSON 内容'
  }
}

function handleClear(): void {
  rawSchemaText.value = ''
  importedButtons.value = []
  errorMessage.value = ''
  message.value = ''
}

function handleFileChange(event: Event): void {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }

  const reader = new FileReader()
  reader.onload = () => {
    rawSchemaText.value = String(reader.result ?? '')
    handleImportFromText()
  }
  reader.onerror = () => {
    errorMessage.value = '读取文件失败，请重试'
  }
  reader.readAsText(file)
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
      <h2>Schema 导入渲染</h2>
      <p class="tip">粘贴或上传从配置页面导出的 JSON Schema</p>
    </header>

    <section class="panel">
      <label>
        JSON Schema
        <textarea
          v-model="rawSchemaText"
          rows="12"
          placeholder="请粘贴 JSON Schema..."
        />
      </label>

      <div class="import-actions">
        <button class="primary-btn" @click="handleImportFromText">导入并渲染</button>
        <label class="secondary-btn file-picker">
          上传 JSON 文件
          <input type="file" accept="application/json,.json" @change="handleFileChange" />
        </label>
        <button class="secondary-btn" @click="handleClear">清空</button>
      </div>

      <div v-if="message" class="message">{{ message }}</div>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </section>

    <section v-if="importedButtons.length" class="panel render-panel">
      <h3>渲染出的配置项</h3>
      <ul class="schema-item-list">
        <li v-for="item in importedButtons" :key="item.id" class="schema-item">
          <div><strong>文本：</strong>{{ item.text }}</div>
          <div><strong>排序：</strong>{{ item.order }}</div>
          <div><strong>动作：</strong>{{ item.action.type }} / {{ item.action.payload }}</div>
          <div>
            <strong>样式：</strong>
            文本色 {{ item.style.textColor }}，背景色 {{ item.style.backgroundColor }}，边框 {{ item.style.borderColor }}，
            圆角 {{ item.style.borderRadius }}px，内边距 {{ item.style.paddingY }}px {{ item.style.paddingX }}px，字号 {{ item.style.fontSize }}px
          </div>
        </li>
      </ul>

      <h3>按钮预览（可点击执行动作）</h3>
      <div class="display-grid">
        <button
          v-for="item in importedButtons"
          :key="`${item.id}-preview`"
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

    <section v-else class="panel empty">
      还未导入有效的 Schema。
    </section>
  </section>
</template>
