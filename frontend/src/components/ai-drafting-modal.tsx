/**
 * Main modal component - full-screen popup with split pane layout.
 * Left: document preview, Right: AI chat.
 */

import { Allotment } from 'allotment'
import 'allotment/dist/style.css'
import { Bot, X } from 'lucide-react'
import { useDraftStream } from '../hooks/use-draft-stream'
import { DocumentPreviewPanel } from './document-preview-panel'
import { ChatPanel } from './chat-panel'

interface Props {
  isOpen: boolean
  onClose: () => void
}

export function AiDraftingModal({ isOpen, onClose }: Props) {
  const { messages, draftContent, isStreaming, isFirstDraft, sendMessage, stopStreaming } =
    useDraftStream()

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="bg-white w-[95vw] h-[95vh] rounded-xl shadow-2xl flex flex-col overflow-hidden animate-scale-in">
        {/* Top header */}
        <div className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-5 shrink-0">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-blue-500 to-indigo-600 p-1.5 rounded-lg shadow-sm">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="font-semibold text-slate-800 leading-tight">Trợ lý Soạn thảo AI</h2>
              <p className="text-[11px] text-slate-500 uppercase tracking-wide font-medium">
                eOffice Intelligence
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1.5 px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-medium border border-green-100 mr-2">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
              Sẵn sàng
            </div>
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-red-600 hover:bg-red-50 p-1.5 rounded-md transition-colors"
              title="Đóng"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Split pane content */}
        <div className="flex-1 overflow-hidden">
          <Allotment defaultSizes={[60, 40]}>
            <Allotment.Pane minSize={300}>
              <DocumentPreviewPanel
                draftContent={draftContent}
                isStreaming={isStreaming}
              />
            </Allotment.Pane>
            <Allotment.Pane minSize={300}>
              <ChatPanel
                messages={messages}
                isStreaming={isStreaming}
                isFirstDraft={isFirstDraft}
                onSend={sendMessage}
                onStop={stopStreaming}
              />
            </Allotment.Pane>
          </Allotment>
        </div>
      </div>
    </div>
  )
}
