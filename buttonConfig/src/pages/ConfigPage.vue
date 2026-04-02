<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { buildButtonConfigSchema } from '../services/buttonSchema'
import { availableBackendMethods } from '../services/backendMethods'
import { useButtonStore } from '../state/buttonStore'
import type { ActionType, ButtonConfig } from '../types/button'

const { buttons, sortedButtons, addButton, removeButton, createEmptyButton, updateButton } = useButtonStore()

const selectedId = ref<string>(sortedButtons.value[0]?.id ?? '')
const draft = ref<ButtonConfig | null>(selectedId.value ? cloneButton(findById(selectedId.value)) : null)
const exportMessage = ref('')

watch(
  sortedButtons,
  (value) => {
    if (!value.length) {
      selectedId.value = ''
      draft.value = null
      return
    }

    const exists = value.some((item) => item.id === selectedId.value)
    if (!exists) {
      selectedId.value = value[0].id
    }
  },
  { immediate: true },
)

watch(
  selectedId,
  (id) => {
    const button = findById(id)
    draft.value = button ? cloneButton(button) : null
  },
  { immediate: true },
)

const actionLabelMap: Record<ActionType, string> = {
  link: '跳转链接',
  backend: '后台方法名',
  'custom-js': '自定义 JS',
}

const currentActionPlaceholder = computed(() => {
  if (!draft.value) {
    return ''
  }
  if (draft.value.action.type === 'link') {
    return '例如: https://example.com'
  }
  if (draft.value.action.type === 'backend') {
    return '例如: ping / submitButtonLog'
  }
  return "例如: await utils.httpRequest('/api/demo'); showMessage('执行成功')"
})

function cloneButton(button?: ButtonConfig): ButtonConfig | null {
  if (!button) {
    return null
  }
  return JSON.parse(JSON.stringify(button)) as ButtonConfig
}

function findById(id: string): ButtonConfig | undefined {
  return buttons.value.find((item) => item.id === id)
}

function handleAddButton(): void {
  const created = addButton(createEmptyButton(buttons.value.length + 1))
  selectedId.value = created.id
}

function handleDeleteButton(id: string): void {
  removeButton(id)
}

function handleSave(): void {
  if (!draft.value) {
    return
  }
  updateButton(cloneButton(draft.value) as ButtonConfig)
}

function moveButton(id: string, direction: 'up' | 'down'): void {
  const current = sortedButtons.value
  const index = current.findIndex((item) => item.id === id)
  if (index === -1) {
    return
  }

  const swapIndex = direction === 'up' ? index - 1 : index + 1
  if (swapIndex < 0 || swapIndex >= current.length) {
    return
  }

  const first = current[index]
  const second = current[swapIndex]
  const oldOrder = first.order
  first.order = second.order
  second.order = oldOrder

  updateButton(cloneButton(first) as ButtonConfig)
  updateButton(cloneButton(second) as ButtonConfig)
}

function resetDraft(): void {
  draft.value = selectedId.value ? cloneButton(findById(selectedId.value)) : null
}

function handleExportSchema(): void {
  const orderedButtons = [...sortedButtons.value]
  const schema = buildButtonConfigSchema(orderedButtons)
  const schemaText = JSON.stringify(schema, null, 2)
  const blob = new Blob([schemaText], { type: 'application/json;charset=utf-8' })
  const url = URL.createObjectURL(blob)

  const link = document.createElement('a')
  link.href = url
  link.download = `button-config-schema-${new Date().toISOString().slice(0, 10)}.json`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)

  exportMessage.value = 'JSON Schema 已导出'
  window.setTimeout(() => {
    exportMessage.value = ''
  }, 1800)
}
</script>

