/**
 * Left panel - renders draft markdown content with proper formatting.
 * Shows blank state when no draft, renders markdown when streaming/complete.
 */

import { FileEdit } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { CopyContentButton } from './copy-content-button'

interface Props {
  draftContent: string
  isStreaming: boolean
}

/** Strip LLM-echoed prompt prefix from draft output */
function sanitizeDraft(content: string) {
  return content.replace(/^#+\s*BẢN THẢO HIỆN TẠI:\s*/i, '').trimStart()
}

export function DocumentPreviewPanel({ draftContent, isStreaming }: Props) {
  const sanitized = sanitizeDraft(draftContent)
  const hasContent = sanitized.length > 0

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header */}
      <div className="h-12 bg-white border-b border-gray-200 flex items-center justify-between px-4 shrink-0 shadow-sm z-10">
        <div className="text-sm font-medium text-slate-700 flex items-center gap-2">
          <FileEdit className="w-4 h-4 text-slate-400" />
          Nội dung Dự thảo
          {isStreaming && (
            <span className="text-[10px] font-medium px-2 py-0.5 bg-blue-50 text-blue-600 rounded-full border border-blue-100 animate-pulse">
              Đang tạo...
            </span>
          )}
        </div>
        {hasContent && <CopyContentButton getText={() => sanitized} />}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6 custom-scrollbar">
        {hasContent ? (
          <div className="max-w-[800px] mx-auto bg-white rounded-lg shadow-sm border border-gray-200 p-8">
            <article className="prose prose-sm max-w-none prose-headings:text-slate-800 prose-p:text-slate-700 prose-p:leading-relaxed prose-li:text-slate-700 prose-strong:text-slate-800">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {sanitized}
              </ReactMarkdown>
            </article>
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-center px-8">
            <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-4">
              <FileEdit className="w-8 h-8 text-blue-400" />
            </div>
            <p className="text-slate-500 text-sm font-medium mb-1">
              Bản thảo trống
            </p>
            <p className="text-slate-400 text-xs max-w-[300px]">
              Dán nội dung tài liệu gốc vào ô chat bên phải để AI tạo dự thảo văn bản.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
