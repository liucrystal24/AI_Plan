export interface Citation {
  chunk_id: string
  doc_id: string
  title: string
  section: string
  source_ref: string
  snippet: string
  score: number
}

export interface AskResponse {
  answer: string
  citations: Citation[]
  is_refusal: boolean
  refusal_reason?: string
  request_id: string
}
