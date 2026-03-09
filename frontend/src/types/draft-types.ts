/** Chat message in the conversation thread */
export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

/** SSE chunk event data from backend */
export interface SSEChunkData {
  content: string
  session_id: string
}

/** SSE done event data */
export interface SSEDoneData {
  status: string
  session_id: string
}

/** SSE error event data */
export interface SSEErrorData {
  error: string
  code: string
}

/** Draft streaming state */
export interface DraftState {
  sessionId: string | null
  messages: ChatMessage[]
  draftContent: string
  isStreaming: boolean
  isFirstDraft: boolean
}
