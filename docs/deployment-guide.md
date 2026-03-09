# Hướng dẫn Triển khai

## Yêu cầu

- Docker 24+ và Docker Compose v2+
- Node.js 20+ (phát triển frontend)
- Python 3.11+ (phát triển backend)
- VNPT LLM API key

## Cấu hình

```bash
cd backend
cp .env.example .env
```

Sửa `backend/.env`:

```env
VNPT_API_KEY=your_actual_api_key    # BẮT BUỘC
VNPT_BASE_URL=https://assistant-stream.vnpt.vn/v1/
VNPT_MODEL=llm-medium-v4
REDIS_URL=redis://redis:6379/0      # Giữ nguyên nếu dùng Docker Compose
SESSION_TTL_HOURS=24
CORS_ORIGINS=http://localhost:3000,https://eoffice.your-domain.com
```

## Deploy Production (Docker)

```bash
# Build và chạy tất cả services
docker compose up -d

# Kiểm tra
docker compose ps
curl http://localhost:8000/health
# Frontend: http://localhost:3000
```

### Quản lý

```bash
docker compose logs -f backend     # Xem logs
docker compose restart backend     # Restart
docker compose down                # Dừng
docker compose up -d --build       # Rebuild sau khi thay đổi code
```

### Cấu trúc services

| Service | Port | Mô tả |
|---|---|---|
| `frontend` | 3000 → 80 | Nginx serve static + proxy `/api/` → backend |
| `backend` | 8000 | FastAPI + SSE streaming |
| `redis` | 6379 | Session store (TTL 24h) |

## Phát triển Local

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Cần Redis chạy sẵn
docker run -d --name redis -p 6379:6379 redis:7-alpine

# Sửa .env: REDIS_URL=redis://localhost:6379/0
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev                        # http://localhost:3000
```

Vite dev server tự proxy `/api/*` → `http://localhost:8000/*` (cấu hình trong `vite.config.ts`).

```bash
npm run build                      # Build production → dist/
```

## Lưu ý quan trọng

- `proxy_buffering off` trong `frontend/nginx.conf` là **bắt buộc** để SSE streaming hoạt động
- Không commit file `backend/.env` (đã có trong `.gitignore`)
- Redis data persist qua Docker volume `redis-data`
