/**
 * Draft API service - handles SSE streaming from FastAPI backend.
 * Uses fetch + ReadableStream (not EventSource, which only supports GET).
 */

const API_BASE = '/api'

/** Callback for each streamed chunk */
type OnChunk = (data: { content: string; session_id: string }) => void
type OnDone = (data: { session_id: string }) => void
type OnError = (error: string) => void

/** Parse SSE lines from a text chunk */
function parseSSELines(text: string): Array<{ event: string; data: string }> {
  const results: Array<{ event: string; data: string }> = []
  let currentEvent = 'message'

  for (const line of text.split('\n')) {
    if (line.startsWith('event: ')) {
      currentEvent = line.slice(7).trim()
    } else if (line.startsWith('data: ')) {
      results.push({ event: currentEvent, data: line.slice(6).trim() })
      currentEvent = 'message'
    }
  }
  return results
}

/** Stream a POST request with SSE response */
async function streamPost(
  url: string,
  body: Record<string, unknown>,
  onChunk: OnChunk,
  onDone: OnDone,
  onError: OnError,
  signal?: AbortSignal,
) {
  const response = await fetch(`${API_BASE}${url}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    signal,
  })

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`)
  }

  if (!response.body) {
    throw new Error('Response body is null')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  const processBlock = (block: string) => {
    for (const parsed of parseSSELines(block)) {
      try {
        const json = JSON.parse(parsed.data)
        if (parsed.event === 'chunk' && json.content) {
          onChunk(json)
        } else if (parsed.event === 'done') {
          onDone(json)
        } else if (parsed.event === 'error') {
          onError(json.error || 'Unknown error')
        }
      } catch {
        // Partial JSON, skip
      }
    }
  }

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n\n')
    buffer = lines.pop() || ''

    for (const block of lines) {
      processBlock(block)
    }
  }

  // Flush remaining buffer (fixes dropped final done event)
  if (buffer.trim()) {
    processBlock(buffer)
  }
}

/** Generate a new draft from file content */
export function generateDraft(
  fileContent: string,
  onChunk: OnChunk,
  onDone: OnDone,
  onError: OnError,
  signal?: AbortSignal,
) {
  return streamPost(
    '/draft/generate',
    { file_content: fileContent },
    onChunk, onDone, onError, signal,
  )
}

/** Refine existing draft with user instruction */
export function refineDraft(
  sessionId: string,
  instruction: string,
  onChunk: OnChunk,
  onDone: OnDone,
  onError: OnError,
  signal?: AbortSignal,
) {
  return streamPost(
    '/draft/refine',
    { session_id: sessionId, instruction },
    onChunk, onDone, onError, signal,
  )
}
