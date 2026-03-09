/**
 * App root - demo page with button to open AI drafting modal.
 * In production, only AiDraftingModal is used (embedded in eOffice).
 */

import { useState } from 'react'
import { Bot } from 'lucide-react'
import { AiDraftingModal } from './components/ai-drafting-modal'

function App() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 max-w-lg text-center">
        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 mx-auto mb-4">
          <Bot className="w-6 h-6" />
        </div>
        <h3 className="text-slate-800 font-semibold mb-1">
          Bạn cần soạn thảo nội dung văn bản?
        </h3>
        <p className="text-sm text-slate-500 max-w-md mx-auto mb-6">
          Sử dụng Trợ lý AI để tự động tạo khung dự thảo dựa trên thông tin văn bản cung cấp.
        </p>
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg flex items-center gap-2 font-medium shadow-sm transition-all hover:shadow mx-auto"
        >
          <Bot className="w-5 h-5" />
          Gợi ý dự thảo văn bản
        </button>
      </div>

      <AiDraftingModal isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </div>
  )
}

export default App
