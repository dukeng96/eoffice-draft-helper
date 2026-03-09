# Hướng dẫn Triển khai

## Mục lục

1. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
2. [Cài đặt Backend](#cài-đặt-backend)
3. [Cài đặt Frontend](#cài-đặt-frontend)
4. [Deploy Production](#deploy-production)

---

## Yêu cầu hệ thống

| Thành phần | Phiên bản tối thiểu | Ghi chú |
|---|---|---|
| Python | 3.11+ | Chạy backend FastAPI |
| Node.js | 20+ | Build frontend |
| Redis | 7+ | Lưu session dự thảo |
| VNPT LLM API | - | Cần API key hợp lệ |

## Cài đặt Backend

### 1. Tạo môi trường ảo

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 2. Cài dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường

```bash
cp .env.example .env
```

Sửa file `.env`:

```env
# BẮT BUỘC - API key từ VNPT
VNPT_API_KEY=your_actual_api_key

# Tuỳ chọn - mặc định đã có sẵn
VNPT_BASE_URL=https://assistant-stream.vnpt.vn/v1/
VNPT_MODEL=llm-medium-v4

# Redis - mặc định localhost
REDIS_URL=redis://localhost:6379/0
SESSION_TTL_HOURS=24

# CORS - danh sách origin được phép (phân cách bằng dấu phẩy)
CORS_ORIGINS=http://localhost:3000,https://eoffice.your-domain.com
```

### 4. Khởi chạy Redis

```bash
# Docker (khuyến nghị)
docker run -d --name redis -p 6379:6379 redis:7-alpine

# Hoặc cài trực tiếp trên Ubuntu
sudo apt install redis-server
sudo systemctl start redis
```

### 5. Chạy backend

```bash
# Development
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Kiểm tra: `curl http://localhost:8000/health`

## Cài đặt Frontend

### 1. Cài dependencies

```bash
cd frontend
npm install
```

### 2. Chạy development server

```bash
npm run dev
# → http://localhost:3000
```

Vite dev server tự proxy `/api/*` → `http://localhost:8000/*` (cấu hình trong `vite.config.ts`).

### 3. Build production

```bash
npm run build
# Output: frontend/dist/
```

## Deploy Production

### Phương án 1: Docker Compose (Khuyến nghị)

Tạo `docker-compose.yml` ở thư mục gốc:

```yaml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file: ./backend/.env
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  redis-data:
```

Tạo `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

Tạo `frontend/Dockerfile`:

```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

Tạo `frontend/nginx.conf`:

```nginx
server {
    listen 80;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_http_version 1.1;
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
    }
}
```

Chạy:

```bash
docker compose up -d
```

### Phương án 2: Nginx Reverse Proxy (Không Docker)

```nginx
server {
    listen 443 ssl;
    server_name ai-draft.eoffice.your-domain.com;

    # Frontend static files
    location / {
        root /var/www/eoffice-draft-helper/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Connection '';
        proxy_buffering off;      # Quan trọng cho SSE streaming
        proxy_cache off;
    }
}
```

**Lưu ý quan trọng**: `proxy_buffering off` là BẮT BUỘC để SSE streaming hoạt động đúng.
