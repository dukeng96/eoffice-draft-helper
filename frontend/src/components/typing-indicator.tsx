/**
 * Animated typing indicator (3 bouncing dots) shown while AI is streaming.
 */

import { Bot } from 'lucide-react'

export function TypingIndicator() {
  return (
    <div className="mb-4 max-w-[90%] flex gap-3">
      <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center shrink-0 mt-1">
        <Bot className="w-4 h-4 text-gray-400" />
      </div>
      <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm p-4 shadow-sm flex items-center gap-1.5 w-[72px]">
        <div className="w-2 h-2 rounded-full bg-blue-400 dot-bounce dot-bounce-1" />
        <div className="w-2 h-2 rounded-full bg-blue-400 dot-bounce dot-bounce-2" />
        <div className="w-2 h-2 rounded-full bg-blue-400 dot-bounce dot-bounce-3" />
      </div>
    </div>
  )
}
