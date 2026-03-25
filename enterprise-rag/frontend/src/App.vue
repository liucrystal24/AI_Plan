<script setup lang="ts">
import { ref } from 'vue'
import { askStream, submitFeedback } from './services/api'
import type { AskResponse } from './types/chat'

const query = ref('')
const loading = ref(false)
const error = ref('')
const result = ref<AskResponse | null>(null)
const streamedAnswer = ref('')
let controller: AbortController | null = null

async function onAsk() {
  if (!query.value.trim()) {
    return
  }

  controller?.abort()
  controller = new AbortController()
  loading.value = true
  error.value = ''
  streamedAnswer.value = ''
  result.value = null

  try {
    const finalResult = await askStream(
      query.value,
      (token) => {
        streamedAnswer.value += token
      },
      controller.signal,
    )
    result.value = { ...finalResult, answer: streamedAnswer.value || finalResult.answer }
  } catch (e) {
    if (e instanceof Error && e.name === 'AbortError') {
      return
    }
    error.value = e instanceof Error ? e.message : '请求失败'
  } finally {
    loading.value = false
  }
}

function onStop() {
  controller?.abort()
  loading.value = false
}

async function onFeedback(vote: 'useful' | 'not_useful') {
  if (!result.value) {
    return
  }
  await submitFeedback(result.value.request_id, vote)
}
</script>

<template>
  <div class="page">
    <header class="hero">
      <h1>企业知识库问答</h1>
      <p>RAG V1: 引用溯源、拒答、权限治理基础能力</p>
    </header>

    <main class="card">
      <textarea v-model="query" rows="5" placeholder="请输入问题，例如：报销额度和发票要求是什么？" />
      <div class="actions">
        <button class="primary" :disabled="loading" @click="onAsk">{{ loading ? '查询中...' : '提交问题' }}</button>
        <button v-if="loading" class="secondary" @click="onStop">中断生成</button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>

      <section v-if="result || streamedAnswer" class="result">
        <h2>回答</h2>
        <p class="answer">{{ streamedAnswer || result?.answer }}</p>

        <h3 v-if="result?.citations?.length">引用来源</h3>
        <ul v-if="result?.citations?.length">
          <li v-for="c in result.citations" :key="c.chunk_id">
            <strong>{{ c.title }}</strong> / {{ c.section }} / score={{ c.score }}
            <p>{{ c.snippet }}</p>
            <small>{{ c.source_ref }}</small>
          </li>
        </ul>

        <div v-if="result?.request_id" class="feedback">
          <button @click="onFeedback('useful')">有用</button>
          <button @click="onFeedback('not_useful')">无用</button>
        </div>
      </section>
    </main>
  </div>
</template>
