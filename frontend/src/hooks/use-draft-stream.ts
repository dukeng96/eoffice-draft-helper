/**
 * React hook managing draft generation/refinement streaming state.
 * Orchestrates API calls and maintains chat + document state.
 */

import { useState, useCallback, useRef } from 'react'
import type { ChatMessage, DraftState } from '../types/draft-types'
import { generateDraft, refineDraft } from '../services/draft-api-service'

function createId() {
  return `msg-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`
}

function createInitialState(): DraftState {
  return {
    sessionId: null,
    messages: [{
      id: 'welcome',
      role: 'assistant',
      content: 'Xin chào! Tôi là **Trợ lý Soạn Thảo AI**.\n\nVui lòng dán toàn bộ nội dung tài liệu gốc vào ô bên dưới, tôi sẽ tạo dự thảo văn bản cho bạn.',
      timestamp: new Date(),
    }],
    draftContent: '',
    isStreaming: false,
    isFirstDraft: true,
  }
}

export function useDraftStream() {
  const [state, setState] = useState<DraftState>(createInitialState())
  const abortRef = useRef<AbortController | null>(null)

  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim() || state.isStreaming) return

    // Add user message
    const userMsg: ChatMessage = {
      id: createId(), role: 'user', content: text, timestamp: new Date(),
    }
    setState(prev => ({
      ...prev,
      isStreaming: true,
      messages: [...prev.messages, userMsg],
      draftContent: prev.isFirstDraft ? '' : prev.draftContent,
    }))

    const controller = new AbortController()
    abortRef.current = controller
    let accumulated = ''
    let capturedSessionId = state.sessionId

    const onChunk = (data: { content: string; session_id: string }) => {
      accumulated += data.content
      if (data.session_id) capturedSessionId = data.session_id
      setState(prev => ({
        ...prev,
        draftContent: accumulated,
        sessionId: capturedSessionId,
      }))
    }

    const onDone = (data: { session_id: string }) => {
      capturedSessionId = data.session_id || capturedSessionId
      const aiMsg: ChatMessage = {
        id: createId(),
        role: 'assistant',
        content: state.isFirstDraft
          ? 'Đã tạo xong dự thảo! Kiểm tra văn bản bên trái. Nếu cần chỉnh sửa, hãy nhập yêu cầu.'
          : 'Đã cập nhật dự thảo theo yêu cầu. Xem lại nội dung bên trái.',
        timestamp: new Date(),
      }
      setState(prev => ({
        ...prev,
        isStreaming: false,
        isFirstDraft: false,
        sessionId: capturedSessionId,
        messages: [...prev.messages, aiMsg],
      }))
    }

    const onError = (error: string) => {
      const errMsg: ChatMessage = {
        id: createId(), role: 'assistant',
        content: `Lỗi: ${error}. Vui lòng thử lại.`,
        timestamp: new Date(),
      }
      setState(prev => ({
        ...prev,
        isStreaming: false,
        messages: [...prev.messages, errMsg],
      }))
    }

    try {
      if (state.isFirstDraft) {
        await generateDraft(text, onChunk, onDone, onError, controller.signal)
      } else {
        if (!capturedSessionId) {
          onError('Không tìm thấy phiên làm việc. Vui lòng tải lại trang.')
          return
        }
        await refineDraft(
          capturedSessionId, text, onChunk, onDone, onError, controller.signal,
        )
      }
    } catch (err: unknown) {
      if ((err as Error).name !== 'AbortError') {
        onError((err as Error).message || 'Lỗi kết nối')
      }
    }
  }, [state.isStreaming, state.isFirstDraft, state.sessionId])

  const stopStreaming = useCallback(() => {
    abortRef.current?.abort()
    setState(prev => ({ ...prev, isStreaming: false }))
  }, [])

  const reset = useCallback(() => {
    abortRef.current?.abort()
    setState(createInitialState())
  }, [])

  return { ...state, sendMessage, stopStreaming, reset }
}
