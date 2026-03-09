# Hướng dẫn Triển khai

## Yêu cầu

- Docker 24+ và Docker Compose v2+
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

## Khởi chạy

```bash
# Build và chạy tất cả services
docker compose up -d

# Kiểm tra
docker compose ps
curl http://localhost:8000/health
# Frontend: http://localhost:3000
```

## Quản lý

```bash
# Xem logs
docker compose logs -f backend

# Restart
docker compose restart backend

# Dừng
docker compose down

# Rebuild sau khi thay đổi code
docker compose up -d --build
```

## Cấu trúc services

| Service | Port | Mô tả |
|---|---|---|
| `frontend` | 3000 → 80 | Nginx serve static + proxy `/api/` → backend |
| `backend` | 8000 | FastAPI + SSE streaming |
| `redis` | 6379 | Session store (TTL 24h) |

## Lưu ý quan trọng

- `proxy_buffering off` trong `frontend/nginx.conf` là **bắt buộc** để SSE streaming hoạt động
- Không commit file `backend/.env` (đã có trong `.gitignore`)
- Redis data persist qua Docker volume `redis-data`
