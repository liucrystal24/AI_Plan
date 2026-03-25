import type { AskResponse } from '../types/chat'

const BASE = 'http://localhost:8000'

export async function askStream(
  query: string,
  onToken: (token: string) => void,
  signal?: AbortSignal,
): Promise<AskResponse> {
  const res = await fetch(`${BASE}/chat/ask/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      user: { user_id: 'u-demo', role: 'employee', dept: 'finance' },
    }),
    signal,
  })

  if (!res.ok || !res.body) {
    throw new Error('问答请求失败')
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder('utf-8')
  let buffer = ''
  let finalPayload: AskResponse | null = null

  while (true) {
    const { value, done } = await reader.read()
    if (done) {
      break
    }
    buffer += decoder.decode(value, { stream: true })
    const events = buffer.split('\n\n')
    buffer = events.pop() ?? ''

    for (const eventBlock of events) {
      const lines = eventBlock.split('\n')
      const eventName = lines
        .find((l) => l.startsWith('event:'))
        ?.replace('event:', '')
        .trim()
      const dataLine = lines
        .find((l) => l.startsWith('data:'))
        ?.replace('data:', '')
        .trim()
      if (!eventName || !dataLine) {
        continue
      }
      if (eventName === 'token') {
        const tokenData = JSON.parse(dataLine) as { text: string }
        onToken(tokenData.text)
      }
      if (eventName === 'final') {
        finalPayload = JSON.parse(dataLine) as AskResponse
      }
    }
  }

  if (!finalPayload) {
    throw new Error('流式响应不完整')
  }
  return finalPayload
}

export async function submitFeedback(
  queryLogId: string,
  vote: 'useful' | 'not_useful',
) {
  await fetch(`${BASE}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query_log_id: queryLogId, vote }),
  })
}
