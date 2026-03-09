/**
 * Single chat message bubble - renders user or assistant messages.
 */

import { Bot } from 'lucide-react'
import type { ChatMessage } from '../types/draft-types'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface Props {
  message: ChatMessage
}

export function ChatMessageBubble({ message }: Props) {
  const isUser = message.role === 'user'

  if (isUser) {
    return (
      <div className="mb-4 max-w-[85%] ml-auto flex flex-col items-end">
        <div className="bg-primary-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 text-sm shadow-sm leading-relaxed whitespace-pre-wrap break-words">
          {message.content.length > 500
            ? message.content.slice(0, 500) + '...'
            : message.content}
        </div>
      </div>
    )
  }

  return (
    <div className="mb-4 max-w-[90%] flex gap-3">
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shrink-0 shadow-sm mt-1">
        <Bot className="w-4 h-4 text-white" />
      </div>
      <div className="flex flex-col gap-1 w-full">
        <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm p-4 text-sm shadow-sm leading-relaxed text-slate-700 prose prose-sm max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
