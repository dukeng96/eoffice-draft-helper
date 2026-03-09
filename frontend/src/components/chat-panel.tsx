/**
 * Right panel - AI chat thread with messages, typing indicator, and input.
 */

import { useEffect, useRef } from 'react'
import { MessageCircle } from 'lucide-react'
import type { ChatMessage } from '../types/draft-types'
import { ChatMessageBubble } from './chat-message-bubble'
import { TypingIndicator } from './typing-indicator'
import { ChatInputArea } from './chat-input-area'

interface Props {
  messages: ChatMessage[]
  isStreaming: boolean
  isFirstDraft: boolean
  onSend: (text: string) => void
  onStop: () => void
}

export function ChatPanel({ messages, isStreaming, isFirstDraft, onSend, onStop }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom on new messages or streaming
  useEffect(() => {
    const el = containerRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [messages, isStreaming])

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div className="h-12 border-b border-gray-200 flex items-center px-4 shrink-0 bg-slate-50/50">
        <span className="text-sm font-semibold text-slate-700 flex items-center gap-2">
          <MessageCircle className="w-4 h-4 text-slate-400" />
          Trao đổi & Chỉnh sửa
        </span>
      </div>

      {/* Messages */}
      <div
        ref={containerRef}
        className="flex-1 overflow-y-auto p-4 custom-scrollbar bg-slate-50"
      >
        {messages.map(msg => (
          <ChatMessageBubble key={msg.id} message={msg} />
        ))}
        {isStreaming && <TypingIndicator />}
      </div>

      {/* Input */}
      <ChatInputArea
        onSend={onSend}
        onStop={onStop}
        isStreaming={isStreaming}
        isFirstDraft={isFirstDraft}
      />
    </div>
  )
}
