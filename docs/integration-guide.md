# Hướng dẫn Tích hợp

## Mục lục

1. [Tổng quan](#tổng-quan)
2. [Phương án 1: iframe (Khuyến nghị)](#phương-án-1-iframe-khuyến-nghị)
3. [Phương án 2: Library build](#phương-án-2-library-build)
4. [Giao tiếp giữa host app và Draft Helper](#giao-tiếp-giữa-host-app-và-draft-helper)
5. [So sánh 2 phương án](#so-sánh-2-phương-án)

---

## Tổng quan

eOffice Draft Helper được thiết kế để nhúng vào web app hiện có dưới dạng popup modal. Khi người dùng nhấn nút "Gợi ý dự thảo văn bản", modal sẽ mở ra với giao diện side-by-side:
- **Bên trái**: Xem trước nội dung dự thảo (Markdown rendered)
- **Bên phải**: Chat AI để tạo và chỉnh sửa

## Phương án 1: iframe (Khuyến nghị)

Cách đơn giản nhất, không lo xung đột CSS/JS với host app.

### Bước 1: Deploy Draft Helper

Deploy backend + frontend theo [hướng dẫn triển khai](deployment-guide.md). Giả sử domain là `https://ai-draft.eoffice.vn`.

### Bước 2: Thêm code nhúng vào host app

```html
<!-- Nút mở popup -->
<button id="btn-draft-helper" onclick="openDraftHelper()">
  Gợi ý dự thảo văn bản
</button>

<!-- Modal overlay -->
<div id="draft-helper-overlay" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.4); z-index:9999; display:flex; align-items:center; justify-content:center;">
  <div style="width:95vw; height:95vh; border-radius:12px; overflow:hidden; box-shadow:0 25px 50px rgba(0,0,0,0.25);">
    <iframe
      id="draft-helper-iframe"
      src="https://ai-draft.eoffice.vn"
      style="width:100%; height:100%; border:none;"
      allow="clipboard-write"
    ></iframe>
  </div>
</div>

<script>
function openDraftHelper() {
  document.getElementById('draft-helper-overlay').style.display = 'flex';
}

// Đóng khi click overlay hoặc nhận message đóng từ iframe
document.getElementById('draft-helper-overlay').addEventListener('click', function(e) {
  if (e.target === this) this.style.display = 'none';
});

// Nhận dữ liệu từ Draft Helper (nếu cần)
window.addEventListener('message', function(e) {
  if (e.origin !== 'https://ai-draft.eoffice.vn') return;

  if (e.data.type === 'DRAFT_APPLY') {
    // Nhận nội dung dự thảo để điền vào form eOffice
    console.log('Draft content:', e.data.content);
    document.getElementById('draft-helper-overlay').style.display = 'none';
  }

  if (e.data.type === 'DRAFT_CLOSE') {
    document.getElementById('draft-helper-overlay').style.display = 'none';
  }
});
</script>
```

### Bước 3: Cấu hình CORS

Trong `backend/.env`, thêm domain host app:

```env
CORS_ORIGINS=https://ai-draft.eoffice.vn,https://eoffice.your-domain.com
```

### Bước 4 (Tuỳ chọn): Gửi dữ liệu từ Draft Helper về host app

Nếu muốn nút "Áp dụng dự thảo" gửi content về host app, thêm vào frontend component:

```typescript
// Trong frontend, thêm hàm gửi message lên parent window
function applyDraft(content: string) {
  window.parent.postMessage(
    { type: 'DRAFT_APPLY', content },
    '*' // Hoặc chỉ định origin cụ thể
  );
}
```

## Phương án 2: Library build

Tích hợp chặt hơn, truyền callback trực tiếp. Phù hợp khi host app cũng là React hoặc cần kiểm soát chặt.

### Bước 1: Build library

Sửa `frontend/vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    lib: {
      entry: 'src/embed.ts',
      name: 'EofficeDraftHelper',
      formats: ['umd', 'es'],
      fileName: (format) => `eoffice-draft-helper.${format}.js`,
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
  },
})
```

### Bước 2: Tạo file entry point

Tạo `frontend/src/embed.ts`:

```typescript
import { createRoot } from 'react-dom/client'
import { createElement } from 'react'
import { AiDraftingModal } from './components/ai-drafting-modal'
import './index.css'

export interface MountOptions {
  onApply?: (content: string) => void
  onClose?: () => void
}

export function mount(element: HTMLElement, options: MountOptions = {}) {
  const root = createRoot(element)
  root.render(
    createElement(AiDraftingModal, {
      isOpen: true,
      onClose: options.onClose || (() => root.unmount()),
    })
  )
  return { unmount: () => root.unmount() }
}
```

### Bước 3: Build

```bash
cd frontend
npm run build
# Output: dist/eoffice-draft-helper.umd.js
#         dist/eoffice-draft-helper.es.js
```

### Bước 4: Sử dụng trong host app

**UMD (script tag):**

```html
<script src="https://ai-draft.eoffice.vn/eoffice-draft-helper.umd.js"></script>
<div id="draft-container"></div>
<script>
  const instance = EofficeDraftHelper.mount(
    document.getElementById('draft-container'),
    {
      onApply: (content) => {
        console.log('Draft:', content);
        // Điền vào form eOffice
      },
      onClose: () => {
        instance.unmount();
      }
    }
  );
</script>
```

**ES Module (React host app):**

```tsx
import { mount } from '@eoffice/draft-helper'
import { useRef, useEffect } from 'react'

function DraftButton() {
  const containerRef = useRef<HTMLDivElement>(null)

  const openDraft = () => {
    if (!containerRef.current) return
    const instance = mount(containerRef.current, {
      onApply: (content) => {
        // Xử lý nội dung dự thảo
        instance.unmount()
      },
      onClose: () => instance.unmount(),
    })
  }

  return (
    <>
      <button onClick={openDraft}>Gợi ý dự thảo</button>
      <div ref={containerRef} />
    </>
  )
}
```

## Giao tiếp giữa host app và Draft Helper

### iframe: postMessage API

```
Host App                          Draft Helper (iframe)
   │                                      │
   │──── openDraftHelper() ───────────────│
   │                                      │
   │        [User tạo/chỉnh sửa dự thảo] │
   │                                      │
   │◄──── postMessage(DRAFT_APPLY) ───────│
   │       { type, content }              │
   │                                      │
   │──── overlay.style.display='none' ────│
```

### Library: Direct callbacks

```
Host App                          Draft Helper (component)
   │                                      │
   │──── mount(el, { onApply }) ──────────│
   │                                      │
   │        [User tạo/chỉnh sửa dự thảo] │
   │                                      │
   │◄──── onApply(content) ───────────────│
   │                                      │
   │──── instance.unmount() ──────────────│
```

## So sánh 2 phương án

| Tiêu chí | iframe | Library build |
|---|---|---|
| **Xung đột CSS/JS** | Không có | Có thể xảy ra nếu host app cũng dùng Tailwind |
| **Deploy độc lập** | Có, hoàn toàn tách biệt | Có, nhưng host app cần import file JS |
| **Truyền dữ liệu** | postMessage (async) | Callback trực tiếp (sync) |
| **Effort tích hợp** | Thấp (chỉ cần HTML + JS) | Trung bình (cần build step) |
| **Performance** | Tốt (sandboxed) | Tốt hơn (cùng process) |
| **Cập nhật** | Deploy lại Draft Helper, host app không cần thay đổi | Phải rebuild và distribute file JS mới |
| **Bảo mật** | Sandbox tự nhiên | Chạy cùng context với host app |

**Khuyến nghị**: Dùng **iframe** cho đa số trường hợp. Chỉ dùng library build khi cần tích hợp chặt (vd: tự động điền form, chia sẻ auth token).
