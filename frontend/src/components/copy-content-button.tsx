/**
 * Copy button with visual feedback - copies text to clipboard.
 */

import { useState } from 'react'
import { Copy, Check } from 'lucide-react'

interface Props {
  getText: () => string
}

export function CopyContentButton({ getText }: Props) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(getText())
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      // Fallback for older browsers
      const textarea = document.createElement('textarea')
      textarea.value = getText()
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <button
      onClick={handleCopy}
      className="text-xs font-medium px-3 py-1.5 bg-white border border-gray-300 text-slate-700 rounded-md hover:bg-gray-50 transition-colors flex items-center gap-1.5"
    >
      {copied ? (
        <>
          <Check className="w-3.5 h-3.5 text-green-600" />
          <span className="text-green-600">Đã sao chép</span>
        </>
      ) : (
        <>
          <Copy className="w-3.5 h-3.5" />
          Sao chép
        </>
      )}
    </button>
  )
}
