/**
 * Chat input area with textarea, send button, and quick prompt chips.
 */

import { useState, useRef, useEffect } from 'react'
import { Send, Square } from 'lucide-react'

const QUICK_PROMPTS = [
  'Rút gọn nội dung',
  'Sửa giọng văn trang trọng hơn',
  'Thêm phần ký tên',
  'Bổ sung căn cứ pháp lý',
]

interface Props {
  onSend: (text: string) => void
  onStop: () => void
  isStreaming: boolean
  isFirstDraft: boolean
}

export function ChatInputArea({ onSend, onStop, isStreaming, isFirstDraft }: Props) {
  const [text, setText] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current
    if (el) {
      el.style.height = ''
      el.style.height = `${el.scrollHeight}px`
    }
  }, [text])

  const handleSend = () => {
    if (!text.trim() || isStreaming) return
    onSend(text.trim())
    setText('')
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="p-4 bg-white border-t border-gray-200">
      {/* Quick prompts - only show after first draft */}
      {!isFirstDraft && (
        <div className="flex gap-2 overflow-x-auto pb-3 mb-1 custom-scrollbar">
          {QUICK_PROMPTS.map(prompt => (
            <button
              key={prompt}
              onClick={() => { setText(prompt); textareaRef.current?.focus() }}
              className="whitespace-nowrap shrink-0 text-[11px] font-medium text-slate-600 bg-gray-100 hover:bg-blue-50 hover:text-blue-700 px-3 py-1.5 rounded-full border border-gray-200 transition-colors"
            >
              {prompt}
            </button>
          ))}
        </div>
      )}

      <div className="relative">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isStreaming}
          className="w-full bg-gray-50 border border-gray-300 text-slate-800 rounded-xl px-4 py-3 pr-14 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 focus:bg-white transition-all resize-none min-h-[52px] max-h-[150px] shadow-inner disabled:opacity-60"
          placeholder={isFirstDraft
            ? 'Dán nội dung tài liệu gốc để tạo dự thảo...'
            : 'Nhập yêu cầu chỉnh sửa...'
          }
          rows={1}
        />
        <div className="absolute right-2 bottom-2">
          {isStreaming ? (
            <button
              onClick={onStop}
              className="p-1.5 bg-red-500 text-white hover:bg-red-600 rounded-lg transition-colors shadow-sm"
              title="Dừng"
            >
              <Square className="w-4 h-4" />
            </button>
          ) : (
            <button
              onClick={handleSend}
              disabled={!text.trim()}
              className="p-1.5 bg-primary-600 text-white hover:bg-primary-700 rounded-lg transition-colors shadow-sm disabled:opacity-40 disabled:cursor-not-allowed"
              title="Gửi"
            >
              <Send className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
      <div className="mt-2 text-[10px] text-center text-slate-400">
        AI có thể mắc sai sót. Vui lòng rà soát lại thông tin trước khi ban hành.
      </div>
    </div>
  )
}