<template>
  <section class="page">
    <header class="page-header">
      <h2>按钮配置管理</h2>
      <div class="header-actions">
        <button class="secondary-btn" @click="handleExportSchema">导出 JSON Schema</button>
        <button class="secondary-btn" @click="handleAddButton">新增按钮</button>
      </div>
    </header>
    <div v-if="exportMessage" class="message">{{ exportMessage }}</div>

    <div class="layout">
      <aside class="panel list-panel">
        <div class="list-title">按钮列表（按排序显示）</div>
        <div v-if="!sortedButtons.length" class="empty">暂无按钮，请先新增</div>
        <ul v-else class="button-list">
          <li
            v-for="item in sortedButtons"
            :key="item.id"
            :class="['row', { active: selectedId === item.id }]"
          >
            <button class="row-main" @click="selectedId = item.id">
              <span>{{ item.text }}</span>
              <small>排序: {{ item.order }}</small>
            </button>
            <div class="row-actions">
              <button class="tiny-btn" @click="moveButton(item.id, 'up')">上移</button>
              <button class="tiny-btn" @click="moveButton(item.id, 'down')">下移</button>
              <button class="tiny-btn danger" @click="handleDeleteButton(item.id)">删除</button>
            </div>
          </li>
        </ul>
      </aside>

      <main class="panel form-panel">
        <template v-if="draft">
          <h3>编辑按钮</h3>
          <div class="form-grid">
            <label>
              显示文本
              <input v-model="draft.text" type="text" />
            </label>
            <label>
              排序
              <input v-model.number="draft.order" type="number" min="1" />
            </label>
            <label>
              文本颜色
              <input v-model="draft.style.textColor" type="color" />
            </label>
            <label>
              背景颜色
              <input v-model="draft.style.backgroundColor" type="color" />
            </label>
            <label>
              边框颜色
              <input v-model="draft.style.borderColor" type="color" />
            </label>
            <label>
              圆角(px)
              <input v-model.number="draft.style.borderRadius" type="number" min="0" />
            </label>
            <label>
              上下内边距(px)
              <input v-model.number="draft.style.paddingY" type="number" min="0" />
            </label>
            <label>
              左右内边距(px)
              <input v-model.number="draft.style.paddingX" type="number" min="0" />
            </label>
            <label>
              字号(px)
              <input v-model.number="draft.style.fontSize" type="number" min="10" />
            </label>
            <label>
              动作类型
              <select v-model="draft.action.type">
                <option value="link">跳转三方链接</option>
                <option value="backend">调用后台方法名</option>
                <option value="custom-js">自定义 JS</option>
              </select>
            </label>
          </div>

          <label class="full-width">
            {{ actionLabelMap[draft.action.type] }}
            <template v-if="draft.action.type === 'custom-js'">
              <textarea
                v-model="draft.action.payload"
                :placeholder="currentActionPlaceholder"
                rows="8"
              />
            </template>
            <template v-else>
              <input v-model="draft.action.payload" type="text" :placeholder="currentActionPlaceholder" />
            </template>
          </label>

          <p v-if="draft.action.type === 'backend'" class="tip">
            可用后台方法：{{ availableBackendMethods.join('、') }}
          </p>

          <p v-if="draft.action.type === 'custom-js'" class="tip">
            自定义 JS 可使用变量：button、utils.httpRequest、showMessage。
          </p>

          <div class="preview">
            <span>预览：</span>
            <button
              :style="{
                color: draft.style.textColor,
                backgroundColor: draft.style.backgroundColor,
                borderColor: draft.style.borderColor,
                borderRadius: `${draft.style.borderRadius}px`,
                padding: `${draft.style.paddingY}px ${draft.style.paddingX}px`,
                fontSize: `${draft.style.fontSize}px`,
                borderStyle: 'solid',
                borderWidth: '1px',
              }"
            >
              {{ draft.text }}
            </button>
          </div>

          <div class="form-actions">
            <button class="primary-btn" @click="handleSave">保存修改</button>
            <button class="secondary-btn" @click="resetDraft">重置</button>
          </div>
        </template>

        <div v-else class="empty">请选择要编辑的按钮</div>
      </main>
    </div>
  </section>
</template>
