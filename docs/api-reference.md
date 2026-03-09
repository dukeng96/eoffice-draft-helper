# API Reference

Base URL: `http://localhost:8000` (development) hoặc `https://ai-draft.eoffice.vn` (production)

---

## Health Check

### `GET /`

Kiểm tra nhanh dịch vụ.

**Response:**
```json
{ "status": "ok", "service": "eOffice Soạn Thảo AI", "version": "1.0.0" }
```

### `GET /health`

Kiểm tra chi tiết bao gồm trạng thái LLM.

**Response:**
```json
{ "status": "healthy", "llm_configured": true, "model": "llm-medium-v4" }
```

---

## Tạo dự thảo

### `POST /draft/generate`

Tạo dự thảo văn bản từ nội dung tài liệu gốc. Trả về SSE stream.

**Request body:**
```json
{ "file_content": "Nội dung văn bản gốc (extracted text từ PDF/DOCX)" }
```

| Field | Type | Required | Mô tả |
|---|---|---|---|
| `file_content` | string | Có | Nội dung văn bản gốc, tối thiểu 1 ký tự |

**Response:** `text/event-stream` (SSE)

Các event types:

#### `chunk` - Mỗi đoạn nội dung từ LLM

```
event: chunk
data: {"content": "## TRÍCH YẾU\n", "session_id": "a1b2c3d4"}
```

#### `done` - Hoàn thành tạo dự thảo

```
event: done
data: {"status": "completed", "session_id": "a1b2c3d4"}
```

#### `error` - Lỗi trong quá trình tạo

```
event: error
data: {"error": "LLM streaming error: ...", "code": "LLM_ERROR"}
```

**Lưu ý**: `session_id` được trả về trong mỗi chunk event. Lưu lại để dùng cho endpoint `/draft/refine`.

---

## Chỉnh sửa dự thảo

### `POST /draft/refine`

Chỉnh sửa dự thảo hiện tại theo yêu cầu. Yêu cầu `session_id` từ lần `generate` trước.

**Request body:**
```json
{
  "session_id": "a1b2c3d4",
  "instruction": "Sửa giọng văn trang trọng hơn"
}
```

| Field | Type | Required | Mô tả |
|---|---|---|---|
| `session_id` | string | Có | Session ID từ lần generate trước |
| `instruction` | string | Có | Yêu cầu chỉnh sửa từ người dùng |

**Response:** `text/event-stream` (SSE) — cùng format với `/draft/generate`.

**Lỗi có thể:**

| HTTP Status | Mô tả |
|---|---|
| 404 | Session không tìm thấy hoặc đã hết hạn |
| 400 | Chưa có dự thảo (chưa gọi `/generate`) |

---

## Luồng sử dụng điển hình

```
1. Client gọi POST /draft/generate { file_content: "..." }
   ↓
2. Server trả SSE stream:
   - Nhiều event "chunk" với content + session_id
   - 1 event "done" khi hoàn thành
   ↓
3. Client lưu session_id
   ↓
4. Người dùng yêu cầu chỉnh sửa
   ↓
5. Client gọi POST /draft/refine { session_id, instruction }
   ↓
6. Server trả SSE stream tương tự bước 2
   ↓
7. Lặp lại bước 4-6 cho mỗi lần chỉnh sửa
```

---

## Ví dụ sử dụng với curl

```bash
# Tạo dự thảo
curl -N -X POST http://localhost:8000/draft/generate \
  -H "Content-Type: application/json" \
  -d '{"file_content": "Công ty ABC kính đề nghị UBND Tỉnh xem xét hỗ trợ về đất đai."}'

# Chỉnh sửa (thay session_id thực tế)
curl -N -X POST http://localhost:8000/draft/refine \
  -H "Content-Type: application/json" \
  -d '{"session_id": "a1b2c3d4", "instruction": "Thêm phần căn cứ pháp lý"}'
```

**Lưu ý**: Flag `-N` (no buffer) cần thiết để xem SSE stream real-time trong terminal.

---

## Ví dụ sử dụng với JavaScript

```javascript
const response = await fetch('/draft/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ file_content: 'Nội dung văn bản...' }),
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const chunk = decoder.decode(value, { stream: true });
  const lines = chunk.split('\n');

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6));
      if (data.content) {
        // Hiển thị content lên UI
        console.log(data.content);
      }
    }
  }
}
```

**Quan trọng**: Không dùng `EventSource` vì nó chỉ hỗ trợ GET. Phải dùng `fetch` + `ReadableStream.getReader()` cho POST-based SSE.
