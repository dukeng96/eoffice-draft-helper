# Hướng dẫn Tích hợp

Nhúng eOffice Draft Helper vào web app hiện có qua **iframe**.

---

## Tổng quan

eOffice Draft Helper được thiết kế để nhúng vào web app hiện có dưới dạng popup modal. Khi người dùng nhấn nút "Gợi ý dự thảo văn bản", modal mở ra với giao diện side-by-side:
- **Bên trái**: Xem trước nội dung dự thảo (Markdown rendered)
- **Bên phải**: Chat AI để tạo và chỉnh sửa

## Bước 1: Deploy Draft Helper

Deploy backend + frontend theo [hướng dẫn triển khai](deployment-guide.md). Giả sử domain là `https://ai-draft.eoffice.vn`.

## Bước 2: Thêm code nhúng vào host app

```html
<!-- Nút mở popup -->
<button id="btn-draft-helper" onclick="openDraftHelper()">
  Gợi ý dự thảo văn bản
</button>

<!-- Modal overlay -->
<div id="draft-helper-overlay" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.4); z-index:9999; align-items:center; justify-content:center;">
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

// Đóng khi click overlay
document.getElementById('draft-helper-overlay').addEventListener('click', function(e) {
  if (e.target === this) this.style.display = 'none';
});

// Nhận dữ liệu từ Draft Helper
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

## Bước 3: Cấu hình CORS

Trong `backend/.env`, thêm domain host app:

```env
CORS_ORIGINS=https://ai-draft.eoffice.vn,https://eoffice.your-domain.com
```

## Bước 4 (Tuỳ chọn): Gửi dữ liệu từ Draft Helper về host app

Nếu muốn nút "Áp dụng dự thảo" gửi content về host app, thêm vào frontend:

```typescript
function applyDraft(content: string) {
  window.parent.postMessage(
    { type: 'DRAFT_APPLY', content },
    '*' // Hoặc chỉ định origin cụ thể
  );
}
```

## Luồng giao tiếp

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
