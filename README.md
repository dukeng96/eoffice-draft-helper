# eOffice Draft Helper

Trợ lý soạn thảo văn bản AI cho hệ thống eOffice. Giao diện side-by-side: bên trái xem trước dự thảo, bên phải chat với AI để tạo và chỉnh sửa văn bản hành chính.

## Kiến trúc

```
eoffice-draft-helper/
├── backend/              # FastAPI + SSE streaming + Redis session
├── frontend/             # React + TypeScript + Tailwind CSS
├── docs/                 # Tài liệu hướng dẫn
├── docker-compose.yml    # Deploy tất cả services
└── .gitignore
```

## Yêu cầu

- Docker 24+ và Docker Compose v2+
- VNPT LLM API key

## Khởi chạy nhanh

```bash
# 1. Cấu hình
cd backend && cp .env.example .env   # Sửa VNPT_API_KEY

# 2. Deploy (Docker)
docker compose up -d

# 3. Truy cập
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000/health
```

## Phát triển local

### Backend

```bash
cd backend && cp .env.example .env   # Sửa VNPT_API_KEY
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Cần Redis chạy sẵn
docker run -d --name redis -p 6379:6379 redis:7-alpine

# Sửa .env: REDIS_URL=redis://localhost:6379/0
uvicorn main:app --host 0.0.0.0 --port 8000 --reload  #http://localhost:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev    # http://localhost:3000
```

## API Endpoints

### POST /draft/generate

Tạo dự thảo từ nội dung văn bản đến.

**Request:**
```json
{
  "file_content": "Văn bản gốc đã extract từ PDF/DOCX..."
}
```

**Response (SSE):**
```
event: chunk
data: {"content": "## TRÍCH YẾU\n...", "session_id": "abc123"}

event: done
data: {"status": "completed", "session_id": "abc123"}
```

### POST /draft/refine

Chỉnh sửa dự thảo theo hướng dẫn của người dùng.

**Request:**
```json
{
  "session_id": "abc123",
  "instruction": "Thêm kính gửi Sở Tài chính"
}
```

**Response (SSE):** Cùng format với `/generate`

### GET /health

Kiểm tra trạng thái service.

## Quản lý phiên (Session)

- Session lưu trong Redis với TTL 24h (cấu hình được)
- Mỗi session lưu: `file_content`, `current_draft`
- `session_id` trả về trong mọi SSE event
- Client chỉ cần lưu `session_id`, backend tự quản lý trạng thái dự thảo

## Tài liệu

- [Hướng dẫn triển khai](docs/deployment-guide.md) - Docker deploy, phát triển local
- [Hướng dẫn tích hợp](docs/integration-guide.md) - Nhúng vào web app khác (iframe)
- [API Reference](docs/api-reference.md) - Chi tiết các endpoint backend

## License

Internal use - eOffice project.
